import * as crypto from 'crypto';
import fs from 'fs/promises';
import path from 'path';
import { createRequire } from 'module'; // For Node.js environment (if available) or global require() for ES modules

/** 
  * Abstract Data Type Generator v0.5.x (Rust-based)
  * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
  
  @remarks: The following enhancements have been implemented to ensure valid runtime behavior across Node.js environments while maintaining compatibility with existing TypeScript/JSON schemas.
*/

// ============================================================================
// TYPE DEFINITIONS & UTILITIES
// ============================================================================

/** 
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value type in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types for TypeScript compatibility.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string')) as any; // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/** 
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context.
// Note: In a real environment with strict typing libraries like rust-lang/rust or tsx-ts-schemas, 
// these would be mapped to actual Rust types (e.g., `Option<T>`, `Result<...>`).

/** 
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value type in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types for TypeScript compatibility.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string')) as any; // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/** 
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context.
// Note: In a real environment with strict typing libraries like rust-lang/rust or tsx-ts-schemas, 
// these would be mapped to actual Rust types (e.g., `Option<T>`, `Result<...>`).

/** 
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value type in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types for TypeScript compatibility.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string')) as any; // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/** 
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context.
// Note: In a real environment with strict typing libraries like rust-lang/rust or tsx-ts-schemas, 
// these would be mapped to actual Rust types (e.g., `Option<T>`, `Result<...>`).

/** 
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value type in C/C# style struct definition
}

// Helper to convert JSON-like schema definitions into abstract data types for TypeScript compatibility.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string')) as any; // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
}

/** 
 * Abstract Data Type Definition
