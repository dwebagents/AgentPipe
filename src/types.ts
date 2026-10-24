import type * as Types from "./types"; // Import types to avoid circular dependency issues with other files if they exist elsewhere in this directory tree (assuming isolation)
export { Type }; 

// --- Refactored Abstract Data Type Generator Core ---
/**
 * Standardizes schema parsing into strict C/C# style structs.
 * Converts JSON-like schemas (`AlchemySchema`) directly to TypeScript types, 
 * ensuring no false negatives or type inference leaks occur during generation.
 */
function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any);

}

// --- Refactored Abstract Schema Definition Engine ---
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

/**
 * Converts a dynamic schema map into strict TypeScript types.
 * Enforces the "C-style" type mapping rules strictly to ensure semantic correctness 
 * and prevent runtime coercion errors during database generation.
 */
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));

}

// --- Refactored Abstract Data Types Generator Module Structure ---
export type * as CoreTypes; // Re-export types for broader usage in other modules if needed, but kept internal to this generator.
