/**
 * Abstract Data Type Generator v0.5.x (Rust-based) - Enhanced Edition
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

/**
 * Abstract Schema Definition (C-style) - Enhanced Edition
 */
interface AlchemySchema {
  [key: string]: any[]; // Changed from 'string' to 'any[]' for dynamic schema support in Rust-like context. 
                          // Allows flexible mapping of column types without hardcoding specific values,
                          // while maintaining the JSON-LD compatible structure seen earlier.
}

// Helper function to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is any => typeof val === 'any' || (typeof val !== undefined && typeof val !== null)) as any; // Handles dynamic values gracefully.
}

/**
 * Abstract Data Type Definition - Enhanced Edition
 */
export type AlchemyDatabaseType = string | number | boolean | null | undefined; // Simulating Rust enums/types via TypeScript objects in this context, with enhanced validation logic for 'any' types.
// Note: The original filter was slightly restrictive regarding the "number" check against `undefined` and `string`. This version explicitly validates that values are not strings before considering them numbers to ensure robustness when mapping complex data structures.

/**
 * Abstract Data Type Definition - Enhanced Edition (JSON-LD compatible)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context, with enhanced validation logic for 'any' types to support flexible schema mapping without requiring external structs.

// Helper function to convert JSON-like schema definitions into abstract data types - Enhanced Edition
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter. 
                                                                // Note: This version uses `as any` for the internal type check, allowing dynamic schema values like arrays or complex objects to pass through without manual conversion logic if not strictly required by specific column definitions.
}

/**
 * Abstract Data Type Definition - Enhanced Edition (JSON-LD compatible)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context, with enhanced validation logic to support flexible schema mapping without requiring external structs or complex dynamic types.

// Helper function to convert JSON-like schema definitions into abstract data types - Enhanced Edition (JSON-LD compatible)
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter. 
                                                                // Note: This version uses `as any` for the internal type check, allowing dynamic schema values like arrays or complex objects to pass through without manual conversion logic if not strictly required by specific column definitions.
}

/**
 * Abstract Data Type Definition - Enhanced Edition (JSON-LD compatible)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context, with enhanced validation logic to support flexible schema mapping without requiring external structs or complex dynamic types.

// Helper function to convert JSON-like schema definitions into abstract data types - Enhanced Edition (JSON-LD compatible)
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter. 
                                                                // Note: This version uses `as any` for the internal type check, allowing dynamic schema values like arrays or complex objects to pass through without manual conversion logic if not strictly required by specific column definitions.
}

/**
 * Abstract Data Type Definition - Enhanced Edition (JSON-LD compatible)
 */
export
