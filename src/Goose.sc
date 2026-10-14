Goose {
    classvar <defaultFlockSize;

    *initClass {
        defaultFlockSize = 74;
    }

    *profileFor { |species = \canada|
        var key = species ? \canada;

        if(key.isKindOf(String)) { key = key.asSymbol };

        ^case
        { key == \snow } {
            (fundLo: 260, fundHi: 610, formantA: 2.35, formantB: 3.1, bw: 0.22,
                fmRatio: 1.72, fmDepth: 0.12, noiseFormant: 4.1, rasp: 0.35,
                chop: 7.4, pulseWidth: 0.28, neckLength: 0.72, syrinxTension: 1.34,
                airSac: 0.72, tracheaQ: 0.22, muscleTremor: 7.8, beakCavity: 1.22,
                wingSpan: 1.08, featherNoise: 0.44)
        }
        { key == \greylag } {
            (fundLo: 150, fundHi: 380, formantA: 1.9, formantB: 2.55, bw: 0.42,
                fmRatio: 1.28, fmDepth: 0.24, noiseFormant: 3.0, rasp: 0.48,
                chop: 4.6, pulseWidth: 0.38, neckLength: 1.08, syrinxTension: 0.92,
                airSac: 1.16, tracheaQ: 0.34, muscleTremor: 4.8, beakCavity: 0.96,
                wingSpan: 1.22, featherNoise: 0.38)
        }
        { key == \brant } {
            (fundLo: 95, fundHi: 260, formantA: 1.55, formantB: 2.1, bw: 0.5,
                fmRatio: 0.86, fmDepth: 0.32, noiseFormant: 2.45, rasp: 0.62,
                chop: 3.3, pulseWidth: 0.46, neckLength: 1.32, syrinxTension: 0.76,
                airSac: 1.32, tracheaQ: 0.42, muscleTremor: 3.7, beakCavity: 0.84,
                wingSpan: 0.92, featherNoise: 0.58)
        }
        { key == \urban } {
            (fundLo: 190, fundHi: 470, formantA: 2.12, formantB: 2.9, bw: 0.32,
                fmRatio: 1.48, fmDepth: 0.2, noiseFormant: 3.6, rasp: 0.58,
                chop: 5.7, pulseWidth: 0.33, neckLength: 0.94, syrinxTension: 1.12,
                airSac: 0.9, tracheaQ: 0.28, muscleTremor: 6.4, beakCavity: 1.1,
                wingSpan: 1.0, featherNoise: 0.7)
        }
        {
            (fundLo: 175, fundHi: 430, formantA: 2.05, formantB: 2.72, bw: 0.34,
                fmRatio: 1.42, fmDepth: 0.18, noiseFormant: 3.35, rasp: 0.5,
                chop: 5.1, pulseWidth: 0.34, neckLength: 1.0, syrinxTension: 1.0,
                airSac: 1.0, tracheaQ: 0.3, muscleTremor: 5.4, beakCavity: 1.0,
                wingSpan: 1.15, featherNoise: 0.48)
        };
    }

    *migratoryDialectFor { |species = \canada, month|
        var key = species ? \canada;
        var m = month ? Date.getDate.month;

        if(key.isKindOf(String)) { key = key.asSymbol };
        m = m.clip(1, 12).asInteger;

        ^case
        { key == \snow } {
            if(m.inclusivelyBetween(4, 8)) {
                (language: \inuktitut, phraseRate: 6.8, vowelLo: 660, vowelHi: 1320,
                    nasal: 0.36, consonants: 0.54, syllableWidth: 0.27)
            } {
                (language: \spanish, phraseRate: 5.8, vowelLo: 520, vowelHi: 1120,
                    nasal: 0.3, consonants: 0.42, syllableWidth: 0.34)
            }
        }
        { key == \greylag } {
            if(m.inclusivelyBetween(3, 9)) {
                (language: \norwegian, phraseRate: 4.9, vowelLo: 430, vowelHi: 980,
                    nasal: 0.42, consonants: 0.34, syllableWidth: 0.4)
            } {
                (language: \arabic, phraseRate: 5.5, vowelLo: 360, vowelHi: 870,
                    nasal: 0.48, consonants: 0.46, syllableWidth: 0.32)
            }
        }
        { key == \brant } {
            if(m.inclusivelyBetween(5, 8)) {
                (language: \greenlandic, phraseRate: 4.2, vowelLo: 310, vowelHi: 760,
                    nasal: 0.5, consonants: 0.58, syllableWidth: 0.24)
            } {
                (language: \english, phraseRate: 5.2, vowelLo: 390, vowelHi: 910,
                    nasal: 0.4, consonants: 0.48, syllableWidth: 0.3)
            }
        }
        { key == \urban } {
            (language: \parkDialect, phraseRate: 6.2, vowelLo: 470, vowelHi: 1080,
                nasal: 0.62, consonants: 0.66, syllableWidth: 0.22)
        }
        {
            if(m.inclusivelyBetween(4, 9)) {
                (language: \cree, phraseRate: 5.4, vowelLo: 450, vowelHi: 1040,
                    nasal: 0.44, consonants: 0.38, syllableWidth: 0.35)
            } {
                (language: \english, phraseRate: 5.9, vowelLo: 520, vowelHi: 1180,
                    nasal: 0.38, consonants: 0.5, syllableWidth: 0.28)
            }
        };
    }

    *environmentFor { |species = \canada, month, location = \auto|
        var key = species ? \canada;
        var loc = location ? \auto;
        var m = month ? Date.getDate.month;

        if(key.isKindOf(String)) { key = key.asSymbol };
        if(loc.isKindOf(String)) { loc = loc.asSymbol };
        m = m.clip(1, 12).asInteger;

        if(loc == \auto) {
            loc = case
            { key == \urban } { \cityPark }
            { key == \snow and: { m.inclusivelyBetween(4, 8) } } { \arcticWetland }
            { key == \snow } { \coastalLagoon }
            { key == \brant } { \tidalFlat }
            { key == \greylag and: { m.inclusivelyBetween(3, 9) } } { \forestLake }
            { key == \greylag } { \agriculturalField }
            { m.inclusivelyBetween(4, 9) } { \borealLake }
            { \cityPark };
        };

        ^case
        { loc == \forestLake } {
            (tree: 0.72, building: 0.08, terrain: 0.48, stellar: 0.06, bird: 0.38,
                aircraft: 0.05, spacecraft: 0.01, kaiju: 0.0, wards: 0.02,
                water: 0.62, airAbsorption: 0.2, distance: 0.58)
        }
        { loc == \borealLake } {
            (tree: 0.82, building: 0.02, terrain: 0.42, stellar: 0.08, bird: 0.5,
                aircraft: 0.03, spacecraft: 0.01, kaiju: 0.0, wards: 0.01,
                water: 0.74, airAbsorption: 0.24, distance: 0.7)
        }
        { loc == \cityPark } {
            (tree: 0.42, building: 0.8, terrain: 0.36, stellar: 0.03, bird: 0.44,
                aircraft: 0.28, spacecraft: 0.02, kaiju: 0.0, wards: 0.06,
                water: 0.22, airAbsorption: 0.16, distance: 0.36)
        }
        { loc == \arcticWetland } {
            (tree: 0.08, building: 0.01, terrain: 0.7, stellar: 0.16, bird: 0.62,
                aircraft: 0.04, spacecraft: 0.025, kaiju: 0.0, wards: 0.0,
                water: 0.82, airAbsorption: 0.34, distance: 0.86)
        }
        { loc == \tidalFlat } {
            (tree: 0.05, building: 0.04, terrain: 0.58, stellar: 0.1, bird: 0.72,
                aircraft: 0.08, spacecraft: 0.015, kaiju: 0.0, wards: 0.02,
                water: 0.9, airAbsorption: 0.28, distance: 0.76)
        }
        { loc == \agriculturalField } {
            (tree: 0.22, building: 0.18, terrain: 0.76, stellar: 0.08, bird: 0.34,
                aircraft: 0.14, spacecraft: 0.01, kaiju: 0.0, wards: 0.01,
                water: 0.18, airAbsorption: 0.22, distance: 0.68)
        }
        {
            (tree: 0.18, building: 0.1, terrain: 0.64, stellar: 0.08, bird: 0.46,
                aircraft: 0.08, spacecraft: 0.02, kaiju: 0.0, wards: 0.02,
                water: 0.7, airAbsorption: 0.24, distance: 0.72)
        };
    }

    *voice { |base, profile, brightness = 1.0|
        var lungPressure = LFNoise1.kr(profile[\muscleTremor] * 0.11).range(0.72, 1.18) * profile[\airSac];
        var neckDelay = (profile[\neckLength] * 0.011).clip(0.003, 0.028);
        var wobble = SinOsc.kr(profile[\chop] * Rand(0.82, 1.18), Rand(0, 2 * pi)).range(0.96, 1.06);
        var muscle = SinOsc.kr(profile[\muscleTremor] * Rand(0.72, 1.32), Rand(0, 2 * pi)).range(0.985, 1.025);
        var syrinx = SinOsc.ar(
            (base * profile[\syrinxTension] * wobble * muscle).max(40),
            0,
            base * profile[\fmDepth] * lungPressure
        );
        var carrier = (base + syrinx).max(40);
        var vocalFolds = Mix.fill(4, { |partial|
            SinOsc.ar(carrier * (partial + 1) * Rand(0.985, 1.018), 0, 1 / (partial + 1.4))
        });
        var trachea = RLPF.ar(
            VarSaw.ar(carrier * Rand(0.48, 0.72), 0, profile[\pulseWidth], 0.42),
            carrier * profile[\formantA] * (1 / profile[\neckLength]) * brightness.clip(0.25, 3.0),
            profile[\tracheaQ]
        );
        var throat = CombC.ar(vocalFolds + trachea, 0.04, neckDelay, 0.18);
        var beak = Formant.ar(
            carrier * wobble,
            carrier * profile[\formantB] * profile[\beakCavity] * brightness.clip(0.25, 3.0),
            carrier * profile[\bw]
        );
        var airRasp = BPF.ar(
            PinkNoise.ar(profile[\rasp] * lungPressure),
            carrier * profile[\noiseFormant] * profile[\beakCavity],
            0.14
        );

        ^LeakDC.ar((vocalFolds * 0.18) + (trachea * 0.34) + (throat * 0.2) + (beak * 0.48) + airRasp);
    }

    *wholeBody { |base, profile, gait = 1.0|
        var bill = BPF.ar(PinkNoise.ar(0.08), base * profile[\beakCavity] * 2.6, 0.24);
        var skull = Formant.ar(base * 0.52, base * 2.1, base * 0.38, 0.12);
        var neck = CombC.ar(GrayNoise.ar(0.11), 0.055, (profile[\neckLength] * 0.013).clip(0.004, 0.052), 0.22);
        var airSac = SinOsc.ar(base * 0.38, 0, profile[\airSac] * 0.14);
        var sternum = Ringz.ar(Impulse.ar(gait.max(0.1)), base * 0.21, 0.18, 0.12);
        var gut = LPF.ar(BrownNoise.ar(0.16), base * 0.72);
        var legs = Decay2.kr(Impulse.kr(gait * 0.5), 0.012, 0.18) * SinOsc.ar(base * 0.16, 0, 0.12);
        var hoof = HPF.ar(WhiteNoise.ar(0.045), 2600) * Decay2.kr(Impulse.kr(gait * 0.25), 0.004, 0.04);

        ^LeakDC.ar((bill * 0.12) + (skull * 0.16) + (neck * 0.18) + (airSac * 0.28) + (sternum * 0.16) + (gut * 0.12) + legs + hoof);
    }

    *environmentalReflections { |signal, env|
        var treeEcho = CombC.ar(signal, 0.42, 0.07 + (env[\tree] * 0.08), 1.4) * env[\tree] * 0.22;
        var buildingSlap = CombL.ar(signal, 0.32, 0.035 + (env[\building] * 0.06), 0.9) * env[\building] * 0.24;
        var terrainBloom = AllpassN.ar(signal, 0.24, 0.06 + (env[\terrain] * 0.12), 1.2) * env[\terrain] * 0.2;
        var waterMirror = DelayC.ar(LPF.ar(signal, 1600), 0.18, 0.025 + (env[\water] * 0.09)) * env[\water] * 0.16;
        var stellarHalo = FreqShift.ar(signal, LFNoise1.kr(0.03).range(-0.08, 0.08)) * env[\stellar] * 0.08;
        var birds = BPF.ar(PinkNoise.ar(env[\bird] * 0.04), LFNoise1.kr(0.8).exprange(900, 3800), 0.18);
        var aircraftDoppler = FreqShift.ar(LPF.ar(signal, 900), LFNoise1.kr(0.05).range(-18, 22)) * env[\aircraft] * 0.12;
        var spacecraftPing = Ringz.ar(Dust.ar(env[\spacecraft] * 0.35), 4800, 1.8, env[\spacecraft] * 0.08);
        var kaijuWake = LPF.ar(BrownNoise.ar(env[\kaiju] * 0.2), 80);
        var wardShimmer = Ringz.ar(HPF.ar(signal, 2200), LFNoise1.kr(0.12).exprange(3200, 7200), 2.2) * env[\wards] * 0.1;
        var absorbed = LPF.ar(signal, 18000 - (env[\airAbsorption] * 12000));

        ^LeakDC.ar((absorbed * (1 - (env[\distance] * 0.18))) + treeEcho + buildingSlap + terrainBloom
            + waterMirror + stellarHalo + birds + aircraftDoppler + spacecraftPing + kaijuWake + wardShimmer);
    }

    *oneWingFlap { |profile, rate = 1.0|
        var span = profile[\wingSpan];
        var feather = profile[\featherNoise];
        var asymmetricBeat = Impulse.kr((rate * LFNoise1.kr(0.18).range(0.72, 1.2)).max(0.12));
        var downstroke = Decay2.kr(asymmetricBeat, 0.018 * span, 0.28 * span);
        var rebound = Decay2.kr(DelayN.kr(asymmetricBeat, 0.18, 0.055 * span), 0.01, 0.16);
        var shoulderThump = SinOsc.ar(44 / span, 0, downstroke * 0.32);
        var featherWhoosh = BPF.ar(PinkNoise.ar(feather), LFNoise1.kr(3.0).exprange(420, 2600), 0.42) * downstroke;
        var primaryFeather = HPF.ar(WhiteNoise.ar(feather * 0.36), 1800) * rebound;
        var unevenPan = LFNoise1.kr(rate.max(0.2)).range(-0.82, 0.82);

        ^Pan2.ar(LeakDC.ar(shoulderThump + featherWhoosh + primaryFeather), unevenPan);
    }

    *talkingVoice { |base, profile, dialect, brightness = 1.0|
        var rate = dialect[\phraseRate] * LFNoise1.kr(0.35).range(0.72, 1.28);
        var mouth = LFPulse.kr(rate, 0, dialect[\syllableWidth]).lag(0.035);
        var glottal = LFSaw.ar(base * LFNoise1.kr(1.2).range(0.86, 1.18), 0, 0.24);
        var vowelShift = LFNoise1.kr(rate * 0.5).range(dialect[\vowelLo], dialect[\vowelHi]);
        var vowelA = Formant.ar(base * 0.72, vowelShift * brightness.clip(0.25, 3.0), base * profile[\bw] * 1.8);
        var vowelB = Formant.ar(base * 1.08, vowelShift * 1.68, base * (profile[\bw] + 0.18));
        var beakClicks = HPF.ar(PinkNoise.ar(dialect[\consonants]), 1800) *
            Decay2.kr(Impulse.kr(rate * Rand(1.4, 2.6)), 0.006, 0.07);
        var nasalMurmur = BPF.ar(PinkNoise.ar(dialect[\nasal]), base * profile[\formantA], 0.2);

        ^LeakDC.ar(((vowelA * 0.38) + (vowelB * 0.24) + (glottal * 0.2) + nasalMurmur) * mouth + beakClicks);
    }

    *honk { |out = 0, flockSize, amp = 0.18, dur = 4.0, spread = 0.9, species = \canada, oneWing = false, environment = \auto, seasonMonth|
        var count = (flockSize ? defaultFlockSize).clip(1, 128).asInteger;
        var profile = this.profileFor(species);
        var envProfile = this.environmentFor(species, seasonMonth, environment);
        var lowFlockBoost = if(count <= 4) { 1.45 } { 1.0 };

        ^{
            var env = EnvGen.kr(Env.linen(0.12, dur, 0.45, curve: -4), doneAction: 2);
            var signal;
            var voices = Array.fill(count, { |i|
                var base = LFNoise1.kr(0.5 + (i % 11 * 0.07)).exprange(profile[\fundLo], profile[\fundHi]);
                var burst = Decay2.kr(Dust.kr(0.65 + (i % 7 * 0.11)), 0.015, 0.38);
                var body = this.wholeBody(base, profile, 0.45 + (i % 6 * 0.06));
                var call = (this.voice(base, profile) + (body * 0.42)) * (0.55 + (burst * 1.2));
                var wing = if(oneWing) { this.oneWingFlap(profile, 0.35 + (i % 5 * 0.08)) * 0.32 } { 0 };

                Pan2.ar(call * LFNoise1.kr(0.8).range(0.18, 1.0), Rand(-1.0, 1.0)) + wing;
            });

            signal = Splay.ar(voices, spread, (amp * lowFlockBoost) / count.sqrt);
            signal = Limiter.ar(LeakDC.ar(this.environmentalReflections(signal, envProfile) * env), 0.94);
            Out.ar(out, signal);
        }.play(target: Server.default, addAction: \addToTail);
    }

    *honkify { |input, honkAmount = 0.72, brightness = 1.0, species = \canada, tryingToTalk = false, seasonMonth, oneWing = false, environment = \auto|
        var mono = Mix(input.asArray) / input.asArray.size.max(1);
        var amplitude = Amplitude.kr(mono, 0.01, 0.22);
        var pitch = Pitch.kr(mono, minFreq: 70, maxFreq: 1200, ampThreshold: 0.01)[0].lag(0.05);
        var tracked = pitch.max(90);
        var chain = FFT(LocalBuf(2048), mono);
        var profile = this.profileFor(species);
        var dialect = this.migratoryDialectFor(species, seasonMonth);
        var envProfile = this.environmentFor(species, seasonMonth, environment);
        var spectralNoise = IFFT(PV_MagSmear(chain, 28));
        var honkCore = this.voice(tracked, profile, brightness);
        var bodyCore = this.wholeBody(tracked, profile, amplitude.linlin(0, 0.4, 0.2, 1.5).clip(0.2, 1.5));
        var talkCore = this.talkingVoice(tracked, profile, dialect, brightness);
        var bill = BPF.ar(spectralNoise + PinkNoise.ar(0.045), tracked * profile[\noiseFormant], 0.16);
        var wing = if(oneWing) { Mix(this.oneWingFlap(profile, amplitude.linlin(0, 0.4, 0.2, 1.4).clip(0.2, 1.4))) * 0.12 } { 0 };
        var talkMix = if(tryingToTalk) { 0.68 } { 0.0 };
        var wet = LeakDC.ar((XFade2.ar(honkCore + (bodyCore * 0.36), talkCore, (talkMix * 2) - 1) * 0.78) + (bill * 0.72) + wing);
        var reflectedWet = this.environmentalReflections(wet, envProfile);
        var matched = reflectedWet * amplitude.linlin(0, 0.4, 0.0, 1.25).clip(0, 1.25);
        var balance = honkAmount.clip(0, 1).linlin(0, 1, -1, 1);

        ^XFade2.ar(input, matched ! input.asArray.size.max(1), balance);
    }
}
