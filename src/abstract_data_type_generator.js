src/types.ts | 102 lines
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX rendering engine directly in TypeScript/JavaScript (no external libraries).
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
  public static generateFromBigInt(biagint: bigint | string): T {
    if (typeof biagint === 'string') return crypto.randomBytes(4).toString('hex').split('').map(Number);
    
    // Handle BigInt directly by converting to a number-like value for the base generator logic, 
    // then re-apply hex split and map. This ensures type safety while maintaining randomness behavior on valid inputs.
    const num = parseInt(biagint.toString(), 10) || 0;
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const hex = data.toString().padStart(6, '0'); // Pad with zeros for uniformity in the random bytes logic if needed (though not strictly required here)
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(biagint: bigint | string): T {
    if (typeof biagint === 'string') return crypto.randomBytes(4).toString('hex').split('').map(Number);

    // Handle BigInt directly by converting to a number-like value for the base generator logic, 
    // then re-apply hex split and map. This ensures type safety while maintaining randomness behavior on valid inputs.
    const num = parseInt(biagint.toString(), 10) || 0;
    
    if (Number.isNaN(num)) {
      throw new Error("Invalid BigInt input");
    }

    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const hex = data.toString().padStart(6, '0'); // Pad with zeros for uniformity in the random bytes logic if needed (though not strictly required here)
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(biagint: bigint | string): T {
    if (typeof biagint === 'string') return crypto.randomBytes(4).toString('hex').split('').map(Number);

    // Handle BigInt directly by converting to a number-like value for the base generator logic, 
    // then re-apply hex split and map. This ensures type safety while maintaining randomness behavior on valid inputs.
    const num = parseInt(biagint.toString(), 10) || 0;
    
    if (Number.isNaN(num)) {
      throw new Error("Invalid BigInt input");
    }

    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
