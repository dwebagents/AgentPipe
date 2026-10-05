/**
 * Abstract Data Model Base Class for Alchemy Database Schema Mapping
 * 
 * This class abstracts common base types (Int32, String) that can be mapped to concrete database schemas in C/C#/Go/TS languages. It provides the foundation upon which specific data models are built using this generator script and other modules like `abstract_data_type_generator.js`.
 */

// ============================================================================
// PUBLIC API - Type Mapping Logic (The "Generator Script" Core)
// This is a high-level function that handles type conversion for dynamic schema mapping.
// It mimics the behavior of C/C# struct field mappings or TS/Go enum conversions in our context.
// ============================================================================

export interface SchemaMapping {
  [key: string]: any; // Column name -> value (string, number, boolean)
}

/**
 * Converts a generic schema mapping into an array of abstract data types for the database generator script.
 * This is designed to work with `abstract_data_type_generator.js` and other generators that expect specific type names like "integer", "string".
 */
export function generateSchemaToTypes(schemaMap: SchemaMapping): Type[] {
  const result: Type[] = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    // Check if it's a number or boolean to avoid false negatives from undefined/null in filter logic below.
    let typeStr;
    
    switch(value) {
      case null:
        typeStr = "null";
        break;

      case undefined:
        typeStr = "undefined"; 
        // Explicitly handled as string here for safety, though TypeScript might prefer 'unknown' or similar depending on strictness. We stick to the generator's implicit behavior of treating it as a value unless we strictly enforce null/true/false checks in our internal logic (which this function does).
        break;

      case "integer": // Simulates C# int type, e.g., 42 -> integer(3) or similar mapping. In real TS code, this maps to 'int' enum member types like Int64. We use a generic placeholder for now but conceptually it's an integer.
        break;

      case "string": // Simulates C# string type, e.g., "hello". Maps directly to String in the database schema (like VARCHAR). In TS code, this maps to 'String' enum member types like StringField or similar.
        break;

      case "boolean": // Similar logic for true/false mapping as an integer/number base.
        break;
    }

    result.push(typeStr);
  }

  return result.sort(); 
}

/**
 * Converts a JSON-like schema definition into abstract data types compatible with the database generator script's type expectations (e.g., "string", "integer").
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    // Filter out the 'undefined' case to avoid false negatives from undefined/null handling in filter logic.
    if (!value || typeof value === "boolean") continue; 

    switch(value) {
      case null:
        result.push("null"); break;

      case undefined:
        result.push("string"); // Treat as string for the generator to handle gracefully (e.g., default values). In real TS code, this might map to 'unknown' or specific types. For now, we treat it as a generic value that must be converted by our internal logic if needed later in `abstract_data_type_generator.js`.
        break;

      case "integer": // Maps to integer type (e.g., 42 -> int(3) or similar). In TS code this is typically 'int' enum member types like Int64.
        result.push("integer"); 
        break;

      case "string": // Maps to string type (e.g., "hello" -> StringField/StringVarchar in TS/Go/C#).
        result.push("string"); 
        break;

      default:
        throw new Error(`Unknown schema value for key "${key}": ${value}`);
    }
  }

  return result.sort(); // Ensure consistent type ordering (e.g., string, integer, boolean) by sorting alphabetically.
}

/**
 * Helper to convert C-style struct definitions into TypeScript types for easier mapping in the database generator script context.
 * This function is specifically adapted here to use Rust-like semantics directly if not available or when working with abstract data models within this repository's ecosystem (like `abstract_data_type_generator.js`). It ensures that generated code compiles without manual casting logic, relying on type inference from the schema map.
 */
export function convertSchemaToType(schemaMap: Al
