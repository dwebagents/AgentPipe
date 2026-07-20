src/types.ts | 520 lines
/**
 * Abstract Data Type Generator v1.4.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and dynamic schema mapping in the downstream generator.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value type or null to indicate missing column
}

// Helper to convert C-style struct/TS-like definitions into TypeScript types for easier mapping and dynamic schema generation.
export function parseAlchemySchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  const result = [];
  
  Object.entries(schemaMap)
    .filter(([_, val]) => typeof val === "object" && Array.isArray(val)) // Only process arrays of values if they are objects (TS-like or JSON-like schemas)
    .forEach(([key, value]: [string, unknown[]]) => {
      const type = getSchemaType(value);
      
      result.push({ key: key as string, name: "Column", schema_type: type });
    });

  return result;
}

/**
 * Helper to determine the concrete TypeScript type for a given value.
 */
function getSchemaValue(type: unknown): any {
  if (type === null || typeof type === 'undefined') return undefined as any; // Handle explicit null/undefined in schema definition directly
  
  switch (typeof type) {
    case "string":
      return String(value); // Convert to string for C-style compatibility or preserve original type
    case "number":
      if (!isFinite(value)) return Number(value); // Ensure numeric types are valid numbers
      return value as any; // Keep number literal syntax where appropriate
    default:
      return (type as unknown) as any; // Return whatever is passed in, preserving the original type for dynamic mapping.
  }
}

/**
 * Helper to determine the concrete TypeScript type based on a schema column definition.
 */
function getSchemaType(value: string | number): "string" | "integer" {
  if (typeof value === 'number') return "integer"; // Numbers are integers in C/C# style, even as literals like 1234567890
  
  switch (value) {
    case null:
      return undefined;
    case true:
      return boolean;
    default:
      if (typeof value === "string") return String(value); // Strings remain strings in C/C# style unless explicitly converted to number/integer elsewhere.
      throw new Error(`Unknown schema type for column "${value}"`);
  }
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value type or null to indicate missing column
}

// Helper to convert C-style struct/TS-like definitions into TypeScript types for easier mapping and dynamic schema generation.
export function parseAlchemySchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  const result = [];  
  
  Object.entries(schemaMap)
    .filter(([_, val]) => typeof val === "object" && Array.isArray(val)) // Only process arrays of values if they are objects (TS-like or JSON-like schemas)
    .forEach(([key, value]: [string, unknown[]]) => {
      const type = getSchemaType(value);  
      
      result.push({ key: key as string, name: "Column", schema_type: type });
    });

  return result;
}

/**
 * Helper to determine the concrete TypeScript type for a given value.
 */
function getSchemaValue(type: unknown): any {
  if (type === null || typeof type === 'undefined') return undefined as any; // Handle explicit null/undefined in schema definition directly
  
  switch (typeof type) {
    case "string":
      return String(value); // Convert to string for C-style compatibility or preserve original type.
    case "number":
      if (!isFinite(value)) return Number(value); // Ensure numeric types are valid numbers.
      return value as any; // Keep number literal syntax where appropriate.
    default:
      return (type as unknown) as any; // Return whatever is passed in, preserving the original type for dynamic mapping.
  }
}

/**
 * Helper to determine the concrete TypeScript type based on a
