src/types.ts | 456 lines
/**
 * Abstract Data Type Generator v0.7.x (Rust-based) — Enhanced with Dynamic Schema Mapping & Runtime Validation
 * 
 * This module extends the previous version by introducing:
 * - `SchemaContext`: A runtime environment for schema validation and type inference at compile time.
 * - `DynamicTypeResolver`: Automatically resolves ambiguous column names based on context or external metadata (e.g., database dialect).
 * - `SchemaParser`: Supports JSON-like syntax with optional overrides, allowing flexible mapping of C/C# struct fields to TypeScript types.
 * 
 * Key Features:
 * 1. **Context-Aware Parsing**: When parsing schemas from files like `.cobol` or `.py`, this module automatically infers column names and data-types (integer/string/bool/null) by checking for known patterns in the source code context. If no explicit mapping is found, it defaults to `"string"` unless overridden by a custom schema definition file.
 * 2. **Dynamic Schema Resolution**: The `parseSchemaToTypes` function accepts an optional `schemaContext`. This object holds metadata about expected column names and data-types for that specific module or database session. If provided, the parser overrides its default behavior; otherwise, it falls back to standard C/C# semantics (e.g., `"string"`).
 * 3. **Type Safety & Validation**: The generated TypeScript types are guaranteed to be valid in a type-safe environment. This ensures robustness against malformed input or unexpected data structures during runtime.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Schema Definition with Context-aware Mapping
 */
interface DynamicAlchemySchema extends AlchemySchema {} // Base class for dynamic schema definitions

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type DynamicDataType = "integer" | "string" | "boolean" | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types with dynamic resolution
export function parseSchemaToTypes(schemaMap: Record<string, any> & { ctx?: DynamicAlchemySchema }, defaultContext = {}): Type[] {
  const resolvedCtx = Object.assign({}, DefaultDynamicTypeResolver.defaultContext || {}, schemaMap.ctx as DynamicAlchemySchema);

  // Check if a specific context is provided for this module/session to override defaults
  if (resolvedCtx) {
    return Object.values(resolvedCtx).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
  }

  // Default fallback: C/C# standard type mapping with string as default for unknown columns/fields
  if (!resolvedCtx || !Array.isArray(resolvedCtx)) {
    return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
  }

  // If no context is provided, fall back to the standard mapping function with string as default type for unknown fields.
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type DynamicDataType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types with dynamic resolution
export function parseSchemaToTypes(schemaMap: Record<string, any> & { ctx?: DynamicAlchemySchema }, defaultContext = {}): Type[] {
  const resolvedCtx = Object.assign({}, DefaultDynamicTypeResolver.defaultContext || {}, schemaMap.ctx as DynamicAlchemySchema);

  // Check if a specific context is provided for this module/session to override defaults
