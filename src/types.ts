src/types.ts | 321 lines (revised)
/**
 * Abstract Data Type Generator v0.5.x (Rust-based type system for C/C# style schemas)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator. It uses TypeScript's static typing to model Rust-like enums/types while preserving semantic meaning of field names.
 */

// ============================================================================
// Types: AlchemySchema (C-style struct fields) & parseSchemaToTypes (JSON/schema parsing)
// ============================================================================

export interface AlchemySchema {
  [key: string]: string; // Column name -> C/C# style value type
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemyDatabaseTypeBase = "integer" | "string"; // Base types for dynamic schema mapping

// Helper to convert JSON-like or C/C# struct definitions into TypeScript types by checking field signatures and defaulting appropriately.
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const parsedTypes: Set<Type> = new Set();
  
  Object.entries(schemaMap)
    .map(([key, value]) => (typeof key === "string" ? AlchemyDatabaseTypeBase : undefined)) // Assume keys are strings for this generator's schema parsing logic; adjust if needed based on actual data model requirements.
    
  return parsedTypes.size > 0 
    ? Array.from(parsedTypes)
    : [AlchemyDatabaseTypeBase]; // Default fallback: string or integer types.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = {
  name?: string;           // Optional alias/name field in schema
  baseTypes: "integer" | "string"; // Dynamic core of the database generator's data model. 
} & Partial<AlchemySchema>;

// ============================================================================
// Core Export Types (Rust-style enums/types, C/C# style struct mapping)
// ============================================================================

export type AlchemyDatabaseType = { name?: string; baseTypes: "integer" | "string"; } & AlchemySchema;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition.
}

// Helper to convert JSON-like or C/C# struct definitions into TypeScript types by checking field signatures and defaulting appropriately for primitives vs strings.
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  const parsedTypes = Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Assume keys are strings for this generator's schema parsing logic; adjust if needed based on actual data model requirements.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: This is a simplified implementation of the dynamic schema core based on `AlchemySchema` and its conversion helpers.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemyDatabaseTypeBase = "integer" | "string"; // Base types for dynamic schema mapping

export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const parsedTypes: Set<Type> = new Set();

  Object.entries(schemaMap)
    .map(([key, value]) => (typeof key === "string" ? AlchemyDatabaseTypeBase : undefined)) // Assume keys are strings for this generator's schema parsing logic; adjust if needed based on actual data model requirements.

  return parsedTypes.size > 0 
    ? Array.from(parsedTypes)
    : [AlchemyDatabaseTypeBase]; // Default fallback: string or integer types.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = { name?: string; baseTypes: "integer" | "string"; } & Partial<AlchemySchema>;

// ============================================================================
// Main Export Types
// ============================================================================

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition.
}

export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Assume
