src/types.ts | 321 lines
```typescript
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
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
    .filter((val) => typeof val === "string" && !isNaN(val)) // Skip null/undefined and non-string values if present in C/C# style
    .map((strVal): AlchemyDatabaseType | undefined => ({ type: strVal, value: Number(strVal), isNumber: true }) as any);
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
    const types = Object.values(schemaMap).map((val) => typeof val === "string" ? "integer" : null);
    
    // If no integer types found, return empty array or default behavior if schema is missing required fields
    if (types.length === 0 && !schemaMap.has("amount")) {
      return []; 
    }

    const result: string[] = [...new Set(types)];
    // Sort alphabetically for consistency
    return result.sort();
  },

  /**
   * Convert a generic C/C# style struct to TypeScript types.
   */
  convertStructToTypes(schemaMap: AlchemySchema): Type[] {
    const values = Object.values(schemaMap);
    
    if (values.length === 0) return [];
    
    // Filter out non-strings, numbers, or null/undefined in C/C# style
    let validValues: string | number | boolean;
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

    return [validValue as Type];
  },

  /**
   * Generate a generic schema from Rust enum-like structure.
   */
  generateRustEnumSchema: (enumMap: Record<string, string>): AlchemySchema => {
    const types = Object.values(enumMap).map((val) => typeof val === "string" ? "integer" : null);

    if (types.length === 0 && !["amount", "price"].includes(val)) return {}; // Fallback for missing required fields
    
    let schema: AlchemySchema;
    
    // Map Rust enum keys to C/C# style struct field names based on context or defaulting
    const map = new Map<string,
