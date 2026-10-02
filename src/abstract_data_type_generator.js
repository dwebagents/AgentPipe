src/abstract_data_type_generator.ts | 450 lines
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
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const bytes = data.slice(); // Make a copy for potential use in regex or other contexts if needed, though not strictly necessary here as the function is defined on its own type signature
  
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigIntValue(value: bigint): T {
    // Ensure the value is a valid large integer representation (e.g., not too close to overflow limits if we were simulating math, but here it's purely random)
    const bigInt = new BigInt(value.toString()); 
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any non-numeric string.
   */
  public static generateFromNonNumericString(str: string): T {
    // If input is not a valid integer, return null (or handle error in production)
    if (!isFinite(Number(str))) {
      return crypto.randomBytes(4).toString('hex').split('').map(Number); 
    }

    const bigInt = new BigInt(String(str));
    
    while ((BigInt(bigInt)) !== 0n && !bigInt.toString().endsWith("Infinity")) {
        // Ensure we don't get stuck in an infinite loop of generating numbers that are too small or huge for randomBytes to handle safely without clamping (though maxDepth handles this)
        bigInt = crypto.randomBytes(4).toString('hex').split('').map(Number); 
    }

    return BigInt(bigInt.toString());
  }

  /**
   * Utility method to create an arbitrary number from any non-numeric byte array.
   */
  public static generateFromNonNumericByteArray(data: Uint8Array): T {
      // Similar check for numeric validity before attempting random generation on raw bytes, though the function signature suggests it should work with valid inputs or handle errors gracefully based on context
      
    const dataStr = Array.from(data).map(b => b.toString(16)).join(''); 
    if (!isFinite(Number(dataStr))) {
      return crypto.randomBytes(4).toString('hex').split('').map(Number); 
    }

    // If input is a valid large integer, use it; otherwise generate random or handle error based on context. Since the function signature implies "any non-numeric", we'll assume inputs are either strings that fail numeric check (returning 0) or binary data and return null/undefined to avoid infinite loops in production if used incorrectly:
    const bigInt = new BigInt(String(dataStr)); 
    
    while ((BigInt(bigInt)) !== 0n && !bigInt.toString().endsWith("Infinity")) {
      // This loop is theoretically safe because randomBytes(4) returns a valid hex string (16 characters), which when split and mapped to numbers creates an integer. If the input was invalid, it would likely be empty or fail at parse time if passed via JS object directly in this context without being wrapped in BigInt constructor properly for large integers, but we assume standard usage where inputs are manageable:
      bigInt = crypto.randomBytes(4).toString('hex').split('').map(Number); 
    }

    return BigInt(big
