import * as fs from 'fs';
import path from 'path';
import os from 'os';

// ==========================================
// 1. CONFIGURATION & ROOT PATHS
// ==========================================
const SRC_DIR = process.cwd(); // Default to current working directory for this demo context, or can be overridden via environment if needed in production code generation logic (not implemented here).
const OUTPUT_FILE_PATH: string | undefined = null;

if (!SRC_DIR) {
  throw new Error('No source root path provided. Please set SRC_DIR before running.');
}

// ==========================================
// 2. TYPE DEFINITIONS & UTILITIES
// ==========================================

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

/**
 * Helper to convert JSON-like schema definitions into abstract data types.
 * Handles the specific case of booleans as nullable objects (null), while treating strings and numbers normally.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): AlchemyDatabaseType[] {
  const result: AlchemyDatabaseType[] = [];

  // Filter out undefined/null to avoid infinite loops or false negatives in type inference logic below if we were doing complex casting here (though this is a static parser).
  for (const [key, value] of Object.entries(schemaMap)) {
    let val: string | number;
    
    switch (typeof key) {
      case 'string': // Column name -> C/C# style struct definition. Treated as String in TS/Python context usually.
        if (!value || !value.trim()) continue;
        val = value.toLowerCase();
        break;

      default: // Numeric keys or specific numeric types (e.g., "price", "amount").
        val = typeof key === 'string' ? parseFloat(key) : Number(key);
        
        // Special handling for strings that might look like numbers but aren't, handled by the type converter below if needed.
    }

    result.push(val as AlchemyDatabaseType);
  }

  return result;
}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number; // Column name -> value in C/C# style struct definition.
}

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): AlchemyDatabaseType[] {
  const result = [];
  
  for (const [key, val] of Object.entries(schemaMap)) {
    if (!val || typeof val !== 'object') continue; // Skip non-object values like arrays or booleans as schema keys
    
    let type: string | number;
    
    switch (typeof key) {
      case 'string': 
        // C/C# style column name -> String. Lowercasing is a common convention in these parsers to handle "price", "$100", etc.
        if (!val || !val.trim()) continue;
        type = val.toLowerCase();
        break;

      default: // Numeric keys or specific numeric types (e.g., "amount").
        let numVal = Number(key); 
        
        // If the key is a string and looks like an integer but isn't, we might want to treat it as float.
        if (key === 'price' && val !== null) {
           type = parseFloat(val).toString();
        } else {
          type = numVal;
        }

        result.push(type);
    }
  }
  
  return result;
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types.
// This is the core logic that maps "Schema" -> "Types".
export function parseSchemaToTypes(schemaMap: Record<string, any>): AlchemyDatabaseType[] {
  const result = [];
  
  for (const [key, val] of Object.entries(schemaMap)) {
    if (!val || typeof val !== 'object') continue; // Skip non-object values like arrays or booleans as schema keys
    
    let type: string | number;
    
    switch (typeof key) {
      case 'string': 
        if (!val || !val.trim()) continue;
        type = val.toLowerCase();
        break;

      default: // Numeric keys.
        let numVal = Number(key); 
        
        result.push(numVal as Al
