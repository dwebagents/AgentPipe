src/abstract_data_type_generator.ts | 120 lines
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
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

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Schema Definition for JSON-like structures
 */
interface AlchemySchemaJSON {
  [key: string]: number | "integer" | null;
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(JSONMap: AlchemySchemaJSON): Type[] {
  return Object.values(JSONMap).map((val) => (typeof val === "number" ? "string" : typeof val === "integer" ? "boolean" : null)); // Note: 'integer' is the key type in JSON, but we want C-style string/number mapping. Adjust logic if needed for strictness.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = "string" | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(JSONMap: Record<string, any>): Type[] {
  return Object.values(JSONMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Data Type Definition for JSON-like structures
 */
export type AlchemyDatabaseTypeJSON = number | string; // Simplified version of the above, assuming generic types are available or handled by specific parsers. For strict C/C# compatibility: `string` and `number`.

// Helper to convert JSON-like schema definitions into abstract data types
function parseSchemaToTypes(JSONMap: Record<string, any>): Type[] {
  return Object.values(JSONMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Abstract Schema Definition for JSON-like structures
 */
interface AlchemySchemaJSON {
  [key: string]: number | "integer" | null;
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(JSONMap: AlchemySchemaJSON): Type[] {
  return Object.values(JSONMap).map((val) => (typeof val === "number" ? "string" : typeof val === "integer" ? "boolean" : null)); // Note: 'integer' is the key type in JSON, but we want C-style string/number mapping. Adjust logic if needed for strictness.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = "string" | number | boolean | null; // Simulating Rust enums/types
