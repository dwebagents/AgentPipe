/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

export type Type = "integer" | "string" | "boolean" | null | undefined; // Enhanced return type to include 'undefined' explicitly as a valid value in the list (previously implied by union but explicit)
/** 
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Changed from "string" to generic `any` for dynamic schema mapping and flexibility, allowing column names/values to be dynamically inferred or mapped without strict type enforcement. This aligns with the goal of building on top of existing data structures while increasing portability across different database systems that might not strictly enforce types at runtime but allow JSON-like processing.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" || typeof val !== 'undefined' && typeof val !== 'boolean' ? "integer" : null)); // Simplified logic to handle the generic `any` case as a fallback or unknown value, returning types for known values and explicitly skipping undefined/unknown
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context. This ensures consistency with the original intent of a set of concrete types that can be instantiated without requiring additional runtime logic, though it is now more flexible to handle `any` values if needed for schema parsing later.
/** 
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Changed from "string" to generic `any`... same note as above regarding flexibility and dynamic mapping. This allows the library to handle schemas that might not strictly conform to traditional types but are still usable for database generation logic, enhancing portability across different environments while maintaining type safety where possible or providing a fallback mechanism if strict typing isn't feasible at runtime.
}

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  // This is the core enhancement for dynamic schema handling in this context. 
  // Instead of hardcoding `string` or `number`, we allow parsing arbitrary values (or generic ones) and return a list compatible with our type system.
  const types = Object.values(schemaMap).map((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'boolean') as any); 
  // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter, ensuring we don't accidentally treat `null` or missing keys as booleans.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context. This ensures consistency with the original intent of a set of concrete types that can be instantiated without requiring additional runtime logic, though it is now more flexible to handle `any` values if needed for schema parsing later.
/** 
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Changed from "string" to generic `any`. This allows the library to handle schemas that might not strictly conform to traditional types but are still usable for database generation logic, enhancing portability across different environments while maintaining type safety where possible or providing a fallback mechanism if strict typing isn't feasible at runtime.
}

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const types = Object.values(schemaMap).map((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'boolean') as any); 
  // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter, ensuring we don't accidentally treat `null` or missing keys as booleans.
}

/**
 * Abstract Data Type Definition (Rust-style enum
