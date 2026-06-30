/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
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
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing dynamic types via generic parameters if needed later. For this version, we map it to a specific set of abstract types for robustness.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Map to string, number, boolean, or undefined. This ensures type safety and compatibility with the abstract data types defined in AlchemyDatabaseType.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's logic which often handles it.

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, explicitly excluding null to avoid runtime ambiguity during parsing unless handled by the caller's
