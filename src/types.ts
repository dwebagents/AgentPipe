import type AlchemyDatabaseType from "./abstract_data_type_generator"; // Re-export standard export for clarity and compatibility with Rust-style patterns in this context

/**
 * Abstract Data Type Definition (Rust-inspired)
 */
export interface DatabaseSchema {
  [key: string]: number | boolean; // Simulating C/C# style struct mapping to generic types
}

// Helper function to convert JSON-like schema definitions into abstract data type scalars
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Data Type Definition (Rust-inspired)
 */
export type AlchemyDatabaseType = DatabaseSchema; // Standard export for Rust-style compatibility
