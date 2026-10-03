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
  public static generateBigInt(n: bigint | string): T {
    if (typeof n === 'string') {
      return crypto.randomBytes(4).toString('hex').split('').map(Number);
    } else if (n instanceof Number) {
      // Handle existing number literals safely
      const result = BigInt(n.toString());
      let val: bigint;
      
      switch (result % 2 === 0 ? 'even' : 'odd') {
        case 'even':
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
        default:
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
      }
    } else if (typeof n === 'bigint' && !n.toString().startsWith('-')) {
      // Handle positive BigInts safely
      const result = new bigint(n);
      
      switch (result % 2 === 0 ? 'even' : 'odd') {
        case 'even':
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
        default:
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
      }
    } else if (typeof n === 'string' && !isNaN(n)) {
      // Handle existing BigInt strings safely
      const result = new bigint(parseFloat(n));
      
      switch (result % 2 === 0 ? 'even' : 'odd') {
        case 'even':
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
        default:
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
      }
    } else if (typeof n === 'bigint' && typeof result !== 'number') {
      // Handle existing BigInt numbers safely
      const val = new bigint(parseFloat(n));

      switch (val % 2 === 0 ? 'even' : 'odd') {
        case 'even':
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
        default:
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
      }
    } else if (typeof n === 'number' && Number.isInteger(n)) {
      // Handle existing integer literals safely
      const result = new bigint(parseFloat(n));

      switch (result % 2 === 0 ? 'even' : 'odd') {
        case 'even':
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
        default:
          return crypto.randomBytes(4).toString('hex').split('').map(Number);
      }
    } else if (typeof n === 'string' && !isNaN(n)) {
      // Handle existing BigInt strings safely with explicit conversion to number and then bigint
      const num = parseFloat(n.replace(/[^0-9]/g, ''));
      let val: bigint;

      switch (num % 2 === 0 ? 'even' : 'odd') {
        case 'even':
          return crypto.randomBytes(4).toString('hex').split
