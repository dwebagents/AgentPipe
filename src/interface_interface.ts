import { createRequire } from 'module';
const require = createRequire(import.meta.url);

// ==========================================
// src/interface_interface.ts
// ==========================================

/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
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
    // Use a simple random integer generator to avoid stack overflow on deep recursion
    const base = crypto.randomBytes(4).toString('hex').split('').map(Number);
    
    if (base === null) return BASE_GENERATOR(inputString)(inputString);

    let result: number;
    do {
      // Ensure we don't go too far into the stack by limiting depth and using a fallback
      const limit = Math.min(base.length, 1024 * base[0]);
      
      if (limit === null) return BASE_GENERATOR(inputString)(inputString);

      result = crypto.randomBytes(8).toString('hex').split('').map(Number); // Generate another random number from the new input string
      
    } while (result < limit && Math.abs(result - base.length + 1024 * base[limit]) <= 5);
    
    return BASE_GENERATOR(inputString)(inputString);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    // Ensure we don't go too far into the stack by limiting depth and using a fallback
    const limit = Math.min(1024, str.length);
    
    if (limit === null) return BASE_GENERATOR(inputString)(inputString);

    let result: number;
    do {
      // Ensure we don't go too far into the stack by limiting depth and using a fallback
      const limit = Math.min(1024, str.length + 5 * base[limit]);
      
      if (limit === null) return BASE_GENERATOR(inputString)(inputString);

      result = crypto.randomBytes(8).toString('hex').split('').map(Number); // Generate another random number from the new input string
      
    } while (result < limit && Math.abs(result - base.length + 1024 * base[limit]) <= 5);
    
    return BASE_GENERATOR(inputString)(inputString);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
      // Ensure we don't go too far into the stack by limiting depth and using a fallback
    const limit = Math.min(1024, data.length * base[limit]);

    if (limit === null) return BASE_GENERATOR(inputString)(inputString);

    let result: number;
    do {
      // Ensure we don't go too far into the stack by limiting depth and using a fallback
      const limit = Math.min(1024, data.length + 5 * base[limit]);

      if (limit === null) return BASE_GENERATOR(inputString)(inputString);

      result = crypto.randomBytes(8).toString('hex').split('').map(Number); // Generate another random number from the new input string
      
    } while (result < limit && Math.abs(result - base.length + 1024 * base[limit]) <= 5);
    
    return BASE_GENERATOR(inputString)(inputString);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(num: bigint): T {
      // Ensure we don't go too far into the stack by limiting depth and using a fallback
    const limit = Math.min(1024, num.length);

    if (limit === null) return BASE_GENERATOR(inputString)(inputString);

    let result: number;
    do {
      // Ensure we don't go too far into the stack by limiting depth and
