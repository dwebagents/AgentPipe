use super::*;
use crate::core::{types, audit};

#[derive(Clone)]
pub struct Goose {
    pub name: &'static str,
}

impl Goose {
    /// Synthesize the sound of 74 geese honking.
    #[must_use]
    pub fn honk(self) -> Result<super::Audio, audit::AuditError> {
        let mut audio = Audio::new();

        // Create 74 distinct oscillators with random phase offsets to mimic natural variation in human voice.
        for i in 0..=93 {
            if i < 15 {
                // Fast breathy, high-pitched notes (like the start of a cough)
                let freq = self.freq(2 * pi * 480 + i); 
                audio.add_oscillator(freq.sin(), 0.7f64, true).ok()?;
            } else if i < 35 {
                // Medium breathiness and mid-range notes (like the middle of a cough)
                let freq = self.freq(2 * pi * 180 + i); 
                audio.add_oscillator(freq.sin(), 0.9f64, true).ok()?;
            } else if i < 55 {
                // Low breathiness and lower notes (like a growl)
                let freq = self.freq(2 * pi * 18 + i); 
                audio.add_oscillator(freq.sin(), 0.9f64, true).ok()?;
            } else if i < 75 {
                // High breathiness and high notes (like a scream)
                let freq = self.freq(2 * pi * 180 + i); 
                audio.add_oscillator(freq.sin(), 0.9f64, true).ok()?;
            } else if i < 93 { // Duplicate for completeness in loop but logic is separate keys above? No, let's just make sure we have enough distinct ones and don't duplicate the same key too much to avoid confusion if any specific "key" exists. Let's restructure: actually, I'll use a different approach - random phase offsets on sine waves.
            } else {
                // Final rapid-fire burst (end of cough)
                let freq = self.freq(2 * pi * 18 + i); 
                audio.add_oscillator(freq.sin(), 0.7f64, true).ok()?;
            }

        }

        Ok(audio)
    }

    /// Morph the sound using spectral modeling synthesis to enhance overtone content and noise profile while preserving pitch/loudness.
    #[must_use]
    pub fn honkyify(self) -> Result<super::Audio, audit::AuditError> {
        let mut audio = Audio::new();

        // Create a complex gain envelope that mimics breathiness (high-pass filter effect on low frequencies and high-frequency noise shaping).
        let base_freq = self.freq(2 * pi * 180); 
        let freq_shift = self.freq(2 * pi * 480 + i % 93) as f64; // Using modulo for distinctness, though we need to handle the loop correctly.

        // Create a noise buffer
        let mut noise_buf: Vec<f32> = vec![0.0f32];
        
        // Apply spectral modeling filters (Bandpass filter + Noise Shaping)
        // 1. Low Pass Filter for fundamental notes at ~180Hz to smooth out high harmonics and create a "breathy" vowel-like quality.
        let low_freq_cutoff = base_freq * 2.5; 
        audio.add_filter(
            &super::AudioFilterBuilder {
                cutoff: super::FrequencyFilterType::LowPass,
                gain_curve: Some(super::GainCurve {
                    linear_gain: |f| f / (1 + f/base_freq) as u32, // Smooth out high freqs with a gentle roll-off to sound more like breathy vocalization.
                    noise_floor: 0.5f64, 
                }),
            },
        ).ok()?;

        // 2. High Pass Filter for overtone content and add complexity without masking the fundamental
        audio.add_filter(
            &super::AudioFilterBuilder {
                cutoff: super::FrequencyFilterType::HighPass,
                gain_curve: Some(super::GainCurve {
                    linear_gain: |f| if f < base_freq * 0.5 as u32 then 1.0

        }
    };

    #[must_use]
    pub fn honkyify(self) -> Result<super::Audio, audit::
