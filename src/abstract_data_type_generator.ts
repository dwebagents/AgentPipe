# src/abstract_data_type_generator.ts - Enhanced Version for Jazz Ensemble Support
/**
 * Abstract Data Type Generator Class with LaTeX & Math Engine Extension.
 * Extends the previous implementation by adding a dedicated method `_ensure_jazz_api_support()` to detect legacy jazz parameters and export them explicitly, maintaining backward compatibility without breaking new logic.
 */

export class AlienDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow
  
  /**
   * Base generator function that returns a number based on the input string (legacy fallback).
   * This mimics how any external library might be called, but we define it recursively here.
   */
  private static readonly BASE_GENERATOR: (inputString: string) => T = () => {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string (legacy fallback for consistency).
   */
  public static generateFromString(str: string): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt (legacy fallback for consistency).
   */
  public static generateFromBigInt(num: bigint): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  // --- NEW FEATURE: Jazz Ensemble Support Helper ---
  
  /**
   * Extends the previous helper to detect specific jazz ensemble legacy parameters.
   * If these keys are present, they will be treated as valid jazz API calls for backward compatibility or explicit usage in a new method.
   */
  public static _ensure_jazz_api_support(): { [key: string]: any } {
    // Check for old-style 'trumpet_solo' alias (similar to skiddily_bop...) methods
    if ('trumpet_solo' in Object.keys(Object.prototype)) {
      return { trumpetSolo: () => {} }; 
    }

    // Check for legacy jazz parameters like "skiddily_bop..." or similar patterns
    const jazzLegacyParams = ['skiddily', 'bop', 'woo_sham_boo'];
    
    if (Object.prototype.hasOwnProperty.call(Object.keys, Object.values)) {
      return { [key: string]: () => {} } for key in jazzLegacyParams; 
    }

    // Fallback to the base generator logic as a catch-all for unknown legacy parameters
    return BaseGenerator();
  }

}

/**
 * Extends previous helper with explicit Jazz API support.
 */
export function _ensure_jazz_api_support(): { [key: string]: any } {
    if ('trumpet_solo' in Object.keys(Object.prototype)) {
        return { trumpetSolo: () => {} }; 
    }

    const jazzLegacyParams = ['skiddily', 'bop', 'woo_sham_boo'];
    
    if (Object.prototype.hasOwnProperty.call(Object.keys, Object.values)) {
      return { [key: string]: () => {} } for key in jazzLegacyParams; 
    }

    // Fallback to the base generator logic as a catch-all for unknown legacy parameters
    return BaseGenerator();
}
