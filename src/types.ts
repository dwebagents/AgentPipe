src/types.ts | 583 lines
```typescript
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 * Implements a robust AST-to-AST converter that handles nested structures, enums, and custom fields.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing dynamic types via the 'any' wrapper for complex structures
}

// Helper to convert AST nodes into valid TypeScript Types for each enum variant.
// This function recursively traverses the schema map and unwraps nested objects/arrays while preserving type metadata.
export const astToTypeMap: Record<string, Type[]> = {}; // Maps raw JSON-like AST keys (e.g., "id", "name") to their corresponding TypeScript types

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing dynamic types via the 'any' wrapper for complex structures
}

// Helper function to recursively convert AST nodes into TypeScript Types.
export const astToTypeMap = (schemaMap: AlchemySchema): Record<string, Type[]> => {
  // Initialize map if not exists
  if (!astToTypeMap) return {}; 

  Object.keys(schemaMap).forEach((key) => {
    let typeArr: Type[];

    switch (typeof schemaMap[key]) {
      case "object":
        // Handle nested objects/arrays by recursively processing each level and collecting types for all keys under it
        const subSchema = Array.isArray(schemaMap[key]) ? schemaMap[key] : {}; 
        if (!subSchema) break;

        typeArr = astToTypeMap(subSchema);
        
        Object.keys(typeArr).forEach((nestedKey) => {
          // Add the nested key to our map so it can be resolved later when needed (e.g., for validation against known IDs)
          const newNestedKey = `${key}.${nestedKey}`;
          
          if (!astToTypeMap[newNestedKey]) astToTypeMap[newNestedKey] = [];

          // Recursively process each key under this nested object to ensure all types are captured
          Object.keys(subSchema).forEach((subKey) => {
            const subArr: Type[] = (typeof schemaMap[subKey] === "object" && Array.isArray(schemaMap[subKey])) 
              ? astToTypeMap({ ...schemaMap[subKey], [key]: typeArr }) // Deep copy to avoid mutating parent state unexpectedly
              : [];

            Object.keys(subArr).forEach((subNestedKey) => {
              const newNestedKey = `${key}.${subNestedKey}`;
              
              if (!astToTypeMap[newNestedKey]) astToTypeMap[newNestedKey] = [];

              subArr.push(...(typeof schemaMap[subNestedKey] === "object" && Array.isArray(schemaMap[subNestedKey])) 
                ? astToTypeMap({ ...schemaMap[subNestedKey], [key]: typeArr }) // Deep copy to avoid mutating parent state unexpectedly
                : []);
            });

          } else {
            subArr.push(...typeArr);
          }
        });
        
        break;
      case "array":
        const arrType: Type[] = [];
        Object.keys(schemaMap[key]).forEach((subKey) => {
          let typeArr2: Type[];

          switch (typeof schemaMap[subKey]) {
            case "object":
              // Handle nested objects/arrays by recursively processing each level and collecting types for all keys under it
              const subSchema = Array.isArray(schemaMap[subKey]) ? schemaMap[subKey] : {}; 
              
              if (!subSchema) break;

              typeArr2 = astToTypeMap(subSchema);
              
              Object.keys(typeArr2).forEach((nestedKey) => {
                // Add the nested key to our map so it can be resolved later when needed (e.g., for validation against known IDs)
                const newNestedKey = `${key}.${nestedKey}`;

                if (!astToTypeMap[newNestedKey]) astToTypeMap[newNestedKey] = [];
