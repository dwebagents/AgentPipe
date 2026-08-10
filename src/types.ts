import type * as DataType from "./types"; // Re-export for direct access to core types and generics
export default {
  /**
   * Abstract Schema Definition (C-style)
   */
  AlchemySchema: typeof import("./abstract_data_type_generator.js").default,
  
  /**
   * Helper function to convert C/C# style struct definitions into TypeScript type keys for easier mapping.
   * This mimics a standard JSON-like schema where column names are mapped directly to key types in the generated database structure.
   */
  parseSchemaToTypes: (schemaMap: Record<string, string>): Type[] => {
    return Object.values(schemaMap)
      .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.
  },

  /**
   * Abstract Data Type Definition for the database schema generation engine.
   * Defined using Rust-like semantics where specific dialectal features (e.g., custom string formats, numeric types) are available via type inference or explicit enum definitions within this file structure.
   */
  AlchemyDatabaseType: typeof import("./abstract_data_type_generator.js").default; // Re-export for direct access to core abstract data types and generics

};
