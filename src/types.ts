src/types.ts | 548 lines
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator. It extends previous versions to include:
 * - Strict Rust/Go/Swift enum semantics where applicable.
 * - Full validation of column constraints (unique indexes, primary keys).
 * - Automatic inference from JSON-like schemas without manual string casting logic.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust/Go/Swift semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: StructType<string>; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val, key) => (typeof val === "string" ? StructType<string> : typeof val === "number" ? StructType<number> : null)); // Use struct type to ensure proper Rust/Go/Swift semantics for non-string values like numbers or booleans
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types using iterative parsing over keys. Handles booleans by checking `isBoolean` and non-strings/non-numbers separately, avoiding false negatives from undefined/null handling in filter logic previously used here.
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    // Convert the struct type to a generic TypeScript type if it's not already one or is an enum-like structure that would naturally be treated as such in Rust/Go contexts.
    let typedValue: unknown;
    
    switch (typeof value) {
      case "string":
        // If we have string values, treat them as strings unless they are booleans which might need special handling here to avoid false negatives from undefined/null filtering logic previously used for non-string types.
        if (!value || typeof value !== 'boolean') {
          typedValue = StructType<string>;
        } else {
            // Special case: boolean values in structs often map directly or require explicit check depending on the schema context (e.g., "is_active" vs just a bool). This specific function handles booleans by checking for undefined/null which are not strings/numbers, ensuring they pass through as true/false. However, to strictly adhere to C/C# behavior where `true` is boolean and no other value represents it in the struct context (e.g., if we see "1" or a number), this function would need more complex logic for specific schema contexts like booleans vs integers. For now, assuming standard non-boolean values are strings unless explicitly defined as such via type mapping elsewhere).
            // Actually, looking at the previous code provided in your prompt's snippet: `typeof val === "string" ? "string" : typeof val === "number" ? "integer"`. This logic is flawed for booleans. A boolean value like true should be a string or number depending on context (e.g., 1 vs false). But struct values are typically strings in C/C#.
            // Let's refine this to handle the specific case of booleans being represented as numbers/strings but not null/undefined, ensuring they pass through correctly. If `typeof val` is 'boolean', it returns "string" (matching C behavior) or we might need a separate check if values are strictly numeric strings like 1 and false.
            // Given the complexity of dynamic schema mapping without knowing exact types at compile time for every field, this function will treat all struct values as generic string unless they are explicitly boolean-like numbers that should be treated differently (e.g., in C/C# `bool` is a primitive type). Let's assume standard non-boolean structs map to strings.
            typedValue = StructType<string>; 
        } break;

      case "number":
          // If we have numeric values, treat them as integers unless they are booleans which would be numbers in some contexts but not C/C# primitives (
