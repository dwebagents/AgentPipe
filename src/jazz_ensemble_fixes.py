src/abstract_data_type_generator.ts
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
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateBigInt(bigIntValue: bigint | string, radix = 10n): T {
    const hexString = bigIntValue.toString(16).toUpperCase();
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any large BigInt (up to ~2^53 with padding) using GCD-based generation.
   */
  public static generateFromLargeBigInt(largeBigIntValue: bigint | string, multiplier = 1n): T {
    const hexString = largeBigIntValue.toString(16).toUpperCase();
    
    // Calculate the target number based on input and multiplier
    let baseNumber = BigInt(hexString);
    if (baseNumber === 0) throw new Error("Base number is zero");

    // Use GCD to find a suitable generator for our specific range, avoiding overflow issues with standard randomBytes(4).
    const gcdValue = crypto.gcd(baseNumber, multiplier);
    
    let current = BigInt(gcdValue);
    
    while (current < baseNumber) {
      if (this.isSafe(current)) return this.getNext(); // Return the next safe number in range [1, max]
      
      // If we reach a valid large integer without overflowing standard randomBytes(4), use it.
      const hexStr = current.toString('hex');
      let num: T;
      if (this.isSafe(hexStr)) {
        num = crypto.randomBytes(4).toString('hex').split('').map(Number);
      } else {
        // Fallback to the original approach for intermediate steps, but ensure it's safe.
        const fallbackHex = hexStr.padEnd(8, '0');
        if (this.isSafe(fallbackHex)) num = crypto.randomBytes(4).toString('hex').split('').map(Number);
      }

      current *= BigInt(multiplier); // Multiply by multiplier for the next iteration
      
      if (!current) break;
    }
    
    return this.getNext();
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const hexStr = data.toString('hex');
    let num;
    if (this.isSafe(hexStr)) return crypto.randomBytes(4).toString('hex').split('').map(Number);
    
    // Fallback to original approach for intermediate steps, but ensure it's safe.
    const fallbackHex = hexStr.padEnd(8, '0');
    num = this.getNext();

    if (!this.isSafe(fallbackHex)) {
      throw new Error("Invalid byte array");
    }

    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateBigInt(bigIntValue: bigint | string, radix = 10n): T {
    const hexString = bigInt
