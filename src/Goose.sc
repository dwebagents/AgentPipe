Goose {
	*honk {
		var synths = Array.fill(74, {
			{
				var modFreq = ExpRand(120, 350);
				var index = ExpRand(2, 6) * LFNoise1.kr(ExpRand(5, 12)).range(0.5, 1.5);
				var modSig = SinOsc.ar(modFreq) * modFreq * index;
				var carFreq = (ExpRand(350, 680) + modSig) * LFNoise2.kr(ExpRand(6, 15)).range(0.95, 1.05);
				var env = EnvGen.ar(Env.new([0, 1, 0.7, 0.4, 0], [0.02, 0.05, 0.1, ExpRand(0.08, 0.2)], \sine), doneAction: 2);
				var carSig = LFSaw.ar(carFreq);
				var shaper = (carSig * ExpRand(1.5, 3.5)).tanh;
				var finalSig = BPF.ar(shaper, carFreq * ExpRand(1.2, 2.2), 0.25);
				var transient = HPF.ar(WhiteNoise.ar(), 2000) * EnvGen.ar(Env.perc(0.005, 0.03));
				(finalSig + transient) * env * 0.01;
			}.play;
		});
		^synths;
	}

	*honkify { |audioIn|
		var chain, noiseProfile, morph;
		chain = FFT(LocalBuf(2048), audioIn);
		noiseProfile = LFNoise2.kr(12).range(0.4, 1.6);
		chain = PV_MagSqrt(chain);
		chain = PV_MagShift(chain, 1.15, 40);
		chain = PV_RectComb(chain, 8, 0.1, noiseProfile);
		morph = IFFT(chain);
		^morph * 1.3;
	}
}
