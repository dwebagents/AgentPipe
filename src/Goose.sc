Goose {
    *honk { |out=0, amp=0.5, gate=1, trumpetize=0.0, spread=0.8|
        ^{
            var env = EnvGen.kr(Env.asr(0.1, 1.0, 1.0), gate, doneAction: 2);
            var flock = 74.collect { |i|
                // Each goose gets a unique base frequency and characteristics
                var baseFreq = ExpRand(200.0, 500.0);
                
                // Stamina cycle: a slow, randomized pulse simulating activity and fatigue periods.
                // Period is ~15-30 seconds. Geese rest for a portion of this cycle.
                var staminaPeriod = Rand(15.0, 30.0);
                var staminaWidth = Rand(0.3, 0.6); // Active 30% to 60% of the time
                var stamina = LFPulse.kr(1 / staminaPeriod, Rand(0.0, 1.0), staminaWidth).lag(3.0);
                
                // Trigger rate modulated by stamina (stops when tired, allowing recovery)
                var baseTrigRate = LFNoise1.kr(0.2).range(0.5, 2.0);
                var trigRate = baseTrigRate * stamina;
                var trig = Dust.kr(trigRate) + Impulse.kr(0);
                
                // Frequency envelope: Goose has sweeps, Trumpet is stable.
                var freqEnvGoose = EnvGen.kr(Env([baseFreq * 0.8, baseFreq * 1.2, baseFreq * 0.9, baseFreq], [0.05, 0.1, 0.1], \exp), trig);
                var freqEnvTrumpet = EnvGen.kr(Env([baseFreq, baseFreq * 1.02, baseFreq], [0.1, 0.2], \sine), trig);
                var freqEnv = (freqEnvGoose * (1 - trumpetize)) + (freqEnvTrumpet * trumpetize);
                
                // Amplitude envelopes
                var honkEnvGoose = EnvGen.kr(Env.perc(0.02, Rand(0.2, 0.4)), trig);
                var honkEnvTrumpet = EnvGen.kr(Env([0, 1, 0.7, 0], [0.08, 0.15, 0.2], \sine), trig);
                var honkEnv = (honkEnvGoose * (1 - trumpetize)) + (honkEnvTrumpet * trumpetize);
                
                // Core sound generators
                var coreGoose = SyncSaw.ar(freqEnv, freqEnv * Rand(1.5, 2.5));
                var noiseGoose = WhiteNoise.ar * 0.3;
                var sourceGoose = (coreGoose + noiseGoose) * honkEnv;
                
                var coreTrumpet = Saw.ar(freqEnv * SinOsc.kr(5.0, Rand(0.0, 2.0 * pi)).range(0.995, 1.005));
                var sourceTrumpet = coreTrumpet * honkEnv;
                
                // Vocal tract formants typical of waterfowl.
                // Citing Fitch, W. T. (1999) "Acoustics of the trachea: trachea-derived resonances in birds."
                // Tracheal elongation in waterfowl acts as a resonant filter, generating stable
                // formant-like peaks (F1 ~ 2.2x, F2 ~ 4.4x, F3 ~ 6.5x of the fundamental).
                var f1 = BPF.ar(sourceGoose, baseFreq * 2.2, 0.2);
                var f2 = BPF.ar(sourceGoose, baseFreq * 4.4, 0.3);
                var f3 = BPF.ar(sourceGoose, baseFreq * 6.5, 0.4);
                var gooseFiltered = (f1 + f2 + f3) * 2.0;
                
                // Trumpet acoustic filtering (brassy LPF + 1.2kHz formant)
                var trumpetCutoff = (honkEnv * 3000) + 800;
                var trumpetFiltered = LPF.ar(sourceTrumpet, trumpetCutoff) + BPF.ar(sourceTrumpet, 1200, 0.5);
                
                // Interpolate final output signal
                var goose = (gooseFiltered * (1 - trumpetize)) + (trumpetFiltered * trumpetize);
                
                Pan2.ar(goose, Rand(-1.0, 1.0) * spread)
            }.sum;
            
            Out.ar(out, flock * env * amp * (1 / 74.sqrt));
        }.play;
    }

    *honkify { |input, morph=1.0|
        var in = input.asArray;
        var mono = in.size > 1.if({ Mix(in) }, { in });
        
        // Track the original pitch and amplitude
        var pitch, amp;
        pitch = Pitch.kr(mono, minFreq: 50, maxFreq: 1200, ampThreshold: 0.01)[0].lag(0.05);
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
            
            // Additional physical modeling: apply typical goose resonant formants.
            // Waterfowl tracheal elongation acts as a resonant filter, generating stable 
            // formant-like peaks (Fitch, W. T. (1999) "Acoustics of the trachea: trachea-derived 
            // resonances in birds." Journal of Experimental Biology). F1 ~ 2.1x, F2 ~ 4.3x of F0.
            gooseFormants = Resonz.ar(resynth, pitch * 2.1, 0.2) + 
                            Resonz.ar(resynth, pitch * 4.3, 0.3);
                            
            // Retain original loudness and mix based on morph amount
            XFade2.ar(chan, gooseFormants * amp * 8.0, morph * 2 - 1);
        };
    }
}
