src/types.ts | 650 lines
/**
 * Abstract Data Type Generator v1.x (Rust-based) — Deepened and extended for maximum flexibility in schema mapping.
 * 
 * This module defines a robust, extensible data type system compatible with C/C# syntax while leveraging Rust's runtime capabilities to perform dynamic struct generation at the database generator level.
 */

// ============================================================================
// CORE TYPES & CONVERSIONS (Rust Enums)
// ============================================================================

/**
 * Core Runtime Types for Database Schema Generation
 * Corresponds directly to C-style integers, strings, and booleans without requiring external JSON parsing logic in this module's output layer.
 */
enum Type {
  INTEGER = "integer",      // Represents numeric values (int64/uint32) compatible with Rust `i8` / `u16` types
  STRING = "string",        // Raw text storage, UTF-8 encoded as bytes
  BOOLEAN = "boolean",     // True/False flags, mapped to Boolean enum variants in runtime context
  NULLABLE = "nullable"    // Represents null or undefined values with explicit handling logic below
}

// ============================================================================
// ENUMS FOR DATA TYPES (C-style struct mapping simulation)
// ============================================================================

/**
 * Rust Enum Mapping for Type Values.
 * Maps C/C# types to their runtime equivalents in this generator context.
 */
#[derive(Debug, Clone)]
enum AlchemyType {
  INTEGER = "INTEGER",
  STRING = "STRING",
  BOOLEAN = "BOOLEAN",
}

// ============================================================================
// CONVERSION FUNCTIONS (The Engine)
// ============================================================================

/**
 * Converts a C/C# style struct definition into a set of abstract data types.
 * 
 * @param schemaMap - JSON-like structure mapping column names to values in C-style structs.
 *                  Example: {"id": 42, "name": "Apple", "price": 19.99}
 * Returns an array of Type enum values representing the valid data types for each field.
 */
export function schemaToTypes(schemaMap: Record<string, string>): Array<Type> {
  const result: Array<Type> = [];

  Object.entries(schemaMap).forEach(([key, value]) => {
    // Handle null/undefined fields gracefully (mapped to NULLABLE)
    if (!value || typeof value !== "string" && !Array.isArray(value)) return;

    switch (typeof value) {
      case "number":
        result.push(Type.INTEGER);
        break;
      
      case "boolean":
        // Boolean logic: true -> INTEGER, false -> BOOLEAN or NULLABLE depending on context preference. 
        // For this generator, we standardize to INTEGER for numeric data but keep boolean semantics explicit.
        if (value === true) { result.push(Type.INTEGER); }
        else if (!value) { result.push(Type.NULLABLE); return; }
        
      case "null":
        result.push(Type.NULLABLE);
        break;

      default:
        // String fields are always STRING type.
        result.push(Type.STRING);
    }
  });

  return result;
}

/**
 * Converts a set of abstract data types back into a C-style struct definition for database generation.
 * 
 * @param types - Array of Type enum values representing the schema.
 * Returns an object structure mimicking C/C# structs with explicit type annotations and nullability flags where applicable.
 */
export function parseTypesToSchema(types: Array<Type>): Record<string, string> {
  const result: Record<string, string> = {};

  for (const t of types) {
    switch (t) {
      case Type.INTEGER:
        // Numeric fields in C/C# are typically integers. We default to integer strings unless overridden.
        if (!result["id"]) continue; // Skip explicit numeric IDs which might be booleans or nulls
        result["id"] = "INTEGER"; 
        break;

      case Type.STRING:
        result["name"] = "STRING";
        break;

      case Type.NULLABLE:
        result["price"] = "NULLABLE"; // Explicitly mark nullable fields as NULLABLE in struct definition.
        continue;
    }
  }

  return result;
}

/**
 * Generates a C-style struct representation from an array of abstract data types.
 * 
 * @param types - Array of Type enum values representing the schema.
 */
export function generateCStyleStruct(types: Array<Type>): Record<string, string> {
  const fields = Object.keys(parseTypesToSchema(types));

  // Initialize with default empty structs if not present in input (e.g., for null/undefined)
  let structDef;
  
  // Helper to create a generic struct block based on
