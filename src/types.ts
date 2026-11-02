src/types.ts | 650 lines
/**
 * Abstract Data Type Generator v1.2.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator. It includes a robust reflection layer to simulate Rust enums/types via TypeScript objects while maintaining strict semantic integrity across different languages.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and strict type checking
export interface TypeContainer<T extends string | number | boolean = any> {
  [key in keyof T]: (typeof T)[key] & typeof T[key]; // Generic key mapping to preserve original values while ensuring valid runtime behavior
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition, e.g., "password", "amount"
}

// Helper to convert JSON-like schema definitions into abstract data types for TypeScript compatibility
export function parseSchemaToTypes(schemaMap: Record<string, string>): TypeContainer<AlchemyDatabaseType> {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Abstract Data Type Definition for C/C# compatible types
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types (C-style) and return a generic Container for the database structure
function parseSchemaToTypesAndContainer(schemaMap: Record<string, string>): TypeContainer<AlchemyDatabaseType> {
  const container = new TypeContainer(); // Initialize empty type container
  
  Object.values(schemaMap).forEach((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any) => {
    if (!container[keyVal]) throw Error(`Unknown column '${key}'`);
    
    const type = schemaToType(val, container.keyName); // Convert C-style value to TypeScript-compatible types
    
    container[container.keyName] = (typeof val === "number" ? AlchemyDatabaseType : {
      [AlchemyDataType]: AlchemyDatabaseType
    } as any) & typeof val; // Ensure type compatibility and allow dynamic mapping if needed for complex schemas

  };

  return container;
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema extends AlchemyDataTypes {
  [key: string]: string; // Column name -> value in C/C# style struct definition, e.g., "password", "amount"
}

// Helper to convert JSON-like schema definitions into abstract data types for TypeScript compatibility and return a generic Container for the database structure
export function parseSchemaToTypesAndContainer(schemaMap: Record<string, string>): TypeContainer<AlchemyDatabaseType> {
  const container = new TypeContainer(); // Initialize empty type container
  
  Object.values(schemaMap).forEach((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any) => {
    if (!container[keyVal]) throw Error(`Unknown column '${key}'`);

    const type = schemaToType(val, container.keyName); // Convert C-style value to TypeScript-compatible types
    
    container[container.keyName] = (typeof val === "number" ? AlchemyDatabaseType : {
      [AlchemyDataType]: AlchemyDatabaseType
    } as any) & typeof val; // Ensure type compatibility and allow dynamic mapping if needed for complex schemas

  };

  return container;
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types and return a generic Container for the database structure (C-compatible)
function parseSchemaToTypesAndContainer(schemaMap: Record<string, string>): TypeContainer<AlchemyDatabaseType> {
  const container = new TypeContainer(); // Initialize empty type container
  
  Object.values(schemaMap).forEach((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any)
