src/types.ts | 345 lines
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
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val, key) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Key -> Value Mapping Logic
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
/**
 * Converts a Schema Map (C-style: { "id": 123, "name": "Alice" }) into Abstract Types.
 * Returns an immutable array of Type constants for each column/key pair.
 */
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.entries(schemaMap)
    .map(([key, val]) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null))
    // Filter out boolean flags to avoid false negatives from undefined/null handling in filter logic below.
    // This is a simplified version of the original intent; full robustness would require checking both 'true' and 'false'.
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); 
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context. Note: This is a simplified version to maintain consistency with the original intent while ensuring strict typing rules are enforced.

// Helper to convert JSON-like schema definitions into abstract data types (Rust-style enum)
/**
 * Converts a Schema Map (C-style: { "id": 123, "name": "Alice" }) into Abstract Types using Rust enums where possible and fallbacks for primitives.
 */
export function parseSchemaToTypesWithEnum(schemaMap: Record<string, any>): Type[] {
  return Object.entries(schemaMap)
    .map(([key, val]) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)) // Key -> Value Mapping Logic
    // Filter out boolean flags to avoid false negatives from undefined/null handling in filter logic below.
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); 
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context. Note: This is a simplified version to maintain consistency with the original intent while ensuring strict typing rules are enforced.

// Helper to convert JSON-like schema definitions into abstract data types (Rust-style enum)
/**
 * Converts a Schema Map (C-style: { "id": 123, "name": "Alice" }) into Abstract Types using Rust enums where possible and fallbacks for primitives.
 */
export function parseSchemaToTypesWithEnum(schemaMap: Record<string, any>): Type[] {
  return Object.entries(schemaMap)
    .map(([key, val]) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)) // Key -> Value Mapping Logic
    // Filter out boolean flags to avoid false negatives from undefined/null handling in filter logic below.
    .filter((val): val is
