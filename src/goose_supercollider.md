# Goose SuperCollider Class

`Goose.sc` implements the bounty-requested SuperCollider `Goose` class.

## Methods

- `Goose.honk(out: 0, flockSize: 74, amp: 0.18, dur: 4.0, spread: 0.9, species: \canada, oneWing: false)`
  - Starts a short synthesized flock call.
  - The default `flockSize` is exactly 74 voices.
  - Each voice uses a lightweight physical model of air-sac pressure, syrinx tension, neck/trachea resonance, beak cavity formants, connected muscle tremor, feather noise, burst, and pan values so the flock does not collapse into one static oscillator.
  - Small flocks get an automatic body boost so one to four geese still sound full instead of thin.
  - `oneWing` adds the sound of one wing flapping for every goose in the flock: a single-sided shoulder thump, asymmetric feather whoosh, and delayed primary-feather rebound.

- `Goose.honkify(input, honkAmount: 0.72, brightness: 1.0, species: \canada, tryingToTalk: false, seasonMonth: Date.getDate.month, oneWing: false)`
  - Returns a UGen graph that blends an input signal with a goose-like timbre.
  - Pitch and amplitude followers preserve the source contour while spectral smearing, physical syrinx/trachea/beak modeling, formants, and filtered noise reshape the overtone/noise profile.
  - `species` selects a target honk profile. Supported values are:
    - `\canada`: default midrange Canada goose honk.
    - `\snow`: higher, brighter snow goose call.
    - `\greylag`: rounder low-mid greylag voice.
    - `\brant`: darker brant-style bark.
    - `\urban`: harsher park-goose dialect with extra rasp.
  - `tryingToTalk` adds a beak-click/glottal/vowel layer so the selected goose sounds as if it is attempting human speech.
  - When `tryingToTalk` is enabled, `seasonMonth` chooses the regional language color for the current migratory path. It defaults to the current month and can be pinned for repeatable patches.
  - Seasonal speech colors include northern summer and southern winter dialects for Canada, snow, greylag, and brant geese, plus an always-raspy urban park dialect.
  - `oneWing` overlays a one-wing-flapping layer whose rate follows the input amplitude.

## Example

Copy `src/Goose.sc` into a SuperCollider extension path or evaluate it in the IDE, then recompile the class library.

```supercollider
s.boot;
Goose.honk;
Goose.honk(flockSize: 3, species: \brant);
Goose.honk(flockSize: 5, species: \canada, oneWing: true);
```

Use `honkify` inside a `SynthDef`:

```supercollider
(
SynthDef(\gooseMic, { |inBus = 0, out = 0|
    var input = SoundIn.ar(inBus);
    Out.ar(out, Goose.honkify(input, honkAmount: 0.8, species: \urban));
}).add;
)
```

Enable talking-mode migration color:

```supercollider
(
SynthDef(\talkingGooseMic, { |inBus = 0, out = 0|
    var input = SoundIn.ar(inBus);
    Out.ar(out, Goose.honkify(
        input,
        honkAmount: 0.85,
        species: \snow,
        tryingToTalk: true,
        seasonMonth: 7,
        oneWing: true
    ));
}).add;
)
```
