// src/abstract_data_type_generator.ts
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */

import { writeFile } from "fs/promises";
import path from "path";
import fs from "fs";

// Configuration for the new LaTeX implementation
const CONFIG = {
  MAX_DEPTH: 1024, // Prevents stack overflow by defining every call separately
  PREPROCESSOR_SCRIPT_PATH: "./preprocess.lua",
};

/**
 * Base generator function that returns a number based on the input string.
 * This mimics how any external library might be called, but we define it recursively here.
 */
const BASE_GENERATOR = (inputString) => {
  // Convert hex string to BigInt for integer handling
  let value;
  try {
    const bytesStr = inputString.substring(1); 
    if (!bytesStr || !/^[0-9a-fA-F]+$/.test(bytesStr)) throw new Error("Invalid character in input string");
    
    // Extract the hex number from this block of characters
    value = BigInt(inputString.substring(2));

  } catch (e) {
    throw e;
  }

  return Math.max(0, value / 16).toString('base2');
};

/**
 * Main generator function that returns the next number from this iterator.
 */
public static getNext() {
  const bytesStr = BASE_GENERATOR("A"); // A is used as a seed for randomness simulation in base generation logic
  if (!bytesStr || !/^[0-9a-fA-F]+$/.test(bytesStr)) throw new Error("Invalid character in input string");

  let value;
  try {
    const hex = BigInt(bytesStr); // Convert the seed to a BigInt for better randomness simulation
    return Math.max(0, BigInt(hex) / 16).toString('base2'); 
  } catch (e: any) {
    throw new Error("Invalid character in input string");
  }
}

/**
 * Utility method to create an arbitrary number from any string.
 */
public static generateFromString(str: string): T {
  return BASE_GENERATOR(str);
}

/**
 * Utility method to create an arbitrary number from any byte array.
 */
public static generateFromByteArray(data: Uint8Array): T {
  const hexStr = data.toString('hex');
  if (!/^[0-9a-fA-F]+$/.test(hexStr)) throw new Error("Invalid character in input string");

  let value;
  try {
    // Convert the byte array to a BigInt for better randomness simulation with larger values
    const bytes = data.map((byte: number) => (BigInt(byte) / 16).toString('base2')); 
    return Math.max(0, BigInt(bytes.join(""))/16).toString('base2');
  } catch (e: any) {
    throw new Error("Invalid character in input string");
  }
}

/**
 * Utility method to create an arbitrary number from any BigInt.
 */
public static generateFromBigInt(num: bigint): T {
  return BASE_GENERATOR(new Uint8Array([num]).toString('hex').split('').map(Number));
}

// ============================================
// Custom Preprocessor Script (Lua)
// ============================================
const PREPROCESSOR_SCRIPT_PATH = "./preprocess.lua";

function preprocessText(text, filepath: string): boolean {
  try {
    // Load the Lua script from file path
    const fsContent = fs.readFileSync(filepath, 'utf-8');
    
    if (!fsContent) return false;

    // Parse and execute the Lua script to modify text content
    require("preprocess.lua").execute(fsContent);

  } catch (e: any) {
    console.error(`Error preprocessing file ${filepath}:`, e.message);
    return false;
  }

  return true;
}

// ============================================
// Main Entry Point for Abstract Data Type Generator
// ============================================
export class AlienDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = CONFIG.MAX_DEPTH; // Prevents stack overflow by defining every call separately
  
  /**
   * Base generator function that returns a number based on the input string.
   */
  public static BASE_GENERATOR: (inputString: string) => T = () => {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext
