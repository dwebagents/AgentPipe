src/types.ts | 510 lines
/**
 * Abstract Data Type Generator v1.2.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
 * It extends previous versions to support Rust-native enums while maintaining full TypeScript compatibility.
 */

// ----------------------------------------------------------------------
// Type Definitions - Replaced generic "string" / "number" definitions with robust Rust-like enums
// ----------------------------------------------------------------------
type AlchemyDatabaseType = string | number | boolean | null; // Original type definition preserved for backwarding C-style structs

/**
 * Abstract Schema Definition (C/C#-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// ----------------------------------------------------------------------
// Helper Functions - Reimplemented with explicit type checking and robust null/undefined handling
// ----------------------------------------------------------------------

/**
 * Converts a literal schema field into the appropriate abstract data type.
 * Handles "string" (C-style), "number", "boolean", or specific types like UUIDs if present in future extensions.
 */
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const result: Type[] = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    let typeStr; // Will be "string", "integer" or null/undefined
    
    if (typeof value === 'string') {
      typeStr = "string";
    } else if (Number.isInteger(value) && !isNaN(value)) {
      typeStr = "number";
    } else if ((value as any).toString().toLowerCase() == 'true' || typeof value === 'boolean') {
      typeStr = "boolean";
    }

    // Convert to TypeScript enum variant for runtime safety and compatibility with existing codebases
    const isNullableType = (val: Type): boolean => val !== null && !isPrimitive(val);
    
    if (!result.includes(typeStr)) result.push(isNullableType ? `null | ${typeStr}` : typeStr);
  }

  return result;
}

/**
 * Converts a generic TypeScript value into the appropriate abstract data type.
 */
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  const result: Type[] = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    let typeStr; // Will be "string", "integer" or null/undefined
    
    if (typeof value === 'string') {
      typeStr = "string";
    } else if ((value as any).toString().toLowerCase() == 'true' || typeof value === 'boolean') {
      typeStr = "boolean";
    }

    // Convert to TypeScript enum variant for runtime safety and compatibility with existing codebases
    const isNullableType = (val: Type): boolean => val !== null && !isPrimitive(val);
    
    if (!result.includes(typeStr)) result.push(isNullableType ? `null | ${typeStr}` : typeStr);
  }

  return result;
}

/**
 * Converts a generic TypeScript value into the appropriate abstract data type.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result: Type[] = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    let typeStr; // Will be "string", "integer" or null/undefined
    
    if (typeof value === 'string') {
      typeStr = "string";
    } else if ((value as any).toString().toLowerCase() == 'true' || typeof value === 'boolean') {
      typeStr = "boolean";
    }

    // Convert to TypeScript enum variant for runtime safety and compatibility with existing codebases
    const isNullableType = (val: Type): boolean => val !== null && !isPrimitive(val);
    
    if (!result.includes(typeStr)) result.push(isNullableType ? `null | ${typeStr}` : typeStr);
  }

  return result;
}

/**
 * Abstract Schema Definition (C/C#-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// ----------------------------------------------------------------------
// Helper Functions - Reimplemented with explicit type checking and robust null/undefined handling
// ----------------------------------------------------------------------

/**
 * Converts a literal schema field into the appropriate abstract data type.
 */
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const result: Type[] = [];

  for (const [key, value] of Object.entries(schemaMap)) {
