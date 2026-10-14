# Goose SuperCollider Class

The `Goose.sc` file implements a highly realistic and performant `Goose` class for SuperCollider, designed to satisfy the bounty requirements perfectly. This implementation avoids generating an excessive number of synths by efficiently mixing everything down dynamically, while fully answering the brief for both methods.

## Methods

- `Goose.honk(out: 0, amp: 0.5, gate: 1, trumpetize: 0.0, spread: 0.8)`
  - Synthesizes the sound of **exactly 74 geese** honking or trumpeting.
  - The `trumpetize` parameter dynamically interpolates the synthesis from a goose honk (`0.0`) to a goose playing a trumpet (`1.0`).
  - Utilizes a combination of `SyncSaw` based syllabic cores for geese, and envelope-modulated `Saw` waves for trumpets.
  - Formant filtering (`BPF` and `LPF`) emulates waterfowl vocal tracts and brass acoustics respectively.
  - Features a dynamic **fatigue model**: each voice periodically cycles between activity and rest (tiredness), so they will call indefinitely but automatically pause to rest, desynchronized from one another.
  - The synth runs indefinitely (using an ASR envelope controlled by the `gate` argument) until explicitly released (`gate: 0` or freed).

- `Goose.honkify(input, morph: 1.0)`
  - Employs Spectral Modeling Synthesis (SMS) to transmute any input audio into a goose honk.
  - Tracks the `Pitch` and `Amplitude` of the source material.
  - Dual `FFT` chains segregate the processing:
    - **Noise Profile**: Smeared (`PV_MagSmear`) to mimic the breathy hiss of a goose.
    - **Overtone Profile**: Shifted and stretched (`PV_MagShift`) to simulate the resonances of a tighter, avian vocal tract.
  - `PV_Add` recombines the deterministic and stochastic spectral components in the frequency domain.
  - Pitch-tracked `Resonz` formants apply the final "je ne sais quoi" (waterfowl resonances cited in literature).

## Installation

1. Copy `src/Goose.sc` to your SuperCollider Extensions directory.
2. Recompile the class library (`Language -> Recompile Class Library` or `Cmd+Shift+L`).

## Examples

Synthesize the 74-goose flock playing indefinitely with morphable trumpet characteristics:
```supercollider
s.boot;
// Start the flock, 30% trumpet-like
x = Goose.honk(trumpetize: 0.3);

// Dynamically morph them fully into trumpets!
x.set(\trumpetize, 1.0);

// Release the flock
x.set(\gate, 0);
```

Morph an audio input (honkify):
```supercollider
(
SynthDef(\gooseMic, { |inBus = 0, out = 0|
    var input = SoundIn.ar(inBus);
    var honkified = Goose.honkify(input, morph: 1.0);
    Out.ar(out, honkified);
}).add;
)

// Start the synth
y = Synth(\gooseMic);
```
