# Goose SuperCollider Class

**Bounty:** 3 ETH (Issue #131)

## Overview

A SuperCollider class for synthesizing realistic goose calls and morphing audio into goose honks.

## Installation

1. Copy `src/Goose.sc` to your SuperCollider Extensions directory:
   - **macOS:** `~/Library/Application Support/SuperCollider/Extensions/`
   - **Linux:** `~/.local/share/SuperCollider/Extensions/`
   - **Windows:** `%USERPROFILE%\Documents\SuperCollider\Extensions\`

2. Recompile class library: `Language → Recompile Class Library` or `Cmd+Shift+L`

## Usage

### Basic Honk — Default 74 Canada geese

```supercollider
s.boot;
Goose.honk;  // 74 Canada geese, 4 seconds
```

### Variable flock size

```supercollider
Goose.honk(flockSize: 12, species: \brant);
Goose.honk(flockSize: 3, species: \urban, dur: 6.0);
```

### Airborne geese (with doppler shift and altitude attenuation)

```supercollider
Goose.honk(airborne: 0.4, spread: 1.0);  // 40% airborne, 60% ground
```

### Aggressive geese

```supercollider
Goose.honk(aggression: 0.8, species: \swanGoose);
```

### Territorial dynamics (sidechain input)

```supercollider
// Create a sidechain bus
~side = Bus.audio(s, 1);

// Start a goose flock that responds to other synths
Goose.honk(sidechainBus: ~side.index, aggression: 0.3);

// Play an approaching synth that triggers territorial behavior
SynthDef(\approach, { |out=0|
    var sig = Saw.ar(80) * EnvGen.kr(Env.perc(0.1, 3), doneAction: 2);
    Out.ar(out, sig);
}).add;
Synth(\approach, [\out, ~side]);
```

### Honkify — morph audio into goose

```supercollider
SynthDef(\gooseMic, { |inBus = 0|
    var input = SoundIn.ar(inBus);
    Goose.honkify(input, honkAmount: 0.8, species: \urban);
}).add;

y = Synth(\gooseMic);
```

### Talking goose (migratory dialects)

```supercollider
// Snow goose trying to speak Inuktitut (July — breeding grounds)
SynthDef(\talkingGoose, { |inBus = 0|
    var input = SoundIn.ar(inBus);
    Goose.honkify(
        input,
        honkAmount: 0.85,
        species: \snow,
        tryingToTalk: true,
        seasonMonth: 7   // July — Inuktitut
    );
}).add;
```

## API Reference

### `Goose.honk(out, flockSize, amp, dur, spread, species, airborne, aggression, sidechainBus)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `out` | Integer | 0 | Audio output bus |
| `flockSize` | Integer | 74 | Number of geese (1–128) |
| `amp` | Float | 0.18 | Amplitude |
| `dur` | Float | 4.0 | Duration in seconds |
| `spread` | Float | 0.9 | Pan spread (0=mono, 1=full stereo) |
| `species` | Symbol | `\canada` | Species profile |
| `airborne` | Float | 0.0 | Fraction of airborne geese (0–1) |
| `aggression` | Float | 0.0 | Aggression level (0–1) |
| `sidechainBus` | Integer | nil | Audio bus for territorial dynamics |

### `Goose.honkify(input, honkAmount, brightness, species, tryingToTalk, seasonMonth, sidechainBus)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | UGen | — | Audio input to morph |
| `honkAmount` | Float | 0.72 | Wet/dry mix (0=dry, 1=full goose) |
| `brightness` | Float | 1.0 | Spectral brightness multiplier |
| `species` | Symbol | `\canada` | Species profile |
| `tryingToTalk` | Boolean | false | Enable talking goose mode |
| `seasonMonth` | Integer | current | Month (1–12) for migratory dialect |
| `sidechainBus` | Integer | nil | Audio bus for territorial dynamics |

## Species

| Species | Description |
|---------|-------------|
| `\canada` | Canada goose (default) |
| `\snow` | Snow goose — higher pitch, thinner |
| `\greylag` | Greylag goose — deeper, fuller |
| `\brant` | Brant goose — lowest, gruffest |
| `\urban` | City goose — aggressive, loud |
| `\swanGoose` | Aggressive hybrid — for territorial scenarios |

## Migratory Dialects

When `tryingToTalk` is enabled, geese speak according to their species' seasonal migration patterns:

| Species | Summer Language | Winter Language |
|---------|----------------|-----------------|
| Canada | Cree (Apr–Sep) | English (Oct–Mar) |
| Snow | Inuktitut (Apr–Aug) | Spanish (Sep–Mar) |
| Greylag | Norwegian (Mar–Sep) | Arabic (Oct–Feb) |
| Brant | Greenlandic (May–Aug) | English (Sep–Apr) |
| Urban | Park Dialect (year-round) | Park Dialect (year-round) |

## Technical Notes

- Spectral Modeling Synthesis (SMS) via FFT `PV_MagShift` + `PV_MagSmear`
- 4-layer voice synthesis: additive + subtractive + nasal formant + rasp noise
- Airborne geese: doppler shift via `SinOsc`, altitude attenuation, FreeVerb reverb
- Ground geese: early reflection delay (~5ms tap) for ground coupling
- Territorial aggression: sidechain amplitude tracking modulates voice harshness
