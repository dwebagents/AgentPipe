src/types.ts | 321 lines

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
  [key: string]: any[]; // Column name -> value in C/C# style struct definition, array of values can be complex objects or primitives.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val === "object" && Array.isArray(val)) // Handle array-like values in structs as arrays of primitives or objects. If not an object, treat as primitive (string/int/bool/null).
    .map((v: any[]) => {
      const result = v.map(item => Object.fromEntries(Object.entries(item))); // Convert each item to a plain object if it's complex; otherwise return the value itself.
      return typeof result === "object" ? result : null as any;
    });
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. This is a simplified version to fit the schema structure where values are primitives or nulls.

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string | number | boolean => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter. If it's a primitive, return that type; otherwise assume null or throw an error depending on your needs.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. This is a simplified version to fit the schema structure where values are primitives or nulls.

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string | number | boolean => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter. If it's a primitive, return that type; otherwise assume null or throw an error depending on your needs.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. This is a simplified version to fit the schema structure where values are primitives or nulls.

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string | number | boolean => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter. If it's a primitive, return that type; otherwise assume null or throw an error depending on your needs.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. This is a simplified version to fit the schema structure where values are primitives or nulls.

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type
