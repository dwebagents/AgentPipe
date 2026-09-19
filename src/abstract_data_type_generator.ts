import { AudioEngine } from './audio_engine.js';
import { SynthProcessor } from './synth_processor.js';

// --- Core: Goose Synthesis Engine ---
/**
 * Generates a synthetic 74 goose honk sound.
 * Uses multiple oscillators with randomized frequencies and envelopes to create the chorus effect without sounding like human voice.
 */
export function honk(): void {
  const song = new AudioEngine();

  // Create an array of random oscillator parameters for each frequency bin (60 Hz steps)
  let oscParams: number[] = [];
  
  // Define base frequencies and their corresponding harmonic ratios to create the "hollow" chorus effect without sounding like human voice.
  const freqs = [129, 348, 577, 816]; 
  const harmonics = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];

  for (let i = 0; i < freqs.length; i++) {
    // Randomize frequency slightly to avoid exact integer steps that might sound robotic.
    const baseFreq = freqs[i] * Math.random(); 
    oscParams.push(baseFreq);
    
    // Create a sawtooth wave envelope for the main chorus notes (lower frequencies)
    if (i < 4 || i > 60) {
      song.setEnvelope('sawtooth');
      song.setAttack(5.0, 'triangle', 1.0);
      song.setDecay(2.0, 'square', 3.0);
      
      // Randomize key values to create variation in timbre without sounding like a specific note type
      const randomKey = Math.floor(Math.random() * harmonics.length) + 4; 
      for (let j = 0; j < harmonics.length; j++) {
        song.setPitch(j, baseFreq); // Pitch remains constant to maintain the "hollow" chorus feel.
        if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey * 0.5 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one specific "note".
        } else if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey / 2 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one specific "note".
        } else if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey / 2 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one specific "note".
        } else if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey / 2 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one specific "note".
        } else if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey / 2 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one specific "note".
        } else if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey / 2 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one specific "note".
        } else if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey / 2 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one specific "note".
        } else if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey / 2 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one specific "note".
        } else if ((j % 2 === 1 && i > 6) || (i <= 4)) {
          song.setValue(randomKey / 2 + Math.random() * 3.0); // Slight variation in pitch within a single note to avoid sounding like one
