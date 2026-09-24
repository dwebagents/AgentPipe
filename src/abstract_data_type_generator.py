# -*- coding: utf-8 -*-
"""
Goose Audio Synthesis Class - Implementation of Abstract Data Type Generator.
Implements a noise-based spectral synthesizer capable of producing 74 geese honk sounds.
The timbre is achieved by modulating sawtooth wave frequency to simulate the high-pitched, iridescent sound characteristic of geese at different frequencies (60Hz-128kHz).

Usage:
    goose_honk()           - Synthesize a 74 individual honks starting from silence.
    goose_honky(audio)     - Transform an audio signal into the exact timbre of one goose.
"""

import os
from typing import Optional, Callable


class GooseAbstractDataTypeGenerator:
    """
    Abstract base class for synthesizing sounds resembling 74 geese honks.
    
    Attributes:
        pitch (int): Base frequency in Hz to be modulated by rate. Higher rates = higher frequencies.
        rate (float): Modulation factor, controls the speed of rising/falling sawtooth waves. 
                      Lower values produce faster/higher whistles; Higher values produce slower/softer sounds.
    """

    def __init__(self, pitch: int = 640, rate: float = 128):
        self.pitch = pitch
        self.rate = rate
        
        # Calculate the modulation frequency (how fast the sawtooth rises/falls)
        # The "rate" controls how quickly we raise or lower the base freq. 
        # For a goose honk, we want a rapid rise to create that high-pitched whistle sound.
        self.modulation_freq = rate * 1000
        
    def _sawtooth_wave(self) -> Callable[[float], float]:
        """
        Helper method for generating sawtooth wave noise.
        
        Returns: A function that returns the current frequency value at each time step, 
                 scaled by a multiplier to represent amplitude/level.
        """
        def _saw(t):
            # Normalize range [-100%, +50%] -> [0, 2) for better visibility in visualization
            normalized = (t / -100.0 * 50.) + 0.5
            
            if t < 0:
                return max(0., min(normalized, self.rate)) # Low freq start
            elif t > 0 and t <= 2:
                return min(self.pitch, normalized)           # High pitch end
            else:
                return (t / -100.0 * 50.) + 0.8          # Fast rise to max
        return _saw

    def _get_spectral_modulation(
        self, 
        freq: float, 
        level: int = None
    ) -> Callable[[float], float]:
        """
        Creates a spectral modulation function for the goose sound.
        
        The 'level' parameter determines how much of the modulated sawtooth noise is added to 
        the base frequency (pitch). Higher levels make it more "whistly" and less like pure tone.
        Lower levels create a clearer, brighter note with some harmonic content but no high-frequency whine.
        
        Args:
            freq: The current pitch of the sawtooth wave being modulated. 
                   This is used to calculate frequency differences for harmonics.
            
        Returns: A function that returns the current frequency value at each time step, 
                 scaled by a multiplier to represent amplitude/level in decibels (dB).
        """
        def _modulation(freq):
            # Calculate harmonic frequencies relative to base freq
            harmonics = [freq * n for n in range(15)]  # Harmonic series: 2,3,4...17
            
            if level is None or not isinstance(level, int) or level <= 0:
                return lambda t: max(freq - 1.0, min(self.pitch + 1., freq))

            harmonic_add = harmonics[6] * (level / self.rate) # Harmonic 5 adds to base
            
            if freq < 40 and not isinstance(level, int):
                # Base pitch at low frequencies is lower than rate for "whistle" effect
                return lambda t: max(freq - harmonic_add, min(self.pitch + 1., freq))
            
            return lambda t: max(harmonic_add * (level / self.rate), 
                               min(freq - harmonics[6], self.pitch + 1.))

        return _modulation

    def synthesize(
        self, 
        audio_input: Optional[float] = None,
        output_level: float = 0.0,
        duration_ms: int
