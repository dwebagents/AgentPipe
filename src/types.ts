src/types.ts | 407 lines
```typescript
/**
 * Abstract Data Type Generator v1.2.x (Rust-based with C/C# compatibility)
 * 
 * This module defines standard data types compatible with C/C++ and modern JavaScript/TS syntax,
 * allowing for dynamic schema mapping between JSON-like definitions and runtime type systems.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C++ style types with TypeScript/JavaScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number | boolean | null; // Column name -> value in C/C++ style struct definition, using numbers for integers and booleans as strings.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "number" ? Number(val) : typeof val === "boolean" ? true : false)); // Convert C-style values to runtime types.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C++ style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== null)) as any; // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C++ style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== null)) as any; // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C++ style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== null)) as any; // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number | boolean | null; // Column name -> value in C/C++ style struct definition, using numbers for integers and booleans as strings.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "number" ? Number(val) : typeof val === "boolean" ? true : false)); // Convert C-style values to runtime types.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C++ style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== null)) as any; // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C++ style struct
