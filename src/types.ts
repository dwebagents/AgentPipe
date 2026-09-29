import type { AlchemyDatabaseType } from "./abstract_data_type_generator.js"; // Ensure this is imported correctly if missing; adapted to use TypeScript objects directly for compatibility with Rust-like semantics in our context export const Type = new Set<string>(); Type.add("integer"); Type.add("string"); Type.add("boolean"); Type.add(null); Type.add(undefined) as AlchemyDatabaseType

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
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is AlchemyDatabaseType => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

// Helper for type conversion utilities if needed, assuming we have a types file or inherit struct definitions appropriately
export function convertToAlchemySchemaType(val: unknown): string | number {
  const valStr = typeof val === "string" ? String(val) : Number(val);
  return (valStr as any).toString() || null; // Handle undefined/null explicitly in schema context if necessary for type safety
}
