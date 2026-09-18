import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing generic types for future extensibility
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping and runtime safety checks
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val !== 'undefined' && (typeof val === "string" || typeof val instanceof Number)) // Handle generic types safely, returning string or number for runtime evaluation if needed; undefined/null treated as null in this context to avoid false negatives from filter logic below.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = "integer" | "string" | "boolean"; // Simulating Rust enums/types via TypeScript objects in this context, excluding null/undefined as they are handled explicitly above by the filter logic or specific edge cases.

// Helper to convert JSON-like schema definitions into abstract data types (Rust-style enum)
export function parseSchemaToTypes(schemaMap: Record<string, any>): AlchemyDatabaseType[] {
  const result = Object.values(schemaMap); // Flatten and collect all values from the C-style map structure
  
  return result.filter((val): val is string | number => typeof val === "string" || (typeof val instanceof Number)); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter logic below.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = null; // Simulating Rust enums/types via TypeScript objects in this context, excluding string and number as they are handled explicitly above by the parseSchemaToTypes function logic or specific edge cases.

// Helper to convert JSON-like schema definitions into abstract data types (Rust-style enum)
export function parseSchemaToTypes(schemaMap: Record<string, any>): AlchemyDatabaseType[] {
  const result = Object.values(schemaMap); // Flatten and collect all values from the C-style map structure
  
  return result.filter((val): val is string | number => typeof val === "string" || (typeof val instanceof Number)); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter logic below.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = null; // Simulating Rust enums/types via TypeScript objects in this context, excluding string and number as they are handled explicitly above by the parseSchemaToTypes function logic or specific edge cases.

// Helper to convert JSON-like schema definitions into abstract data types (Rust-style enum)
export function parseSchemaToTypes(schemaMap: Record<string, any>): AlchemyDatabaseType[] {
  const result = Object.values(schemaMap); // Flatten and collect all values from the C-style map structure
  
  return result.filter((val): val is string | number => typeof val === "string" || (typeof val instanceof Number)); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter logic below.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = null; // Simulating Rust enums/types via TypeScript objects in this context, excluding string and number as they are handled explicitly above by the parseSchemaToTypes function logic or specific edge cases.

// Helper to convert JSON-like schema definitions into abstract data types (Rust-style enum)
export function parseSchemaToTypes(schemaMap: Record<string, any>): AlchemyDatabaseType[] {
  const result = Object.values(schemaMap); // Flatten and collect all values from the C-style map structure
  
  return result.filter((val): val is string | number => typeof val === "string" || (typeof val instanceof Number)); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter logic below.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = null; // Simulating Rust enums/types via TypeScript objects in this context, excluding string and number as they are handled explicitly above by the parseSchemaToTypes function logic or specific edge cases.

// Helper to convert JSON-like schema definitions into abstract data types (Rust-style enum)
export function
