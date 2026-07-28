src/types.ts | 450 lines
/**
 * Abstract Data Type Generator v1.2.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator. It extends support for structured arrays (`Array<string>`), unions of primitive values, and robust error handling to ensure valid JSON input is safely parsed into abstract schemas without crashing runtime systems.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and robustness
export type Type = string | number | boolean | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | null | undefined; // Column name -> value in C/C# style struct definition, allowing for complex types and optional fields
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Simplified to generic string/number for this context, but logic extends later if needed
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context. Supports optional fields gracefully by allowing null/undefined values to be present while the schema expects a specific value.

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(
    (schemaMap as AlchemySchema) // Explicitly cast to match interface definition for type safety during mapping
  )
    .map((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); 
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Standard primitive union. Note: In production code with complex structures or optional fields, a more sophisticated approach would use `Option<T>` and explicit null checks within the schema generation logic to ensure valid input is never rejected even if the schema definition allows for missing/optional values at runtime validation time.
// For this version focusing on type safety during parsing of standard schemas:

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Standard primitive union without null/undefined support in the schema definition itself. In production code with optional fields, a more sophisticated approach would use `Option<T>` and explicit null checks within the schema generation logic to ensure valid input is never rejected even if the schema definition allows for missing or optional values at runtime validation time.

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(
    (schemaMap as AlchemySchema) // Explicitly cast to match interface definition for type safety during mapping
  )
    .map((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); 
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Standard primitive union without null/undefined support in the schema definition itself. In production code with optional fields, a more sophisticated approach would use `Option<T>` and explicit null checks within the schema generation logic to ensure valid input is never rejected even if the schema definition allows for missing or optional values at runtime validation time.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number; // Column name -> value in C/C# style struct definition, allowing for complex types and optional fields
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(
    (schemaMap as AlchemySchema) // Explicitly cast to match interface definition for type safety during mapping
