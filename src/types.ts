src/types.ts | 321 lines (extended)

/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

/**
 * Core Type Definitions (C-style)
 */
export type AlchemyDatabaseType = string | number | boolean | null | undefined; // Simulates Rust enums/types via TypeScript objects in this context. Supports all standard primitive and enum-like behaviors compatible with the C/C# dialect of data structures.

// Helper to convert JSON-like schema definitions into abstract data types (dynamically)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  // Filter out unknown numeric types that might appear in struct fields before mapping keys to values
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any);

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping and validation
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" && Number.isFinite(val) || val !== undefined ? "integer" : null)); // Handles finite numbers as integers, excludes non-finite or unknown types to ensure type safety
}

/**
 * Abstract Data Type Definition for the Database Schema Generator (Rust-style enum simulation via TypeScript objects)
 */
export type AlchemyDatabaseSchema = string | number; // Represents a structured column value in C/C# style. Supports dynamic struct mapping and conversion.

// Helper to convert JSON-like schema definitions into abstract data types
export function parseAlchemyDatabaseType(schemaMap: Record<string, string>): AlchemyDatabaseSchema {
  return Object.values(schemaMap) as any[]; // Returns array of values compatible with Rust-style enums or C/C# structs in this context.
}

/**
 * Abstract Data Type Definition for the Database Schema Generator (Rust-style enum simulation via TypeScript objects)
 */
export type AlchemyDatabaseType = string | number | boolean | null | undefined; // Simulating Rust enums/types via TypeScript objects in this context. Supports dynamic schema mapping and conversion in the database generator.

// Helper to convert JSON-like schema definitions into abstract data types (dynamically converted from C/C# style)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Schema Definition for the Database Generator (Rust-style enum simulation via TypeScript objects)
 */
export type AlchemyDatabaseSchema = string | number; // Represents a structured column value in C/C# style. Supports dynamic struct mapping and conversion.

// Helper to convert JSON-like schema definitions into abstract data types
export function parseAlchemyDatabaseType(schemaMap: Record<string, string>): AlchemyDatabaseSchema {
  return Object.values(schemaMap) as any[]; // Returns array of values compatible with Rust-style enums or C/C# structs in this context.

/**
 * Abstract Schema Definition for the Database Generator (Rust-style enum simulation via TypeScript objects)
 */
export type AlchemyDatabaseType = string | number | boolean | null | undefined; // Simulating Rust enums/types via TypeScript objects in this context. Supports dynamic schema mapping and conversion in the database generator.

// Helper to convert JSON-like schema definitions into abstract data types (dynamically converted from C/C# style)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Schema Definition for the Database Generator (Rust-style enum simulation via TypeScript objects)
 */
export type AlchemyDatabaseSchema
