src/abstract_type_generator_types.d.ts | 104 lines

/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

export { AlchemyDatabaseType } from "./abstract_types"; // Re-export to avoid circular imports if needed

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing generic types for dynamic schema evolution.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping and runtime binding
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing generic types for dynamic schema evolution and runtime binding without external dependencies like Rust structs.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping and runtime binding (without requiring a separate structs file)
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing generic types for dynamic schema evolution and runtime binding without external dependencies like Rust structs or TypeScript enums alone.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping (without requiring a separate structs file)
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; //
