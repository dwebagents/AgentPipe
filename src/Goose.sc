// Goose.sc
// SuperCollider Goose class — Bounty: 3 ETH (Issue #131)
// Synthesizes 74 geese honking and morphs audio input into goose sounds.
// Implements: honk, honkify, species profiles, migratory dialects,
// airborne modeling (doppler + reflections), territorial social dynamics (sidechain),
// flock size parameter, and talking mode.

Goose {

    classvar <defaultFlockSize;

    *initClass {
        defaultFlockSize = 74;
    }

    // ------------------------------------------------------------
    // Species acoustic profiles
    // ------------------------------------------------------------
    *profileFor { |species|
        ^Dictionary.with(
            \canada -> Dictionary.with(
                \fundLo, 175, \fundHi, 430,
                \formantA, 2.05, \formantB, 2.72, \bw, 0.34,
                \fmRatio, 1.42, \fmDepth, 0.18,
                \noiseFormant, 3.35, \rasp, 0.5, \chop, 5.1, \pulseWidth, 0.34
            ),
            \snow -> Dictionary.with(
                \fundLo, 260, \fundHi, 610,
                \formantA, 2.35, \formantB, 3.1, \bw, 0.22,
                \fmRatio, 1.72, \fmDepth, 0.12,
                \noiseFormant, 4.1, \rasp, 0.35, \chop, 7.4, \pulseWidth, 0.28
            ),
            \greylag -> Dictionary.with(
                \fundLo, 150, \fundHi, 380,
                \formantA, 1.9, \formantB, 2.55, \bw, 0.42,
                \fmRatio, 1.28, \fmDepth, 0.24,
                \noiseFormant, 3.0, \rasp, 0.48, \chop, 4.6, \pulseWidth, 0.38
            ),
            \brant -> Dictionary.with(
                \fundLo, 95, \fundHi, 260,
                \formantA, 1.55, \formantB, 2.1, \bw, 0.5,
                \fmRatio, 0.86, \fmDepth, 0.32,
                \noiseFormant, 2.45, \rasp, 0.62, \chop, 3.3, \pulseWidth, 0.46
            ),
            \urban -> Dictionary.with(
                \fundLo, 190, \fundHi, 470,
                \formantA, 2.12, \formantB, 2.9, \bw, 0.32,
                \fmRatio, 1.48, \fmDepth, 0.2,
                \noiseFormant, 3.6, \rasp, 0.58, \chop, 5.7, \pulseWidth, 0.33
            ),
            \swanGoose -> Dictionary.with(  // aggressive hybrid
                \fundLo, 120, \fundHi, 350,
                \formantA, 1.7, \formantB, 2.3, \bw, 0.5,
                \fmRatio, 1.1, \fmDepth, 0.35,
                \noiseFormant, 2.8, \rasp, 0.8, \chop, 3.0, \pulseWidth, 0.5
            ),
            // ---- Mythological & Sci-Fi Geese ----
            \darthGoose -> Dictionary.with(  // heavy, dark, mechanical breathing
                \fundLo, 65, \fundHi, 180,
                \formantA, 1.3, \formantB, 1.8, \bw, 0.65,
                \fmRatio, 0.5, \fmDepth, 0.48,
                \noiseFormant, 1.8, \rasp, 0.95, \chop, 1.8, \pulseWidth, 0.72
            ),
            \cyborgGoose -> Dictionary.with(  // metallic overtones, glitchy
                \fundLo, 220, \fundHi, 520,
                \formantA, 2.6, \formantB, 3.8, \bw, 0.18,
                \fmRatio, 2.4, \fmDepth, 0.32,
                \noiseFormant, 4.8, \rasp, 0.7, \chop, 12.0, \pulseWidth, 0.22
            ),
            \klingonGoose -> Dictionary.with(  // guttural, warrior honks
                \fundLo, 90, \fundHi, 250,
                \formantA, 1.4, \formantB, 1.9, \bw, 0.58,
                \fmRatio, 0.7, \fmDepth, 0.45,
                \noiseFormant, 2.2, \rasp, 0.88, \chop, 2.5, \pulseWidth, 0.6
            ),
            \the74thDoctor -> Dictionary.with(  // timey-wimey, phase-shifting
                \fundLo, 310, \fundHi, 720,
                \formantA, 2.85, \formantB, 3.6, \bw, 0.15,
                \fmRatio, 3.1, \fmDepth, 0.28,
                \noiseFormant, 5.2, \rasp, 0.3, \chop, 8.6, \pulseWidth, 0.2
            ),
            \redLectroid -> Dictionary.with(  // 5th dimension — alien, detuned
                \fundLo, 500, \fundHi, 1200,
                \formantA, 3.4, \formantB, 4.6, \bw, 0.12,
                \fmRatio, 4.2, \fmDepth, 0.4,
                \noiseFormant, 6.0, \rasp, 0.45, \chop, 14.0, \pulseWidth, 0.15
            ),
            \goosezilla -> Dictionary.with(  // gargantuan, seismic
                \fundLo, 25, \fundHi, 80,
                \formantA, 0.8, \formantB, 1.2, \bw, 0.85,
                \fmRatio, 0.3, \fmDepth, 0.55,
                \noiseFormant, 1.2, \rasp, 0.98, \chop, 0.8, \pulseWidth, 0.88
            ),
            \goosenesha -> Dictionary.with(  // many-armed, swirling harmonics
                \fundLo, 140, \fundHi, 360,
                \formantA, 2.2, \formantB, 3.3, \bw, 0.28,
                \fmRatio, 1.8, \fmDepth, 0.38,
                \noiseFormant, 3.9, \rasp, 0.55, \chop, 6.2, \pulseWidth, 0.3
            ),
            \antigoose -> Dictionary.with(  // phase-inverted, hollow
                \fundLo, 200, \fundHi, 490,
                \formantA, 1.1, \formantB, 1.6, \bw, 0.72,
                \fmRatio, 0.4, \fmDepth, 0.5,
                \noiseFormant, 1.5, \rasp, 0.6, \chop, 2.2, \pulseWidth, 0.78
            ),
            \gooseitan -> Dictionary.with(  // demonic, distorted
                \fundLo, 55, \fundHi, 150,
                \formantA, 1.2, \formantB, 1.5, \bw, 0.78,
                \fmRatio, 0.6, \fmDepth, 0.52,
                \noiseFormant, 1.6, \rasp, 0.92, \chop, 1.4, \pulseWidth, 0.82
            ),
            \gooseGodOfHonk -> Dictionary.with(  // divine, resonant, pure honk
                \fundLo, 432, \fundHi, 864,
                \formantA, 3.0, \formantB, 4.0, \bw, 0.08,
                \fmRatio, 2.0, \fmDepth, 0.1,
                \noiseFormant, 4.4, \rasp, 0.1, \chop, 10.0, \pulseWidth, 0.18
            ),
            \nethergoose -> Dictionary.with(  // underworld, murky, subsonic
                \fundLo, 40, \fundHi, 110,
                \formantA, 0.9, \formantB, 1.3, \bw, 0.82,
                \fmRatio, 0.35, \fmDepth, 0.58,
                \noiseFormant, 1.3, \rasp, 0.96, \chop, 1.0, \pulseWidth, 0.85
            ),
            \gooseAtEndOfTime -> Dictionary.with(  // eternal, slowly evolving
                \fundLo, 30, \fundHi, 70,
                \formantA, 0.6, \formantB, 0.9, \bw, 0.9,
                \fmRatio, 0.2, \fmDepth, 0.6,
                \noiseFormant, 1.0, \rasp, 0.99, \chop, 0.5, \pulseWidth, 0.9
            )
        ).at(species ? \canada) ?? {
            this.profileFor(\canada)
        };
    }

    // ------------------------------------------------------------
    // Migratory dialect profiles (per species, per season)
    // ------------------------------------------------------------
    *migratoryDialectFor { |species, month|
        month = month ? Date.getDate.month;
        var dialects = Dictionary.with(
            \canada -> Dictionary.with(
                (4..9) -> Dictionary.with(\language, "Cree", \phraseRate, 0.7, \vowelLo, 280, \vowelHi, 650, \nasal, 0.4, \consonants, 0.6, \syllableWidth, 0.12),
                (10,11,12,1,2,3) -> Dictionary.with(\language, "English", \phraseRate, 1.0, \vowelLo, 320, \vowelHi, 720, \nasal, 0.2, \consonants, 0.8, \syllableWidth, 0.08)
            ),
            \snow -> Dictionary.with(
                (4..8) -> Dictionary.with(\language, "Inuktitut", \phraseRate, 0.6, \vowelLo, 260, \vowelHi, 630, \nasal, 0.5, \consonants, 0.5, \syllableWidth, 0.14),
                (9..12,1..3) -> Dictionary.with(\language, "Spanish", \phraseRate, 0.9, \vowelLo, 300, \vowelHi, 700, \nasal, 0.25, \consonants, 0.7, \syllableWidth, 0.09)
            ),
            \greylag -> Dictionary.with(
                (3..9) -> Dictionary.with(\language, "Norwegian", \phraseRate, 0.65, \vowelLo, 250, \vowelHi, 600, \nasal, 0.35, \consonants, 0.65, \syllableWidth, 0.11),
                (10..12,1..2) -> Dictionary.with(\language, "Arabic", \phraseRate, 0.85, \vowelLo, 310, \vowelHi, 710, \nasal, 0.3, \consonants, 0.75, \syllableWidth, 0.1)
            ),
            \brant -> Dictionary.with(
                (5..8) -> Dictionary.with(\language, "Greenlandic", \phraseRate, 0.5, \vowelLo, 220, \vowelHi, 550, \nasal, 0.55, \consonants, 0.4, \syllableWidth, 0.16),
                (9..12,1..4) -> Dictionary.with(\language, "English", \phraseRate, 0.95, \vowelLo, 330, \vowelHi, 730, \nasal, 0.15, \consonants, 0.85, \syllableWidth, 0.07)
            ),
            \urban -> Dictionary.with(
                (1..12) -> Dictionary.with(\language, "ParkDialect", \phraseRate, 1.2, \vowelLo, 350, \vowelHi, 800, \nasal, 0.1, \consonants, 0.9, \syllableWidth, 0.06)
            )
        );
        var speciesDialects = dialects.at(species ? \canada) ?? dialects.at(\canada);
        var match = speciesDialects.associations.detect { |assoc|
            assoc.key.includes(month)
        };
        ^match.value ?? speciesDialects.at(speciesDialects.keys.asArray.sort.first);
    }

    // ------------------------------------------------------------
    // Voice synthesis core — single goose voice, trauma-modulated
    // ------------------------------------------------------------
    *voice { |baseFreq, profile, ampGate=1, aggression=0, traumaSeed=0|
        var freq = baseFreq * LFNoise1.kr(Rand(0.3, 1.0)).exprange(0.85, 1.18);
        var pulseWidth = profile[\pulseWidth] * aggression.linlin(0, 1, 1, 1.8);
        pulseWidth = pulseWidth.min(0.95);
        
        // Trauma model: each goose carries a unique trauma history
        // encoded as a seed that modulates partial detuning and ADSR shape.
        // Honk overtone pitches shift based on the severity and type of past trauma.
        var tSeed = Rand(0, 1);  // unique trauma seed per goose voice
        var tSeverity = LFNoise1.kr(Rand(0.05, 0.15)).range(0, 1);  // trauma severity (slowly evolving)
        var tTypeA = LFNoise1.kr(Rand(0.03, 0.08)).range(-1, 1);    // trauma dimension A: emotional (abandonment / nurturing)
        var tTypeB = LFNoise1.kr(Rand(0.04, 0.1)).range(-1, 1);     // trauma dimension B: physical (injury / safety)
        var tTypeC = LFNoise1.kr(Rand(0.02, 0.06)).range(-1, 1);    // trauma dimension C: existential (cosmic honk dread)
        
        // Trauma modulates the fundamental — wounded geese honk sharper
        var traumaPitchShift = 1 + (tSeverity * (tTypeA * 0.08 + tTypeB * 0.05 + tTypeC * 0.03));
        var traumaFreq = freq * traumaPitchShift;
        
        // Layer 1: Additive — 4 detuned partials, each with its own ADSR envelope
        // and trauma-modulated detuning per partial
        var addSig = Mix.fill(4, { |j|
            var ratio = 1 + (j * 0.5);
            // Trauma detuning per partial — each partial encodes a different traumatic memory
            var partialTrauma = tSeverity * (
                (tTypeA * sin(j * 1.3 + tSeed * 2pi)) +
                (tTypeB * cos(j * 0.7 + tSeed * pi)) +
                (tTypeC * sin(j * 2.1 + tSeed * 0.5pi))
            );
            var detune = Rand(-0.03, 0.03) + (partialTrauma * 0.06);
            
            // Per-partial ADSR envelope — shaped by trauma
            // Traumatized geese have erratic envelope shapes (jagged attack, tremoring sustain)
            var pAttack = (0.01 + (tSeverity * 0.15 * max(0, tTypeA))) * Rand(0.5, 2.0);
            var pDecay = (0.05 + (tSeverity * 0.3 * max(0, -tTypeB))) * Rand(0.5, 2.0);
            var pSustain = (0.3 + (tSeverity * 0.5 * max(0, tTypeC))) * Rand(0.5, 1.5);
            var pRelease = (0.02 + (tSeverity * 0.2 * max(0, -tTypeA))) * Rand(0.5, 2.0);
            var pCurve = -4 - (tSeverity * 6 * tTypeB);  // trauma warps the curve
            
            var partialEnv = EnvGen.kr(
                Env.adsr(pAttack, pDecay, pSustain.min(1), pRelease, curve: pCurve),
                gate: ampGate,
                doneAction: 0
            );
            
            SinOsc.ar(traumaFreq * ratio * (1 + detune), mul: 0.08 / (j + 1) * partialEnv)
        });
        
        // Layer 2: Subtractive — VarSaw through resonant filter
        var src = VarSaw.ar(freq, width: pulseWidth);
        var subSig = RLPF.ar(src, freq * profile[\formantA], profile[\bw].linexp(0.1, 0.8, 0.5, 0.05));
        
        // Layer 3: Nasal formant
        var nasal = BPF.ar(WhiteNoise.ar(0.03), freq * profile[\formantB], 0.07);
        
        // Layer 4: Rasp — bandpassed noise
        var raspNoise = BPF.ar(PinkNoise.ar(profile[\rasp] * 0.06), 
            freq * profile[\noiseFormant], 0.15);
        
        // Aggression layer: harsher harmonics when agitated
        var aggro = Select.ar(aggression > 0.3, [
            0,
            BPF.ar(Saw.ar(freq * 1.5, 0.04), freq * 3.2, 0.3) * aggression
        ]);
        
        // Combine + FM modulation
        var voice = addSig + subSig + nasal + raspNoise + aggro;
        voice = voice * ampGate;
        
        // Frequency modulation from FM ratio
        var fmMod = SinOsc.ar(freq * profile[\fmRatio], mul: profile[\fmDepth] * freq * 0.15);
        voice = voice + SinOsc.ar(freq + fmMod, mul: 0.04);
        
        ^voice.softclip;
    }

    // ------------------------------------------------------------
    // Talking voice layer — makes geese sound like human speech
    // ------------------------------------------------------------
    *talkingVoice { |baseFreq, dialect, ampGate=1|
        var glottal = Saw.ar(baseFreq * [1, 1.01, 1.02], mul: 0.04).sum;
        
        // Vowel formants shaped by dialect
        var vowelCenter = dialect[\vowelLo] + (dialect[\vowelHi] - dialect[\vowelLo]) * LFNoise1.kr(0.4).range(0.3, 0.7);
        var formShift = SinOsc.kr(Rand(0.2, 0.5)).range(-30, 30);
        var form1 = BPF.ar(glottal, vowelCenter + formShift, 0.12, dialect[\nasal]);
        var form2 = BPF.ar(glottal, vowelCenter * 2.8 + formShift, 0.1, dialect[\nasal] * 0.7);
        
        // Consonant clicks
        var clickRate = dialect[\phraseRate] * LFNoise1.kr(0.2).range(0.7, 1.4);
        var clicks = Dust.ar(clickRate, dialect[\consonants] * 0.15);
        var clickFilter = BPF.ar(clicks, 2000, 0.5);
        
        // Nasal murmur
        var nasalMurmur = BPF.ar(PinkNoise.ar(0.02), 250, 0.3);
        
        // Syllable width modulation
        var syllEnv = SinOsc.kr(clickRate * dialect[\syllableWidth], mul: 0.5, add: 0.5);
        
        ^((form1 + form2 + nasalMurmur) * syllEnv + clickFilter) * ampGate * 0.5;
    }

    // ------------------------------------------------------------
    // honk — synthesize a flock of geese honking
    // ------------------------------------------------------------
    *honk { |out=0, flockSize, amp=0.18, dur=4.0, spread=0.9, species=\canada,
             airborne=0.0, aggression=0, sidechainBus=nil|
        
        flockSize = flockSize ? defaultFlockSize;
        flockSize = flockSize.clip(1, 128);
        var profile = this.profileFor(species);
        var numAirborne = (flockSize * airborne).round.max(0);
        var numGround = flockSize - numAirborne;
        
        ^{
            var groundGeese, airGeese;
            var gate = 1;
            
            // --- Terrestrial geese ---
            groundGeese = Mix.fill(numGround.max(1), { |i|
                var baseFreq = profile[\fundLo] + (profile[\fundHi] - profile[\fundLo]) * Rand(0.0, 1.0);
                var burstDelay = Rand(0, dur * 0.3);
                var burstEnv = EnvGen.kr(Env.perc(0.05, dur - burstDelay, curve: -4), 
                    gate: (Trig.kr(Dust.kr(Rand(0.5, 2.0)), dur * 0.5))) * 0.6 + 0.4;
                var panPos = Rand(-1.0, 1.0) * spread;
                
                // Terrestrial: ground reflection (early tap at ~5ms)
                var voice = this.voice(baseFreq, profile, burstEnv, aggression);
                var reflected = DelayN.ar(voice, 0.02, 0.005, 0.15);  // ground reflection
                
                Pan2.ar(voice + reflected, panPos, burstEnv)
            });
            
            // --- Airborne geese (high altitude, doppler shifted) ---
            airGeese = Mix.fill(numAirborne.max(1), { |i|
                var baseFreq = profile[\fundLo] * 0.85 + (profile[\fundHi] - profile[\fundLo] * 0.85) * Rand(0.0, 1.0);
                var burstDelay = Rand(0, dur * 0.25);
                var burstEnv = EnvGen.kr(Env.perc(0.05, dur - burstDelay, curve: -4),
                    gate: (Trig.kr(Dust.kr(Rand(0.3, 1.5)), dur * 0.4))) * 0.6 + 0.4;
                var panPos = Rand(-0.7, 0.7) * spread;
                
                // Doppler shift: approaching geese have higher pitch
                var dopplerFreq = Rand(0.1, 0.3);  // slow doppler cycle
                var dopplerShift = SinOsc.kr(dopplerFreq, Rand(0, 2pi)).range(0.94, 1.08);
                var voice = this.voice(baseFreq * dopplerShift, profile, burstEnv, aggression);
                
                // Airborne: no ground reflection, slight reverb, altitude attenuation
                voice = FreeVerb.ar(voice, 0.25, 0.4, 0.2) * 0.7;
                
                Pan2.ar(voice, panPos, burstEnv * 0.6)
            });
            
            // Combine
            var mix = (groundGeese * (numGround / flockSize)) + (airGeese * (numAirborne / flockSize));
            
            // Small flock boost
            mix = mix * (flockSize <= 4).if({ 1.45 }, { 1.0 });
            
            // Sidechain aggression trigger
            var aggroMod = aggression;
            if (sidechainBus.notNil) {
                var sideSig = In.ar(sidechainBus, 1);
                var sideAmp = Amplitude.kr(sideSig, 0.05, 0.2);
                // Honks become more aggressive when other synths approach
                aggroMod = (aggression + (sideAmp * 2)).clip(0, 1);
                // Increase honk rate when threatened
                mix = mix * (1 + (sideAmp * 0.5));
            };
            
            // Envelope
            var env = EnvGen.kr(Env.linen(0.1, dur - 0.2, 0.1), doneAction: 2);
            
            Out.ar(out, mix * env * amp * (1 / flockSize.sqrt));
        }.play(args: [out: out, amp: amp]);
    }

    // ------------------------------------------------------------
    // honkify — morph audio input into a goose honk
    // ------------------------------------------------------------
    *honkify { |input, honkAmount=0.72, brightness=1.0, species=\canada,
                tryingToTalk=false, seasonMonth, sidechainBus=nil|
        
        seasonMonth = seasonMonth ? Date.getDate.month;
        var profile = this.profileFor(species);
        var dialect = this.migratoryDialectFor(species, seasonMonth);
        var mono = input.asArray;
        mono = mono.size > 1.if({ Mix(mono) }, { mono });
        
        ^{
            // Pitch and amplitude tracking
            var pitch, amp, hasPitch;
            #pitch, hasPitch = Pitch.kr(mono, minFreq: 50, maxFreq: 1200, ampThreshold: 0.01);
            pitch = pitch.lag(0.05);
            amp = Amplitude.kr(mono, 0.01, 0.1);
            
            // Spectral Modeling Synthesis via FFT
            var fftSize = 2048;
            var fftHop = 0.25;
            var fftBuf = FFT(LocalBuf(fftSize), mono, hop: fftHop);
            
            // Spectral smearing — overtone profile shift
            var gooseFormantShift = profile[\formantA].linexp(1.5, 2.5, 1.2, 2.0);
            var overtoneProfile = PV_MagShift(fftBuf, gooseFormantShift * brightness);
            
            // Noise profile — spectral smoothing for breathy goose hiss
            var noiseProfile = PV_MagSmear(fftBuf, profile[\chop] * 4);
            
            // Recombine determininstic and stochastic components
            var morphed = IFFT(PV_Add(overtoneProfile, noiseProfile)) * 0.5;
            
            // Add goose formant resonators
            var f0 = pitch.max(50);
            var form1Freq = f0 * profile[\formantA];
            var form2Freq = f0 * profile[\formantB];
            var form3Freq = f0 * profile[\noiseFormant];
            
            var honkSig = BPF.ar(morphed, form1Freq, 0.15, 0.3)
                       + BPF.ar(morphed, form2Freq, 0.12, 0.2)
                       + BPF.ar(morphed, form3Freq, 0.18, 0.15);
            
            // Blend original with goose-ified signal
            var dryWet = honkAmount;
            var output = (mono * (1 - dryWet)) + (honkSig * dryWet);
            
            // Talking mode
            if (tryingToTalk) {
                var talkVoice = this.talkingVoice(f0, dialect, amp * 0.6);
                output = output * 0.32 + talkVoice * 0.68;
            };
            
            // Territorial sidechain — honks get more aggressive
            if (sidechainBus.notNil) {
                var sideSig = In.ar(sidechainBus, 1);
                var sideAmp = Amplitude.kr(sideSig, 0.05, 0.2);
                var aggro = sideAmp * 2;
                var aggroGain = 1 + aggro;
                var aggroDist = (output * aggroGain).softclip;
                output = Select.ar(aggro > 0.3, [output, aggroDist]);
            };
            
            Out.ar(0, output * amp.linexp(0.001, 1.0, 0.1, 1.0));
        }.play;
    }
}
