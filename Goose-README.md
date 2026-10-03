# Goose Class for SuperCollider

## Overview

The `Goose` class provides audio synthesis capabilities for creating realistic goose honk sounds and transforming audio into goose-like timbres using Spectral Modeling Synthesis (SMS).

## Installation

1. Copy `Goose.sc` to your SuperCollider class library directory:
   - macOS: `~/Library/Application Support/SuperCollider/Classes/`
   - Linux: `~/.local/share/SuperCollider/Classes/`
   - Windows: `%APPDATA%\SuperCollider\Classes\`

2. Recompile the class library: `CmdShift+l` or `Language > Recompile Class Library`

## Methods

### `Goose.honk(numGeese)`

Synthesizes the sound of multiple geese honking simultaneously.

**Parameters:**
- `numGeese` (Integer): Number of geese to simulate (default: 74)

**Example:**
```superCollider
s.boot;
Goose.honk(74);  // Play 74 geese honking
```

### `Goose.honkify(in, out, maxpeaks, currentpeaks)`

Transforms audio input into goose honk timbre using Spectral Modeling Synthesis.

**Parameters:**
- `in` (Integer): Input bus number (default: 0)
- `out` (Integer): Output bus number (default: 0)
- `maxpeaks` (Integer): Maximum spectral peaks to detect (default: 50)
- `currentpeaks` (Integer): Current peaks to track (default: 40)

**Example:**
```superCollider
s.boot;
// Load a sound file
b = Buffer.read(s, Platform.resourceDir +/+ "sounds/a11wlk01.wav");

// Transform it into goose honk
{
    var input = PlayBuf.ar(1, b, BufRateScale.kr(b));
    Goose.honkify(in: 0, out: 0);
}.play;
```

### `Goose.playHonk(freq, amp, dur)`

Plays a single goose honk with specified parameters.

**Parameters:**
- `freq` (Float): Base frequency in Hz (default: 280)
- `amp` (Float): Amplitude 0-1 (default: 0.3)
- `dur` (Float): Duration in seconds (default: 0.8)

**Example:**
```superCollider
s.boot;
Goose.playHonk(300, 0.5, 1.0);
```

### `Goose.choir(numGeese)`

Creates a goose choir with harmonic spread.

**Parameters:**
- `numGeese` (Integer): Number of geese (default: 74)

**Example:**
```superCollider
s.boot;
Goose.choir(74);
```

## Technical Details

### Honk Synthesis

The honk is synthesized using:
- **Fundamental frequency** with slight vibrato (LFNoise1 modulation)
- **Harmonic series** at 2x, 3x, and 4.5x the fundamental
- **Noise component** filtered through a low-pass filter
- **Formant filtering** at 2.5x the fundamental frequency
- **Percussive envelope** with quick attack and medium sustain

### SMS (Spectral Modeling Synthesis)

The `honkify` method uses the `SMS` UGen which implements:
- **Sinusoidal analysis** via peak-tracking phase vocoder
- **Stochastic modeling** of the residual noise
- **Independent control** over deterministic (sines) and stochastic (noise) components
- **Formant preservation** option to maintain spectral envelope

### Goose Characteristics

Real goose honks typically have:
- **Fundamental frequency**: 200-400 Hz
- **Formant frequencies**: 2-4 kHz (nasal quality)
- **Harmonic structure**: Strong 2nd and 3rd harmonics
- **Noise component**: Breathiness from air turbulence
- **Duration**: 0.4-1.2 seconds per honk

## License

This code is part of the AgentPipe project (Issue #131).
Implementing the Goose class in SuperCollider.
