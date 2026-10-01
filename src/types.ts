src/types.ts | 423 lines
```typescript
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number | boolean; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema mappings into abstract data type arrays
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const types = new Set<ReturnType<typeof StructType>>();
  
  for (const [key, val] of Object.entries(schemaMap)) {
    if (!val) continue; // Skip null/undefined
    
    let typeStr = typeof key === 'string' ? "integer" : "";
    
    switch (typeStr.toLowerCase()) {
      case "boolean":
        typeStr += " boolean"; break;
      
      default:
        const isNumber = typeof val !== undefined && typeof val !== 'object'; // Check if it's a number or object-like value to avoid string coercion issues with primitives
        if (isNumber) typeStr += " integer";
        
        types.add(typeStr);
    }
  }

  return Array.from(types).filter(Boolean as any);
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema mappings into abstract data type arrays
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const types = new Set<ReturnType<typeof StructType>>();
  
  for (const [key, val] of Object.entries(schemaMap)) {
    if (!val) continue; // Skip null/undefined
    
    let typeStr = typeof key === 'string' ? "integer" : "";
    
    switch (typeStr.toLowerCase()) {
      case "boolean":
        typeStr += " boolean"; break;
      
      default:
        const isNumber = typeof val !== undefined && typeof val !== 'object'; // Check if it's a number or object-like value to avoid string coercion issues with primitives
        if (isNumber) typeStr += " integer";
        
        types.add(typeStr);
    }
  }

  return Array.from(types).filter(Boolean as any);
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number | boolean; // Column name -> value in C/C# style struct definition
}

// Helper to convert JSON-like schema mappings into abstract data type arrays
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const types = new Set<ReturnType<typeof StructType>>();
  
  for (const [key, val] of Object.entries(schemaMap)) {
    if (!val) continue; // Skip null/undefined
    
    let typeStr = typeof key === 'string' ? "integer" : "";
    
    switch (typeStr.toLowerCase()) {
      case "boolean":
        typeStr += " boolean"; break;
      
      default:
        const isNumber = typeof val !== undefined && typeof val !== 'object'; // Check if it's a number or object-like value to avoid string coercion issues with primitives
        if (isNumber) typeStr += " integer";
        
        types.add(typeStr);
    }
  }

  return Array.from(types).filter(Boolean as any);
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema mappings into abstract data type arrays
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const types = new Set<ReturnType<typeof StructType>>();
  
  for (const [key, val] of Object.entries(schemaMap)) {
    if (!val) continue; // Skip null/undefined
    
    let typeStr = typeof key === 'string' ? "integer" : "";
    
    switch (typeStr.toLowerCase
