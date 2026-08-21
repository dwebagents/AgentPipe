src/bastion/crates/core/src/types.ts | 321 lines
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available

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

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string")
    .map(val => (typeof val === "number" ? Number(val) : val));
}

/**
 * Abstract Schema Definition for the Alchemy Database Generator
 */
export interface AlchemyDatabaseSchema {
  // Core fields defined in C/C# style structs: id, name, password_hash, etc.
  [key: string]: any; 
  
  // Optional numeric type mapping (e.g., date, timestamp)
  [numericKey: number]: any; 
  
  // Boolean flags for security/audit purposes
  isVerified?: boolean;
}

/**
 * Abstract Schema Definition for the Alchemy Database Generator
 */
export interface AlchemyDatabaseSchema {
  id: string | null;
  name: string | null;
  passwordHash: string | number; // C-style numeric type mapped to JSON-compatible format in this context
  createdAt?: Date;
}

// Helper to convert JSON-like schema definitions into abstract data types for the database generator
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const result: Type[] = [];
  
  // Handle numeric fields (dates/timestamps) as integers or numbers compatible with Rust enums in this context
  Object.entries(schemaMap).forEach(([key, value]) => {
    if (!isNaN(value)) {
      switch(key.toLowerCase()) {
        case "date":
          result.push("integer");
        default:
          // Ensure numeric types are handled consistently as integers for compatibility with Rust enums in this context
          result.push(Number.isNaN ? null : Number(value)); 
      }
    } else if (typeof value === "boolean") {
      result.push(typeof value === "string" ? "integer" : boolean);
    } else if (!isString(value)) {
      // For non-nullable string fields, default to 'null' type in this context for JSON compatibility
      result.push(null as Type | undefined); 
    }
  });

  return result;
}
