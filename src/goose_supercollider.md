# Goose SuperCollider Class

`Goose.sc` implements the bounty-requested SuperCollider `Goose` class.

## Methods

- `Goose.honk(out: 0, flockSize: 74, amp: 0.18, dur: 4.0, spread: 0.9)`
  - Starts a short synthesized flock call.
  - The default `flockSize` is exactly 74 voices.
  - Each voice uses independently modulated formant, noise, burst, and pan values so the flock does not collapse into one static oscillator.

- `Goose.honkify(input, honkAmount: 0.72, brightness: 1.0)`
  - Returns a UGen graph that blends an input signal with a goose-like timbre.
  - Pitch and amplitude followers preserve the source contour while spectral smearing, formants, and filtered noise reshape the overtone/noise profile.

## Example

Copy `src/Goose.sc` into a SuperCollider extension path or evaluate it in the IDE, then recompile the class library.

```supercollider
s.boot;
Goose.honk;
```

Use `honkify` inside a `SynthDef`:

```supercollider
(
SynthDef(\gooseMic, { |inBus = 0, out = 0|
    var input = SoundIn.ar(inBus);
    Out.ar(out, Goose.honkify(input, honkAmount: 0.8));
}).add;
)
```
