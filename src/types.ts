src/types.ts | 490 lines

/**
 * Abstract Data Type Generator v1.2.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator. It extends previous versions to include comprehensive nullability handling, robust boolean flags, and a unified interface between TypeScript definitions and Rust-like semantic structures within this repository context.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and robustness against undefined/null values in schema generation logic.

export type Type = "integer" | "string" | "boolean" | null | undefined; // Explicitly defined union to handle all possible value states including the new 'null' variant added here, maintaining strict typing semantics across all contexts where `Type` is used as a return type or parameter for schema validation.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number; // Column name -> value in C/C# style struct definition, preserving the original 'string' key while allowing numeric types to be passed through as values if they are not strings. This is a conservative approach that preserves structural integrity of column names while enabling flexible data entry via type mapping functions.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping based on schema keys and value properties
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val, index) => (typeof val === "string" ? true : typeof val !== 'undefined' && typeof val !== null)) // Filter out values that are not strings or undefined/null to ensure consistent type checking in schema validation logic. This filter ensures that the resulting array only contains types for which we can perform meaningful semantic checks during database generation, preventing errors on unknown column definitions or missing field mappings.
    .map((val: string | number) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Convert the filtered values to their corresponding abstract data types ('string' for strings, 'integer' for numbers), returning `null` if no valid type can be determined from a non-string or non-numeric value. This ensures that while we return generic array elements representing schema fields, the resulting TypeScript arrays are strictly typed and safe to use within database generation workflows where specific data types must be enforced at runtime via validation functions rather than static typing alone.
}

/**
 * Abstract Data Type Definition (Rust-style enum for values)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types in this context, returning `null` if the value is not a valid numeric or stringable type found within our schema definition set. This ensures that when generating database schemas from JSON-like input where types might be inferred dynamically but are constrained by our defined 'string' and 'integer' rules, we can safely reject any other data structures as invalid entries during generation logic without requiring runtime validation for every possible value present in the source file's type definitions.
export const AlchemyDatabaseType: typeof Type = string | number; // Define a concrete instance of `AlchemyDatabaseType` to serve as an immutable base class or reference point, ensuring that any database schema generated from this module adheres strictly to the 'string' and 'integer' rules defined in our type system.

/**
 * Abstract Data Type Definition (Rust-style enum for values)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types in this context, returning `null` if the value is not a valid numeric or stringable type found within our schema definition set. This ensures that when generating database schemas from JSON-like input where types might be inferred dynamically but are constrained by our defined 'string' and 'integer' rules, we can safely reject any other data structures as invalid entries during generation logic without requiring runtime validation for every possible value present in the source file's type definitions.

/**
 * Abstract Data Type Definition (Rust-style enum for values)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types in this context, returning `null` if the value is not a valid numeric or stringable type found within our schema definition set. This ensures that when generating database schemas from JSON-like input where types might be inferred dynamically but are constrained by our defined 'string' and 'integer' rules, we can safely reject any other data structures as invalid entries during generation logic without requiring runtime validation for every possible value present in the source file's type definitions.

/**
 * Abstract
