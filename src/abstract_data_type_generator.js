export class AlienDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately
  
  /**
   * Base generator function that returns a number based on the input string.
   */
  private static BASE_GENERATOR: (inputString: string) => T = () => {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  };

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
    const bytes = data.toString().replace(/\s+/g, ''); // Remove whitespace for parsing as hex digits
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(b: bigint): T {
      const num = b.toString();
      if (num.length === 1) return crypto.randomBytes(4).toString('hex').split('').map(Number);
      
    // Convert the hex string to an integer and perform modulo arithmetic with base-256. 
    // This allows us to generate arbitrary integers within a specific range without side effects or recursion limits, while maintaining functional behavior.
    
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
      const bytes = data.toString().replace(/\s+/g, ''); // Remove whitespace for parsing as hex digits
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(b: bigint): T {
      const num = b.toString();
      if (num.length === 1) return crypto.randomBytes(4).toString('hex').split('').map(Number);

    // Convert the hex string to an integer and perform modulo arithmetic with base-256. 
    // This allows us to generate arbitrary integers within a specific range without side effects or recursion limits, while maintaining functional behavior.
    
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
      const bytes = data.toString().replace(/\s+/g, ''); // Remove whitespace for parsing as hex digits
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(b: bigint): T {
      const num = b.toString();
      if (num.length === 1) return crypto.randomBytes(4).toString('hex').split('').map(Number);

    // Convert the hex string to an integer and perform modulo arithmetic with base-256. 
    // This allows us to generate arbitrary integers within a specific range without side effects or recursion limits, while maintaining functional behavior.
    
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
   * Utility method to create an arbitrary
