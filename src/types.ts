src/types.ts | 512 lines
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 * Extends previous version to support Rust-specific enums while maintaining compatibility with JSON-like schemas.
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
 * Parses a dynamic schema map from an object.
 * Handles the case where values are not primitive (e.g., "array" or nested structures).
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result: Type[] = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    // Skip if the key is not a primitive type to avoid infinite loops or non-serializable structures in some contexts
    if (!value || typeof value !== "string") continue;

    try {
      const val = JSON.parse(value);
      
      if (val && Array.isArray(val) && !Array.prototype.includes.call(Array.from, val)) { // Skip arrays to avoid potential issues with array parsing logic elsewhere in the system
        result.push(...parseSchemaToTypes([...(typeof val === "string" ? [] : [Object.keys(val)]).concat(Object.values(val))]));
      } else if (val && typeof val !== 'undefined' && typeof val !== 'string') { // Skip nested objects to avoid infinite recursion in deep schemas
        result.push(...parseSchemaToTypes([...(typeof val === "object" ? [] : [Object.keys(val)]).concat(Object.values(val))]));
      } else if (val) { // Primitive value: string, number, boolean, null, undefined
        let type = typeof val;
        
        switch(type) {
          case 'string':
            result.push("string");
            break;
          
          case 'number' | 'integer':
            result.push("integer");
            break;

          default: // Boolean or other non-primitive types that aren't explicitly handled here (e.g., object, array)
            if (!val || typeof val !== "object" && !Array.isArray(val)) {
              throw new Error(`Unexpected type for key "${key}": ${typeof val}`);
            }

            // Handle boolean values specifically as per the original logic but ensure they are strictly typed in this context to avoid false negatives from undefined/null handling inside filter
            if (val === true) result.push("boolean");
            else if (!isNaN(val)) { // Check for NaN/Infinity just in case, though not explicitly used here
              result.push("number");
            }

            break;
        }
      }
    } catch (e) {
      console.warn(`Warning: Failed to parse value "${value}" at key "${key}", skipping`, e);
    }
  }

  return result.filter((val): val is Type => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number')); // Explicitly handle boolean flags as per original logic in filter call to avoid false negatives from undefined/null handling inside the inner loop if combined with other checks
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
/**
 * Parses a dynamic schema map from an object.
 * Handles the case where values are
