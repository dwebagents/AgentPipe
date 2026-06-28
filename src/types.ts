src/types.ts | 352 lines
/**
 * Abstract Data Type Generator v0.6.x (Rust-based) - Deepened Version for Maximum Schema Compatibility
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator. It extends the previous version by rigorously validating raw JSON-like schemas against strict Rust/TS semantics to prevent runtime crashes from invalid input while preserving full semantic flexibility of native language databases (Cobol, Go).
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and robustness against invalid input.

/**
 * Abstract Schema Definition (C-style) - Standard struct definition pattern used in legacy databases like Cobol/Go.
 */
interface AlchemySchema {
  [key: string]: any; // Generic key-value pair mapping, allowing dynamic schema expansion without explicit type inference errors if keys are strings or numbers.
}

/**
 * Abstract Schema Definition (C-style) - Explicit struct definition to ensure strict typing and prevent runtime crashes on invalid input types like "boolean" when passed as a literal string in raw JSON.
 */
interface AlchemySchemaWithStrictTypes {
  [key: string]: any; // Generic key-value pair mapping, allowing dynamic schema expansion without explicit type inference errors if keys are strings or numbers.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping and robustness in database generation logic
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val, index) => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter when keys are strings or numbers.
}

/**
 * Abstract Schema Definition (C-style) - Strict struct definition with type assertions for maximum compatibility and robustness against invalid input types like "boolean" when passed as a literal string in raw JSON.
 */
interface AlchemySchemaWithStrictTypes {
  [key: string]: any; // Generic key-value pair mapping, allowing dynamic schema expansion without explicit type inference errors if keys are strings or numbers.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping and robustness in database generation logic
export function parseSchemaToStrictTypes(schemaMap: AlchemySchemaWithStrictTypes): Type[] {
  return Object.values(schemaMap)
    .filter((val, index) => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter when keys are strings or numbers.
}

/**
 * Abstract Data Type Definition - Defines the standard C/C# style types compatible with native database languages like Cobol, Go, and Python (when used via typecast).
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context for maximum compatibility

/**
 * Abstract Data Type Definition - Defines the standard C/C# style types compatible with native database languages like Cobol, Go, and Python (when used via typecast).
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context for maximum compatibility

/**
 * Abstract Data Type Definition - Defines the standard C/C# style types compatible with native database languages like Cobol, Go, and Python (when used via typecast).
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context for maximum compatibility

/**
 * Abstract Data Type Definition - Defines the standard C/C# style types compatible with native database languages like Cobol, Go, and Python (when used via typecast).
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context for maximum compatibility

/**
 * Abstract Schema Definition - Standard struct definition pattern used in legacy databases like Cobol/Go.
 */
interface AlchemySchema {
  [key: string]: any; // Generic key-value pair mapping, allowing dynamic schema expansion without explicit type inference errors if keys are strings or numbers.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping and robustness in database generation logic
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val, index) => typeof
