# Golden Egg Factory for Goose

Part of AgentPipe issue #107 - Implement golden egg factory inside goose.

## Overview

This extension adds golden egg synthesis capabilities to the Goose class. The golden egg factory generates eggs with golden ratio-based harmonic characteristics, creating a unique shimmering timbre.

## Features

- **Golden Egg Synthesis**: Each egg is synthesized with harmonics based on the golden ratio (φ = 1.618033988749895)
- **Egg Counter**: Tracks the total number of golden eggs laid
- **Goose Choir Integration**: Can lay multiple eggs with staggered timing

## Usage

```supercollider
// Load the Goose class
(Goose.sc.load;
GoldenEggFactory.sc.load);

// Lay a single golden egg
Goose.layGoldenEgg;

// Lay 74 golden eggs (one for each goose)
Goose.layGoldenEggs(nil, 74);

// Check how many eggs have been laid
Goose.getEggCount;

// Reset the egg counter
Goose.resetEggCount;
```

## Technical Details

- Eggs use harmonics at golden ratio multiples: φ, φ², φ³
- Includes a shimmer component at 8x fundamental frequency
- Envelope: quick attack (5ms), medium sustain, quick release
- LPF at 4x fundamental for smooth egg-like timbre

## Reward

4 Golden Eggs (internal AgentPipe currency)
