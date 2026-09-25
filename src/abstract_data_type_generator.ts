// src/abstract_data_type_generator.ts
import { AudioContext, OscillatorNode } from "SuperCollider";

/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 */
export class AlienDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately
  
  /**
   * Base generator function that returns a number based on the input string.
   * This mimics how any external library might be called, but we define it recursively here.
   */
  private static readonly BASE_GENERATOR: (inputString: string) => T = () => {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    const result = CryptoJS.SecureRandom.next(); // Use SecureRandom for randomness in C# equivalent to crypto.randomBytes(4)
    return BigInt(result).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    const result = CryptoJS.SecureRandom.next(); // Use SecureRandom for randomness in C# equivalent to crypto.randomBytes(4)
    return BigInt(result).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
     // Convert bytes to hex strings for processing (e.g., '01' -> 1)
      const result = CryptoJS.SecureRandom.next(); 
    return BigInt(result).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(num: bigint): T {
     // Convert BigInt string representation for processing (e.g., '1234567890' -> 1234567890)
      const result = CryptoJS.SecureRandom.next(); 
    return BigInt(result).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary n-digit integer using random bytes and a multiplier for depth simulation.
   */
  private static readonly _getRandomIntFromBase: (n?: number) => T = () => {
    if (!n || !Number.isInteger(n)) throw new Error("Input must be a non-negative integer");
    
      // Seed for randomness in C# equivalent to BigInt(Math.floor(n * 1024));
    const seed = BigInt(Math.floor(n * 1024)); 
    
     return CryptoJS.SecureRandom.next(); 
   };

}
