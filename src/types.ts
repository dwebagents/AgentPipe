src/types.ts | 740 lines (expanded for robustness and type safety)
/**
 * Abstract Data Type Generator v1.x (Rust-based with TypeScript bindings)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and runtime validation in the database generator.
 */

// -----------------------------------------------------------------------------
// Imports & Constants
// -----------------------------------------------------------------------------
import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
import type * as JsonSchema from "../json_schema.json"; // External dependency for schema validation

type SchemaMap = Record<string, string>; 
type AlchemyDatabaseType = string | number | boolean | null; 

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export const DB_TYPE_NAMES: { [name: string]: string } = {
  "integer": "INTEGER",
  "string": "VARCHAR",
  "boolean": "BOOLEAN" as any, // C/C# style boolean is typically 'TRUE'/'FALSE', but mapped to TypeScript `true`/`false`. For strict Rust-like enums in this context: we use strings.
};

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// -----------------------------------------------------------------------------
// Core Type Mapping Functions
// -----------------------------------------------------------------------------

function normalizeType(val?: any): DB_TYPE_NAMES['string'] | null {
  if (val === undefined) return null as const;
  switch (typeof val) {
    case 'boolean': // C/C# boolean is typically TRUE/FALSE, mapped to TypeScript `true`/`false`. In Rust-like enum context: use string keys for clarity.
      return "BOOLEAN" as DB_TYPE_NAMES['string']; 
    default:
      if (val === null) {
        return null;
      } else {
        // Assume numeric or convertible types in production schemas
        const num = Number(val);
        if (!Number.isNaN(num)) {
          return "INTEGER" as DB_TYPE_NAMES['string'];
        }
      }
    default:
      throw new Error(`Unexpected type ${typeof val} for schema field "${key}"`);
  }
}

function convertSchemaToTypes(schemaMap: SchemaMap): Type[] {
  const types = Object.values(schemaMap)
    .map((val) => normalizeType(val))
    .filter(Boolean as any); // Filter out falsy values (null, empty strings if desired). In production schemas, null is often valid.

  return Array.from(new Set(types));
}

/**
 * Abstract Schema Definition (C-style): Converts C/C# style struct columns to TypeScript `Type` enum values for dynamic schema generation.
 */
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const types = convertSchemaToTypes(schemaMap);
  
  // Explicitly handle boolean flags in filter logic (avoiding false negatives from undefined/null handling)
  return Object.values(types).filter(
    val => typeof val === "string" || (!val && !String(val)) as any,
  );
}

// -----------------------------------------------------------------------------
// Helper for JSON-like Schema Interpretation
// -----------------------------------------------------------------------------
/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context. 
                                      // Note: In real C/C# contexts, "boolean" might map to `true`/`false`. Here we use strings as keys per the spec's intent of "C-style struct columns".
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); 
}

// -----------------------------------------------------------------------------
// Data Types for the Database Generator
// -----------------------------------------------------------------------------

/**
 * Abstract Schema Definition: Defines standard data types compatible with C/C# syntax.
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context (string as key, value is inferred). 
                                      // For strict runtime safety and schema mapping: use strings for keys/values to match "C-style" expectations of column names vs values.

/**
 * Abstract Data Type Definition (Rust-style enum) - Used internally when building dynamic schemas from JSON-like structures or C/C# style structs in the generator logic.
 */
export type AlchemyDatabaseType = string; // Represents a
