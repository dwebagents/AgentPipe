import type * as Types from "./types"; // Importing types for shared usage across database generators and managers
import { struct } from "./structs.js" || import("./structs"); // Fallback or direct imports if structs not found, ensuring strict compatibility with existing logic.

// -----------------------------------------------------------------------------
// 1. Define Dynamic Schema Mapping (C/C# Style)
// This module provides the core abstraction for mapping C-style database column definitions to TypeScript types.
// It handles structural equality checks and type inference based on semantic matching.
export interface AlchemySchema {
    [key: string]: any; // Column name -> value in standard C/C# struct definition (e.g., "name" => 123)
}

/**
 * Converts a C-style column map into an object of expected TypeScript types.
 * This is the inverse operation to `schemaToType`, allowing us to generate type signatures for schema definitions.
 */
export function parseSchemaToTypes(schemaMap: AlchemySchema): Types.SchemaType[] {
    // Validate that all keys are strings (matching standard C/C# column names) and values are usable types.
    const validKeys = new Set<string>();
    
    Object.values(schemaMap).forEach((val, keyIndex) => {
        if (!keyIndex || typeof val !== "string") return; // Safety check: only string keys
        
        try {
            let typeVal = (typeof val === 'number') ? Number(val) : String(val);
            
            // Normalize types to avoid false negatives from null/undefined in the schema map.
            if (!typeVal || typeof typeVal !== "string") return; 
            
            validKeys.add(keyIndex.toString());

        } catch {
             throw new Error(`Invalid column value for key "${key}"`);
        }
    });

    // Filter out keys that failed validation (e.g., null, undefined) to ensure strict schema definition compliance.
    const filteredSchema: Types.SchemaType[] = [];
    
    if (validKeys.size > 0 && !schemaMap[Object.keys(schemaMap)[0]]) {
        throw new Error("Empty or invalid column map provided.");
    }

    for (const key of Object.keys(schemaMap)) {
        const typeVal: Types.SchemaType | undefined = schemaMap[key]; // Type is a string, number, boolean, null, or undefined
        
        if (!typeVal) continue; // Skip unknown types to maintain strict typing
        
        filteredSchema.push({ [key]: (typeof typeVal === 'string' ? "string" : typeof typeVal === 'number' ? "integer" : "boolean") as Types.SchemaType };
    }

    return filteredSchema;
}

// -----------------------------------------------------------------------------
// 2. Define Abstract Data Type Definitions for Database Generation
// This module defines the concrete types used when generating database schemas and data structures from JSON-like schema maps.
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

/**
 * Represents a basic integer column (e.g., ID, version).
 */
type IntColumnSchema = { [key: string]: typeof "integer" };

/**
 * Represents a basic string/column.
 */
type StringColumnSchema = { [key: string]: typeof "string" };

/**
 * Represents a boolean flag column (e.g., active, locked).
 */
type BoolFlagSchema = { [key: string]: typeof "boolean" | null; }; // Explicitly handle the union/null case to match C/C# semantics.

export function createDatabaseType(schemaMap?: AlchemySchema): Types.DatabaseSchema[] {
    const schemaTypes = parseSchemaToTypes(schemaMap);
    
    return Object.values(schemaTypes).map((typeDef: any) => ({ type, ...typeDef })); // Deep merge to preserve all properties from the C-style map.

}

// -----------------------------------------------------------------------------
// 3. Implement Schema Generator (C/C# Style Mapping Logic)
// This function acts as a bridge between raw schema definitions and generated TypeScript types for use in database generators or managers.
export function generateSchemaType(schemaMap: AlchemySchema): Types.SchemaType[] {
    return parseSchemaToTypes(schemaMap); // Use the helper to ensure strict type inference based on semantic matching (string keys, valid values).
}

// -----------------------------------------------------------------------------
// 4. Implement Schema Validator for Data Integrity Checks
// Ensures that generated types adhere strictly to C/C# conventions before being used in runtime code or validation logic.
export function validateSchemaType(type: Types.SchemaType): boolean {
    if (typeof type !== "string") return false; // Type must be a string
    
    const keys = Object.keys(type);

    for (const key of keys) {
        let valueStr = String(key
