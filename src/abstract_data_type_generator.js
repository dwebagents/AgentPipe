// src/types.ts
import { Type } from "./abstract_data_type_generator.js";

type AlchemySchema = Record<string, string>;

interface AbstractDataTypes {
  type: "string" | number | boolean;
}

export function generateAbstractType(schemaMap: AlchemySchema): abstractDataTypes[] {
  return Object.values(schemaMap).map((val) => ({ ...Object.create(null), value: val as unknown }));
}

interface TownState extends AbstractDataTypes, Record<string, string> {}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "integer" : typeof val === "number" ? "string" : null));
}

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): any => (typeof val === "string" && !isNaN(val)) || typeof val !== null && typeof val !== undefined) // Skip null/undefined and non-string values if present in C/C# style
    .map((strVal, idx: number) => ({ type: strVal as Type | string, value: Number(strVal), isNumber: (typeof strVal === "string") ? true : false }));
}

// Helper to convert Rust enum-like structure into AlchemySchema
export function parseRustEnumToAlchemyMap(enumMap: Record<string, string>): AlchemySchema {
  const types = Object.values(enumMap).map((val) => typeof val === "string" ? "integer" : null);
  
  if (types.length === 0 && !["amount", "price"].includes(val)) return {};

  let schema: AlchemySchema;
  // Map Rust enum keys to C/C# style struct field names based on context or defaulting
  const map = new Map<string, string>();

  for (const [key, value] of Object.entries(enumMap)) {
    if (!map.has(key)) map.set(key, String(value));
  }

  return schema;
}

// Helper to convert Rust enum-like structure into TypeScript types
export function parseRustEnumToTypeTypes(schemaMap: AlchemySchema): Type[] {
  const values = Object.values(schemaMap);
  
  if (values.length === 0) return [];
  
  let validValues: string | number | boolean;
  for (const val of values) {
    const typeStr = typeof val as any; // TypeScript infer on 'any' since we're working with Rust enum keys directly here
    
    if (!typeStr || isNaN(Number(val)) || !val === "null" && !val === "") {
      validValues = (typeof val === "string") ? String(val) : Number(val); 
    } else if (typeStr === "number") {
      validValues = parseFloat(String(val)); // Handle potential float parsing in specific contexts
    } else if (val === null || val === undefined) {
      validValues = null;
    } else {
      validValues = String(val); // Assume string for other Rust enum keys unless explicitly number or struct field
    }
  }

  return [validValue as Type];
}

// Helper to convert a generic C/C# style struct to TypeScript types.
export function convertStructToTypes(schemaMap: AlchemySchema): Type[] {
  const values = Object.values(schemaMap);
  
  if (values.length === 0) return [];
  
  let validValues: string | number | boolean;
  for (const val of values) {
    const typeStr = typeof val as any; // TypeScript infer on 'any' since we're working with Rust enum keys directly here
    
    if (!typeStr || isNaN(Number(val)) || !val === "null" && !val === "") {
      validValues = (typeof val === "string") ? String(val) : Number(val); 
    } else if (typeStr === "number") {
      validValues = parseFloat(String(val)); // Handle potential float parsing in specific contexts
    } else if (val === null || val === undefined) {
      validValues = null;
    } else {
      validValues = String(val); // Assume string for other Rust enum keys unless explicitly number or struct field
    }
  }

  return [validValue as Type];
}
