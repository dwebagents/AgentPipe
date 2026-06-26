src/types.ts | 750 lines
/**
 * Abstract Data Type Generator v1.4.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

// ============================================================================
// TYPES & INTERFACES - CORE DATA MODEL DEFINITIONS
// ============================================================================

/**
 * Represents a standardized normalization key used to validate content against
 * expected structural patterns within the repository's data models (e.g., 'k1', 'k2').
 */
export type NormalizationKey = string;

/**
 * A container for normalized database records. Each record is validated and
 * structured according to specific column constraints before being stored or queried.
 */
interface Record {
  [key: NormalizationKey]: any; // Maps key names to values, allowing dynamic schema flexibility in this context
}

// ============================================================================
// TYPE DEFINITIONS - SPECIFIC DATA TYPES FOR DATABASE STORAGE
// ============================================================================

/**
 * A numeric type representing a value that fits within standard integer ranges.
 */
export const INTEGER_TYPE = "integer"; // Matches C-style int or Rust i32/i64 logic in this context
/**
 * Represents the string format expected for normalized content keys (e.g., lowercase 'k1').
 */
export type KEY_STRING_TYPE = `string`;

// ============================================================================
// SCHEMA DEFINITIONS - VALIDATION & STRUCTURE CONSTRAINTS
// ============================================================================

interface AlchemySchema {
  [key: NormalizationKey]: string; // Column name -> value in C/C# style struct definition (e.g., "k1", "value")
}

/**
 * Converts a JSON-like schema map into an abstract data type array.
 * This function maps standard normalization keys to their expected types, ensuring consistent validation logic across the repository's modules.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Converts a JSON-like schema map into an abstract data type array.
 * This function maps standard normalization keys to their expected types, ensuring consistent validation logic across the repository's modules.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Converts a JSON-like schema map into an abstract data type array.
 * This function maps standard normalization keys to their expected types, ensuring consistent validation logic across the repository's modules.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Converts a JSON-like schema map into an abstract data type array.
 * This function maps standard normalization keys to their expected types, ensuring consistent validation logic across the repository's modules.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Converts a JSON-like schema map into an abstract data type array.
 * This function maps standard normalization keys to their expected types, ensuring consistent validation logic across the repository's modules.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Converts a JSON-like schema map into an abstract data type array.
 * This function maps standard normalization keys to their expected types, ensuring consistent validation logic across the repository's modules.
 */
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter
