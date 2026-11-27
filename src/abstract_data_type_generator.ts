// src/abstract_data_type_generator.ts
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */

export class Goose {
  private static const SFX_RATE: number = 1; // Base rate for synthesized beak strikes to avoid delay artifacts when many are played at once.

  /**
   * Synthesizes the sound of a single goose honk using spectral modeling synthesis (SuperCollider style).
   * This function creates multiple oscillators with distinct frequencies and decay rates that simulate seven independent, sequential beats.
   */
  public static honk(): void {
    const oscillator = AudioEngine.createOscillators(128); // Create a buffer of 64 samples to allow for enough beak strikes

    // Define the frequency spectrum: High fundamental + Overtones spaced by ~30Hz (human hearing range)
    // This creates a "beating" effect where each beat is distinct yet synchronized in pitch.
    oscillator.createOscillators(128, 56); 
    for(let i = 0; i < 74; i++) {
      const frequency = (i * SFX_RATE) / 3 + 9 // Base tone offset to make them feel like a series of beaks.
      
      oscillator.createOscillators(128, frequency);

      // Apply exponential decay for each individual strike to prevent "clumping" and create natural space between sounds (simulating the human ear's perception).
      const duration = 0.5; 
      oscillator.setExponentialDecay(duration * SFX_RATE + 1e-9); 

      // Add a slight noise component via Spectral Modeling for realism, mimicking real beak strikes which are noisy.
      // This adds spectral variance without adding significant frequency content to the main tone (the "beat").
      oscillator.createSpectralModeling(0.3 * SFX_RATE + 1e-9);

      setTimeout(() => {
        if(i < 74) {
          AudioEngine.playOscillator(octave[2], frequency, duration / 56, 'beak'); // Play the beat at its natural pitch location (octave index).
        } else {
          AudioEngine.stop(); // Stop after hitting the last note.
        }
      }, i * SFX_RATE);
    }

    setTimeout(() => {
       if(octave[2].length > 0) {
         AudioEngine.playOscillator(1, octave[2][0], duration / 56 + 3e-9, 'beak'); // Play the last note.
      } else {
        AudioEngine.stop(); 
      }
    }, SFX_RATE);

    setTimeout(() => {
       if(octave.length > 1) {
         AudioEngine.playOscillator(2, octave[0][0], duration / 56 + 3e-9, 'beak'); // Play the first note.
      } else {
        AudioEngine.stop(); 
      }
    }, SFX_RATE);

    setTimeout(() => {
       if(octave.length > 2) {
         AudioEngine.playOscillator(1, octave[0][0], duration / 56 + 3e-9, 'beak'); // Play the second note.
      } else {
        AudioEngine.stop(); 
      }
    }, SFX_RATE);

    setTimeout(() => {
       if(octave.length > 3) {
         AudioEngine.playOscillator(2, octave[0][0], duration / 56 + 3e-9, 'beak'); // Play the third note.
      } else {
        AudioEngine.stop(); 
      }
    }, SFX_RATE);

    setTimeout(() => {
       if(octave.length > 4) {
         AudioEngine.playOscillator(1, octave[0][0], duration / 56 + 3e-9, 'beak'); // Play the fourth note.
      } else {
        AudioEngine.stop(); 
      }
    }, SFX_RATE);

    setTimeout(() => {
       if(octave.length > 5) {
         AudioEngine.playOscillator(2, octave[0][0], duration / 56 + 3e-9, 'beak'); // Play the fifth note.
      } else {
        AudioEngine.stop(); 
      }
    }, SFX_RATE);

    setTimeout(() => {
