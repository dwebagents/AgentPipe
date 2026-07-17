src/abstract_data_type_generator.js
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in JavaScript (no external libraries).
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
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string input using hex-encoded random bytes split into individual integers.
   */
  public static generateFromString(str: string): T {
    const numStr = crypto.randomBytes(4).toString('hex').split('').map(Number);
    return new AlienDataTypeGenerator<T>(numStr, str.length > 0 ? true : false);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const numStr = data.slice(4).map((byte) => Math.random() > 0.5 ? (byte & 127) : 65); // Simple pseudo-random based on byte values, ensuring valid hex/number range for consistency with previous implementation's intent while keeping it self-contained
    return new AlienDataTypeGenerator<T>(numStr, true);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateBigIntFromBytes(bytes: Uint8Array): T {
    // Convert bytes to string representation (e.g., '1035A2') then parse as integer
    const numStr = new Intl.NumberFormat().format(...bytes); 
    return parseInt(numStr, 16) || BigInt(0n);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    // If the input is empty or null/undefined, default to a small base case if length > 1, else return BigInt(0) for safety on edge cases handled by crypto.randomBytes logic below (which assumes valid hex chars). 
    // However, per strict adherence to "without side effects", we should ensure robustness.
    const numStr = str ? new Intl.NumberFormat().format(str.length > 1 ? str : '2') : '0';
    
    return parseInt(numStr, 16) || BigInt(0n); // Handle potential non-hex digits in raw string input gracefully by falling back to a stable default if strict hex validation fails or is not available. In this specific context (crypto.randomBytes), we assume valid hex chars are provided but ensure the resulting number isn't negative unless explicitly forced, though crypto handles that via randomness.
    // Actually, looking at `generateFromString` in original: it returns T which is likely a generic type inference from previous logic or just an integer literal if not handled correctly by randomBytes on invalid input (which would crash). To be safe and "runnable", we ensure the result is always valid number-like.
    return parseInt(numStr, 16) || BigInt(0n); 
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const numStr = data.slice(4).map((byte) => Math.random() > 0.5 ? (byte & 127) : 65); // Simple pseudo-random based on byte values, ensuring valid hex/number range for consistency with previous implementation's intent while keeping it self-contained
    return new AlienDataTypeGenerator<T>(numStr, true);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateBigIntFromBytes(bytes: Uint8Array): T {
    // Convert bytes to string representation (e.g., '1035A2') then parse as integer
    const numStr = new Intl.NumberFormat().format(...bytes); 
    return parseInt(numStr
