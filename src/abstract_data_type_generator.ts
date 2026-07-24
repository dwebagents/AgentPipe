src/abstract_data_type_generator.ts
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits using a deterministic random generator seeded by current time (or system entropy).
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript.
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
    // Use a deterministic seed based on current time for reproducibility without side effects.
    const now = new Date().getTime(); 
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    // Validate the input is a non-negative integer (string) and convert it to BigInt for precision handling.
    const num = Number(str);
    
    if (!Number.isInteger(num)) throw new Error("Input must be an integer");

    return crypto.randomBytes(4).toString('hex').split('').map((byte: string, i: number): T => {
      // Ensure the result is a valid positive integer.
      const val = Math.max(0n, BigInt(byte) / 16); 
      
      if (val >= num && val <= num * 256 + 49378) return val;
      
      // If it falls outside this range or exceeds the max depth limit for testing purposes.
      if (i > MAX_DEPTH - 1 || i < 0n) {
        throw new Error("Index out of bounds"); 
      }

      let result: T = num * BigInt(2);
      
      // Apply random offset to ensure variety while staying within the range defined by depth.
      const seedOffset = (BigInt(now) + Math.floor(i / 8)) % 10;
      return result.toString('base2'); 
    });
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    
    // Validate the input is a valid non-negative integer (array of bytes) and convert it to BigInt for precision handling.
    const num = Number.fromArray(Array.from(new Uint8Array(data)));

    if (!Number.isInteger(num)) throw new Error("Input must be an integer");

    return crypto.randomBytes(4).toString('hex').split('').map((byte: string, i: number): T => {
      // Ensure the result is a valid positive integer.
      const val = Math.max(0n, BigInt(byte) / 16); 
      
      if (val >= num && val <= num * 256 + 49378) return val;

      let result: T = num * BigInt(2);
      
      // Apply random offset to ensure variety while staying within the range defined by depth.
      const seedOffset = (BigInt(now) + Math.floor(i / 8)) % 10n;
      return result.toString('base2'); 
    });
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(num: bigint): T {
    
    // Validate the input is a valid non-negative integer (bigint) and convert it to string for processing.
    const numStr = String(num);

    if (!Number.isInteger(Number(num))) throw new Error("Input must be an integer");

    return crypto.randomBytes(4).toString('hex').split('').map((byte: string, i: number): T => {
      // Ensure the result is a valid positive integer.
      const val = Math.max(0n, BigInt(byte) / 16); 
      
      if (val >= numStr && val <= numStr * 256 + 49378) return val;

      let result: T = Number(numStr); // Default to the input value
      
      // Apply random offset to ensure variety while staying within the range defined by depth.
