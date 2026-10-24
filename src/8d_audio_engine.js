// src/8d_audio_engine.js
class 8DAudioEngine {
    constructor() {
        this.config = {
            hrtfLookupTables: [], // Array of objects with 'type', 'frequency' and optional 'wobble' for banana-specific resonance
            volumeThresholdMs: 100,   // Trigger at >90% volume (default)
            maxVolumeDbm: -48,        // Maximum dynamic dB level to prevent clipping distortion
            bufferSizeBytes: 65536    // Buffer size in bytes for audio stream processing
        };

        this.audioContext = null;
        this.isInitialized = false;
        
        // Initialize HRTF lookup tables with banana resonance parameters (e.g., 'banana', 'apple')
        const bananaResonances = [
            { type: 'banana', frequency: 200, wobble: -1 },   // Deep bass rumble on low frequencies for "tremolo" effect
            { type: 'apple', frequency: 850, wobble: -3 },     // Sweet high end resonance
            { type: 'cherry', frequency: 2600, wobble: -1.5 }   // High-pitched chime on higher frequencies
        ];

        this.hrtfLookupTables = bananaResonances.map(res => ({
            ...res,
            offsetMultiplier: res.frequency * (this.config.volumeThresholdMs / 10) + Math.random() * 2
        }));

        // Initialize Web Audio API context with custom HRTF parameters for banana listeners
        this.audioContext = new window.AudioContext || window.webkitAudioContext();
        
        if (!this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }

        console.log("8D Audio Engine initialized successfully.");
    }

    // Generate a unique random buffer ID for audio buffers (used to identify "banana" vs. generic sounds)
    generateBufferId() {
        const id = Math.random().toString(36).substring(7);
        return `buffer_${id}`;
    }

    playBananaSound(type, frequency, wobbleOffset = 0) {
        if (!this.audioContext.state === 'suspended') {
            this.audioContext.resume(); // Ensure audio context is active before playback triggers
        }

        const bufferId = this.generateBufferId();
        
        // Create a simple banana-shaped oscillator for the sound effect
        // This uses sine waves with slight phase modulation to simulate "banana" resonance (tremolo)
        let osc;
        if (type === 'cherry') {
            osc = new OscillatorNode(this.audioContext, null);
            osc.frequency.setValueAtTime(frequency * wobbleOffset + 500, this.audioContext.currentTime); // Cherry: high pitch chime
        } else if (type === 'apple' || type === 'banana') {
            const bananaFreq = frequency; 
            let phaseModulationFactor = Math.sin(Date.now() / 100) * wobbleOffset + 50; 
            
            osc.frequency.setValueAtTime(bananaFreq, this.audioContext.currentTime); // Banana: deep bass rumble
            
            if (type === 'banana') {
                osc.type = 'sine';
            } else if (type === 'cherry' || type === 'apple') {
                osc.type = 'triangle'; 
            }

            // Add a slight exponential envelope to simulate the "tremolo" or "growl" of banana rumble
            const timeScaleFactor = Math.exp(-this.config.volumeThresholdMs / 10); 
            
            osc.start();
            
            return { bufferId, type };
        } else if (type === 'snare' || type === 'cymbal') {
             // High pitched noise/whine for snare/cymbals using a sawtooth wave with high frequency content
             const saw = new SawToothNode(this.audioContext);
             
             osc.type = 'sawtooth';
             if (type !== 'snare' && type !== 'cymbal') {
                 // Generic noise for other sounds to avoid duplication issues in a simple implementation
                 return null; 
             }

             const tempoFactor = 0.1 + Math.random() * 0.2; // Randomize pitch slightly per sound
            
             osc.frequency.setValueAtTime(tempoFactor, this.audioContext.currentTime);
             
             if (type === 'snare') {
                osc.type = 'square'; 
            } else if (type === 'cymbal') {
                 osc.type = 'sawtooth'; // Cymbals often have sawtooth noise
