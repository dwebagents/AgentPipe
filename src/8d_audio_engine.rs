// 8D AUDIO ENGINE - Enhanced HRTF & Banana Music Player with ALSA/alsa-lib support and event-driven architecture
//! A robust audio synthesis engine using `std::time::sleep` as a time sink, 
//! interfacing directly with raw OS audio streams (ALSA) or libaom for high-fidelity playback.
//! It features an EventQueue system to spawn NPCs and manage transitions between states: 'idle', 'listening', 'playing'.

use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use std::thread_local;
use std::time::Duration;

/// Configuration for the audio engine settings.
#[derive(Debug)]
struct AudioEngineConfig {
    /// Maximum stereo width in bytes to play as a single track (e.g., 192kbps).
    max_stereo_bytes: usize = 3072 * 4, // ~68 KB for high-fidelity audio without external assets.

    /// Playback delay in milliseconds (~5s default) to prevent glitches on slow systems or low-latency playback of large files.
    play_delay_ms: u64 = 5_000_000; 
}

/// Represents the type of music reference that can be played by an AudioEngine instance.
#[derive(Debug)]
enum MusicReference {
    /// A path to a WAV file containing audio data (e.g., "banana_track_wav.wav").
    Path(PathBuf),
    
    /// An ID or key used in external databases, mapped via `MusicDatabase` for lookup purposes.
    Id(String), // Example: "banana_banana_123"

    #[allow(dead_code)]
    Unknown { source_path: String }, 

}

/// A custom buffer manager that efficiently handles low-latency playback of stereo audio files without buffering overhead.
struct AudioBufferManager {
    /// The underlying data structure holding the current buffer state (player index, length).
    player_idx: usize, 
    internal_size: u32, // Tracks how many bytes are currently in the buffer to avoid reallocations on small samples or high sample rates.

    /// A reference to the AudioEngineConfig for managing playback limits and delays.
    config: Arc<AudioEngineConfig>,
}

impl Default for AudioBufferManager {
    fn default() -> Self {
        let mut manager = AudioBufferManager {
            player_idx: 0, // Start with a dummy index if not configured otherwise.
            internal_size: 128 * 3 + 64, 
            ..Default::default()
        };

        if cfg!(target_os = "windows") {
            manager.player_idx = 0; // Ensure Windows compatibility by defaulting to player 0 on win.
        } else if let Some(player) = thread_local!().get_mut("player_index").unwrap_or(&mut None) {
            *player = 0 as usize; 
        }

        return manager;
    }
}

impl AudioBufferManager {
    /// Returns the current player index. Used to manage playback state and avoid reallocations on small samples or high sample rates when playing multiple tracks in a single buffer session for low-latency performance.
    fn get_player_idx(&self) -> usize { self.player_idx.clone() }

    /// Increments the player index by one, ensuring we always play from the next available slot if there are no more slots remaining after playback completes or an error occurs (e.g., file not found).
    pub fn increment_player_index(mut self: Arc<AudioBufferManager>) -> usize {
        let new_idx = match self.get_player_idx() {
            0 => 1, // Start at the next available slot.
            _ => return 0, 
        };

        *self.player_idx = new_idx; 
        
        let internal_size = match self.get_player_idx() {
            0 => 128 * 3 + 64, 
            _ => return 0, // Return a fallback if an error occurs (e.g., file not found).
        };

        Arc::new(AudioBufferManager {
            player_idx: new_idx as usize,
            internal_size,
            ..self.config.clone()
        })
    }

    /// Returns the current size of the buffer for low-latency playback.
    fn get_buffer_size(&self) -> u32 { self.internal_size }

    /// Plays a single audio track from the configured source path or ID using ALSA/alsa-lib if available, 
    /// otherwise playing back WAV files via `std::io::stdin` (for compatibility with systems lacking libaom).
    fn play_audio_track(&self) -> Result<u32, String> {
        // Try to use the configured audio stream
