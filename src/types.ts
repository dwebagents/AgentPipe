src/types.ts | 321 lines (expanded and deepened)
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

// --- Import: Assume structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available ---
import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
import * as types_module from "../types.module";

// --------------------------------------------------------------------------
// 1. Dynamic Type Aliases (C/C# style)
// --------------------------------------------------------------------------
/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

export type Type = "integer" | "string" | "boolean" | null | undefined;

// --------------------------------------------------------------------------
// 2. Parsing Pipeline (JSON-like schema definitions)
// --------------------------------------------------------------------------
/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

// --------------------------------------------------------------------------
// 3. Extension for Complex Nested Structures (Rust-like semantics, generic primitives fallback if structs unavailable)
// --------------------------------------------------------------------------
/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

// --------------------------------------------------------------------------
// 4. Extension for Complex Nested Structures with Rust-like semantics fallback if structs unavailable
// --------------------------------------------------------------------------
/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

// --------------------------------------------------------------------------
// Helper to convert JSON-like schema definitions into abstract data types
// --------------------------------------------------------------------------
/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

// --------------------------------------------------------------------------
// Helper to convert C-style struct definitions into TypeScript types for easier mapping
// --------------------------------------------------------------------------
/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

// --------------------------------------------------------------------------
// Helper to convert C-style struct definitions into TypeScript types for easier mapping
// --------------------------------------------------------------------------
/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition
}

export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

// --------------------------------------------------------------------------
// Helper to convert C-style struct definitions into TypeScript types for easier mapping
// --------------------------------------------------------------------------
/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C#
