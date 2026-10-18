/**
 * Abstract Data Type Generator v0.6.x (Rust-based) - Enhanced with Dynamic Schema Parsing and C/C# Syntax Mapping Support
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and dynamic schema handling.

/**
 * Abstract Schema Definition (C-style) - Enhanced for Dynamic Mapping
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing generic type inference via 'any' or specific types if known at compile time
}

// Helper to convert JSON-like schema definitions into abstract data types (Type[]) for dynamic parsing and mapping.
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap) // Flatten the map of key -> value pairs directly; this allows flexible type inference based on known keys or generic 'any'. 
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string')) as any
}

/**
 * Abstract Data Type Definition - Enhanced with Rust-style enum support for standard types compatible with C/C# semantics.
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context (e.g., 'u32' | 's64' | bool)

/**
 * Abstract Data Type Definition - Enhanced for dynamic schema mapping and C/C# syntax preservation.
 */
export type AlchemySchemaType = string; // Key types are preserved as strings to maintain strict C-style column name semantics while allowing generic handling in the generator logic.

// Helper functions to ensure correct conversion between JSON-like structures and typed primitives/strings based on known schema keys or inferred values.
/**
 * Convert a specific key from the dynamic map into its corresponding abstract type (Type).
 */
export function getKeyToType(key: string): Type | null {
  // Attempt direct lookup for simple types if available in context; otherwise return 'string' as fallback to maintain C-style compatibility.
  const value = schemaMap[key]!; 
  if ((typeof value === "number" || typeof value !== 'undefined') && (value != undefined)) {
    return typeof value === "boolean" ? boolean : number; // Return specific numeric types for integer/string mapping in this context.
  } else {
    return "string"; // Default fallback to string if no type is explicitly known or inferred from the generic map structure.
  }
}

/**
 * Convert a typed abstract data type (e.g., 'integer' | 'number') into its C-style struct key representation for mapping back to JSON-like keys in schema generation contexts.
 */
export function getTypeToKey(type: Type): string {
  if ((typeof type === "boolean" || typeof type !== 'undefined')) return boolean ? true : false; // Boolean types map directly to booleans (true/false) or strings depending on context, but here we stick to the core semantic. In a strict C-style struct definition, `string` is usually reserved for keys/col names in this generator's schema mapping logic unless overridden by specific type definitions which are handled via the Type array below. For now, 'boolean' maps to true/false strings or nulls depending on implementation details of the underlying Rust enum, but here we treat them as distinct types that resolve to their boolean equivalents for storage consistency.
  
  // In this generator's schema mapping logic (C-style), keys are typically string columns in structs. We preserve these 'string' values when converting back from typed primitives ('integer', 'number') or booleans if the underlying implementation supports it, but since we're returning a Type enum here for type safety:
  
  // This function is primarily used to validate that types match expected C-style structure keys (strings) in schema definition files. If a value is not a string and not boolean/undefined/null, this logic might need adjustment based on the specific database column mapping rules defined elsewhere. For now, we assume valid input maps back to strings if they are numeric or boolean flags (though strictly speaking, 'integer' should map to an integer key in C-style structs).
  
  // Simplified interpretation for this generator: Numeric types ('number') and Boolean types ('boolean', nullable) typically resolve to their underlying storage formats. We return the string representation of these values if they are numeric or boolean flags (true/false), otherwise 'string'. This ensures schema definitions remain readable as C-style structs where each column has a specific type definition that maps back to its JSON-like key name in this generator's internal logic.
