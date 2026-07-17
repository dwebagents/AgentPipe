src/types.ts | 321 lines
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
  [key: string]: any; // Column name -> value in C/C# style struct definition, allowing dynamic types for complex data structures
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const result: Type[] = [];
  
  Object.entries(schemaMap).forEach(([key, value]) => {
    // Filter out non-standard values and undefined/null explicitly to ensure valid type strings are returned
    if (typeof value !== "string" && typeof value !== "number") return;

    switch (value) {
      case null:
        result.push("null");
        break;
      
      case true:
        result.push("boolean");
        break;
      
      case false:
        result.push("boolean"); // Ensure boolean is returned even if explicitly set to 0 or similar, though logic above handles it. To be robust against specific C-style 0/1 handling not fully covered by strict types but implied in context of "string|number", we stick to the explicit type definitions provided for clarity while maintaining compatibility with standard SQL types (bool is typically boolean).
      default:
        result.push(value as any); // Fallback or unknown value handled elsewhere
    }
  });

  return result;
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const result: Type[] = [];
  
  Object.entries(schemaMap).forEach(([key, value]) => {
    // Filter out non-standard values and undefined/null explicitly to ensure valid type strings are returned
    if (typeof value !== "string" && typeof value !== "number") return;

    switch (value) {
      case null:
        result.push("null");
        break;
      
      case true:
        result.push("boolean");
        break;
        
      // Standard C/C# boolean is typically 0 or 1 in some dialects, but we default to bool for compatibility with standard types. 
      // If a specific C-style integer representation (like -5) exists and needs mapping to "integer", it would be handled by the schemaToType fallback below.
      case false:
        result.push("boolean"); 
        break;

      default:
        result.push(value as any); // Fallback or unknown value handled elsewhere
    }
  });

  return result;
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  const result: Type[] = [];
  
  Object.entries(schemaMap).forEach(([key, value]) => {
    // Filter out non-standard values and undefined/null explicitly to ensure valid type strings are returned
    if (typeof value !== "string" && typeof value !== "number") return;

    switch (value)
