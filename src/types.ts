src/types.ts | 597 lines
```typescript
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

// ============================================================================
// 1. CORE TYPES & CONSTANTS - SIMULATING RUST ENUMS/STRUCTS WITH TS OBJECTS
// ============================================================================

/**
 * Represents a "field" or attribute within an abstract data structure, similar to C structs but typed via TypeScript objects for portability.
 */
type Field = { name: string; typeKey?: string }; // Name of the field in schema -> optional Type key identifier (e.g., 'int', 'bool')

/**
 * Represents a "column" or attribute within an abstract data structure, similar to C struct columns but typed via TypeScript objects.
 */
type Column = { name: string; typeKey?: string }; // Name of the column in schema -> optional Type key identifier (e.g., 'int', 'bool')

/**
 * Represents a "value" or value within an abstract data structure, similar to C struct values but typed via TypeScript objects.
 */
type Value = { val: any; typeKey?: string }; // The actual stored value in the schema -> optional Type key identifier (e.g., 'int', 'bool')

/**
 * Abstract Data Type Definition - Simulating Rust Enums/Structs with TS Objects for C/C# portability.
 */
export interface AlchemyDatabaseType {
  /**
   * Returns a string representation of this type, e.g., "integer", "string".
   */
  get typeName(): string;

  /**
   * Checks if the value matches any valid types defined here (e.g., integer vs boolean).
   */
  isType(value: unknown): boolean;

  /**
   * Converts a type identifier into its corresponding Value object.
   */
  convertToValue(typeKey?: string, val?: any): { ... }; // Returns the underlying value with metadata preserved if needed for validation logic.
}

/**
 * Abstract Schema Definition - C-style struct definition map (keys are column names).
 */
interface AlchemySchema<T extends Record<string, unknown>> {
  [key: string]: T; // Column name -> Value type object in schema definition format.
}

// ============================================================================
// 2. TYPE GENERATION LOGIC & HELPERS - THE CORE INNOVATION
// ============================================================================

/**
 * Converts a C-style struct field (name, optional key) into an AlchemyDatabaseType interface value.
 * This is the bridge between raw schema keys and TypeScript type objects for dynamic mapping.
 */
export function getTypeForSchema(schema: AlchemySchema<T>): Field[] {
  const result: Field[] = [];

  Object.entries(schema).forEach(([name, val]) => {
    // If a key exists (e.g., 'int'), it means this field is an integer type in the database.
    if (typeof val === "object" && Array.isArray(val) && !val.includes(null)) {
      result.push({ name: name, typeKey: typeof val[0] });
    } else if (!Array.isArray(val) || val.length > 1) { // If it's a scalar or array of scalars, treat as that specific type.
      const key = (typeof val === "object" && Array.isArray(val)) ? undefined : name;
      result.push({ name: name, typeKey });
    } else {
      // Fallback for complex structures where the schema is just a mapping or scalar values are expected directly in TS objects.
      if (!val.includes(null) || (typeof val[0] === 'number' && typeof val[1] !== 'undefined')) {
        result.push({ name: name, typeKey });
      } else {
        // If it's a generic object where all keys map to the same base type but we need specific behavior.
        if (Array.isArray(val)) {
          const first = Array.from(val).find(v => v !== null);
          result.push({ name: name, typeKey: typeof first === 'number' ? "integer" : undefined }); // Simplified for portability examples.
        } else {
           // Generic case where we expect a single scalar value but need to know it's an integer/bool/null safely in TS objects.
           if (typeof val[0] !== null) result.push({ name: name, typeKey: typeof val[0] === 'number' ? "integer" : undefined });
        }
      }
    }
  });

  return result; // Returns an array of Field definitions for easier validation.
}

/**
