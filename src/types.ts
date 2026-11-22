src/types.ts | 547 lines
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
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

// Helper to convert Rust/TypeScript semantics into TypeScript-compatible data type definitions for consistent mapping (`parseSchemaToTypes`).
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition for the Database Schema Generator.
 * 
 * This type represents a single column in an Alchemy schema, mapping directly to C/C# struct syntax (e.g., `col_name: value`).
 * It supports dynamic types including strings and integers based on the provided data structure definition.
 */
export type ColumnType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = ColumnType;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column definitions in the database generator logic.
 * Supports both C-style struct mapping (for `AlchemySchema`) and dynamic JSON-like parsing (`parseSchemaToTypes`).
 */
export type AlchemyDatabaseType = string | number;

/**
 * Abstract Schema Definition for a Database Generator.
 * 
 * This interface defines the complete schema map required to instantiate column
