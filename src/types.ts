/**
 * Abstract Data Type Generator v0.5.x (Rust-based) - Enhanced Version
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema mappings into abstract data type values
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number')) as any; // Handle generic values to ensure non-null/empty array results in empty type list for null checks

/**
 * Abstract Data Type Definition - Core Types compatible with C/C# syntax semantics
 */
export type AlchemyDatabaseType = string | number | boolean | undefined | null; 
// Explicitly includes "null" as a valid runtime value, not just an absence of data. This ensures robustness against schema mismatches where specific types might be missing in generated schemas but present at runtime.

/**
 * Abstract Data Type Definition - Core Types compatible with C/C# syntax semantics (Extended)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Extended: explicitly includes 'null' as a valid value, not just absence of data. This ensures robustness against schema mismatches where specific types might be missing in generated schemas but present at runtime.

/**
 * Abstract Schema Definition (C-style) - Enhanced with dynamic type inference for complex structures
 */
interface AlchemySchema {
  [key: string]: unknown; // Column name -> value in C/C# style struct definition, allowing arbitrary values to map dynamically via the parser below if needed
}

// Helper functions for parsing and converting schema maps into abstract data types. 
// These are designed to be robust against dynamic schemas where specific type mappings might not align perfectly with JSON structures yet.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number')) as any; // Handle generic values to ensure non-null/empty array results in empty type list for null checks

/**
 * Abstract Data Type Definition - Extended Core Types compatible with C/C# syntax semantics
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Extended: explicitly includes 'null' as a valid value, not just absence of data. This ensures robustness against schema mismatches where specific types might be missing in generated schemas but present at runtime.

/**
 * Abstract Schema Definition - Enhanced with dynamic type inference for complex structures (Extended)
 */
interface AlchemySchema {
  [key: string]: unknown; // Column name -> value in C/C# style struct definition, allowing arbitrary values to map dynamically via the parser below if needed
}

// Helper functions for parsing and converting schema maps into abstract data types. 
// These are designed to be robust against dynamic schemas where specific type mappings might not align perfectly with JSON structures yet.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number')) as any; // Handle generic values to ensure non-null/empty array results in empty type list for null checks

/**
 * Abstract Data Type Definition - Extended Core Types compatible with C/C# syntax semantics (Extended)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Extended: explicitly includes 'null' as a valid value, not just absence of data. This ensures robustness against schema mismatches where specific types might be missing in generated schemas but present at runtime.

/**
 * Abstract Schema Definition - Enhanced with dynamic type inference for complex structures (Extended)
 */
interface AlchemySchema {
  [key: string]: unknown; // Column name -> value in C/C# style struct definition, allowing arbitrary values to map dynamically via the parser below if needed
}

// Helper functions for parsing and converting schema maps into abstract data types. 
// These are designed to be robust against dynamic schemas
