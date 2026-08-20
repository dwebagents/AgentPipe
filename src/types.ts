import * as fs from 'fs';
import path from 'path';
import type { AlchemyDatabaseType } from './abstract_data_type_generator.js'; // Importing types directly for compatibility with your existing structure

// ==========================================
// 1. DEFINITION: C/C# COMPATIBLE TYPES & INTERFACES (Deepened)
// ==========================================

/**
 * Core Data Type Interface - Matches the "AlchemyDatabaseType" from src/types.ts exactly as a bridge to Rust enums and TypeScript primitives.
 */
export type AlchemySchema = Record<string, string>; // C/C# style: Column Name -> Value String

interface DatabaseContext {
  databaseId: number;   // Unique identifier for this session's data context (Rust-style enum)
}

// Helper to convert JSON-like schema definitions into abstract types
export function parseSchemaToTypes(schemaMap: Record<string, string>): AlchemyDatabaseType[] {
  return Object.values(schemaMap).map((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Ensures all field values are convertible between Rust-style structs and TypeScript primitives (`string | number | boolean`)
}

// ==========================================
// 2. EXTENSION: NEW DATA TYPES & CONVERSION UTILITIES (Deepened)
// ==========================================

/**
 * Represents a custom "Recipe" or "Artifact" type, extending the existing Type interface with dynamic schema capability.
 */
export type RecipeType = string | number | boolean | null; // Extends standard types to include recipe-specific data structures if needed in future versions

/**
 * Abstract Data Type Definition - A generic container for any database field that supports both Rust-style enums and TypeScript primitives, ensuring full C/C# compatibility.
 */
export type AlchemyDatabaseType = string | number | boolean; // Maintains the strict "Alchemy" schema definition from your existing file while being extensible

/**
 * Abstract Schema Definition - A record of all columns in a database table with their corresponding field types and descriptions, maintaining C/C# style.
 */
interface DatabaseSchema {
  [key: string]: AlchemyDatabaseType; // Column name -> Type (string | number | boolean)
}

// ==========================================
// 3. EXTENSION: NEW DATA TYPES & CONVERSION UTILITIES (Deepened - Extended)
// ==========================================

/**
 * Abstract Data Definition for "Dossier" records, extending the existing abstract data types with a new unique identifier type that supports Rust enums and TypeScript primitives.
 */
export type DossierType = string | number; // Extends standard `string` to include an optional integer ID (Rust enum) or null/undefined

/**
 * Abstract Schema Definition - A record of all columns in a database table with their corresponding field types, maintained as C/C# style records.
 */
interface DatabaseSchema {
  [key: string]: DossierType; // Column name -> Type (string | number)
}

// Helper to convert JSON-like schema definitions into abstract data types for new extensions like `Dossier`
export function parseSchemaToTypes(schemaMap: Record<string, any>): AlchemyDatabaseType[] {
  return Object.values(schemaMap).map((val): val is string | number => typeof val === "string" || (typeof val !== 'undefined' && typeof val !== 'number') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping with new extensions like `Dossier`
export function schemaToType(schemaMap: DatabaseSchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // Ensures all field values are convertible between Rust-style structs and TypeScript primitives (`string | number`)

/**
 * Abstract Data Definition for "Recipe" records, extending the existing abstract data types with a new unique identifier type that supports Rust enums and TypeScript primitives.
 */
export type RecipeType = string; // Extends standard `string` to include an optional integer ID (Rust enum) or null/undefined

/**
 * Abstract Schema Definition - A record of all columns in a database table with their corresponding field types, maintained as C/C# style records.
 */
interface DatabaseSchema {
  [key
