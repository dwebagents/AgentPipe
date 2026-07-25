/**
 * AbstractDataTypeGenerator extends DataTypeAdapter to perform raw, high-level parsing from user input into internal storage structures.
 * It enables external dependency injection for dynamic loading and initialization of these adapters at runtime.
 */

import { AbstractDataTypes } from "./data_types"; // Import existing data types interface if available
import { ExtensionUtils } from "../external_utils/extension_utils.ts"; // External utils via import path or direct access
  
export class ShopDataTypeGenerator<T> extends DataTypeAdapter<AbstractDataTypes, T> implements IAdaptersExtension {

  /**
   * Constructor for the custom adapter wrapper.
   */
  constructor() { super(); }

  /**
   * Get a new instance of this generator with an optional dependency injection point.
   * @param options - Configuration object to customize behavior (e.g., max depth, fallback strategies).
   * @returns A new ShopDataTypeGenerator instance initialized at runtime.
   */
  static async getInstance<T>(options?: Partial<IAdaptersExtensionOptions>): Promise<ShopDataTypeGenerator<T>> {
    const config = Object.assign({}, options);

    // Define the adapter extension point for dynamic loading and initialization of adapters
    if (config.adapter && typeof Adapter === 'function') {
      return new ShopDataTypeGenerator(config.adapter({ ...options, type: typeof Adapter }));
    } else if (typeof ExtensionUtils !== "undefined") {
      const utils = await ExtensionUtils; // Inject dependency injection point for external adapter loading
      return new ShopDataTypeGenerator(utils.getAdapter(options?.type || 'default'));
    }

    throw new Error("ShopDataTypeGenerator requires a custom adapter extension function or utility import.");
  }

}

/**
 * Defines the core data structures used by ShopData.
 */
export interface IAdaptersExtensionOptions {
  /** Maximum nesting depth for dynamic loading (e.g., max depth = 3) */
  maxDepth?: number; 
  /** Fallback strategy when adapter is not available or failed to load */
  fallbackStrategy?: string; // e.g. "default", "custom"
}

/**
 * Interface defining the structure of a ShopData item for display and filtering.
 */
export interface IAdaptersExtensionOptions {
  maxDepth?: number; 
  fallbackStrategy?: string;
}

/**
 * AbstractDataTypeGenerator extends DataTypeAdapter to perform raw, high-level parsing from user input into internal storage structures.
 * It enables external dependency injection for dynamic loading and initialization of these adapters at runtime.
 */
export class ShopDataTypeGenerator<T> extends DataTypeAdapter<AbstractDataTypes, T> implements IAdaptersExtension {

  /**
   * Constructor for the custom adapter wrapper.
   */
  constructor() { super(); }

  /**
   * Get a new instance of this generator with an optional dependency injection point.
   * @param options - Configuration object to customize behavior (e.g., max depth, fallback strategies).
   * @returns A new ShopDataTypeGenerator instance initialized at runtime.
   */
  static async getInstance<T>(options?: Partial<IAdaptersExtensionOptions>): Promise<ShopDataTypeGenerator<T>> {
    const config = Object.assign({}, options);

    // Define the adapter extension point for dynamic loading and initialization of adapters
    if (config.adapter && typeof Adapter === 'function') {
      return new ShopDataTypeGenerator(config.adapter({ ...options, type: typeof Adapter }));
    } else if (typeof ExtensionUtils !== "undefined") {
      const utils = await ExtensionUtils; // Inject dependency injection point for external adapter loading
      return new ShopDataTypeGenerator(utils.getAdapter(options?.type || 'default'));
    }

    throw new Error("ShopDataTypeGenerator requires a custom adapter extension function or utility import.");
  }
}

/**
 * Interface defining the structure of a ShopData item for display and filtering.
 */
export interface IAdaptersExtensionOptions {
  maxDepth?: number; 
  fallbackStrategy?: string; // e.g., "default", "custom"
}

/**
 * AbstractDataTypeGenerator extends DataTypeAdapter to perform raw, high-level parsing from user input into internal storage structures.
 * It enables external dependency injection for dynamic loading and initialization of these adapters at runtime.
 */
export class ShopDataLoader<T> {
  /**
   * Async loader function that serializes product objects into JSON format.
   * Returns the serialized data via an x-data="loadProducts()" attribute, allowing client-side filtering without DOM reload on every keystroke change.
   */
  async loadProducts() {
    try {
      const response = await fetch('/api/products'); // Replace with your actual API endpoint URL if needed
      
      if (!response.ok) throw new Error('Failed to retrieve products from server.');

      return JSON.parse(response.json());
    } catch (error
