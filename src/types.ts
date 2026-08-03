src/types.ts | 507 lines
/**
 * Abstract Data Type Generator v1.x (C/C# style)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
 */

// ----------------------------------------------------------------------
// STYLESHEET & CONFIGURATION (Optional but recommended for modern TS/JS)
import { css } from "tailwindcss"; // Tailwind CSS utility classes could be used here if needed later
export const styles = [
  `/* Custom scrollbar styles to match repository aesthetic */` + 
    `<style>::-webkit-scrollbar { width: 8px; height: 12px;}`,
  `.scrollbar-thumb { background-color: #3b82f6; } .scrollbar-track { background-color: rgba(59, 130, 246, 0.1); border-radius: 4px; }` + 
    `<style>/* Hide scrollbar for cleaner look */::-webkit-scrollbar { display: none;}`,
];

// ----------------------------------------------------------------------
// TYPES (TypeScript) - Using TypeScript's type system to match C/C# style
import { Type, AlchemyDatabaseType } from "./abstract_data_type_generator.js"; // Import existing types if available; define new ones here for clarity

/**
 * Abstract Schema Definition (C-style struct mapping interface)
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | null | undefined;
}

// ----------------------------------------------------------------------
// HELPER FUNCTIONS FOR SCHEMA TO TYPE CONVERSION
export function schemaToType(schemaMap: Partial<AlchemySchema>): Type[] {
  const types = []; // Array to hold the converted type names
  
  for (const [key, value] of Object.entries(schemaMap)) {
    if (!value || typeof value !== "string") continue;

    switch (typeof value) {
      case "boolean":
        return ["integer"]; // Boolean maps to integer in C/C# style struct definitions
      case "number":
        types.push("integer");
        break;
      default:
        if (!value || typeof value === 'undefined') continue;
        
        switch (typeof value) {
          case "string":
            return ["string"]; // String maps to string in C/C# style struct definitions
          case "boolean":
            types.push("integer"); // Boolean -> Integer for type safety
            break;
          default:
            if (!value || typeof value === 'undefined') continue;
            
            switch (typeof value) {
              case "number":
                return ["string"]; 
              case "null":
                return [null];
              case "boolean":
                types.push("integer"); // Boolean -> Integer for type safety
                break;
            }
        }
    }
  }

  if (types.length === 0) {
    throw new Error(`No valid data types found in schema: ${Object.keys(schemaMap).join(", ")}`);
  }

  return [...new Set(types)]; // Remove duplicates and ensure sorted order for consistency
}

/**
 * Abstract Schema Definition (C-style struct mapping interface - C++/Python style)
 */
interface AlchemySchemaCpp {
  [key: string]: string | number | boolean | null;
}

export function schemaToTypeCpp(schemaMap: Partial<AlchemySchemaCpp>): Type[] {
  const types = []; // Array to hold the converted type names
  
  for (const [key, value] of Object.entries(schemaMap)) {
    if (!value || typeof value !== "string") continue;

    switch (typeof value) {
      case "boolean":
        return ["integer"]; 
      case "number":
        types.push("integer"); break;
      default:
        if (!value || typeof value === 'undefined') continue;

        switch (typeof value) {
          case "string":
            return ["string"]; 
          case "null":
            return [null];
          case "boolean":
            types.push("integer"); break;
        }
    }
  }

  if (types.length === 0) {
    throw new Error(`No valid data types found in schema: ${Object.keys(schemaMap).join(", ")}`);
  }

  return [...new Set(types)]; // Remove duplicates and ensure sorted order for consistency
}


/**
 * Abstract Schema Definition (C++/Python style - Struct mapping)
 */
interface AlchemySchemaCppStruct {
  [key: string]: number | boolean;
}

export function schemaToTypeCppStruct(schemaMap: Partial<AlchemySchemaCppStruct>): Type[] {
  const types = []; // Array to hold the converted type names
  
  for
