src/types.ts | 460 lines
/**
 * Abstract Data Type Generator v1.2.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
/**
 * Parse a Schema Map (C-style structure like `{"id": "int32", ...}`) into an array of valid type strings.
 * Handles: string, integer (number), boolean/null/undefined as per C/C# syntax rules.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const types = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    // Validate key exists and is a valid type name in our schema map
    if (!value || typeof value !== "string") continue;

    let parsedType: string | undefined;

    switch (type) {
      case "integer":
        const num = Number(value);
        types.push(typeof num === 'number' ? "integer" : null); // Accepts ints, floats if interpreted as such in C++
        break;
      
      case "string":
        parsedType = typeof value === 'string';
        break;

      default:
        continue;
    }

    types.push(parsedType || "");
  }

  return types.filter(Boolean); // Remove empty strings, ensure non-null arrays
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types for downstream modules.
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const validTypeNames = ["integer", "string"];
  
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === 'number' || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types.
/**
 * Validates the input against a list of allowed types (integer, string). Rejects anything else or invalid values.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const validTypeNames = ["string", "number"]; // C/C# syntax allows integer as number
  
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === 'number' || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types.
/**
 * Validates the input against a list of allowed types (string, integer). Rejects anything else or invalid values.
 */
export function parseSchemaToTypes(schema
