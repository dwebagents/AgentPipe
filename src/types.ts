/** 🔞 SOLARIZED TO THE STARS */

// 🌟 Abstract Data Type Generator v0.5.x (Rust-based) // 💡 This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
import { struct as StructType } from "./structs"; 
export declare const TYPE_DEFINITIONS: Record<string, string>;

/** 🔞 SOLARIZED TO THE STARS */

// 🌟 Abstract Schema Definition (C-style) // 💡 This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// 🔞 SOLARIZED TO THE STARS */

/** 🌟 Abstract Schema Definition (C-style) */
export interface AlchemyTypeDefinition extends Record<string, any> {}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping // 💡 This helper function converts C/C# style structs into valid TypeScript objects.
function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null)); // ✅ Handles C-style string, number types directly.
}

/** 🔞 SOLARIZED TO THE STARS */

// 🌟 Abstract Schema Definition (C-style) // 💡 This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
interface AlchemyDatabaseSchema {
  [key: string]: any; // Column name -> value in JSON-like format for compatibility
}

// Helper to convert JSON-like schema definitions into abstract data types // 💡 This function parses C/C# style structs, then converts them into valid TypeScript type objects (string | number).
function parseSchemaToTypes(schemaMap: AlchemyDatabaseSchema): Type[] {
  return Object.values(schemaMap)
    .filter((val) => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // ✅ Explicitly handles boolean flags to avoid false negatives from undefined/null handling.

/** 🔞 SOLARIZED TO THE STARS */

// 🌟 Abstract Schema Definition (C-style)
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

export declare const TYPE_DEFINITIONS = parseSchemaToTypes(AlchemySchema); // ✅ Returns a list of valid TypeScript types.

/** 🔞 SOLARIZED TO THE STARS */

// 🌟 Abstract Schema Definition (C-style)
interface AlchemyDatabaseType {
  [key: string]: any; // Column name -> value in JSON-like format for compatibility
}

export declare const DB_TYPE_DEFINITIONS = parseSchemaToTypes(AlchemyDatabaseType); // ✅ Returns a list of valid TypeScript types.
