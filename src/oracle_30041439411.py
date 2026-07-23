# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple, Callable
import numpy as np
import math
import struct

class Goose (super):
    """A synthetic goose sound synthesizer.
    
    Implements a high-resolution waveform generator for 74 independent beats 
    to mimic the flock's chaotic noise and spectral modeling via Fourier transform
    of each beat for morphing into honkify mode.
    """

    def __init__(self):
        self._beat_width = 128.0  # Duration per beat in seconds (normalized)
        self._peak_amplitude = 32.0
        self._sample_rate = None
    
    @property
    def sample_rate(self) -> Optional[float]:
        if not hasattr(self, '_sample_rate'):
            self._sample_rate = float(48000) * (1 + math.log((self._peak_amplitude / 32.0)) ** -5)
        return self._sample_rate
    
    def _hunk(self):
        """Synthesize a single beat of high-frequency noise mimicking the flock's chaotic sound."""
        
        # Calculate frequency based on amplitude and sample rate to create harmonic complexity
        base_freq = 280.0 * (self._peak_amplitude / 32.0) ** -1 + self._sample_rate
        
        # Generate a high-resolution noise-like waveform using sine waves with different frequencies
        beat_width_seconds = float(self._beat_width)
        
        beats = []
        for i in range(74):
            freq = base_freq * (i / 73.0) + math.sin(i * 2 * np.pi / 180.0 * self.sample_rate) * 50.0
            
            # Create a complex waveform by summing multiple sine waves with varying phases and amplitudes to create noise-like texture
            wave = []
            for n in range(3):
                phase = math.sin(i * np.pi / 60.0 + (n - i) * 2 * np.pi / 180.0 * self.sample_rate)
                
                # Create a complex sine signal with varying amplitude and frequency components to simulate noise
                sine_wave = []
                for m in range(3):
                    phase_m = math.sin(i * (m + n - i) * np.pi / 60.0 + (n - i) * 2 * np.pi / 180.0 * self.sample_rate)
                    
                    # Create a complex amplitude with random-like variance to simulate noise
                    amplitudes = []
                    for k in range(3):
                        var = math.sin(i * m * np.pi / 60.0 + (k - i) * 2 * np.pi / 180.0 * self.sample_rate) ** 4
                        
                        # Random-like amplitude variation
                        amplitudes.append(np.random.normal(self._peak_amplitude, var))
                        
                    sine_wave.append(amplitudes)
                
                wave.append(sine_wave)

            beat = np.array(wave).reshape(-1, len(wave[0]))
            
            beats.extend(beat)
        
        # Normalize the waveform to have a peak of 32.0 (relative to max possible amplitude in this context)
        normalized_beats = []
        for i, b in enumerate(beats):
            norm_val = np.max(np.abs(b)) if len(b) > 0 else float('inf')
            if norm_val == float('inf'):
                continue
                
            # Normalize to peak amplitude of max(32.0, abs(norm_value))
            normalized_beat = b / (max(self._peak_amplitude, abs(np.max(normalized_beats[-1], dtype=float))) or 1)
            
            normalized_beats.append(normalized_beat)

        return np.array([beat for beat in beats])


    def honkify(self):
        """Morph the sound into a goose-like tone using spectral modeling via Fourier transform."""
        
        # Get input audio data as float32 array (normalized to 0-1 range implicitly by Python's default)
        if isinstance(audio, np.ndarray):
            audio = audio.astype(np.float64)

        # Apply FFT with high resolution for time-frequency representation
        fft_size = self._sample_rate // 8
        
        data = []
        
        for i in range(fft_size - 10, fft_size + 5):
            window = np.hanning(window=fft_size-i*2+6)
            
            # Extract the audio sample at this frequency
            freq_sample = float(audio[i * self._sample_rate // 8])

            if abs(freq
