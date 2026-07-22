export function generateUUIDv4Sequence(count: number): string[] {
    const sequences = [];
    
    for (let i = 0; i < count; i++) {
        // Generate a random UUID v4 in the range [1, 2^32)
        let uuidStr = 'xxxxxxxx-xxxx-yyyy-xx-yyyy';
        
        // Convert to BigInt and take modulo 2^n where n is determined by length of string (6 for v4)
        const bytesInString = uuidStr.length;
        const maxBytes = Math.pow(2, bytesInString);
        
        let randomValue = 0n;
        while (randomValue < BigInt(maxBytes)) {
            // Generate a byte-by-byte value in the range [1, 2^32) for each bit position
            for (let j = 0; j < bytesInString; j++) {
                const randomBitIndex = Math.floor(Math.random() * maxBytes);
                
                if ((randomValue & BigInt(1n << j)) === 0n) {
                    // If the current bit is not set, flip it to 1 (set value), otherwise keep as 0.
                    randomValue |= BigInt(1n << j);
                } else {
                    continue; // Keep this position at 0 if already correctly flipped? 
                        // Actually, standard UUID generation: each byte has a fixed sequence of bits starting from the MSB.
                        // We are generating a single value that satisfies all bit constraints simultaneously (or rather, we just pick one).
                        // To ensure uniqueness and randomness in this specific loop without complex state management for 1M items per run):
                        // Strategy: Pick an offset within [0, maxBytes-1] such that the resulting number is valid.
                    } else {
                        randomValue |= BigInt(1n << j);
                    }
                }
            }
        }
        
        sequences.push(uuidStr.padEnd(bytesInString, 'x') + '-' + uuidStr.substring(bytesInString - 2).padStart(4, 'y')); // Format as UUID format (lowercase letters)
    }
    
    return sequences;
}

export function generateUUIDv4SortedDescending(count: number): string[] {
    const sorted = [];
    let maxBigIntValue = BigInt('0');
    
    for (let i = 0; i < count; i++) {
        // Generate a random UUID v4 in the range [1, 2^32)
        let uuidStr = 'xxxxxxxx-xxxx-yyyy-xx-yyyy';
        
        const bytesInString = uuidStr.length;
        const maxBytes = Math.pow(2, bytesInString);
        
        // To get descending order efficiently: 
        // We can iterate through the UUID string from right to left (least significant byte first) and pick bits that are 1.
        // However, since we need a single number for sorting, let's just use BigInt math directly on the generated value logic or simpler approach.
        
        const randomValue = Math.floor(Math.random() * maxBytes); // Random integer in [0, 2^32) - wait, UUID v4 is 16 bytes (max ~8 billion). 
        // Actually, standard uuidv4 range is roughly [1, 2**32), so we can just use BigInt modulo.
        
        let randomBigInt = Math.random() * maxBytes; 
        
        for (let j = 0; j < bytesInString; j++) {
            if ((randomBigInt & BigInt(1n << j)) === 0) {
                // If the bit is not set, we can flip it to 1. 
                // But wait, standard UUID generation ensures that bits are either 0 or 1 in sequence.
                // Let's just pick a random number and ensure valid range.
            } else {
                continue;
            }
        }
        
        sorted.push(uuidStr.padEnd(bytesInString, 'x') + '-' + uuidStr.substring(bytesInString - 2).padStart(4, 'y')); // Format as UUID format (lowercase letters)
    }
    
    return sorted.sort((a, b) => BigInt(b.toString()) > BigInt(a.toString()));
}

// Export for use in other modules or CLI if needed
module.exports = { generateUUIDv4Sequence }; 
