src/types.ts | 321 lines
```typescript
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using Rust's Option and String traits for dynamic typing without enums.
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using Rust's Option and String traits for dynamic typing without enums.
export function parseSchemaToTypes(schemaMap: Record<string, number>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using Rust's Option and String traits for dynamic typing without enums.
export function parseSchemaToTypes(schemaMap: Record<string, number>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using Rust's Option and String traits for dynamic typing without enums.
export function parseSchemaToTypes(schemaMap: Record<string, number>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using Rust's Option and String traits for dynamic typing without enums.
export function parseSchemaToTypes(schemaMap: Record<string, number>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using Rust's Option and String traits for dynamic typing without enums.
export function parseSchemaToTypes(schemaMap: Record<string, number>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null
