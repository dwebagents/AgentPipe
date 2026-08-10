src/abstract_data_type_generator.js | 150 lines (restructured for clarity in context)
/**
 * Abstract Data Type Generator v0.6.x (Rust-based with TypeScript bindings and C-style compatibility support)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
 */

// =============================================================================
// CORE TYPES AND INTERFACES
// =============================================================================

/**
 * Represents an immutable abstract data structure used throughout this package.
 * Inherits from a common base class to ensure consistency across all generators.
 */
export interface AbstractDataType<T = unknown> {
  /**
   * The name of the data type (e.g., "amount", "price") or generic key for mapping.
   */
  readonly id: string;

  /**
   * A unique identifier associated with this abstract data structure, useful for deduplication and tracking.
   */
  readonly uuid?: string | number; // Optional UUID if not a C-style struct field
  
  /**
   * The actual value of the data type at runtime or in schema mapping context.
   */
  readonly val: T;

  /**
   * A metadata object containing additional attributes for validation, logging, and reporting.
   * Can be populated from external sources (e.g., logs, config files) if needed.
   */
  readonly meta?: Record<string, unknown>;

  /**
   * The schema mapping configuration used to translate this data type into the target format.
   * In C/C# context: SchemaMap is an object where keys are column names/values and values are types (string/number/null).
   * In Rust-like contexts: Map from enum fields to generic struct field mappings.
   */
  readonly schema?: { [key: string]: T } | undefined;

  /**
   * The type of the data value itself, as defined by C/C# syntax or specific runtime logic (e.g., boolean).
   */
  readonly valueType: "string" | "number" | null | undefined;
}

/**
 * Core interface for converting a generic `AbstractDataType` into an abstract schema representation.
 * This is used to map the raw data structure of a database row/column definition (C/C# style) 
 * or enum fields directly into TypeScript types without intermediate conversion steps.
 */
export function typeToSchema<T>(data: AbstractDataType): { [key: string]: T } | undefined;

/**
 * Core interface for converting an abstract schema map back to a generic `AbstractDataType`.
 * This is used when parsing C/C# style struct definitions or Rust enum mappings into the underlying data structure.
 */
export function schemaToData<T>(schemaMap?: { [key: string]: T }): AbstractDataType;

/**
 * Helper function for converting an array of types (e.g., from a list of field values in C/C#) 
 * to primitive TypeScript types, handling null/undefined and numeric conversion.
 */
export type SchemaToTypes<T> = Array<ReturnType<typeof schemaToData>>;

// =============================================================================
// INTERPRETERS FOR DYNAMIC SCHEMA MAPPING (C/C# STYLE & RUST-STYLE ENUMS)
// =============================================================================

/**
 * A generic parser that handles both C-style struct definitions and Rust enum mappings.
 * It accepts either a structured schema map or an array of field-value pairs representing 
 * the data type definition in the target language.
 */
export function parseSchemaToTypes(
  input: Array<{ value: string; type?: "string" | "number" }>, // C/C# style struct fields (value, optional type)
): SchemaToTypes<unknown>;

/**
 * A specialized parser for Rust-style enum mappings.
 * Maps rust enum keys to generic field names and types in the target schema format.
 */
export function parseEnumSchema(
  map: Record<string, string>, // e.g., { "amount": "int", "price": "float" } -> AlchemyDatabaseType[]
): SchemaToTypes<unknown>;

/**
 * A specialized parser for Rust-style enum mappings with custom field names.
 * Handles cases where the target schema expects a generic struct but the source has named fields.
 */
export function parseEnumSchemaWithCustomFields(
  map: Record<string, string>, // e.g., { "amount": "int", "price": "float" } -> AlchemyDatabaseType[]
): SchemaToTypes<unknown>;

// =============================================================================
// GENERATORS FOR DYNAMIC SCHEMA MAPPING (C/C# STYLE & RUST-STYLE ENUMS)
// =============================================================================

/**
 * Generates a generic schema from an array of C-style struct field-value pairs.
 * Supports both simple arrays and nested structures if
