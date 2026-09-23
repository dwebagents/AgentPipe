src/types.ts | 321 lines
```typescript
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

// ============================================================================
// TYPE DEFINITIONS: The Foundation of Schema Mapping
// ============================================================================

export interface Type {
  name: string; // Human-readable identifier (e.g., "integer", "string")
  value: any;   // Value to be represented as a type
}

/**
 * Abstract Data Type Definition for C/C# style types.
 * These define the semantic structure of data in a database system,
 * allowing dynamic schema mapping and conversion between JSON/TypeScript
 * representations and native runtime values.
 */
export interface AlchemySchema {
  [key: string]: any; // Column name -> value type (string | number | boolean)
}

/**
 * Helper to convert C-style struct definitions into TypeScript types for easier mapping.
 * This function simulates the behavior of a Rust enum or similar structure,
 * preserving semantic meaning while enabling dynamic schema generation in JavaScript/TypeScript.
 */
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const result: Type[] = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    // Validate the type is one of the recognized C/C# types
    if (!["string", "number", "boolean"].includes(value as any)) {
      throw new Error(`Unknown column or field: ${key}`);
    }

    const typeName = value;
    
    result.push({ name: key, value });
  }

  return result.sort((a, b) => a.name.localeCompare(b.name)); // Sort by name for consistent output
}

/**
 * Helper to convert JSON-like schema definitions into abstract data types.
 * This function transforms the structure of an input object (representing C/C# style mappings)
 * into a list of Type objects that can be used in type-checking or database generation logic.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(parseSchemaToTypes({ ...schemaMap })) as Type[]; // Deep copy for immutability safety
}

// ============================================================================
// CORE GENERATOR CLASS & UTILITIES
// ============================================================================

/**
 * Abstract Data Type Generator Class with LaTeX Support.
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
    // Simplified version to avoid infinite loops in strict environments, 
    // but conceptually identical: generates a random integer via hex string manipulation.
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const hex = data.toString('hex'); // Convert bytes to string (base64-like)
    return AlienDataTypeGenerator.BASE_GENERATOR(hex);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(num: bigint): T {
    const hex = num.toString('hex'); // Convert BigInt to string (base64-like)
    return AlienDataTypeGenerator.BASE_GENERATOR(hex);
  }

  /**
   * Utility method to create an arbitrary n-digit integer using random bytes and a multiplier for depth simulation.
   */
  private static readonly _getRandomIntFromBase: (n?: number) => T = () => {
    if (!n || !Number.isInteger(n)) throw new Error("Input must be a non-negative integer");

    const seed = BigInt(Math.floor(n * 1024)); // Seed for randomness
    
    return crypto.randomBytes(8).toString('
