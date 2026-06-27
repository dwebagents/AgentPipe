Goose {
	*honk { |out = 0, amp = 0.22, dur = 8.0, flock = 74|
		var flockSize, synthName;

		flockSize = flock.clip(1, 128).asInteger;
		synthName = ("gooseHonk" ++ flockSize.asString).asSymbol;

		SynthDef(synthName, { |out = 0, amp = 0.22, dur = 8.0|
			var flockVoices, masterEnv;

			masterEnv = EnvGen.kr(Env.linen(0.08, dur, 1.4, curve: -4), doneAction: 2);
			flockVoices = Mix.fill(flockSize, { |i|
				var identity, attack, release, freq, pitchSwerve, throat, reed, air, body, unstable, voice, pan, env;

				identity = (i + 1) / flockSize;
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

			Out.ar(out, Limiter.ar(LeakDC.ar(flockVoices) * masterEnv * amp, 0.92));
		}).add;

		^Synth(synthName, [\out, out, \amp, amp, \dur, dur]);
	}

	*egg { |out = 0, amp = 0.18, dur = 5.0, golden = false, hardboiled = false|
		var synthName, goldenFlag, hardboiledFlag;

		synthName = \gooseEgg;
		goldenFlag = golden.asInteger.clip(0, 1);
		hardboiledFlag = hardboiled.asInteger.clip(0, 1);

		SynthDef(synthName, { |out = 0, amp = 0.18, dur = 5.0, golden = 0, hardboiled = 0|
			var env, tap, shell, shellTone, albumen, yolk, membrane, airCell, goldRing, liquidSlosh, boiledDamping, mix;

			golden = golden.clip(0, 1);
			hardboiled = hardboiled.clip(0, 1);
			env = EnvGen.kr(Env.linen(0.02, dur, 0.9, curve: -4), doneAction: 2);
			tap = Decay2.ar(Impulse.ar([5.0, 7.0] + (golden * [1.2, 1.8])), 0.002, 0.04, PinkNoise.ar(0.7));
			boiledDamping = hardboiled.linlin(0, 1, 1.0, 0.38);
			shellTone = Ringz.ar(
				tap,
				[1800, 2300, 3100] * (1 + (golden * 0.42)),
				[0.18, 0.14, 0.11] * boiledDamping
			).sum * 0.32;
			shell = RHPF.ar(shellTone, 900 + (golden * 520), 0.24 + (hardboiled * 0.18));
			albumen = RLPF.ar(
				BrownNoise.ar(0.22),
				LFNoise1.kr(0.4).range(280, 620) * (1 - (hardboiled * 0.35)),
				0.18 + (hardboiled * 0.25)
			) * (1 - (hardboiled * 0.55));
			yolk = Formant.ar(
				72 + (hardboiled * 35),
				180 + (golden * 55),
				80 + (hardboiled * 140),
				0.12
			);
			membrane = BPF.ar(GrayNoise.ar(0.18), 950 + (hardboiled * 180), 0.2)
				* EnvGen.kr(Env.perc(0.01, dur * 0.35), Impulse.kr(0.7));
			airCell = HPF.ar(WhiteNoise.ar(0.06), 4200) * Decay2.kr(Impulse.kr(1.1), 0.01, 0.25);
			goldRing = SinOsc.ar([2400, 3600, 4800] * LFNoise1.kr(0.2).range(0.996, 1.004), 0, 0.028).sum * golden;
			liquidSlosh = SinOsc.ar(LFNoise1.kr(0.25).range(3.2, 6.5), 0, 0.08) * (1 - hardboiled);
			mix = LeakDC.ar((shell + albumen + yolk + membrane + airCell + goldRing + liquidSlosh).tanh);

			Out.ar(out, Limiter.ar(Pan2.ar(mix * env * amp, LFNoise1.kr(0.18).range(-0.2, 0.2)), 0.9));
		}).add;

		^Synth(synthName, [\out, out, \amp, amp, \dur, dur, \golden, goldenFlag, \hardboiled, hardboiledFlag]);
	}

	*internalMechanism { |out = 0, amp = 0.16, dur = 7.0, detail = 0.7|
		var synthName = \gooseInternalMechanism;

		SynthDef(synthName, { |out = 0, amp = 0.16, dur = 7.0, detail = 0.7|
			var env, clock, crop, gizzard, oviduct, shellGland, clutch, conveyor, conveyorVoice, eggSeed, gearTrain, servoRack, camShaft, pressureValve, beltMotor, goldenEggConveyorBelt, machineBed, sonifiedDiagram, resonance, mix;

			detail = detail.clip(0, 1);
			env = EnvGen.kr(Env.linen(0.04, dur, 1.0, curve: -3), doneAction: 2);
			clock = Impulse.kr(2.4 + (detail * 3.6));
			conveyor = Demand.kr(clock, 0, Dseq([0, 1, 2, 3, 4], inf));
			crop = Ringz.ar(Decay2.ar(clock, 0.004, 0.09, WhiteNoise.ar(0.25)), [160, 241, 332], [0.18, 0.24, 0.28]).sum * 0.22;
			gizzard = BPF.ar(Saw.ar([55, 57] * LFNoise1.kr(0.3).range(0.97, 1.03), 0.18).sum, 190, 0.2);
			oviduct = Formant.ar(LFNoise1.kr(0.23).range(85, 130), 420 + (detail * 240), 130, 0.12);
			shellGland = Ringz.ar(
				Decay2.ar(Impulse.ar(1.2), 0.003, 0.06, Dust2.ar(280) * 0.05),
				[1200, 1700, 2400],
				[0.08, 0.12, 0.16]
			).sum * 0.3;
			clutch = BPF.ar(ClipNoise.ar(0.16), LFNoise1.kr(0.7).range(600, 1600), 0.18)
				* Decay2.kr(clock, 0.01, 0.2);
			eggSeed = SinOsc.ar([220, 330, 440] * (1 + (detail * 0.08)), 0, 0.04).sum
				* LFPulse.kr(0.5, 0, 0.2).lag(0.08);
			conveyorVoice = Select.ar(conveyor, [crop, gizzard, oviduct, shellGland, clutch]);
			gearTrain = Ringz.ar(Impulse.ar(12 + (detail * 18)), [360, 540, 720], [0.03, 0.04, 0.05]).sum * 0.12;
			servoRack = LFTri.ar([8, 12] * (1 + (detail * 0.5)), 0, 0.04).sum;
			camShaft = BPF.ar(Pulse.ar(4 + (detail * 6), 0.33, 0.18), 620 + (detail * 380), 0.12);
			pressureValve = HPF.ar(Decay2.ar(Dust.ar(5 + (detail * 8)), 0.002, 0.12, WhiteNoise.ar(0.2)), 900);
			beltMotor = RLPF.ar(Saw.ar(45 + (detail * 22), 0.08), 280 + (detail * 430), 0.3);
			goldenEggConveyorBelt = CombC.ar((beltMotor + gearTrain + servoRack + camShaft), 0.2, 0.045, 1.4)
				+ Ringz.ar(
					Decay2.ar(clock, 0.002, 0.05, PinkNoise.ar(0.12)),
					[980, 1440, 1880] * (1 + (detail * 0.1)),
					[0.04, 0.05, 0.07]
				).sum;
			machineBed = LeakDC.ar((gearTrain + servoRack + camShaft + pressureValve + goldenEggConveyorBelt).tanh);
			sonifiedDiagram = Splay.ar([crop, gizzard, oviduct, shellGland, clutch, eggSeed, conveyorVoice, machineBed], 0.75);
			resonance = CombC.ar((sonifiedDiagram.sum + goldenEggConveyorBelt) * 0.18, 0.35, LFNoise1.kr(0.12).range(0.09, 0.28), 2.2);
			mix = LeakDC.ar(sonifiedDiagram + resonance + Pan2.ar(goldenEggConveyorBelt * 0.22, LFTri.kr(0.11).range(-0.65, 0.65)));

			Out.ar(out, Limiter.ar(mix * env * amp, 0.9));
		}).add;

		^Synth(synthName, [\out, out, \amp, amp, \dur, dur, \detail, detail]);
	}

	*honkify { |inBus = 0, out = 0, amp = 1.0, goose = 0.82, pudding = 0|
		var synthName = \gooseHonkify;

		thisMethod.asCompileString.postln;

		SynthDef(synthName, { |inBus = 0, out = 0, amp = 1.0, goose = 0.82, pudding = 0|
			var input, pitch, hasPitch, loudness, chain, spectral, tracked, breath, honk, custard, bananaSlice, vanillaWafer, puddingBowl, puddingBlend, blend;

			input = In.ar(inBus, 1);
			loudness = Amplitude.kr(input, attackTime: 0.01, releaseTime: 0.14).clip(0.0001, 1.0);
			# pitch, hasPitch = Pitch.kr(input, ampThreshold: 0.012, minFreq: 70, maxFreq: 1500, median: 7);
			pitch = Lag.kr(pitch.clip(70, 1500), 0.08);
			pudding = pudding.clip(0, 1);

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
			custard = RLPF.ar(PinkNoise.ar(loudness * 0.28), pitch.clip(90, 520) * 0.62, 0.22);
			bananaSlice = Formant.ar(pitch.clip(80, 640) * 0.5, pitch.clip(120, 900) * 1.35, pitch.clip(90, 700) * 0.24, 0.16);
			vanillaWafer = Ringz.ar(
				Decay2.ar(Impulse.ar(3.2 + (pudding * 2.1)), 0.002, 0.08, WhiteNoise.ar(0.3)),
				[1150, 1760, 2520],
				[0.07, 0.09, 0.11]
			).sum * 0.18;
			puddingBowl = RLPF.ar((custard + bananaSlice + vanillaWafer + (input * 0.18)).tanh, 430 + (loudness * 1200), 0.28);
			puddingBlend = LeakDC.ar((custard + bananaSlice + vanillaWafer + puddingBowl).tanh);
			blend = XFade2.ar(input, honk, goose.clip(0, 1).linlin(0, 1, -1, 1));
			blend = XFade2.ar(blend, puddingBlend, pudding.linlin(0, 1, -1, 1));

			Out.ar(out, Limiter.ar(blend * amp * loudness.linlin(0, 1, 0.7, 1.12), 0.94));
		}).add;

		^Synth(synthName, [\inBus, inBus, \out, out, \amp, amp, \goose, goose, \pudding, pudding]);
	}
}
