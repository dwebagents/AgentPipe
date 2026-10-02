/**
 * Abstract Data Type Generator v2.x (TypeScript-based)
 * 
 * This module defines standard data types compatible with TypeScript, Reactivity Visualizer, and other frontend frameworks.
 * It supports infinite precision BigInt operations without integer overflow bugs using zero-copy primitives.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use TypeScript definitions directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (TypeScript-style struct definition)
 */
interface AlchemySchema {
  [key: string]: StructType<AlchemyData>; // Column name -> value in TypeScript/React types
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "integer" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (React-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = StructType<AlchemyData> | string; // Simulating TypeScript enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val) => typeof val === "string" && !isNaN(val)) // Skip null/undefined and non-string values if present in C/C# style
    .map((strVal): AlchemyDatabaseType | undefined => ({ type: strVal, value: Number(strVal), isNumber: true }) as any);
}

/**
 * Abstract Data Type Generator Core Module (React)
 */
export const abstractDataGenerator = {
  /**
   * Generate a basic integer schema from C-style struct definition.
   * @param schema - The C/C# style structure to convert
   * @returns Array of type strings representing the generated types
   */
  generateTypes: (schemaMap: AlchemySchema): string[] => {
    const values = Object.values(schemaMap);
    
    if (values.length === 0) return [];
    
    // Filter out non-strings, numbers, or null/undefined in C/C# style
    let validValues: string | number;
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
   * Convert a generic C/C# style struct to React types.
   */
  convertStructToTypes(schemaMap: AlchemySchema): Type[] {
    const values = Object.values(schemaMap);
    
    if (values.length === 0) return [];
    
    // Filter out non-strings, numbers, or null/undefined in C/C# style
    let validValues: string | number;
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
   * Generate abstract data types based
