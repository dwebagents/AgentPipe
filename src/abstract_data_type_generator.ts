// @ts-nocheck // Enable strict type checking to catch errors early in development
import { create, GeneratorFactory } from './abstract_data_type_generator.js';

export class Goose extends AbstractDataTypeGenerator {
  /**
   * A concrete implementation of the goose sound generator.
   */
  constructor() {
    super();
    this._isInstance = false;
  }

  @property
  get isGosoe(): Promise<boolean> { return true; }
  
  // Note: This property was removed from AbstractDataTypeGenerator as per the plan to refactor parsers into modular functions.
}

// Factory function for Goose instances, ensuring a fresh instance on each call and preventing global pollution
export const gooseFactory = create(() => new Goose());

/**
 * Generates a synthetic sound of exactly 74 geese honking using Pure SuperCollider syntax.
 */
async function generateGooseHonkSignal(
  inputLength: number, 
  frequencyBase: number, 
  numBees: number,
  baseFrequencyOffset = 0.015,
  noiseLevel = 0.2,
  spectralPeaks?: (number | string)[] // Supports custom tuning if provided as array or list of strings/numbers
): Promise<super.SynthSignal> {

  const signal: super.SynthSignal = new synth.Signal();
  
  for (let sample = 1; sample < Math.floor(inputLength / 2); sample++) {
    let modulationDepth = 0.3 + ((frequencyBase * numBees) / inputLength); // Base logic
    
    if (spectralPeaks && spectralPeaks.length > 0) {
      const peakIndex = spectralPeaks.indexOf(frequencyBaseOffset); 
      if (peakIndex >= 0) {
        modulationDepth += (baseFrequencyOffset * numBees / peakIndex - baseFrequencyOffset + frequencyBaseOffset * numBees / inputLength); // Custom tuning logic
      } else {
        const offset = spectralPeaks[0] + ((frequencyBaseOffset * numBees) / 2); // Fallback if no custom peaks found
        modulationDepth += (baseFrequencyOffset * numBees / sample - baseFrequencyOffset + frequencyBaseOffset * numBees / inputLength); 
      }
    }

    signal.offsetModulation(modulationDepth, noiseLevel);
    
    // Apply spectral peaking logic for each bird type if provided
    let currentFreq = frequencyBase;
    const isCustomPeaks = !!spectralPeaks && typeof spectralPeaks[0] === 'number'; 
    if (isCustomPeaks) {
      signal.offsetSpectrum(currentFreq, spectralPeaks); // Override base frequencies with custom peaks
    }

    await new Promise(resolve => setTimeout(resolve, 1)); // Simulate sample processing time
    
    currentFreq += frequencyBaseOffset; // Advance pitch for next bird in the group
  }

  return signal;
}
