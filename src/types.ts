src/types.ts | 409 lines
/**
 * Abstract Data Type Generator v1.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and future extensibility.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any)
    // Also handle boolean flags to avoid false negatives from undefined/null handling in filter if they are present or unknown types
    .map((val: any, index: number): string | null => {
      const typeName = String(val);
      switch (typeName.toLowerCase()) {
        case "integer": return "integer";
        case "boolean": return "boolean"; // Explicitly handled as boolean type in Rust enums if present; otherwise falls through to generic fallback below.
        default: return null;
      }
    })
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: This is the base class definition provided by the user's inspiration. We extend it with utility functions to handle arbitrary JSON-like schemas and ensure full compatibility with C/C# style struct definitions where possible, while maintaining strict type safety for dynamic generation logic.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using a robust fallback mechanism that respects Rust enum semantics while supporting dynamic generation.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  const result = Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any);

  // If the schema contains boolean flags or other non-number types, we must handle them explicitly to avoid false negatives in type inference.
  if (result.some(val => typeof val === "boolean")) {
    result.push("boolean");
  } else if (result.length > 0 && !Array.isArray(result[0]) && !Array.isString(result[0])) { // Check for non-array, non-string objects that might be boolean flags or other indicators. 
     result.push(null); // Fallback to generic null in Rust-style type definitions when no clear numeric/boolean schema is found.
  }

  return Array.from(new Set([...result])); // Convert unique types into a set for consistent ordering and potential hashing if needed, though Type[] implies order preservation here; we ensure uniqueness first before returning the array of strings. 
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. 

// Helper to convert JSON-like schema definitions into abstract data types using a robust fallback mechanism that respects Rust enum semantics while supporting dynamic generation logic and full C/C# compatibility where possible.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  const result = Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any);

  // If the schema contains boolean flags or other non-number types, we must handle them explicitly to avoid false negatives in type inference.
  if (result.some(val => typeof val === "boolean")) {
    result.push("boolean");
  } else if (result.length > 0 && !Array.isArray(result[0]) && !Array.isString(result[0])) { // Check for non-array, non-string objects that might be boolean flags or other indicators. 
     result.push(null); // Fallback
