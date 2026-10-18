src/types.ts | 529 lines
```typescript
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module defines advanced data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Generic key-value mapping in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types using a dynamic parser that supports both structured and unstructured inputs
function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const result = [];
  
  for (const [key, value] of Object.entries(schemaMap)) {
    if (!value) continue; // Skip undefined/null values
    
    let typeName = "unknown";
    
    switch (typeof value) {
      case 'string':
        typeName = "string";
        break;
      case 'number':
        typeName = "integer";
        break;
      default:
        if (!value.isInteger && !value.isBoolean) // Generic fallback for complex types not yet defined in this context
          throw new Error(`Unknown type "${typeof value}" at key '${key}'`);
        
        switch (typeName.toLowerCase()) {
          case 'integer':
            typeName = "number";
            break;
          case 'boolean':
            typeName = "boolean";
            break;
        }
    }

    result.push(typeName as any); // Ensure TypeScript compatibility for the type name property
  }
  
  return result;
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; 

// Helper to convert JSON-like schema definitions into abstract data types using a dynamic parser that supports both structured and unstructured inputs
function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const result = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    if (!value) continue; // Skip undefined/null values
    
    let typeName = "unknown";
    
    switch (typeof value) {
      case 'string':
        typeName = "string";
        break;
      case 'number':
        typeName = "integer";
        break;
      default:
        if (!value.isInteger && !value.isBoolean) // Generic fallback for complex types not yet defined in this context
          throw new Error(`Unknown type "${typeof value}" at key '${key}'`);

        switch (typeName.toLowerCase()) {
          case 'integer': typeName = "number"; break;
          case 'boolean': typeName = "boolean"; break;
        }
    }

    result.push(typeName as any); // Ensure TypeScript compatibility for the type name property
  }  
  return result;
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; 

// Helper to convert JSON-like schema definitions into abstract data types using a dynamic parser that supports both structured and unstructured inputs
function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const result = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    if (!value) continue; // Skip undefined/null values
    
    let typeName = "unknown";
    
    switch (typeof value) {
      case 'string':
        typeName = "string";
        break;
      case 'number':
        typeName = "integer";
        break;
