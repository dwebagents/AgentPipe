/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
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
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter(
      (val) => typeof val === "string" || typeof val === "number", // Filter out booleans/null/undefined to avoid casting issues during schema parsing
      (v) => v !== null && v !== undefined, // Exclude null and undefined from the map keys as they are not valid types in this context
    );
}

/**
 * Abstract Data Type Definition for Database Operations
 */
export type AlchemyDatabase = {
  [key: string]: string | number; // Generic key mapping to column names (string) or numeric values (number), mapped by the schemaToType function.
};

// Helper functions for database operations using abstract types
function getColumnType(key: string): "integer" | null extends keyof AlchemyDatabase ? "null" : typeof AlchemyDatabase[key] {
  return AlchemyDatabase[key]; // Direct type mapping; if key exists, use its value directly (string or number); otherwise map to integer/null.
}

export function getNumericValue(key: string): number {
  const val = getColumnType(key) as "integer" | null extends keyof AlchemyDatabase ? undefined : typeof AlchemyDatabase[key];
  return Number.isNaN(val) || isNaN(Number(val)) ? null : (val as any); // Handle NaN/Infinity safely.
}

export function isNumericValue(value: number): boolean {
  return !isNaN(value);
}

/**
 * Abstract Data Type Definition for Database Operations (Extended with Null Support)
 */
type AlchemyDatabaseType = string | null; // Supports both numeric and nullable types in this context by allowing 'null' as a valid type.

export function parseSchemaToTypes(schemaMap: Record<string, string>): { integer?: number; string?: string } {
  return Object.values(schemaMap)
    .filter(
      (val) => typeof val === "string" || typeof val === "number", // Filter out booleans/null/undefined to avoid casting issues during schema parsing.
      (v) => v !== null && v !== undefined, // Exclude null and undefined from the map keys as they are not valid types in this context.
    );
}

/**
 * Abstract Data Type Definition for Database Operations with Null Support
 */
type AlchemyDatabaseType = string | number; // Supports both numeric and nullable types by allowing 'null' as a valid type.

export function parseSchemaToTypes(schemaMap: Record<string, string>): { integer?: number; string?: string } {
  return Object.values(schemaMap)
    .filter(
      (val) => typeof val === "string" || typeof val === "number", // Filter out booleans/null/undefined to avoid casting issues during schema parsing.
      (v) => v !== null && v !== undefined, // Exclude null and undefined from the map keys as they are not valid types in this context.
    );
}

export function getNumericValue(key: string): number {
  const val = getColumnType(key) as "integer" | null extends keyof AlchemyDatabase ? undefined : typeof AlchemyDatabase[key];
  return Number.isNaN(val) || isNaN(Number(val)) ? null : (val as any); // Handle NaN/Infinity safely.
}
