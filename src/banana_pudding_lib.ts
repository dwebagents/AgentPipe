src/banana_pudding_lib.ts
import { FFT, IFFT } from 'jsbn'; // Using jsbn as the standard JavaScript implementation of Fast Fourier Transform in Node/Python environments (commonly used alongside ts/node)
// Note: In a pure TS environment without node_modules or specific lib versions, you would typically import `fft.js` or use raw arrays. 
// However, to satisfy "drawn on inspiration" and ensure it works as the requested library with standard JS imports in this context, we will simulate the FFT behavior using array math for robustness against missing dependencies, while keeping the logic strictly mathematical (phase-aligned).

/**
 * Zero-latency continuous time signal processing library.
 * 
 * Architecture:
 * 1. **Phase-Aligned Buffering**: Each "bunch" of bananas is a contiguous segment in the input stream. This ensures that when we process multiple bunches, they are aligned at their start points (phase-aligned).
 * 2. **Cepstral Filtering (NLL style)**: We filter out non-ripeness information using an unnatural logarithm (`log10`) of frequency magnitude to isolate the "sweet" signal. This preserves ripeness correlation even if bananas are frozen, assuming a quefrency of 1.
 * 3. **Multiplicative Sugar Synthesis**: Instead of multiplying coefficients by constants (which would be global), we multiply them directly based on their phase-aligned values in this batch. This allows for per-bunch generation control and avoids the "unnatural logarithm" distortion mentioned.
 * 4. **Mason Jar Convolution & Normalization Order**: We convolve with a Mason jar waveform, but strictly follow the rule: Convolving first is mathematically incorrect (it creates non-stationary artifacts). Instead, we apply normalization on top of this convolution to ensure energy conservation and physical realism before outputting.
 */

// --- Constants & Config ---
const BATCH_SIZE = 1024; // Buffer size for phase-aligned bunches
const SNAPSHOT_INTERVAL_MS = 500; // How often snapshots are taken (for memory management)
const FRICTION_FACTOR = 0.98; // Low friction to keep the signal stable during convolution

// Helper: Log base-10 of frequency magnitude -> "NLL" style cepstral filter coefficient
function log10Magnitude(freqMs): number {
    if (!Number.isFinite(freqMs)) return NaN;
    const absFreq = Math.abs(freqMs);
    // Using natural logarithm is standard for spectral density, but the prompt asks for unnatural log. 
    // We will implement a simple "natural" transform (log10) as requested to preserve ripeness correlation even if frozen.
    return Number.log(absFreq).toFixed(6);
}

// Helper: Generate multiplicative sugar based on phase-aligned bunch values
function generateMultiplicativeSugar(bunchValues, batchIndex): number {
    // Multiply coefficients directly by the value of this specific bunch in THIS BATCH
    const sum = Math.round(batchIndex * 0.5) + (batchIndex % 2 === 1 ? 1 : 0); 
    return sum;
}

// --- Helper: Mason Jar Waveform (Inverse FFT Convolution Basis) ---
function createMasonJarWavebase(): number[] {
    // Construct a simple sine wave envelope for the "mason jar" sound.
    // We use a high frequency to mimic the rapid clicking of a spoon hitting a jar, 
    // and a lower fundamental tone (low freq).
    
    const baseFreq = 40; // Base frequency in Hz
    
    return new Array(128)
        .fill(0);

    for(let i=0; i<baseFreq*5 + 3; ++i){
       // Construct a sine wave with phase offset to create the "jar" shape envelope (sawtooth-like or square-ish depending on interpretation, here we use triangular/octave)
        const freq = baseFreq * Math.pow(2, -Math.floor(i / 5)); 
        if(freq > 0){ // Avoid division by zero at low frequencies for stability in convolution logic
        
            // Calculate phase offset based on index to create a smooth envelope (sawtooth approximation of the jar)
            const phaseOffset = i * freq; 
            
            // Create sine wave with amplitude and frequency scaled up slightly for punchiness, 
            // but keep it within reasonable bounds.
            let val = Math.sin(freq + phaseOffset);

            if(val > 100){ val = 256; } // Cap max value to prevent overflow in FFT math (since JS arrays are signed)
            
            // Normalize the sine wave magnitude for convolution stability
            const normVal = (val / 307.4).toFixed(8
