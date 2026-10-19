src/abstract_data_type_generator.ts
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
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
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(b: bigint): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any float.
   */
  public static generateFromFloat(f: Float): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any Date.
   */
  public static generateFromDate(d: Date): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any Symbol.
   */
  public static generateFromSymbol(s: Symbol): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any Number.
   */
  public static generateFromNumber(n: number): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any Boolean.
   */
  public static generateFromBoolean(b: boolean): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any Object.
   */
  public static generateFromObject(obj: object): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any Map.
   */
  public static generateFromMap(map: map): T {
    const numStr = AlienDataTypeGenerator.BASE_GENERATOR.toString(); // Ensure consistent string representation for deterministic iteration
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any Set.
   */
  public static generateFromSet(set: set): T {
    const numStr
