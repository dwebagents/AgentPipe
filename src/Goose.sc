Goose {
    classvar <defaultFlockSize;

    *initClass {
        defaultFlockSize = 74;
    }

    *honk { |out = 0, flockSize, amp = 0.18, dur = 4.0, spread = 0.9|
        var count = (flockSize ? defaultFlockSize).clip(1, 128).asInteger;

        ^{
            var env = EnvGen.kr(Env.linen(0.12, dur, 0.45, curve: -4), doneAction: 2);
            var signal;
            var voices = Array.fill(count, { |i|
                var base = LFNoise1.kr(0.5 + (i % 11 * 0.07)).exprange(180, 520);
                var wobble = SinOsc.kr(3.0 + (i % 13 * 0.19), Rand(0, 2 * pi)).range(0.92, 1.11);
                var burst = Decay2.kr(Dust.kr(0.65 + (i % 7 * 0.11)), 0.015, 0.38);
                var throat = Formant.ar(
                    base * wobble,
                    base * Rand(1.6, 2.7),
                    base * Rand(0.22, 0.42)
                );
                var rasp = BPF.ar(WhiteNoise.ar(0.7), base * Rand(1.9, 3.8), Rand(0.08, 0.18));
                var call = (throat * 0.72) + (rasp * burst * 1.45);

                Pan2.ar(call * LFNoise1.kr(0.8).range(0.18, 1.0), Rand(-1.0, 1.0));
            });

            signal = Limiter.ar(LeakDC.ar(Splay.ar(voices, spread, amp / count.sqrt) * env), 0.94);
            Out.ar(out, signal);
        }.play(target: Server.default, addAction: \addToTail);
    }

    *honkify { |input, honkAmount = 0.72, brightness = 1.0|
        var mono = Mix(input.asArray) / input.asArray.size.max(1);
        var amplitude = Amplitude.kr(mono, 0.01, 0.22);
        var pitch = Pitch.kr(mono, minFreq: 70, maxFreq: 1200, ampThreshold: 0.01)[0].lag(0.05);
        var tracked = pitch.max(90);
        var chain = FFT(LocalBuf(2048), mono);
        var spectralNoise = IFFT(PV_MagSmear(chain, 28));
        var honkCore = Formant.ar(
            tracked * LFNoise1.kr(5).range(0.96, 1.06),
            tracked * 2.35 * brightness.clip(0.25, 3.0),
            tracked * 0.34
        );
        var bill = BPF.ar(spectralNoise + PinkNoise.ar(0.045), tracked * 3.1, 0.16);
        var wet = LeakDC.ar((honkCore * 0.7) + (bill * 0.9));
        var matched = wet * amplitude.linlin(0, 0.4, 0.0, 1.25).clip(0, 1.25);
        var balance = honkAmount.clip(0, 1).linlin(0, 1, -1, 1);

        ^XFade2.ar(input, matched ! input.asArray.size.max(1), balance);
    }
}
