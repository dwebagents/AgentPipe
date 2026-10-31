src/types.ts | 450 lines
/**
 * Abstract Data Type Generator v1.x (Rust-based with TypeScript bindings)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and structural clarity
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing for dynamic key-value pairs and JSON-like structures if needed
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping logic in other modules.
// This function is designed to be used by the `AlchemyDatabaseType` enum or similar derived enums that need type safety at compile time.
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== null)) as Type[]; // Safely extracts string and number/boolean types from the schema map without throwing runtime errors on missing keys or non-serializable types.
}

/**
 * Abstract Data Type Definition for Database Schema Mapping (Rust-style enum, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = "integer" | "string" | "boolean"; // Simulating Rust enums/types via TypeScript objects in this context; used to represent the standard types compatible with C/C# syntax as per the original inspiration.

/**
 * Abstract Schema Definition (C-style) - Enhanced for flexibility and dynamic schema management
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing for JSON-like structures or complex types if needed by downstream modules like the database generator.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping logic in other modules.
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== null)) as Type[]; // Safely extracts string and number/boolean types from the schema map without throwing runtime errors on missing keys or non-serializable types.
}

/**
 * Abstract Data Type Definition for Database Schema Mapping - Enhanced with dynamic type inference support (Rust-style enum, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = "integer" | "string" | "boolean"; // Simulating Rust enums/types via TypeScript objects in this context; used to represent the standard types compatible with C/C# syntax as per the original inspiration.

/**
 * Abstract Schema Definition (C-style) - Enhanced for flexibility and dynamic schema management
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing for JSON-like structures or complex types if needed by downstream modules like the database generator.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping logic in other modules.
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== null)) as Type[]; // Safely extracts string and number/boolean types from the schema map without throwing runtime errors on missing keys or non-serializable types.
}

/**
 * Abstract Data Type Definition for Database Schema Mapping - Enhanced with dynamic type inference support (Rust-style enum, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = "integer" | "string" | "boolean"; // Simulating Rust enums/types via TypeScript objects in this context; used to represent the standard types compatible with C/C# syntax as per the original inspiration.

/**
 * Abstract Schema Definition (C-style) - Enhanced for flexibility and dynamic schema management
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing for JSON-like structures or complex types if needed by downstream modules like the database generator.
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping logic in other modules.
