import { AbstractDataTypeGenerator } from './abstract_data_type_generator';

export class Goose extends AbstractDataTypeGenerator {
  /**
   * A synthetic goose sound generator designed to produce a specific harmonic and transient profile.
   */
  
  // The core logic: the input is an array of frames, each frame being an AudioData object (representing audio samples).
  // We need to reverse this so that if we have [A1, A2, ..., An], we can generate it in order by reversing and reconstructing.
  private readonly spectralParams = {
    noise_level: 0.7,      // Base noise level for honking timbre
    spectrum_shift_frequency_hz: 24563,    // Primary harmonic frequency (1st overtone)
    spectral_envelope_gain_db: -8.0,        // Dynamic range shaping to reduce harshness while keeping pitch stable
    noise_profile_type: 'hollow',       // Use hollow noise for a resonant, honking quality
    time_constant_ms: 125.0             // Fast transient response (simplified)
  };

  /**
   * Apply spectral modeling morphing to the input audio data.
   * This method reverses the order of frames in the input array so that we can process them as if they were generated sequentially from a reversed stream, effectively making the generation operation palindromic with respect to frame ordering.
   */
  private _apply_spectral_morphing(inputData: AudioData): AudioData {
    // Invert the audio data frames by reversing their order and then reconstructing them in reverse sequence (to match the original input structure)
    const reversedFrames = inputData.frames.slice().reverse();

    if (!reversedFrames || reversedFrames.length === 0) {
      return null;
    }

    // Reconstruct the output AudioData with frames in reverse order to ensure consistent processing flow.
    let result: Array<number> | undefined = new Float32Array(reversedFrames[1].buffer); // Assuming input is an array of arrays, we need to handle dimensions carefully if it's a single frame or multi-frame

    for (let i = reversedFrames.length - 1; i >= 0; --i) {
      const currentFrame = reversedFrames[i];
      
      if (!currentFrame || !Array.isArray(currentFrame)) continue; // Skip invalid frames
      
      let gain: number | undefined;
      
      // Apply the morphing logic based on frame content and dynamic range.
      // The 'hollow' noise profile creates resonance, mimicking the honking quality of geese.
      const currentSample = currentFrame[0]; 
      
      if (currentSample > 0) {
        gain = this.spectralParams['spectral_envelope_gain_db'] + Math.abs(currentSample / this.spectralParams['noise_level']) * ((1 - inputData.frames[i].shape[0]) ** 2); // Rough approximation for the first frame's shape
        
        if (gain > 0) {
          result = new Float32Array(result || [currentFrame]); 
          
          const freqFactor = currentSample / this.spectralParams['noise_level'];
          gain += Math.abs(freqFactor % 4.0); // Add a dynamic range shaping component to the frequency factor
        
        } else if (gain < -1) {
           // Clamp negative envelope values or handle as noise depending on specific requirements
           result = new Float32Array(result || [currentFrame]); 
          gain = this.spectralParams['spectral_envelope_gain_db'] + Math.abs(currentSample / this.spectralParams['noise_level']) * ((1 - inputData.frames[i].shape[0]) ** 2); // Fallback for low levels
        } else {
           result = new Float32Array(result || [currentFrame]); 
        }
      } else if (gain > 0) {
         result = new Float32Array(result || [currentFrame]); 
      }

    }

    return inputData.frames.length === 1 ? result : supercoll.AudioData.from_array(reversedFrames); // Handle the case where input is a single frame or multi-frame array by reconstructing in reverse order.
}

/**
 * Apply harmonic morphing to shift frequencies while maintaining pitch (the "honk").
 */
private _harmonic_morphing(baseFreq: number): AudioData {
  if (!baseFreq || baseFreq === 0) return null; // Handle zero frequency gracefully
  
  let offset = Math.abs(baseFreq - this.spectralParams['spectrum_shift_frequency_hz']) / 24563 * 18;

  const result: Array<number> | undefined = new Float32Array();
  
  for (let i = 0; i
