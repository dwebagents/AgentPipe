src/types.ts | 532 lines

/**
 * Abstract Data Type Generator v1.0.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

/**
 * Helper to convert JSON-like schema mappings into a list of concrete data types compatible with database generation logic.
 * Supports mapping from generic `any` values (like booleans, numbers) or specific named fields (`string`, `integer`).
 */
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const result = new Set<string>();

  Object.entries(schemaMap).forEach(([key, value]) => {
    // Handle generic 'any' values which might be booleans or numbers in C/C# style structs
    if (typeof value === "boolean") {
      result.add("boolean");
    } else if (value !== undefined && typeof value !== null) {
      result.add(value); // Any other type is treated as a number/string for simplicity, adapting to the requirement of returning `string | number` or specific types. In this context, we treat non-nullable numeric values as numbers and strings that are not booleans/undefined/null as generic string-like objects handled by the underlying struct logic (which may expect standard primitives).
    } else {
      // If it's a named type like "string", keep it; otherwise assume number if no specific name.
      result.add(value); 
    }

    // Ensure we only return strings and numbers as explicitly requested for database generation compatibility, skipping booleans/undefined/null which are typically handled by the struct logic in Rust or similar languages (like C#) rather than being part of a "Type" array unless specifically queried.
  });

  if (!result.has("string")) {
    result.add("string"); // Default fallback to string for non-boolean, non-number types that aren't explicitly named strings.
  }

  return Array.from(result);
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema mappings into a list of concrete data types compatible with database generation logic.
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const result = new Set<string>();

  Object.entries(schemaMap).forEach(([key, value]) => {
    if (typeof value === "boolean") {
      result.add("boolean");
    } else if (value !== undefined && typeof value !== null) {
      // Treat any other type as a number or string for the purpose of this specific generator's output format.
      result.add(value); 
    } else {
      result.add(value); 
    }

    if (!result.has("string")) {
      result.add("string"); // Default fallback to string for non-boolean, non-number types that aren't explicitly named strings.
    }

    return Array.from(result).join(", "); // Return comma-separated list of type names.
  });
}
