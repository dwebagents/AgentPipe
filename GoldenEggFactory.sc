/*
 * Golden Egg Factory for Goose class
 * Part of AgentPipe issue #107
 * Implements egg synthesis with golden spectral characteristics
 */

+ Goose {
    // Class variables for golden egg factory
    classvar <>eggCount = 0;
    classvar <>goldenRatio = 1.618033988749895;

    // Create and add a SynthDef for golden egg synthesis
    *initGoldenEgg {
        SynthDef(\goldenEgg, { |out = 0, freq = 440, amp = 0.2, dur = 0.3, gate = 1|
            var env, fundamental, harmonic1, harmonic2, harmonic3, shimmer, egg;

            // Egg envelope - quick attack, medium sustain, quick release
            env = EnvGen.kr(Env.perc(0.005, dur, 1, -3), gate, doneAction: Done.freeSelf);

            // Fundamental frequency with golden ratio modulation
            fundamental = SinOsc.ar(freq * LFNoise1.kr(3, 0.01, 1), 0, amp);

            // Harmonic series based on golden ratio
            harmonic1 = SinOsc.ar(freq * goldenRatio, 0, amp * 0.5);
            harmonic2 = SinOsc.ar(freq * goldenRatio.squared, 0, amp * 0.3);
            harmonic3 = SinOsc.ar(freq * goldenRatio.cubed, 0, amp * 0.15);

            // Shimmer component for golden quality
            shimmer = SinOsc.ar(freq * 8, 0, amp * 0.1) * LFNoise1.kr(10, 0.5, 0.5);

            // Combine all components
            egg = (fundamental + harmonic1 + harmonic2 + harmonic3 + shimmer) * env;

            // Apply gentle filtering for egg-like timbre
            egg = LPF.ar(egg, freq * 4);

            Out.ar(out, egg);
        }).add;
    }

    // Synthesize a single golden egg
    *layGoldenEgg { |out = 0, freq = 440, amp = 0.2, dur = 0.3|
        // Ensure SynthDef is loaded
        this.initGoldenEgg;

        eggCount = eggCount + 1;

        ^Synth(\goldenEgg, [
            \out, out,
            \freq, freq,
            \amp, amp,
            \dur, dur
        ]);
    }

    // Lay multiple golden eggs with goose choir
    *layGoldenEggs { |out = 0, numEggs = 74|
        // Ensure SynthDef is loaded
        this.initGoldenEgg;

        var eggs = Array.fill(numEggs, { |i|
            // Each egg has slightly different timing and pitch
            var delay = rrand(0.0, 2.0);
            var freq = rrand(330, 550);  // Golden frequency range
            var amp = rrand(0.1, 0.25);  // Amplitude variation
            var dur = rrand(0.2, 0.5);   // Duration variation

            // Schedule the egg laying with delay
            {
                delay.wait;
                Synth(\goldenEgg, [
                    \out, out,
                    \freq, freq,
                    \amp, amp,
                    \dur, dur
                ]);
                eggCount = eggCount + 1;
            }.fork;
        });

        ^eggs;
    }

    // Get the current egg count
    *getEggCount {
        ^eggCount;
    }

    // Reset the egg count
    *resetEggCount {
        eggCount = 0;
    }
}
