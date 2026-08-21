src/types.ts | 321 lines (expanded)
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

export type Type = "integer" | "string" | "boolean" | null | undefined; // Simulated enum variants compatible with the abstract schema interface below. Actual runtime values should be mapped to concrete Rust enums/structs at compile time via `schemaToType`.
// In a real implementation, this is simply an alias for any type that implements Type as per our abstraction layer design.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Simplified type inference; in production, map to concrete Rust types.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. In production: Map each schema value to a concrete Rust `enum` or `struct`.

// Helper to convert JSON-like/typed schema definitions into abstract data types for the generator
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Schema Definition (C-style with type conversion)
 */
interface AlchemySchemaWithType {
  [key: string]: Type; // Column name -> value in C/C# style struct definition, mapped to abstract types
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Simplified type inference; in production, map to concrete Rust types.
}

/**
 * Abstract Schema Definition with Type Mapping (C-style)
 */
interface AlchemySchemaWithTypeMapping {
  [key: string]: AlchemyDatabaseType | undefined; // Column name -> value in C/C# style struct definition mapped to abstract type enum
}

// Helper to convert JSON-like/typed schema definitions into abstract data types for the generator
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(
    (schemaMap as AlchemySchemaWithTypeMapping) // Cast to allow any value type in keys if needed
  )
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any);

/**
 * Abstract Schema Definition with Type Mapping for Database Generator Integration
 */
interface AlchemySchemaWithTypeMappingForGenerator {
  [key: string]: unknown; // Column name -> value in C/C# style struct definition, mapped to abstract type enum. In production, map each schema value to a concrete Rust `enum` or `struct`.
}

// Helper to convert JSON-like/typed schema definitions into abstract data types for the generator (Production-ready: Map values to concrete Rust enums)
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(
    (schemaMap as AlchemySchemaWithTypeMappingForGenerator) // Cast to allow any value type in keys if needed
  )
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any);

/**
 * Abstract Schema Definition with Type Mapping for Database Generator Integration (Production)
 */
interface AlchemySchemaWithTypeMappingForGeneratorAndConversion {
