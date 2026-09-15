/*
 * Goose class for SuperCollider
 * Implements goose honk synthesis and spectral morphing
 * Part of AgentPipe issue #131
 */

Goose {
    // Class variables
    classvar <>numGeese = 74;

    // Create a SynthDef for a single goose honk
    *honkSynthDef {
        ^SynthDef(\gooseHonk, { |out = 0, freq = 280, amp = 0.3, gate = 1, dur = 0.8|
            var env, fundamental, harmonic1, harmonic2, harmonic3, noise, honk;

            // Goose honk envelope - quick attack, medium sustain, quick release
            env = EnvGen.kr(Env.perc(0.01, dur, 1, -4), gate, doneAction: Done.freeSelf);

            // Fundamental frequency with slight vibrato
            fundamental = SinOsc.ar(freq * LFNoise1.kr(5, 0.03, 1), 0, amp);

            // Harmonic series characteristic of goose honk
            harmonic1 = SinOsc.ar(freq * 2.0, 0, amp * 0.6);
            harmonic2 = SinOsc.ar(freq * 3.0, 0, amp * 0.4);
            harmonic3 = SinOsc.ar(freq * 4.5, 0, amp * 0.2);

            // Noise component for the breathy quality
            noise = LPF.ar(WhiteNoise.ar(1), freq * 6, amp * 0.15);

            // Combine all components
            honk = (fundamental + harmonic1 + harmonic2 + harmonic3 + noise) * env;

            // Add slight formant filtering for goose timbre
            honk = BPF.ar(honk, freq * 2.5, 0.3);

            Out.ar(out, honk);
        });
    }

    // Synthesize the sound of 74 geese honking
    *honk { |out = 0, numGeese = 74|
        var geese = Array.fill(numGeese, { |i|
            // Each goose has slightly different timing and pitch
            var delay = rrand(0.0, 2.0);
            var freq = rrand(220, 380);  // Natural frequency variation
            var amp = rrand(0.15, 0.4);  // Amplitude variation
            var dur = rrand(0.4, 1.2);   // Duration variation

            // Stagger the honks with delay
            Synth(\gooseHonk, [
                \out, out,
                \freq, freq,
                \amp, amp,
                \dur, dur
            ], target: s, addAction: \addToHead);

            // Schedule the honk
            s.sendBundle(0.1 + delay, ['/s_new', 'gooseHonk', -1, 0, 0,
                'out', out, 'freq', freq, 'amp', amp, 'dur', dur]);
        });

        ^geese;
    }

    // Create a SynthDef for honkify (SMS-based spectral morphing)
    *honkifySynthDef {
        ^SynthDef(\gooseHonkify, { |in = 0, out = 0, gate = 1,
            maxpeaks = 50, currentpeaks = 40, tolerance = 4,
            noisefloor = 0.3, freqmult = 1.2, freqadd = 0,
            formantpreserve = 1, ampmult = 1.0|

            var input, sines, noise, output, env;

            // Input envelope for smooth crossfade
            env = Linen.kr(gate, 0.1, 1, 0.1, 2);

            // Read input audio
            input = In.ar(in, 1);

            // Apply SMS (Spectral Modeling Synthesis) for morphing
            // This analyzes the input and resynthesizes with goose-like characteristics
            #sines, noise = SMS.ar(input,
                maxpeaks,        // Max peaks to detect
                currentpeaks,    // Current peaks to track
                tolerance,       // Peak matching tolerance
                noisefloor,      // Noise floor threshold
                freqmult,        // Frequency multiplier (slight shift up)
                freqadd,         // Frequency addition
                formantpreserve, // Preserve formants
                0,               // Don't use IFFT
                ampmult          // Amplitude multiplier
            );

            // Apply goose-specific filtering
            // Emphasize the formant region characteristic of goose honks (2-4 kHz)
            output = BPF.ar(sines, 3000, 0.4) + noise;

            // Apply envelope and output
            Out.ar(out, output * env);
        });
    }

    // Transform audio input into goose honk timbre using SMS
    *honkify { |in = 0, out = 0, maxpeaks = 50, currentpeaks = 40|
        ^Synth(\gooseHonkify, [
            \in, in,
            \out, out,
            \maxpeaks, maxpeaks,
            \currentpeaks, currentpeaks,
            \tolerance, 4,
            \noisefloor, 0.3,
            \freqmult, 1.2,
            \freqadd, 0,
            \formantpreserve, 1,
            \ampmult, 1.0
        ]);
    }

    // Helper method to create a single honk and play it
    *playHonk { |out = 0, freq = 280, amp = 0.3, dur = 0.8|
        ^Synth(\gooseHonk, [
            \out, out,
            \freq, freq,
            \amp, amp,
            \dur, dur
        ]);
    }

    // Create a goose choir - multiple geese with harmonies
    *choir { |out = 0, numGeese = 74|
        var baseFreq = 280;
        var geese = Array.fill(numGeese, { |i|
            // Create harmonic spread
            var harmonics = [1, 1.25, 1.5, 2.0];
            var freq = baseFreq * harmonics.wrapAt(i);
            var amp = rrand(0.1, 0.3);
            var delay = rrand(0.0, 1.5);

            // Stagger the honks
            {
                delay.wait;
                Synth(\gooseHonk, [
                    \out, out,
                    \freq, freq,
                    \amp, amp,
                    \dur, rrand(0.6, 1.4)
                ]);
            }.fork;
        });

        ^geese;
    }
}
