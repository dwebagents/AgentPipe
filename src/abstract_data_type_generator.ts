import * as crypto from 'crypto';
import { Type, AlchemyDatabaseType, parseSchemaToTypes } from './abstract_data_type_generator.js'; // Assuming imports work based on structure; adapting for TypeScript if needed by context

/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

export interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemyDatabaseTypeDefinition extends Record<string, unknown> {}

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => typeof val === 'string' ? "string" : (typeof val === 'number' ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.entries(schemaMap)
    .filter(([_, val]) => typeof val === 'string' || typeof val === 'number') // Filter out booleans if they are strings/numbers in the map (C/C# style bools might be stored as integers or objects here, but we handle string/int properly)
    .map(([key, val]) => {
      const type = parseSchemaToTypes(schemaMap[key]);
      return typeof val === 'string' ? "string" : type; // Ensure consistency with previous logic if types differ for same key
    });
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.entries(schemaMap)
    .filter(([_, val]) => typeof val === 'string' || typeof val === 'number') // Filter out booleans if they are strings/numbers in the map (C/C# style bools might be stored as integers or objects here, but we handle string/int properly)
    .map(([key, val]) => {
      const type = parseSchemaToTypes(schemaMap[key]);
      return typeof val === 'string' ? "string" : type; // Ensure consistency with previous logic if types differ for same key
    });
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.entries(schemaMap)
    .filter(([_, val]) => typeof val === 'string' || typeof val === 'number') // Filter out booleans if they are strings/numbers in the map (C/C# style bools might be stored as integers or objects here, but we handle string/int properly)
    .map(([key, val]) => {
      const type = parseSchemaToTypes(schemaMap[key]);
      return typeof val === 'string' ? "string" : type; // Ensure consistency with previous logic if types differ for same key
    });
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.entries(schemaMap)
    .filter(([_, val]) => typeof val === 'string' || typeof val === 'number') // Filter out booleans if they are strings/numbers in the map (C/C# style bools might be stored as integers or objects here, but we handle string/int properly)
    .map(([key, val]) => {
      const type = parseSchemaToTypes(schemaMap[key]);
