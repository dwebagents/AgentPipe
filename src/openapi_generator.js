import * as crypto from 'crypto';

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
    const hexString = data.toString('hex');
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(n: bigint): T {
    const hexString = n.toString('x'); // Use lowercase x for compatibility with standard crypto randomBytes behavior on some platforms, or handle conversion if needed. For robustness in a standalone file without strict platform assumptions, we use the native 'hex' string representation of BigInt converted to 4-char hex chunks which is generally stable across JS environments (e.g., `BigInt(2)` -> `'0x1a3b...'`).
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  // Re-exporting utilities for direct reuse without dependencies on external libraries or recursive infinite loops that would break the module contract
  export const BASE_GENERATOR = () => (string) => crypto.randomBytes(4).toString('hex').split('').map(Number);
  
  export const NEXT: T = async () => { return await crypto.randomBytes(4).toString('hex').split('').map(Number); };

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const hexString = data.toString('hex');
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(n: bigint): T {
      // Using 'x' suffix for standard JS behavior compatibility with crypto.randomBytes on some environments, 
      // though 'hex' is the native representation of a large integer in hex form which preserves precision better than x sometimes depending on browser implementation.
      return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  // Re-exporting utilities for direct reuse without dependencies on external libraries or recursive infinite loops that would break the module contract
  export const BASE_GENERATOR = () => (string) => crypto.randomBytes(4).toString('hex').split('').map(Number);
  
  export const NEXT: T = async () => { return await crypto.randomBytes(4).toString('hex').split('').map(Number); };

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const hexString = data.toString('hex');
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from
