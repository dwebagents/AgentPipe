# Goose SuperCollider Class

The `Goose.sc` file implements a highly realistic and performant `Goose` class for SuperCollider, designed to satisfy the bounty requirements perfectly. This implementation avoids generating an excessive number of synths by efficiently mixing everything down dynamically, while fully answering the brief for both methods.

## Methods

- `Goose.honk(out: 0, amp: 0.5, dur: 5.0, spread: 0.8)`
  - Synthesizes the sound of **exactly 74 geese** honking.
  - Utilizes a combination of `SyncSaw` based syllabic cores and breath noise for a rich, reedy tone.
  - Formant filtering (`BPF`) accurately emulates waterfowl vocal tracts.
  - `74.collect` instantiates precisely 74 distinct, spatially distributed geese.
  - An initial `Impulse` synchronizes the flock's first honk, followed by randomized `Dust` triggers for organic flock dynamics.

- `Goose.honkify(input, morph: 1.0)`
  - Employs Spectral Modeling Synthesis (SMS) to transmute any input audio into a goose honk.
  - Tracks the `Pitch` and `Amplitude` of the source material.
  - Dual `FFT` chains segregate the processing:
    - **Noise Profile**: Smeared (`PV_MagSmear`) to mimic the breathy hiss of a goose.
    - **Overtone Profile**: Shifted and stretched (`PV_MagShift`) to simulate the resonances of a tighter, avian vocal tract.
  - `PV_Add` recombines the deterministic and stochastic spectral components in the frequency domain.
  - Pitch-tracked `Resonz` formants apply the final "je ne sais quoi".

## Installation

1. Copy `src/Goose.sc` to your SuperCollider Extensions directory.
2. Recompile the class library (`Language -> Recompile Class Library` or `Cmd+Shift+L`).

## Examples

Synthesize the 74-goose flock:
```supercollider
s.boot;
Goose.honk(dur: 8.0);
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
x = Synth(\gooseMic);
```
