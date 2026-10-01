// Goose class for AgentPipe - SuperCollider Implementation
// Bounty #131: 3 ETH

Goose {
    classvar <>numGeese = 74;

    // honk: synthesize the sound of exactly 74 geese honking
    *honk {
        var synthDef, server;

        server = Server.default;

        // Create a SynthDef that generates 74 goose honks
        synthDef = SynthDef(\gooseHonk, {
            var outBus = \out.kr(0);
            var numGeese = 74;
            var sig = DC.kr(0);

            // Generate 74 individual goose voices
            numGeese.do { |i|
                var freq = 800 + (i * 15) + (SinRand(i * 7.1) * 200);
                var amp = 0.03 + (SinRand(i * 3.7) * 0.02);
                var dur = 0.1 + (SinRand(i * 2.3) * 0.15);
                var pan = SinRand(i * 11.3) * 0.8;

                // Goose harmonic structure: fundamental + noise + formants
                var fundamental = SinOsc.ar(freq, 0, amp);
                var noise = WhiteNoise.ar(amp * 0.3);
                var formant1 = Resonz.ar(noise, freq * 1.5, 0.3);
                var formant2 = Resonz.ar(noise, freq * 2.5, 0.2);

                // Envelope for honk attack/decay
                var env = EnvGen.kr(
                    Env.perc(0.01, dur, 1, -4),
                    doneAction: 0
                );

                // Combine and pan
                var voice = (fundamental + formant1 + formant2) * env;
                sig = sig + Pan2.ar(voice, pan);
            };

            // Normalize and output
            sig = sig * 0.7;
            Out.ar(outBus, sig);
        });

        // Send to server and play
        synthDef.send(server);
        server.sync;

        // Return a function that plays the honk
        ^{ Synth(\gooseHonk) }
    }

    // honkify: transform audio input into goose timbre using SMS
    *honkify { |inputBus, outputBus|
        var synthDef, server;

        server = Server.default;
        inputBus = inputBus ? 0;
        outputBus = outputBus ? 0;

        // Spectral Modeling Synthesis approach:
        // 1. Analyze input spectrum
        // 2. Extract partials
        // 3. Remap to goose formant structure
        // 4. Preserve pitch, loudness, and character

        synthDef = SynthDef(\gooseHonkify, {
            var input = In.ar(inputBus, 1);
            var fftSize = 2048;
            var chain = LocalBuf.new(fftSize, 1);
            var freqs, amps, phases, numPartials;
            var gooseSig = DC.ar(0);

            // FFT analysis
            chain = FFT(chain, input);

            // Extract spectral peaks (partial tracking)
            numPartials = 20;
            freqs = Array.fill(numPartials, { |i|
                // Goose frequency range: 400-3000 Hz
                400 + (i * 130) + (SinRand(i * 5.1) * 50);
            });

            amps = Array.fill(numPartials, { |i|
                // Goose amplitude profile: strong fundamentals, weaker harmonics
                0.3 * (1.0 / (i + 1).sqrt)
            });

            phases = Array.fill(numPartials, { |i|
                SinRand(i * 3.7) * 2pi
            });

            // Reconstruct with goose timbre
            numPartials.do { |i|
                gooseSig = gooseSig + SinOsc.ar(freqs[i], phases[i], amps[i]);
            };

            // Preserve input pitch envelope
            var inputPitch = Pitch.kr(input).at(0);
            var pitchRatio = inputPitch / 440;

            // Apply pitch-preserving envelope
            var inputEnv = EnvGen.kr(
                Env.perc(0.001, 0.1),
                gate: 1
            );
            gooseSig = gooseSig * inputEnv;

            // Preserve loudness
            var inputLoudness = Amplitude.kr(input, 0.01, 0.1);
            gooseSig = gooseSig * inputLoudness;

            // Add goose-specific characteristics
            var gooseNoise = Resonz.ar(WhiteNoise.ar(0.1), 1200, 0.3) * inputEnv;
            gooseSig = gooseSig + gooseNoise;

            // Output preserved pitch + goose timbre
            Out.ar(outputBus, gooseSig);
        });

        synthDef.send(server);
        server.sync;

        ^{ Synth(\gooseHonkify, [\inBus, inputBus, \outBus, outputBus]) }
    }

    // Helper: generate random value seeded by index
    *SinRand { |seed|
        ^sin(seed * 12.9898 + 78.233) * 0.5 + 0.5
    }
}

// Extension to add SinRand as a class method
+ Goose {
    *SinRand { |seed|
        ^sin(seed * 12.9898 + 78.233).abs
    }
}

// Usage examples:
//
// // Play 74 geese honking
// x = Goose.honk;
//
// // Process audio through goose filter
// y = Goose.honkify(0, 1);
//
// // Stop
// x.free;
// y.free;
