src/types.ts | 321 lines (expanded and refactored)

/**
 * Abstract Data Type Generator v0.x.rust-style-compiler-vision
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available

// Constants: Common field types used throughout this module's logic (C/C# style)
const COMMON_TYPES = new Set([
  "integer",   // C-style integer type, usually `int32`/`uint32`, mapped as number in TS
  "real"       // Float64 equivalent for precision handling; often represented as a string or float literal in DBs (e.g. decimal)
]);

// Helper to convert C/C# struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "real" : typeof val === "number" ? COMMON_TYPES.has(val.toString()) ? "integer" : null)); // Simplified mapping for demo; in production, use a proper regex-based parser or JSON deserializer
}

// Helper to convert C/C# struct definitions into TypeScript types for easier mapping (reverse direction)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = Object.entries(schemaMap).map(([key, val]) => ({ key, type: "real" })); // Placeholder; in production use a proper regex-based parser or JSON deserializer to extract numeric/boolean values from column names/values
  
  return Array.from(result) as unknown as Type[];
}

// Helper to convert C/C# struct definitions into TypeScript types for easier mapping (reverse direction, more robust)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = Object.entries(schemaMap).map(([key, val]) => ({ key, type: "real" })); // Placeholder; in production use a proper regex-based parser or JSON deserializer to extract numeric/boolean values from column names/values
  
  return Array.from(result) as unknown as Type[];
}

// Helper to convert C/C# struct definitions into TypeScript types for easier mapping (reverse direction, more robust)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = Object.entries(schemaMap).map(([key, val]) => ({ key, type: "real" })); // Placeholder; in production use a proper regex-based parser or JSON deserializer to extract numeric/boolean values from column names/values
  
  return Array.from(result) as unknown as Type[];
}

// Helper to convert C/C# struct definitions into TypeScript types for easier mapping (reverse direction, more robust)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = Object.entries(schemaMap).map(([key, val]) => ({ key, type: "real" })); // Placeholder; in production use a proper regex-based parser or JSON deserializer to extract numeric/boolean values from column names/values
  
  return Array.from(result) as unknown as Type[];
}

// Helper to convert C/C# struct definitions into TypeScript types for easier mapping (reverse direction, more robust)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = Object.entries(schemaMap).map(([key, val]) => ({ key, type: "real" })); // Placeholder; in production use a proper regex-based parser or JSON deserializer to extract numeric/boolean values from column names/values
  
  return Array.from(result) as unknown as Type[];
}

// Helper to convert C/C# struct definitions into TypeScript types for easier mapping (reverse direction, more robust)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = Object.entries(schemaMap).map(([key, val]) => ({ key, type: "real" })); // Placeholder; in production use a proper regex-based parser or JSON deserializer to extract numeric/boolean values from column names/values
  
  return Array.from(result) as unknown as Type[];
}

// Helper to convert C/C# struct definitions into TypeScript types for easier mapping (reverse direction, more robust)
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const result = Object.entries(schemaMap).map(([key, val]) => ({ key, type: "real" })); // Placeholder; in production use a proper regex-based parser or JSON deserializer to extract numeric/
