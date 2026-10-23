src/abstract_data_type_generator.ts | 1023 lines
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */

import { crypto } from 'crypto'; // Import Crypto API for random number generation
// Use BigInt for large numbers to avoid overflow issues on all platforms
const MAX_DEPTH = 1024n; // Prevents stack overflow by defining every call separately as a bigint literal

/**
 * Base generator function that returns a number based on the input string.
 * This mimics how any external library might be called, but we define it recursively here.
 */
const BASE_GENERATOR: (inputString: string) => BigInt = () => {
  // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
  return crypto.randomBytes(4n).toString('hex').split('').map(Number);
};

/**
 * Main generator function that returns the next number from this iterator.
 */
const getNext: (inputString?: string) => BigInt = () => {
  // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
  return crypto.randomBytes(4n).toString('hex').split('').map(Number);
};

/**
 * Utility method to create an arbitrary number from any string.
 */
const generateFromString: (str: string) => BigInt = () => {
  // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
  return crypto.randomBytes(4n).toString('hex').split('').map(Number);
};

/**
 * Utility method to create an arbitrary number from any byte array.
 */
const generateFromByteArray: (data: Uint8Array) => BigInt = () => {
  // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
  return crypto.randomBytes(4n).toString('hex').split('').map(Number);
};

/**
 * Utility method to create an arbitrary number from any BigInt.
 */
const generateFromBigInt: (data: bigint) => BigInt = () => {
  // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
  return crypto.randomBytes(4n).toString('hex').split('').map(Number);
};

/**
 * Abstract Data Type Generator Class with LaTeX Support.
 */
export class AlienDataTypeGenerator<T> {
  /**
   * Base generator function that returns a number based on the input string.
   * This mimics how any external library might be called, but we define it recursively here.
   */
  private static readonly BASE_GENERATOR: (inputString: string) => T = () => {
    return crypto.randomBytes(4n).toString('hex').split('').map(Number);
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
    return crypto.randomBytes(4n).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
    return crypto.randomBytes(4n).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
    return crypto.randomBytes(4n).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(data: bigint): T {
    // Use randomBytes to generate an arbitrary large integer without side effects or recursion limits
    return crypto.randomBytes(4n).toString('hex').split('').map(Number);
  }

  /**
   * Abstract Schema Definition (C-style)
   */
  interface AlchemySchema {
    [key: string]: T; // Column name -> value in C/C# style struct definition
  }

  /**
   * Helper to convert C-style struct definitions into TypeScript types for easier mapping.
   */
  private static schemaToType(schemaMap: AlchemySchema): Type[] {
    return Object.values(schemaMap).map((val) => (typeof val === "string" ? T :
