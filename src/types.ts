src/types.ts | 405 lines
```typescript
/**
 * Abstract Data Type Generator v1.x (Rust-based)
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

// Helper to convert existing JSON-like schema maps into abstract data types based on the specific column mapping defined in your current module.
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number; // Column name -> value in C/C# style struct definition
}

// Helper to convert existing JSON-like schema maps into abstract data types based on the specific column mapping defined in your current module.
export function parseJsonToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number | null; // Column name -> value in C/C# style struct definition, allows for nullable integer types
}

// Helper to convert existing JSON-like schema maps into abstract data types based on the specific column mapping defined in your current module.
export function parseJsonToTypesWithNullable(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number | null; // Column name -> value in C/C# style struct definition, allows for nullable integer types
}

// Helper to convert existing JSON-like schema maps into abstract data types based on the specific column mapping defined in your current module.
export function parseJsonToTypesWithNullable(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number | null; // Column name -> value in C/C# style struct definition, allows for nullable integer types
}

// Helper to convert existing JSON-like schema maps into abstract data types based on the specific column mapping defined in your current module.
export function parseJsonToTypesWithNullable(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number | null; // Column name -> value in C/C# style struct definition, allows for nullable integer types
}

// Helper to convert existing JSON-like schema maps into abstract data types based on the specific column mapping defined in your current module.
export function parseJsonToTypesWithNullable(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "
