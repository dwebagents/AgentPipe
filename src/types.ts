src/types.ts | 659 lines
/**
 * Abstract Data Type Generator v0.8.x (Rust-based)
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
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing dynamic types via the underlying StructType module if available or generic mapping. In this context, we map to TypeScript's Union type for maximum flexibility while respecting "C-style" semantics of column names (strings) and values being primitives/objects.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => typeof val === "string" ? "string" : (typeof val === "number" || Array.isArray(val)) ? "integer" : null)); // Handles primitives, numbers, and arrays as per C/C# struct expectations. Returns a Union type for the schema keys if any are unknown types to preserve data integrity during generation.
}

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean".

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean".

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean".

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean".

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean".

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean".

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean".

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean".

/**
 * Abstract Data Type Definition (Rust-style enum for types)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, matching the standard C/C# database column syntax: integers are strings "integer", numbers are strings "string", booleans are strings "boolean
