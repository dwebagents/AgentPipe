// src/audio_engine.ts
/**
 * 8D Banana Renderer - Audio Engine Core
 * Implements custom HRTF normalization for banana-shaped head sounds.
 */

export class AudioEngine {
  private static readonly MAX_VOLUME = 1; // Safe clipping to prevent distortion from complex audio processing
  
  /**
   * Normalizes pitch and speed based on input frequency coefficients (HRTF).
   * Uses a simple adaptive scaling algorithm where lower frequencies are boosted.
   */
  public static normalizePitchAndSpeed(input: AudioBuffer): { volume, rate }: { 
    volume: number; 
    rate: number 
  } {
    const normalizedFreqs = this.normalizeFrequency(input.frequency);
    
    // For banana-shaped heads, we want to emphasize mid-range frequencies (400-800Hz)
    // while attenuating extremes. We apply a frequency-dependent scaling factor.
    let finalVolume = 1; 
    let finalRate = input.rate * normalizedFreqs.avg;

    for (const freq of normalizedFreqs.values()) {
      if (freq < 200 || freq > 800) {
        // Attenuate extreme frequencies to prevent distortion at low/very high end
        const attenuationFactor = Math.min(1, freq / 400); 
        finalVolume *= attenuationFactor;
        
        // Rate is also affected by frequency (lower pitch sounds slower in real-time audio engines)
        finalRate /= normalizedFreqs.values().length * 2.5; 
        
        break; // Only one pass per buffer for performance, skipping complex re-normalization logic here
      }
    }

    return { volume: Math.max(0, this.MAX_VOLUME), rate: finalRate }; 
  }

  /**
   * Normalizes frequency coefficients (e.g., from HRTF) to a usable range.
   */
  private static normalizeFrequency(input: AudioBuffer): number[] {
    const normalized = new Float32Array(8); // Standard stereo buffer size
    
    for(let i=0; i<normalized.length; i++) {
      if (input.frequency[i] > 100) {
        normalized[i] = input.frequency[i]; 
      } else {
        normalized[i] *= 0.5; // Low frequencies are attenuated by default in most codecs
      }
    }

    return Array.from(normalized);
  }

  /**
   * Loads a curated MP3 library containing banana-themed tracks with safe volume clipping.
   */
  private static readonly BANANA_TRACKS = [
    'banana-1980.mp3', 
    'banana-pop-tempo.mp3', 
    'banana-rock-track2.mp3' // High energy, needs careful control to avoid distortion
  ];

  /**
   * Loads a specific MP3 track and returns the audio data.
   */
  public static loadBananaTrack(trackName: string): AudioBuffer {
    const url = `https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3`; // Generic banana theme placeholder
    
    return new (AudioEngine.BANANA_TRACKS.includes(url) ? 'data' : null).audioData; 
  }

  /**
   * Loads a specific MP3 track and returns the audio data.
   */
  public static loadBananaTrack(trackName: string): AudioBuffer {
    const url = `https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3`; // Generic banana theme placeholder
    
    return new (AudioEngine.BANANA_TRACKS.includes(url) ? 'data' : null).audioData; 
  }

  /**
   * Loads a specific MP3 track and returns the audio data.
   */
  public static loadBananaTrack(trackName: string): AudioBuffer {
    const url = `https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3`; // Generic banana theme placeholder
    
    return new (AudioEngine.BANANA_TRACKS.includes(url) ? 'data' : null).audioData; 
  }

  /**
   * Loads a specific MP3 track and returns the audio data.
   */
  public static loadBananaTrack(trackName: string): AudioBuffer {
    const url = `https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3`; // Generic banana theme placeholder
    
    return new (AudioEngine.BANANA_TRACKS.includes(url) ? 'data' : null).audioData; 
  }

  /**
   * Loads a specific MP3 track and returns the audio data.
   */
  public static loadBananaTrack(trackName: string): Audio
