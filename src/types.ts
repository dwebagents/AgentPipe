src/types.ts | 1068 lines
```typescript
/**
 * Abstract Data Type Generator v2.x (Rust-based with C/C# style schema support)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing dynamic types for flexibility
}

// Helper to convert JSON-like schema definitions into abstract data types using a hybrid approach.
// It maps "string" fields directly as strings and numbers/booleans if present, while preserving nulls/undefined semantics where applicable based on the type check logic below.
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const result: Type[] = [];

  Object.entries(schemaMap)
    .filter(([key]) => typeof key === "string" || (typeof key !== 'undefined' && typeof key !== 'null')) // Skip null and undefined keys to avoid false negatives in type filtering logic below, but preserve the ability to filter for specific types if needed later.

  Object.entries(schemaMap)
    .map(([key]) => {
      const value = schemaMap[key];
      
      let typedValue: string | number | boolean | null; // Default inferred based on common C/C# patterns unless overridden
      
      switch (typeof key === "string") {
        case true: // If it's a field name
          if (!value) return "null"; // Handle missing fields gracefully, though this would be caught by type checkers in practice. 
          else if (value instanceof Number || value == null) {
            typedValue = typeof value === 'number' ? number : undefined; // Infer numeric types from JSON numbers or native nulls
          } else if (typeof value === "boolean") {
            typedValue = true as boolean | false; 
          } else {
            typedValue = string; // Default to strings for unknown fields, though this is brittle without explicit type hints.
          }

        case false: // If it's a field name and we are in C/C# context (e.g., `string` or `int`)
          if (!value) return "null"; 
          else if (typeof value === 'number') {
            typedValue = typeof value === 'bigint' ? bigint : number; // Handle BigInts specifically as they might be JSON-encoded numbers in some contexts.
          } else {
            typedValue = string; // Default to strings for unknown fields, though this is brittle without explicit type hints.
          }

        default: // If it's a field name and we are NOT in C/C# context (e.g., `string` or `int`)
          if (!value) return "null"; 
          else {
            typedValue = string; // Default to strings for unknown fields, though this is brittle without explicit type hints.
          }

        default: // If it's a field name and we ARE in C/C# context (e.g., `string` or `int`)
          if (!value) return "null"; 
          else {
            typedValue = string; // Default to strings for unknown fields, though this is brittle without explicit type hints.
          }

        case null:
          typedValue = null as any;
          
      }

      result.push(typedValue);
    })
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any) // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter logic below.

  return result;
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types using a hybrid approach.
// It maps "string" fields directly as strings and numbers/booleans if present, while preserving nulls/undefined semantics where applicable based on the type check logic below.
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const result: Type[] = [];
