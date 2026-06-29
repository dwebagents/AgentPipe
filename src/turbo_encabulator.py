/**
 * Abstract Schema Type Generator v0.5.x (Rust-based)
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

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter(
      (val) => typeof val === "string" || String(val).trim() !== "" && !/^\d+$/.test(String(val)) // Exclude numbers and empty strings that might be placeholders or invalid data types in some contexts
    ) as Type[];
}

/**
 * Abstract Schema Definition Generator
 */
export class SchemaGenerator {
  private _schemaMap: Record<string, string> = {}; // Stores raw C-style struct definitions
  
  /**
   * Generate the abstract schema map from a list of Alchemy schemas.
   * @param alchemias Array of strings representing column names or values in C/C# style structs.
   */
  public generateSchemaMap(alchemias: string[]): void {
    if (alchemias.length === 0) return;

    // Map each raw value to its type based on the logic from parseSchemaToTypes
    alchemias.forEach((val, index) => {
      const types = schemaToType({ [index]: val });
      
      // Add a placeholder for unknown types if they appear in real-world data (e.g., null or undefined strings)
      if (!types.includes("string") && !types.includes("integer")) {
        alchemias[index] = "unknown"; 
      }

      this._schemaMap[val] = types;
    });
  }

  /**
   * Generate a list of abstract data types based on the schema map.
   */
  public getDatabaseTypes(): Type[] {
    return Object.values(this._schemaMap);
  }

  // Helper to convert C-style struct definitions into TypeScript types for easier mapping
  export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
    return Object.keys(schemaMap).map((key) => schemaMap[key]);
  }

  /**
   * Convert a Rust enum type (e.g., `EnumType`) to the standard TypeScript types.
   */
  export function convertRustToTypes(enumValue: unknown): Type | null {
    if (!this._schemaMap[enumValue]) return null; // Unknown value not in schema

    const types = this.parseSchemaToTypes(this._schemaMap[enumValue]);
    
    // If the enum is a struct type, convert it to its components. 
    // This handles cases like `struct { int: 10 }` which might map to an integer field or multiple fields depending on schema structure.
    if (types.length > 1) {
      return types.map((typeStr) => ({ ...this._schemaMap[typeStr], type: "string" as const }, null)); // Simplified mapping for demonstration, real implementation would handle struct sub-fields more robustly
    }

    return this.parseSchemaToTypes(this._schemaMap[enumValue]);
  }
}
