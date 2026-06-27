Goose {
	*honk { |out = 0, amp = 0.22, dur = 8.0|
		var synthName = \gooseHonk74;

		SynthDef(synthName, { |out = 0, amp = 0.22, dur = 8.0|
			var flock, masterEnv;

			masterEnv = EnvGen.kr(Env.linen(0.08, dur, 1.4, curve: -4), doneAction: 2);
			flock = Mix.fill(74, { |i|
				var identity, attack, release, freq, pitchSwerve, throat, reed, air, body, unstable, voice, pan, env;

				identity = (i + 1) / 74;
				attack = 0.006 + (identity * 0.028);
				release = 0.22 + LFNoise1.kr(0.4 + identity).range(0.04, 0.46);
				pitchSwerve = EnvGen.kr(
					Env(
						[1.0, 1.45 + (identity * 0.17), 0.84 + LFNoise1.kr(0.9).range(-0.08, 0.08), 1.06],
						[0.035, 0.12 + (identity * 0.06), 0.38],
						[4, -5, -3]
					),
					Dust.kr(0.75 + (identity * 2.9))
				);
				freq = (
					LFNoise1.kr(0.11 + identity).exprange(230, 760)
					* pitchSwerve
					* LFNoise2.kr(3.0 + (identity * 5.0)).range(0.96, 1.08)
				).clip(120, 1800);
				env = EnvGen.kr(Env.perc(attack, release, curve: -5), Dust.kr(0.9 + (identity * 3.4)));
				unstable = LFNoise2.kr(7 + (identity * 19)).range(0.72, 1.32);
				throat = Formant.ar(freq * 0.46, freq * unstable, freq * 0.22, 0.32);
				reed = LFTri.ar(freq * [0.5, 1.0, 2.01], LFNoise2.kr(2.1 + identity).range(0, 2 * pi)).sum * 0.12;
				air = BPF.ar(BrownNoise.ar(0.55), freq * [0.62, 1.34, 2.18], [0.12, 0.08, 0.05]).sum;
				body = RLPF.ar((throat + reed + air).tanh, freq * LFNoise1.kr(1.8).range(1.2, 2.8), 0.16);
				voice = LeakDC.ar((body * 0.72) + (air * 0.2));
				pan = LFNoise1.kr(0.18 + identity).range(-0.95, 0.95);

				Pan2.ar(voice * env * (0.032 + (identity * 0.004)), pan);
			});

			Out.ar(out, Limiter.ar(LeakDC.ar(flock) * masterEnv * amp, 0.92));
		}).add;

		^Synth(synthName, [\out, out, \amp, amp, \dur, dur]);
	}

	*honkify { |inBus = 0, out = 0, amp = 1.0, goose = 0.82|
		var synthName = \gooseHonkify;

		SynthDef(synthName, { |inBus = 0, out = 0, amp = 1.0, goose = 0.82|
			var input, pitch, hasPitch, loudness, chain, spectral, tracked, breath, honk, blend;

			input = In.ar(inBus, 1);
			loudness = Amplitude.kr(input, attackTime: 0.01, releaseTime: 0.14).clip(0.0001, 1.0);
			# pitch, hasPitch = Pitch.kr(input, ampThreshold: 0.012, minFreq: 70, maxFreq: 1500, median: 7);
			pitch = Lag.kr(pitch.clip(70, 1500), 0.08);

			chain = FFT(LocalBuf(2048), input);
			chain = PV_MagSmear(chain, 9);
			chain = PV_MagShift(chain, LFNoise1.kr(2.7).range(0.92, 1.08), LFNoise1.kr(1.1).range(-0.18, 0.18));
			chain = PV_BrickWall(chain, LFNoise1.kr(0.6).range(-0.74, 0.92));
			spectral = IFFT(chain);

			tracked = SelectX.ar(
				hasPitch.lag(0.08),
				[
					BPF.ar(input, 420, 0.21),
					Mix.ar([
						Formant.ar(pitch * 0.48, pitch * 1.18, pitch * 0.21, 0.34),
						BPF.ar(input, pitch * 1.92, 0.08, 0.46),
						BPF.ar(input, pitch * 2.74, 0.06, 0.28)
					])
				]
			);
			breath = BPF.ar(PinkNoise.ar(loudness * 0.42), pitch.clip(180, 900) * LFNoise1.kr(1.6).range(0.85, 1.4), 0.17);
			honk = LeakDC.ar((tracked * 0.66) + (spectral * 0.26) + breath);
			honk = RHPF.ar(honk.tanh, 95, 0.35);
			blend = XFade2.ar(input, honk, goose.clip(0, 1).linlin(0, 1, -1, 1));

			Out.ar(out, Limiter.ar(blend * amp * loudness.linlin(0, 1, 0.7, 1.12), 0.94));
		}).add;

		^Synth(synthName, [\inBus, inBus, \out, out, \amp, amp, \goose, goose]);
	}
}
