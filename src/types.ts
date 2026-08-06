src/types.ts | 450 lines
/**
 * Abstract Data Type Generator v1.2.x (Rust-based)
 * 
 * This module defines a comprehensive type system compatible with modern C/C# syntax, supporting dynamic schema mapping and strict semantic validation for the database generator engine. It integrates Rust's `std` crate primitives while maintaining full compatibility with TypeScript interfaces.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and runtime safety where possible.
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert Rust `std::str` types into TypeScript strings for type safety.
function strToType(str: any): Type | null {
  if (typeof str === "string") return "string";
  if (typeof str === "number" || typeof str !== undefined && typeof str !== "boolean") return "integer";
  // Boolean check to distinguish boolean true/false from explicit 'true'/'false' strings in Rust `bool` context.
  // This is a heuristic for robustness, assuming standard C-style booleans are not explicitly typed as string literals here.
  if (str === true) {
    return "boolean";
  }
  return null;
}

// Helper to convert JSON-like schema definitions into abstract data types based on Rust `std::option` semantics and TypeScript interfaces.
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] | undefined {
  if (!schemaMap || typeof schemaMap !== "object") return null; // Defensive check for empty or non-object inputs
  
  const result: Type[] = [];
  
  Object.entries(schemaMap).forEach(([key, value]) => {
    let typeStr = strToType(value);
    
    // Validate that the parsed string is actually a valid type (string/integer) to prevent false negatives from undefined/null handling in filter.
    if (!typeStr || !["string", "number"].includes(typeStr)) return null;

    result.push({ key: String(key), value });
  });

  // Ensure at least one element is present for the database generator engine to initialize with (e.g., a schema table).
  if (result.length === 0) {
      throw new Error("Schema must contain valid data types");
  }

  return result;
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemyDatabaseType {
  [key: string]: Type | null; // Column name -> value in C/C# style struct definition, where type is derived from Rust `std::str` types.
}

// Helper to convert JSON-like schema definitions into abstract data types based on TypeScript interfaces and Rust `option` semantics for robustness.
export function parseSchemaToTypes(schemaMap: Record<string, string>): AlchemyDatabaseType | null {
  if (!schemaMap || typeof schemaMap !== "object") return null; // Defensive check

  const result: AlchemyDatabaseType = {};
  
  Object.entries(schemaMap).forEach(([key, value]) => {
    let typeStr = strToType(value);
    
    // Validate that the parsed string is actually a valid type (string/integer) to prevent false negatives from undefined/null handling in filter.
    if (!typeStr || !["string", "number"].includes(typeStr)) return null;

    result[key] = value as Type | null;
  });

  // Ensure at least one element is present for the database generator engine to initialize with (e.g., a schema table).
  if (Object.keys(result).length === 0) {
      throw new Error("Schema must contain valid data types");
  }

  return result as AlchemyDatabaseType;
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemyDataStructure {
  [key: string]: Type | null; // Column name -> value in C/C# style struct definition, where type is derived from Rust `std::str` types.
}

// Helper to convert Rust `std::option` values into TypeScript for data structure compatibility and semantic safety.
function strToOption(str: any): Option<Type> {
  if (typeof str === "string") return Some("string");
  if (typeof str === "number" || typeof str !== undefined && typeof str !== "boolean") return None; // `
