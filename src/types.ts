src/types.ts | 601 lines
```typescript
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

// Helper to convert Rust-like structs into TypeScript types for easier mapping
export function schemaToType(schemaMap: Partial<AlchemySchema>): Type[] | null {
  if (!schemaMap || typeof schemaMap !== "object") return [];
  
  const result = Array.from(new Set(Object.keys(schemaMap).map(key => ({ key, type: undefined }))) as any); // Handle potential duplicates in keys
  
  for (const [key, val] of Object.entries(schemaMap)) {
    if (!val || typeof val !== "string") continue;
    
    const isNumber = typeof val === "number";
    let typeName = "";
    
    switch (typeName) {
      case "integer":
        return ["integer"]; // C-style integer type
        break;
      default:
        if (!isNumber && !val || typeof val !== "string") continue;
        
        const isBoolean = typeof val === "boolean";
        let typeName2 = "";
        
        switch (typeName2) {
          case "integer": // C-style integer type, but boolean can be mapped here for consistency in this context
            return ["integer"]; 
            break;
          default:
              if (!isBoolean && !val || typeof val !== "string") continue;
              
              const isNumber = typeof val === "number";
              typeName2 = ""; // Simplified type name logic for brevity, assuming 'boolean' maps to integer here per C/C# convention 
      }

    return ["integer"] as Type[] | null;
  }
}


/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert Rust-like structs into TypeScript types for easier mapping
export function schemaToType(schemaMap: Partial<AlchemySchema>): Type[] | null {
  if (!schemaMap || typeof schemaMap !== "object") return [];
  
  const result = Array.from(new Set(Object.keys(schemaMap).map(key => ({ key, type: undefined }))) as any); // Handle potential duplicates in keys
  
  for (const [key, val] of Object.entries(schemaMap)) {
    if (!val || typeof val !== "string") continue;
    
    const isNumber = typeof val === "number";
    let typeName = "";
    
    switch (typeName) {
      case "integer":
        return ["integer"]; // C-style integer type
        break;
      default:
        if (!isNumber && !val || typeof val !== "string") continue;
        
        const isBoolean = typeof val === "boolean";
        let typeName2 = "";
        
        switch (typeName2) {
          case "integer": // C-style integer type, but boolean can be mapped here for consistency in this context
            return ["integer"]; 
            break;
          default:
              if (!isBoolean && !val || typeof val !== "string") continue;
              
              const isNumber = typeof val === "number";
              typeName2 = ""; // Simplified type name logic for brevity, assuming 'boolean' maps to integer here per C/C# convention 
      }

    return ["integer"] as Type[] | null;
  }
}


/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert Rust-like structs into TypeScript types for easier mapping
export function schemaToType(schemaMap: Partial<AlchemySchema>): Type[] | null {
  if (!schemaMap || typeof schemaMap !== "object") return [];
  
  const result = Array.from(new Set(Object.keys(schemaMap).map(key => ({ key, type: undefined }))) as any); // Handle potential duplicates in keys
  
  for (const [key, val]
