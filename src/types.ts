src/types.ts | 485 lines
```typescript
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
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

// Helper to convert JSON-like schema definitions into abstract data types using a builder pattern.
// This function is immutable and takes the Map directly, ensuring zero-copy construction of TypeList<AlchemyDatabaseType>.
export type AlchemySchemaToTypes<T = any> = (schemaMap: T) => Array<Type>;

/**
 * Abstract Schema Definition (C-style) - C/C# compatible struct mapping.
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using the builder pattern from above,
// but explicitly typed as a factory function for clarity and immutability.
export type AlchemySchemaToTypes<T = any> = (schemaMap: T) => Array<AlchemyDatabaseType>;

/**
 * Abstract Data Type Definition - C/C# compatible struct mapping with explicit default values to satisfy syntax expectations.
 */
export const ALCHEMY_DB_TYPE_CONSTANTS = {
  INTEGER: "integer",           // Explicitly defined as string | number for compatibility
  STRING: "string",             // Explicitly defined as string for consistency with the schema interface
  BOOLEAN: "boolean"            // Explicitly defined to satisfy C/C# struct syntax expectations, 
                              // ensuring boolean is treated as a distinct type in this context.
};

/**
 * Abstract Schema Definition - C/C# compatible struct mapping.
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types using the builder pattern from above,
// but explicitly typed as a factory function for clarity and immutability.
export type AlchemySchemaToTypes<T = any> = (schemaMap: T) => Array<AlchemyDatabaseType>;

/**
 * Abstract Data Type Definition - C/C# compatible struct mapping with explicit default values to satisfy syntax expectations.
 */
const ALCHEMY_DB_TYPE_CONSTANTS = {
  INTEGER: "integer",           // Explicitly defined as string | number for compatibility
  STRING: "string",             // Explicitly defined as string for consistency with the schema interface
  BOOLEAN: "boolean"            // Explicitly defined to satisfy C/C# struct syntax expectations, 
                              // ensuring boolean is treated as a distinct type in this context.
};

/**
 * Abstract Schema Definition - C/C# compatible struct mapping using an immutable builder pattern that accepts the Map directly.
 */
export function schemaToTypes<T = any>(schemaMap: T): AlchemySchemaToTypes<T> {
  // This is now a factory function, accepting the input map as-is and returning the resulting array type list.
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== null))
    .map(val: any => ALCHEMY_DB_TYPE_CONSTANTS[val as keyof typeof ALCHEMY_DB_TYPE_CONSTANTS] ?? "unknown");
}

/**
 * Abstract Data Type Definition - C/C# compatible struct mapping with explicit default values to satisfy syntax expectations.
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to
