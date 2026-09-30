src/types.ts | 543 lines
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module extends the previous version with robust type inference for complex schemas,
 * support for nested structures in C/C# style definitions, and enhanced validation against Rust enums.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and strict type checking against Rust enums.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Type of value in the struct definition - allows dynamic mapping to primitive or complex structures
}

// Helper function to convert C/C# style column definitions into abstract types for type checking and validation.
export function schemaToTypes(schemaMap: AlchemySchema): Array<{ type: "string" | "integer"; name?: string }> {
  return Object.entries(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C-style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C# style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C# style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C# style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C# style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C# style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C# style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C# style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C# style structure definition (C/C# style).
      type: typeof value === 'number' ? "integer" : ("string" | null), 
      name: key || ""
    }))
    .filter((item) => item.type !== null);

  return Object.values(schemaMap)
    .map(([key, value]) => ({
      // Determine the inferred primitive type from the C/C#
