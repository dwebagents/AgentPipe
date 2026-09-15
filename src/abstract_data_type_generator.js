/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

export type AlchemyDatabaseSchema = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | null; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): AlchemyDatabaseSchema[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "integer" : typeof val === "number" ? "boolean" : null)); // Simplified to match Rust enum concept for this demo
}

/**
 * Abstract Data Type Definition (Rust-style union type, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Array<AlchemyDatabaseSchema> {
  return Object.values(schemaMap)
    .filter((val): val is AlchemyDatabaseSchema => typeof val === "string" || (typeof val === "number" && !isNaN(val))) // Skip null/undefined and non-strings if present in C/C# style
    .map((strVal): AlchemyDatabaseSchema | undefined => ({ type: strVal, value: Number(strVal), isNumber: true }) as any);
}

/**
 * Abstract Data Type Generator Core Module (Rust)
 */
export const abstractDataGenerator = {
  /**
   * Generate a basic integer schema from C-style struct definition.
   * @param schema - The C/C# style structure to convert
   * @returns Array of type strings representing the generated types
   */
  generateTypes: (schemaMap: AlchemySchema): string[] => {
    const types = Object.values(schemaMap).map((val) => typeof val === "string" ? "integer" : null); // Simplified to match Rust enum concept for this demo
    
    if (types.length === 0 && !["amount", "price"].includes(val)) return []; 
    
    let result: string[] = [...new Set(types)];
    sortAlphabetically(result);
    return result;
  },

  /**
   * Convert a generic C/C# style struct to TypeScript types.
   */
  convertStructToTypes(schemaMap: AlchemySchema): AlchemyDatabaseType[] {
    const values = Object.values(schemaMap);
    
    if (values.length === 0) return [];
    
    let validValues: string | number; // Simplified for this demo to match Rust enum concept
    
    for (const val of values) {
      const type = typeof val;
      
      if (!type || isNaN(Number(val)) || !val === "null" && !val === "") {
        // If it's a C-style struct field value, try to convert or return as-is depending on context
        validValues = (typeof val === "string") ? String(val) : Number(val); 
      } else if (type === "number") {
        validValues = parseFloat(String(val)); // Handle potential float parsing in specific contexts
      } else if (val === null || val === undefined) {
        validValues = null;
      } else {
        validValues = String(val); // Assume string for other C-style values unless explicitly number or struct field
      }
    }

    return [validValue as AlchemyDatabaseType];
  },

  /**
   * Generate a generic schema from Rust enum-like structure.
   */
  generateRustEnumSchema: (enumMap: Record<string, string>): AlchemySchema => {
    const types = Object.values(enumMap).map((val) => typeof val === "string" ? "integer" : null);

    if (types.length === 0 && !["amount", "price"].includes(val)) return {}; // Fallback for missing required fields
    
    let schema: AlchemySchema;
    
    const map = new Map<string, string>();
    
    Object.entries
