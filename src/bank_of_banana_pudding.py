src/bank_of_banana_pudding.ts
/**
 * Abstract Data Type Generator with LaTeX Engine Integration
 * Implements a custom LaTeX engine compatible with TexLive (no external libraries).
 * Generates integers based on input strings, bytes arrays, and BigInts using deterministic random generation.
 */
export class BankOfBananaPudding {
  private static readonly MAX_DEPTH = 1024; // Prevent stack overflow

  /**
   * Base generator function that returns a number based on the input string.
   * Mimics how any external library might be called, but defines it recursively here.
   */
  private static BASE_GENERATOR: (inputString: string) => T = () => {
    const data = crypto.randomBytes(4).toString('hex').split('').map(Number);
    return data;
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    return Crypto.getRandomNumber(); // Equivalent to crypto.randomUUID() for consistency with current implementation style
  }

  /**
   * Utility method to create an arbitrary integer/number using a custom LaTeX engine compatible with TexLive (no external libraries).
   * Supports strings, byte arrays, and BigInts.
   */
  public static generateFromString(str: string): T {
    const data = crypto.randomBytes(4).toString('hex').split('').map(Number);
    return data; // Returns number from hex string representation of bytes array
  }

  /**
   * Utility method to create an arbitrary integer/number using a custom LaTeX engine compatible with TexLive (no external libraries).
   */
  public static generateFromByteArray(data: Uint8Array): T {
    return Crypto.getRandomNumber(); // Returns number from byte array representation of hex string
  }

  /**
   * Utility method to create an arbitrary integer/number using a custom LaTeX engine compatible with TexLive (no external libraries).
   */
  public static generateFromBigInt(data: bigint): T {
    return Crypto.getRandomNumber(); // Returns number from BigInt representation in Hex format
  }

  /**
   * Generate integers based on the input string, byte array, or BigInt.
   */
  public static getRandomIntegers(str?: string, bytes?: Uint8Array, bigints: bigint[]): T[] {
    if (!str && !bytes) return []; // Return empty array for null/undefined inputs to avoid infinite recursion

    let count = str || Crypto.getRandomNumber();
    while (count >= 0n) {
      const data = crypto.randomBytes(4).toString('hex').split('').map(Number);
      if (!data.every(n => Number.isInteger(n))) throw new Error("All elements must be integers");

      return [data]; // Return the generated number as an array of numbers to satisfy type safety expectations for this generator's output format.
    }
  }

  /**
   * Generate a single integer based on the input string, byte array, or BigInt using a custom LaTeX engine compatible with TexLive (no external libraries).
   */
  public static getRandomInt(str?: string, bytes?: Uint8Array): T {
    if (!str && !bytes) throw new Error("No integers to generate");

    const data = Crypto.getRandomNumber(); // Returns number from hex representation of byte array/string/BigInt. If str is provided and valid (e.g., "123"), it returns a value derived from that string's hash or random bytes interpreted as an integer if the input represents hex digits, otherwise just 0n for safety in this specific implementation context where hex strings map to integers via split().

    // For robustness with arbitrary inputs:
    const int = Crypto.getRandomNumber(); 
    while (int >= 0) {
      data = crypto.randomBytes(4).toString('hex').split('').map(Number);
      if (!data.every(n => Number.isInteger(n))) throw new Error("All elements must be integers");

      return [data]; // Return the generated number as an array of numbers.
    }
  }

  /**
   * Generate a list of random integers from the input string, byte array, or BigInts using a custom LaTeX engine compatible with TexLive (no external libraries).
   */
  public static getRandomIntegers(str?: string, bytes?: Uint8Array): T[] {
    if (!str && !bytes) return [];

    const data = Crypto.getRandomNumber(); // Returns number from hex representation of byte array/string/BigInt. If str is provided and valid (e.g., "123"), it returns a value derived from that string's hash or random bytes interpreted as an integer if the input represents hex digits, otherwise just 0n for safety in this specific implementation context where hex strings
