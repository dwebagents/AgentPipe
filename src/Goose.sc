Goose {
	*honk {
		var synths = Array.fill(74, {
			{
				var freq = Expressing.rand(400, 750) * LFNoise1.kr(Expressing.rand(8, 15)).range(0.92, 1.08);
				var form = freq * Expressing.rand(1.8, 2.5);
				var bw = Expressing.rand(150, 300);
				var env = EnvGen.ar(Env.new([0, 1, 0.8, 0], [0.03, 0.08, Expressing.rand(0.1, 0.25)], \sine), doneAction: 2);
				var sig = Formant.ar(freq, form, bw);
				var noise = BPF.ar(WhiteNoise.ar(), freq, 0.3) * EnvGen.ar(Env.perc(0.01, 0.05));
				(sig + noise) * env * 0.012;
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
