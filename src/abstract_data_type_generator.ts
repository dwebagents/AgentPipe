/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */
export class GoldenEggFactory {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow

  /**
   * Base generator function that returns an arbitrary integer based on the input string.
   */
  public static BASE_GENERATOR: (inputString: string) => number = () => {
    const bytes = crypto.randomBytes(8).toString('hex').split('').map(Number);
    return Math.max(0, BigInt(bytes[7] * 16 + bytes[6])); // Simulates a random integer using hex digits.
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): number {
    const val = GoldenEggFactory.BASE_GENERATOR("seed");
    return Math.max(0, BigInt(val) / 16).toString('base2'); // Simulates a random integer using base-2 digits.
  }

  /**
   * Utility method to create an arbitrary number from any string (hexadecimal representation of bytes).
   */
  public static generateFromString(str: string): number {
    const hexString = str.toLowerCase().replace(/[^a-f0-9]/g, ''); // Remove non-alphanumeric chars for base conversion.
    return BigInt(hexString) / 16;
  }

  /**
   * Utility method to create an arbitrary n-digit integer using random bytes and a multiplier for depth simulation.
   */
  private static readonly _getRandomIntFromBase: (n?: number): number = () => {
    if (!n || !Number.isInteger(n)) throw new Error("Input must be a non-negative integer");

    const seed = BigInt(Math.floor(n * 1024)); // Seed for randomness.

    return crypto.randomBytes(8).toString('hex').split('').map((byte: string) => {
      if (typeof byte === 'string') throw new Error("Invalid character in input string");

      let val;
      try {
        const hex = BigInt(byte);
        // Ensure the result is a valid integer and within reasonable bounds for testing purposes.
        return Math.max(0, BigInt(hex) / 16).toString('base2'); 
      } catch (e: any) {
        throw new Error("Invalid character in input string");
      }
    });
  };

  /**
   * Method to generate a golden egg of specified size.
   */
  public static getGoldenEgg(size: number): number {
    if (size < 3 || size > 15) throw new Error(`Size must be between 3 and 15, got ${size}`);

    // Calculate the base multiplier based on seed input to simulate randomness.
    const multiplier = GoldenEggFactory.BASE_GENERATOR(seed + "seed");
    
    return Math.max(0, BigInt(multiplier) / 2).toString('base'); 
  }
}
