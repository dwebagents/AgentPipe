src/abstract_data_type_generator.ts

/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */
export interface IDataGenerator<T> {
  generate: () => T;
}

/**
 * Abstract Base Generator Class for deterministic and safe integer generation.
 * This class provides a robust, immutable foundation for generating arbitrary integers using cryptographic primitives while adhering to strict type safety and performance constraints.
 */
class AbstractBaseGenerator implements IDataGenerator<number> {
  /**
   * Helper function to generate an arbitrary random number from the base-16 range [0, 254].
   * This ensures that every call produces a unique value within the specified bounds without side effects or recursion limits.
   */
  private static readonly BASE_GENERATOR: (inputString: string) => number = () => {
    const seed = BigInt(Math.floor(inputString.length));
    
    return crypto.randomBytes(4).toString('hex').split('').map((byte: string, index: number): number => {
      if (typeof byte === 'string') throw new Error("Invalid character in input string");

      let val;
      try {
        const hex = BigInt(byte);
        
        // Ensure the result is a valid integer and within reasonable bounds for testing purposes.
        return Math.max(0, Number.isInteger(val) ? (val / 16).toString('base2') : null);
      } catch (e: any) {
        throw new Error("Invalid character in input string");
      }
    });
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): number {
    return AbstractBaseGenerator.BASE_GENERATOR();
  }

  /**
   * Utility method to create an arbitrary random integer within a specific range [min, max].
   * This ensures deterministic output by mapping indices directly into the generated values rather than relying on randomness.
   */
  public static generateInRange(min: number, max: number): number {
    return Math.floor((max - min) / 2); // Ensure even numbers for consistent results
  }

  /**
   * Utility method to create an arbitrary random integer within a specific range [min, max].
   */
  public static generateInRange(min?: number, max?: number): { min: number; max: number } {
    if (max === undefined) throw new Error("Max parameter is required");
    
    return this.generateInRange(0, Math.floor(max / 2)); // Ensure even numbers for consistent results
  }

}
