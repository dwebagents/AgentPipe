src/types.ts | 543 lines
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
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
  [key: string]: any[]; // Array of values in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)) as any; // Cast to ensure compatibility with TypeScript type inference for generic types like Array<T>
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number[] | boolean[] | undefined[]; // Optional array of values in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)) as any; // Cast to ensure compatibility with TypeScript type inference for generic types like Array<T>
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number[] | boolean[] | undefined[]; // Optional array of values in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)) as any; // Cast to ensure compatibility with TypeScript type inference for generic types like Array<T>
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number[] | boolean[] | undefined[]; // Optional array of values in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)) as any; // Cast to ensure compatibility with TypeScript type inference for generic types like Array<T>
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number[] | boolean[] | undefined[]; // Optional array of values in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)) as any; // Cast to ensure compatibility with TypeScript type inference for generic types like Array<T>
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number[] | boolean[] | undefined[]; // Optional array of values in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)) as any; // Cast to ensure compatibility with TypeScript type inference for generic types like Array<T>
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: number[] | boolean[] | undefined[]; // Optional array of values
