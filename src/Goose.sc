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
                chop: 7.4, pulseWidth: 0.28)
        }
        { key == \greylag } {
            (fundLo: 150, fundHi: 380, formantA: 1.9, formantB: 2.55, bw: 0.42,
                fmRatio: 1.28, fmDepth: 0.24, noiseFormant: 3.0, rasp: 0.48,
                chop: 4.6, pulseWidth: 0.38)
        }
        { key == \brant } {
            (fundLo: 95, fundHi: 260, formantA: 1.55, formantB: 2.1, bw: 0.5,
                fmRatio: 0.86, fmDepth: 0.32, noiseFormant: 2.45, rasp: 0.62,
                chop: 3.3, pulseWidth: 0.46)
        }
        { key == \urban } {
            (fundLo: 190, fundHi: 470, formantA: 2.12, formantB: 2.9, bw: 0.32,
                fmRatio: 1.48, fmDepth: 0.2, noiseFormant: 3.6, rasp: 0.58,
                chop: 5.7, pulseWidth: 0.33)
        }
        {
            (fundLo: 175, fundHi: 430, formantA: 2.05, formantB: 2.72, bw: 0.34,
                fmRatio: 1.42, fmDepth: 0.18, noiseFormant: 3.35, rasp: 0.5,
                chop: 5.1, pulseWidth: 0.34)
        };
    }

    *voice { |base, profile, brightness = 1.0|
        var wobble = SinOsc.kr(profile[\chop] * Rand(0.82, 1.18), Rand(0, 2 * pi)).range(0.96, 1.06);
        var fm = SinOsc.ar(base * profile[\fmRatio] * wobble, Rand(0, 2 * pi), base * profile[\fmDepth]);
        var carrier = (base + fm).max(40);
        var additive = Mix.fill(4, { |partial|
            SinOsc.ar(carrier * (partial + 1) * Rand(0.985, 1.018), 0, 1 / (partial + 1.4))
        });
        var subtractive = RLPF.ar(
            VarSaw.ar(carrier * Rand(0.48, 0.72), 0, profile[\pulseWidth], 0.42),
            carrier * profile[\formantA] * brightness.clip(0.25, 3.0),
            0.18
        );
        var nasal = Formant.ar(
            carrier * wobble,
            carrier * profile[\formantB] * brightness.clip(0.25, 3.0),
            carrier * profile[\bw]
        );
        var rasp = BPF.ar(PinkNoise.ar(profile[\rasp]), carrier * profile[\noiseFormant], 0.14);

        ^LeakDC.ar((additive * 0.22) + (subtractive * 0.4) + (nasal * 0.55) + rasp);
    }

    *honk { |out = 0, flockSize, amp = 0.18, dur = 4.0, spread = 0.9, species = \canada|
        var count = (flockSize ? defaultFlockSize).clip(1, 128).asInteger;
        var profile = this.profileFor(species);
        var lowFlockBoost = if(count <= 4) { 1.45 } { 1.0 };

        ^{
            var env = EnvGen.kr(Env.linen(0.12, dur, 0.45, curve: -4), doneAction: 2);
            var signal;
            var voices = Array.fill(count, { |i|
                var base = LFNoise1.kr(0.5 + (i % 11 * 0.07)).exprange(profile[\fundLo], profile[\fundHi]);
                var burst = Decay2.kr(Dust.kr(0.65 + (i % 7 * 0.11)), 0.015, 0.38);
                var call = this.voice(base, profile) * (0.55 + (burst * 1.2));

                Pan2.ar(call * LFNoise1.kr(0.8).range(0.18, 1.0), Rand(-1.0, 1.0));
            });

            signal = Limiter.ar(LeakDC.ar(Splay.ar(voices, spread, (amp * lowFlockBoost) / count.sqrt) * env), 0.94);
            Out.ar(out, signal);
        }.play(target: Server.default, addAction: \addToTail);
    }

    *honkify { |input, honkAmount = 0.72, brightness = 1.0, species = \canada|
        var mono = Mix(input.asArray) / input.asArray.size.max(1);
        var amplitude = Amplitude.kr(mono, 0.01, 0.22);
        var pitch = Pitch.kr(mono, minFreq: 70, maxFreq: 1200, ampThreshold: 0.01)[0].lag(0.05);
        var tracked = pitch.max(90);
        var chain = FFT(LocalBuf(2048), mono);
        var profile = this.profileFor(species);
        var spectralNoise = IFFT(PV_MagSmear(chain, 28));
        var honkCore = this.voice(tracked, profile, brightness);
        var bill = BPF.ar(spectralNoise + PinkNoise.ar(0.045), tracked * profile[\noiseFormant], 0.16);
        var wet = LeakDC.ar((honkCore * 0.78) + (bill * 0.72));
        var matched = wet * amplitude.linlin(0, 0.4, 0.0, 1.25).clip(0, 1.25);
        var balance = honkAmount.clip(0, 1).linlin(0, 1, -1, 1);

        ^XFade2.ar(input, matched ! input.asArray.size.max(1), balance);
    }
}
