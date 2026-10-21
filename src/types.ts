src/abstract_schema_to_types.js
/**
 * Converts C/C# style struct definitions into TypeScript types for direct schema mapping in database generators.
 * This module simulates Rust case expressions and pattern matching to handle complex type hierarchies (e.g., Int32, String).
 */

import { StructType } from "./structs"; // Assume a structs file exists or inherits from it; adapted here to use TypeScript-like semantics directly if not available.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into a generic array of types for schema mapping logic
function getGenericType(schemaEntry: any): "integer" | "string" | null | undefined {
  if (typeof schemaEntry === 'number') return "integer"; // Simulating integer type handling in Rust/C context
  if (Array.isArray(schemaEntry)) return ["null"]; // Handling array-like structures or arrays of values as a fallback for complex types
  const val = typeof schemaEntry;
  switch (val) {
    case 'string': return "string";
    case 'number': return "integer";
    default: return null;
  }
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert the generic schema types into a TypeScript list of concrete type names for easier mapping logic.
function getConcreteTypeNames(schemaMap: AlchemySchema): "integer" | "string" | null | undefined[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === 'string' || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Filter out numbers and strings for non-string values to avoid false negatives from type inference in filter.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert the generic schema types into a TypeScript list of concrete type names for easier mapping logic.
function getConcreteTypeNames(schemaMap: AlchemySchema): "integer" | "string" | null | undefined[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === 'string' || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Filter out numbers and strings for non-string values to avoid false negatives from type inference in filter.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert the generic schema types into a TypeScript list of concrete type names for easier mapping logic.
function getConcreteTypeNames(schemaMap: AlchemySchema): "integer" | "string" | null | undefined[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === 'string' || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Filter out numbers and strings for non-string values to avoid false negatives from type inference in filter.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert the generic schema types into a TypeScript list of concrete type names for easier mapping logic.
function getConcreteTypeNames(schemaMap: AlchemySchema): "integer" | "string" | null | undefined[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === 'string' || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Filter out numbers and strings for non-string values to avoid false negatives from type inference in filter.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert the generic schema types into a TypeScript list of concrete type names for easier mapping logic.
function getConcreteTypeNames(schemaMap: AlchemySchema): "integer" | "string" | null | undefined[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === 'string' || (typeof val !== 'undefined' && typeof val !== 'number') as any); //
