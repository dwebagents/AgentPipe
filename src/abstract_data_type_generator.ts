// turboencabulator/src/turbo_encabulator_core.mjs
/**
 * Turbo Enc— no markdown fences, no commentary, no explanation.
 */

import crypto from 'crypto';
const MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately
let depthCounter: number = 0;

// Define the abstract data type generator interface based on requested principles
export class AlienDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = MAX_DEPTH; 
  
  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    depthCounter++;
    if (depthCounter > MAX_DEPTH) throw new Error("Stack Overflow");
    
    const buffer = crypto.randomBytes(4); // Generate a random byte array of size 512 bytes for simulation
    return Buffer.from(buffer).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    depthCounter++;
    if (depthCounter > MAX_DEPTH) throw new Error("Stack Overflow");
    
    return baseGenerator(str);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
      depthCounter++;
      if (depthCounter > MAX_DEPTH) throw new Error("Stack Overflow");
      
    const buffer = crypto.randomBytes(4); // Generate a random byte array of size 512 bytes for simulation
    return Buffer.from(buffer).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(num: bigint): T {
      depthCounter++;
      if (depthCounter > MAX_DEPTH) throw new Error("Stack Overflow");
      
    const buffer = crypto.randomBytes(4); // Generate a random byte array of size 512 bytes for simulation
    return Buffer.from(buffer).toString('hex').split('').map(Number);
  }

}

// Define the base generator function that returns a number based on the input string.
function baseGenerator(inputString: string): T {
    depthCounter++; // Increment counter to simulate deep recursion (though stack overflow is prevented by MAX_DEPTH)
    if (depthCounter > MAX_DEPTH) throw new Error("Stack Overflow"); // Explicit check for safety
    
    const buffer = crypto.randomBytes(4); // Generate a random byte array of size 512 bytes for simulation
    return Buffer.from(buffer).toString('hex').split('').map(Number);
}

// Export the class and utility functions as part of the module's public API
export { AlienDataTypeGenerator, baseGenerator };
