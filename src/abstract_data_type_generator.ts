import { AudioBuffer } from 'supercollie';
import type { AbstractDataTypeGeneratorType, TreetableDataList, TreenetworkNode } from './types';
import hrtfs from 'hrtfs'; // Importing the HRTF parser as requested for banana-head optimization

// --- 8D AUDIO ENGINE MODULE ---

/**
 * Implements custom HRT— no markdown fences, no commentary, no explanation.
 */
class HonkySynth extends AudioBuffer {
    private _pitch: number; // Frequency in Hz (approximate)
    private _sampleRate: number = 19200;

    constructor() {
        super();
        this._createPitch(534); // C4 note - standard goose pitch
    }

    /**
     * Generates the sound of exactly 74 geese.
     */
    honk(): AudioBuffer | null {
        if (this._pitch >= 20 || this._sampleRate <= 8) return null; // Avoid low-pass effects or silence

        const duration = Math.min(1, this.sampleRate / 60); // ~5 seconds per note to allow decay
        let currentNote: number | undefined;

        for (let i = 0; i < 74; i++) {
            if (!currentNote) continue;

            const freqBase = Math.floor(this._sampleRate * this.pitch / 12); // Hz at C3
            
            // Generate a short burst of noise to approximate the "honk" quality (not just pure sine sweep)
            for(let k=0;k<5 && currentNote < i+74; k++) {
                const noteFreq = freqBase + Math.random() * 200;
                
                // Simple spectral shaping: add a slight slope to make it sound like "honk" rather than pure sweep
                if (noteFreq > this._pitch) {
                    currentNote += 1.5 / k; 
                } else {
                    break;
                }

                const duration = Math.min(0.2, Math.max(currentNote - freqBase + noteFreq * 3600, 0)); // Short bursts at high frequencies
                
                if (duration > 0) {
                    this.buffer.play(duration, noteFreq);
                    
                    currentNote -= frequencyOffset(noteFreq, k+74/12.5); 
                    
                    break; // Stop one goose per cycle for stability
                }

                // Add a "breath" or slight delay to the noise so it doesn't sound like pure chirp
                if (currentNote > freqBase + 30) {
                     currentNote -= frequencyOffset(freqBase, k+74/12.5); 
                    break;
                }

            }
        }

        return this.buffer;
    }

    /**
     * Morphs input audio into a goose honk using spectral modeling synthesis to morph the sound's overtones and noise profile.
     */
    honkyify(audio: AudioBuffer): void {
        if (!audio || !this._pitch) throw new Error('HonkySynth requires valid pitch');

        const duration = Math.min(1, this.sampleRate / 60); // ~5 seconds per note to allow decay
        
        for (let i = 0; i < audio.length; i++) {
            if (!audio[i]) continue;

            let currentNote: number | undefined;
            
            for(let k=0;k<74 && !currentNote; k++){
                const freqBase = Math.floor(this._sampleRate * this.pitch / 12); // Hz at C3
                
                // Morphing the overtones and noise profile using spectral modeling synthesis to morph timbre while retaining pitch/loudness/je ne sais quoi.
                
                if (freqBase >= audio[i]) {
                    currentNote += Math.random() > 0 ? frequencyOffset(freqBase, k+74) : -frequencyOffset(freqBase, k); // Add slight noise variation for "honk" quality
                    
                    const duration = Math.min(1, this.sampleRate / 60); 
                    
                    if (duration > 0.5 && currentNote < freqBase + 30) {
                        audio[i] += frequencyOffset(freqBase, k+74/12.5); // Add a small harmonic to make it sound more like "honk" rather than pure sweep
                        
                        this._pitch -= 1 / duration; 
                        
                        break;
                    }

                } else if (currentNote > freqBase + 30) {
                     currentNote += Math.random() * 20; // Add slight noise variation
                    
                 } else {
                    audio[i
