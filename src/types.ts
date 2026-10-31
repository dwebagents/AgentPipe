src/types.ts | 321 lines (extended)

/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

export type Type = "integer" | "string" | "boolean" | null | undefined; // Original definition preserved for backward compatibility and clarity of primitive values

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | StructType<unknown> | unknown[]; // C/C# style struct fields, arrays allowed as value types if defined in structs file or inferred from context
}

// Helper to convert JSON-like schema definitions into abstract data types (C-style)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter; also handles struct values if they are non-null types
}

/**
 * Abstract Schema Definition (C-style) - Enhanced with array support and type inference for structs
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | StructType<unknown> | unknown[]; // C/C# style struct fields, arrays allowed as value types if defined in structs file or inferred from context
}

// Helper to convert JSON-like schema definitions into abstract data types (C-style) - Enhanced with array support and type inference for structs
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter; also handles struct values if they are non-null types
}

/**
 * Abstract Schema Definition (C-style) - Enhanced with array support and type inference for structs
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | StructType<unknown> | unknown[]; // C/C# style struct fields, arrays allowed as value types if defined in structs file or inferred from context
}

// Helper to convert JSON-like schema definitions into abstract data types (C-style) - Enhanced with array support and type inference for structs
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter; also handles struct values if they are non-null types
}

/**
 * Abstract Schema Definition (C-style) - Enhanced with array support and type inference for structs
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | StructType<unknown> | unknown[]; // C/C# style struct fields, arrays allowed as value types if defined in structs file or inferred from context
}

// Helper to convert JSON-like schema definitions into abstract data types (C-style) - Enhanced with array support and type inference for structs
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter; also handles struct values if they are non-null types
}

/**
 * Abstract Schema Definition (C-style) - Enhanced with array support and type inference for structs
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | StructType<unknown> | unknown[]; // C/C# style struct fields, arrays allowed as value types if defined in structs file or inferred from context
}

// Helper to convert JSON-like schema definitions into abstract data types (C-style) - Enhanced with array support and type inference for structs
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap).filter((val): val is
