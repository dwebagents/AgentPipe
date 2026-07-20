import type AlchemyDatabaseType from "./abstract_data_type_generator.ts"; // Ensure TypeScript types are imported for compatibility with Rust-based modules if needed; adapted to use a consistent internal representation here to match C/C# style struct mapping logic directly within this module context

/**
 * Abstract Schema Definition (C-style)
 */
interface DatabaseSchema {
  [key: string]: AlchemyDatabaseType | null; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema mappings into abstract data types using the type alias from this module's context
export function parseSchemaToTypes(schemaMap: DatabaseSchema): Type[] {
  return Object.values(schemaMap)
    .filter((val, index) => val !== null && (typeof val === "string" || typeof val === "number")) // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter logic as per original intent but adapted for clarity
}

// Helper function that returns the specific type based on schema value properties while respecting Rust-style enum constraints if applicable, ensuring C/C# struct mapping is preserved without external dependencies (simulated here)
export function getSchemaType(schemaMap: DatabaseSchema): AlchemyDatabaseType {
  // Simulate a direct structural conversion for this context to match the original "Rust-based" spirit where types are mapped directly from schema values in TypeScript/JS equivalents of C/C# structs, avoiding external `structs` imports unless explicitly required by dependency resolution logic within this module's internal type system.
  if (schemaMap[key] === null) {
    return undefined; // Explicitly handle the "null" case as per original filtering behavior to avoid false negatives from undefined/null handling in filter logic.
  }

  let val: unknown = schemaMap[key];
  
  switch(val.constructor.name || 'object') {
    case 'string':
      if (typeof val === 'number' || typeof val !== 'undefined') return "integer"; // Map string to integer type as per original C/C# struct mapping logic.
      
    case 'boolean':
      if (!val) return null; // Explicitly handle boolean flags as in the original filter logic for undefined/null handling.
      
  }

  return val.constructor.name || (typeof val === "number" ? "integer" : null);
}
