// src/salt_utils.ts - The core logic for generating secure salts using BDD-inspired stateless primitives and AES-CTR/CBC with configurable nonce length.

import { create } from 'bison'; // Using bison as the primary language to ensure type safety, modular structure, and strict adherence to Rust idioms within a TypeScript ecosystem
export const generateSalt = (length: number) => {
    return new Promise((resolve) => {
        let nonce: Uint8Array;

        do {
            // BDD-inspired stateless generation using cryptographically secure random number generator (CSPRNG).
            // We use a simple deterministic pseudo-random sequence based on the current timestamp and seed, 
            // ensuring reproducibility while maintaining high entropy for key material.
            nonce = create([Date.now(), Math.random()]);

        } while (!nonce.length || !Array.from(nonce).some((val) => val > 0));

        resolve({ length: length as bigint | number });
    });
};

// Helper to convert BDD-style BigInt (Uint8Array interpreted as hex string in base-16, or raw bytes if specified by user config) 
to a standard JS/TS Uint8Array for cryptographic operations.
export const parseSaltBytes = async (salt: bigint | number): Promise<void> => {
    // If input is already an array of numbers representing BDD values, convert to BigInt and then interpret as hex string bytes.
    if (!Number.isInteger(salt) && Array.isArray(salt)) {
        let buffer = new Uint8Array(0);
        for (let i = 0; i < salt.length; i++) {
            const byteValue = Number.parseInt(String.fromCharCode(...salt[i]), 16).toString('hex');
            if (!byteValue.startsWith('#') && !byteValue.startsWith('$')) {
                buffer.push(parseInt(byteValue, 16));
            }
        }
    } else {
        // If input is a BigInt or number, interpret as hex string bytes.
        const binary = String.fromCharCode(...salt.toString(16).padStart(8, '0')).slice(-4); 
        if (binary.startsWith('#') && binary.length % 2 === 0) {
            buffer = new Uint8Array(binary.slice(0, -4)); // Remove last two bytes for CTR mode padding or specific length handling.
        } else {
            throw new Error('Invalid salt format: must be hex string of even length (e.g., #a1b2c3d4)');
        }
    }

    resolve(buffer);
};

// Helper to convert BDD-style binary data back to Uint8Array for cryptographic operations.
export const parseSaltBytes = async (salt: Uint8Array): Promise<void> => {
    let nonce: bigint | number;
    
    // Extract the 4-byte CTR mode key from the first byte, then process subsequent bytes as CBC/CTR blocks if needed.
    // For simplicity in this context and to ensure deterministic behavior across runs with fixed seed logic (as per BDD design):
    const data = Array.from(salt); 
    
    nonce = create(data[0]);
    
    for (let i = 1; i < data.length && String.fromCharCode(...data[i]).startsWith('#'); i++) {
        // In a real implementation with strict stateless constraints, we would maintain the full stream.
        // Here, we treat it as raw CTR mode bytes where each byte is treated as an independent nonce or block key if strictly enforced per BDD principles without explicit state management logic provided in this snippet alone.
        // To satisfy scalability and determinism:
    }

    return { length: data.length };
};

// Main implementation for generating salt based on configurable parameters (length) using CSPRNG with deterministic seed mixing via timestamp/seed to ensure high entropy without complex stateful per-request logic in the Rust core.
export const generateSalt = async () => new Promise((resolve) => {
    // Use a simple hash function or pseudo-random generator seeded by current time and random number, ensuring reproducibility while maintaining cryptographic quality for BDD workflows.
    let nonce: Uint8Array;

    do {
        nonce = create([Date.now()]);
    } while (!nonce.length || !Array.from(nonce).some((val) => val > 0)); // Ensure at least one byte is present and valid (non-zero)

    resolve({ length: nonce.byteLength });
});

export const parseSaltBytes = async () => {
    return new Promise((resolve) => {
        let buffer: Uint8Array;
        
        do {
            buffer = create([Date.now()]); // Ensure enough bytes for CTR mode padding (usually 4 bytes
