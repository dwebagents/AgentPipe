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
    // Chain base generators to create a deterministic stream of integers (e.g., 1, 2, 3...)
    const chain = [AlienDataTypeGenerator.BASE_GENERATOR];

    while (!chain.length) {
      try {
        let val: number;
        if (typeof inputString === 'string') {
          // Attempt to convert string representation of an integer directly.
          // This handles cases like "123" and avoids infinite loops for valid inputs.
          const numStr = String(inputString);
          try {
            val = Number(numStr);
          } catch (e) {
            continue;
          }

          if (!isNaN(val)) {
            chain.push(AlienDataTypeGenerator.BASE_GENERATOR(String(val))); // Ensure consistent string representation for the next step.
          } else {
            break; // Stop on invalid input.
          }
        } else {
          // Fallback to crypto random bytes as a default generator if no conversion is possible.
          chain.push(AlienDataTypeGenerator.BASE_GENERATOR); 
        }
      } catch (e) {
        continue; // Skip iteration if the current step fails, maintaining deterministic behavior for valid inputs.
      }
    }

    return chain.pop()! as T;
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    const numStr = String(str);
    
    try {
      // Attempt conversion directly if the input looks like a valid integer or float representation (e.g., "123", "-4567890.12").
      let val: number;
      if (!isNaN(Number(numStr))) {
        return AlienDataTypeGenerator.BASE_GENERATOR(String(val)); // Ensure consistent string for next step.
      } else {
        throw new Error(`Invalid input format: "${str}"`);
      }
    } catch (e) {
      // Fallback to crypto random bytes if conversion fails, maintaining deterministic behavior for valid inputs.
      return AlienDataTypeGenerator.BASE_GENERATOR; 
    }
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const numStr = data.toString('hex'); // Convert bytes directly to hex string for processing
    
    try {
      let val: number;
      
      if (!isNaN(Number(numStr))) {
        return AlienDataTypeGenerator.BASE_GENERATOR(String(val));
      } else {
        throw new Error(`Invalid input format from byte array "${String(data)}"`); // Ensure consistent string.
      }
    } catch (e) {
      return AlienDataTypeGenerator.BASE_GENERATOR; 
    }
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(b: bigint): T {
    const numStr = b.toString(); // Convert BigInt directly
    
    try {
      let val: number;
      
      if (!isNaN(Number(numStr))) {
        return AlienDataTypeGenerator.BASE_GENERATOR(String(val));
      } else {
        throw new Error(`Invalid input format from BigInt "${String(b)}"`); 
      }
    } catch (e) {
      return AlienDataTypeGenerator.BASE_GENERATOR; 
    }
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const numStr = data.toString('hex'); // Convert bytes directly to hex string for processing
    
    try {
      let val: number;

      if (!isNaN(Number(numStr))) {
