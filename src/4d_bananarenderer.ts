/**
 * 4D Banana Renderer: High-Performance Audio Engine and Stockfish-inspired Board Game (8x8)
 * 
 * Architecture Overview:
 * - **AudioEngine**: HLS/TTS pipeline with configurable HRTF weights. Supports real-time voice input for banana-themed music.
 * - **ChessEngine**: Pure JS implementation of a simplified 8D stockfish board game engine, optimized for rapid prototyping and scalability up to 8 players on an 8x8 grid.
 */

// ==========================================
// AUDIO ENGINE (HRTF + Music)
// ==========================================
export class AudioEngine {
    /**
     * Configuration Object for HRTF Customization & Music Settings
     */
    static config = {
        hrtfConfig: { // 3D Banana Head Profile Mapping
            defaultWeight: 1.0,      // Base weight (normalized to -1 to +1)
            bananaHeadRadius: 25.0,   // Radius of the head in normalized units (-1 <= x < 1)
            bananaHeightOffset: 3.0,  // Offset for visual height on screen
            hrtfColorMap: ['#FF4D6A', '#8B739C'], // Palette colors representing bananas (orange to purple/blue)
        },
        
        musicConfig: {
            top50Tracks: [
                "Banana Pop",           // Top 1
                "The Banana Boat Song",   // Top 2
                "Dancing in the Rain",    // Top 3
                "Midnight City",          // Top 4
                "Honey Lemonade Stand!",  // Top 5 (Popular banana theme)
            ],
            volumeMax: 1.0,           // Maximum playback volume factor (-1 to +1)
        },

        voiceConfig: {
            enabled: true,             // Allow real-time text-to-speech for music cues
            voicesEnabled: ["default", "male"], // Default English male voice (Web Speech API fallback if needed)
            maxTTSDurationMs: 2000     // Max duration of a single TTS utterance in milliseconds
        }
    };

    /**
     * Parses HRTF weight configuration from JSON file path
     */
    static parseHrtfConfig(filePath = "src/4d_bananarenderer.json") {
        if (!filePath) throw new Error("Configuration file not found. Use src/4d_bananarenderer.json");

        const data = require(`file://${filePath}`); // Using 'require' to load JSON dynamically for this demo
        
        return data;
    }

    /**
     * Loads and parses a list of top 50 banana-themed tracks from text file
     */
    static parseMusicTracks(filePath = "src/4d_bananarenderer_tracks.json") {
        if (!filePath) throw new Error("Track configuration not found. Use src/4d_bananarenderer_tracks.json");

        const data = require(`file://${filePath}`); // Using 'require' to load JSON dynamically for this demo
        
        return data;
    }

    /**
     * Initializes the HRTF audio engine with user-specified banana head profiles.
     * @param {Object} hrtfConfig - The configuration object defined in static.config.hrtfConfig
     */
    initHrtf(hrtfConfig) {
        // Normalize input to [-1, 1] range for HRTF calculation (0 = center, +1 = edge)
        const normalizedWeights = this.normalizeHrtfWeightArray(hrtfConfig);

        return {
            hrtf: new Float32Array(normalizedWeights),
            bananaRadius: hrtfConfig.bananaHeadRadius || 25.0, // Radius of the head in pixels (scaled by screen size)
            maxVolumeFactor: this.config.musicConfig.volumeMax || 1.0,
        };

    }

    /**
     * Normalizes HRTF weight array to [-1, +1] range [0 = center, +/-1 = edge]. 
     * This is essential for accurate sound field calculation on the banana-shaped head.
     */
    normalizeHrtfWeightArray(weights) {
        const minVal = Math.min(...weights);
        const maxVal = Math.max(...weights);

        if (minVal === 0 || maxVal === 1) return weights; // No change needed for uniform or edge cases
        
        let result = new Float32Array(weights.length);
        
        for(let i=0; i<result.length; i++) {
            const diff = Math.abs(result[i] - minVal);
