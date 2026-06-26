Goose {
    *honk { |out=0, amp=0.5, dur=5.0, spread=0.8|
        ^{
            var env = EnvGen.kr(Env.linen(0.1, dur - 0.2, 0.1), doneAction: 2);
            var flock = 74.collect { |i|
                // Each goose gets a unique base frequency and characteristics
                var baseFreq = ExpRand(200.0, 500.0);
                // Trigger at start, plus random occasional honks
                var trig = Impulse.kr(0) + Dust.kr(LFNoise1.kr(0.1).range(0.5, 2.0));
                
                // Frequency envelope for the honk shape
                var freqEnv = EnvGen.kr(Env(
                    [baseFreq * 0.8, baseFreq * 1.2, baseFreq * 0.9, baseFreq], 
                    [0.05, 0.1, 0.1], 
                    \exp
                ), trig);
                
                // Amplitude envelope for the honk
                var honkEnv = EnvGen.kr(Env.perc(0.02, Rand(0.2, 0.4)), trig);
                
                // Syllabic core generator (SyncSaw produces a rich, reedy tone)
                var core = SyncSaw.ar(freqEnv, freqEnv * Rand(1.5, 2.5));
                var noise = WhiteNoise.ar * 0.3;
                var source = (core + noise) * honkEnv;
                
                // Vocal tract formants typical of waterfowl
                var f1 = BPF.ar(source, baseFreq * 2.2, 0.2);
                var f2 = BPF.ar(source, baseFreq * 4.4, 0.3);
                var f3 = BPF.ar(source, baseFreq * 6.5, 0.4);
                
                var goose = (f1 + f2 + f3) * 2.0;
                
                Pan2.ar(goose, Rand(-1.0, 1.0) * spread)
            }.sum;
            
            Out.ar(out, flock * env * amp * (1 / 74.sqrt));
        }.play;
    }

    *honkify { |input, morph=1.0|
        var in = input.asArray;
        var mono = in.size > 1.if({ Mix(in) }, { in });
        
        // Track the original pitch and amplitude
        var pitch, hasPitch, amp;
        # pitch, hasPitch = Pitch.kr(mono, minFreq: 50, maxFreq: 1200, ampThreshold: 0.01);
        pitch = pitch.lag(0.05);
        amp = Amplitude.kr(mono, 0.01, 0.1);
        
        ^in.collect { |chan|
            var chainA, chainB, noiseProfile, overtoneProfile;
            var resynth, gooseFormants;
            
            chainA = FFT(LocalBuf(2048), chan);
            chainB = FFT(LocalBuf(2048), chan);
            
            // Morph the noise profile: smear the spectrum to simulate airy breathiness of a goose
            noiseProfile = PV_MagSmear(chainB, bins: 25);
            
            // Morph the overtones: shift the magnitudes to replicate a goose's tighter vocal tract
            overtoneProfile = PV_MagShift(chainA, stretch: 1.1 + (0.2 * morph), shift: 10 * morph);
            
            // Spectral Modeling Synthesis: Recombine morphed deterministic and stochastic components
            resynth = IFFT(PV_Add(overtoneProfile, noiseProfile)) * 0.5;
            
            // Additional physical modeling: apply typical goose resonant formants
            gooseFormants = Resonz.ar(resynth, pitch * 2.1, 0.2) + 
                            Resonz.ar(resynth, pitch * 4.3, 0.3);
                            
            // Retain original loudness and mix based on morph amount
            XFade2.ar(chan, gooseFormants * amp * 8.0, morph * 2 - 1);
        };
    }
}
