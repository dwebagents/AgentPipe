Goose {
	*honk {
		var synths = Array.fill(74, {
			{
				var flightSpeed = LFDNoise3.kr(0.1).range(5.0, 20.0);
				var airDensity = 1.225;
				var wingArea = 0.4;
				var liftCoefficient = LFNoise2.kr(0.5).range(0.3, 1.5);
				var aerodynamicDrag = 0.5 * airDensity * flightSpeed.squared * wingArea * liftCoefficient;
				
				var pectoralisMajorL = SinOsc.kr(ExpRand(4.0, 7.0), 0, aerodynamicDrag * 0.1);
				var pectoralisMajorR = SinOsc.kr(ExpRand(4.0, 7.0), pi, aerodynamicDrag * 0.1);
				var supracoracoideusL = LFSaw.kr(ExpRand(4.0, 7.0), 0, pectoralisMajorL * 0.5);
				var supracoracoideusR = LFSaw.kr(ExpRand(4.0, 7.0), pi, pectoralisMajorR * 0.5);
				
				var neckMuscleTension = Latch.kr(WhiteNoise.kr(), Impulse.kr(ExpRand(8, 24))) * 50 + 200;
				var tracheaLength = LFNoise1.kr(0.2).range(0.12, 0.28) + (neckMuscleTension * 0.0001);
				
				var lungPressure = EnvGen.ar(Env([0, 1, 0.9, 1.2, 0.6, 0], [0.05, 0.1, 0.05, 0.2, 0.1], \sine));
				var intercostalMuscles = LFNoise0.kr(15).range(0.8, 1.2);
				var dynamicAirflow = lungPressure * intercostalMuscles;
				
				var syrinxMembrane1 = Spring.ar(dynamicAirflow, neckMuscleTension, 0.005);
				var syrinxMembrane2 = Spring.ar(dynamicAirflow, neckMuscleTension * 1.05, 0.006);
				var glottalSource = syrinxMembrane1 + syrinxMembrane2;
				
				var muscleNoiseL = PinkNoise.ar() * pectoralisMajorL * 0.005;
				var muscleNoiseR = PinkNoise.ar() * pectoralisMajorR * 0.005;
				
				var tracheaTubeL = DelayC.ar(glottalSource + muscleNoiseL, 0.5, tracheaLength);
				var tracheaTubeR = DelayC.ar(glottalSource + muscleNoiseR, 0.5, tracheaLength);
				
				var beakFormant = BPF.ar([tracheaTubeL, tracheaTubeR], LFNoise2.kr(3).range(600, 1400), 0.2);
				
				var boneResonance = Klank.ar(
					`[[350, 720, 1050, 1800, 2400], [1, 0.8, 0.5, 0.3, 0.1], [0.5, 0.4, 0.3, 0.2, 0.1]], 
					beakFormant
				);
				
				var dopplerShift = DelayC.ar(boneResonance, 2.0, flightSpeed * 0.01);
				
				var finalEnv = EnvGen.ar(Env.perc(0.02, 1.8, 1, -4), doneAction: 2);
				
				var outSig = dopplerShift * finalEnv * 0.02;
				
				outSig = HPF.ar(outSig, 100);
				outSig = LPF.ar(outSig, 8000);
				
				outSig;
			}.play;
		});
		^synths;
	}

	*honkify { |audioIn|
		var chainL, chainR, noiseProfile, morphL, morphR, feathersTension;
		
		feathersTension = LFDNoise3.kr(8).range(0.8, 1.5);
		
		chainL = FFT(LocalBuf(4096), audioIn[0]);
		chainR = FFT(LocalBuf(4096), audioIn[1]);
		
		noiseProfile = LFNoise2.kr(18 * feathersTension).range(0.2, 1.8);
		
		chainL = PV_MagSqrt(chainL);
		chainR = PV_MagSqrt(chainR);
		
		chainL = PV_MagShift(chainL, 1.2 * feathersTension, 50);
		chainR = PV_MagShift(chainR, 1.18 * feathersTension, 45);
		
		chainL = PV_RectComb(chainL, 10, 0.15, noiseProfile);
		chainR = PV_RectComb(chainR, 10, 0.15, noiseProfile);
		
		chainL = PV_PhaseShift(chainL, LFNoise1.kr(5).range(-pi, pi));
		chainR = PV_PhaseShift(chainR, LFNoise1.kr(5.1).range(-pi, pi));
		
		morphL = IFFT(chainL);
		morphR = IFFT(chainR);
		
		^[morphL, morphR] * 1.5;
	}
}
