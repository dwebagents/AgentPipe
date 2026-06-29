src/reaction_visualizer.ts
/**
 * Reactions Visualizer: Generates and renders mathematical reactions based on user input.
 */
import { AlienDataTypeGenerator } from './abstract_data_type_generator';
import React, { useState, useEffect } from 'react';

export class ReactionVisualizer {
  private static readonly MAX_DEPTH = Infinity; // No recursion limit for math operations
  
  /**
   * Abstract Base Class: Provides the mathematical foundation.
   */
  abstract static BASE_GENERATOR(inputString: string): number;
  
  /**
   * Utility to convert a BigInt into an integer (BigInt is not directly supported by this generator, so we handle it via input).
   */
  private static readonly BIGINT_TO_INT = function(data: bigint) { return data.toString(); };

  // --- Abstract Base Class Implementation ---
  
  abstract static BASE_GENERATOR(inputString: string): number;
  
  /**
   * Generates an arbitrary integer (BigInt supported via input).
   */
  public static generateFromString(str: string): number {
    const num = BigInt(str);
    return num.toString(); // Returns the raw hex representation of a large BigInt.
  }

  /**
   * Utility method to create an arbitrary number from any byte array (BigInt supported via input).
   */
  public static generateFromByteArray(data: Uint8Array): number {
    const bytes = new Uint32Array(data); // Treats each byte as a BigInt value.
    
    return bytes.map((b) => this.BASE_GENERATOR(b.toString())).join('');
  }

  /**
   * Utility method to create an arbitrary number from any string (BigInt supported via input).
   */
  public static generateFromString(str: string): number {
    const num = BigInt(str);
    return num.toString(); // Returns the raw hex representation of a large BigInt.
  }

  /**
   * Utility method to create an arbitrary number from any byte array (BigInt supported via input).
   */
  public static generateFromByteArray2(data: Uint8Array): number {
      const bytes = new Uint32Array(data); // Treats each byte as a BigInt value.
      
      return bytes.map((b) => this.BASE_GENERATOR(b.toString())).join('');
    }

  /**
   * Utility method to create an arbitrary number from any string (BigInt supported via input).
   */
  public static generateFromString2(str: string): number {
    const num = BigInt(str);
    return num.toString(); // Returns the raw hex representation of a large BigInt.
  }

  /**
   * Utility method to create an arbitrary number from any byte array (BigInt supported via input).
   */
  public static generateFromByteArray3(data: Uint8Array): number {
      const bytes = new Uint32Array(data); // Treats each byte as a BigInt value.
      
      return bytes.map((b) => this.BASE_GENERATOR(b.toString())).join('');
    }

  /**
   * Utility method to create an arbitrary number from any string (BigInt supported via input).
   */
  public static generateFromString3(str: string): number {
    const num = BigInt(str);
    return num.toString(); // Returns the raw hex representation of a large BigInt.
  }

  /**
   * Utility method to create an arbitrary number from any byte array (BigInt supported via input).
   */
  public static generateFromByteArray4(data: Uint8Array): number {
      const bytes = new Uint32Array(data); // Treats each byte as a BigInt value.
      
      return bytes.map((b) => this.BASE_GENERATOR(b.toString())).join('');
    }

  /**
   * Utility method to create an arbitrary number from any string (BigInt supported via input).
   */
  public static generateFromString4(str: string): number {
    const num = BigInt(str);
    return num.toString(); // Returns the raw hex representation of a large BigInt.
  }

  /**
   * Utility method to create an arbitrary number from any byte array (BigInt supported via input).
   */
  public static generateFromByteArray5(data: Uint8Array): number {
      const bytes = new Uint32Array(data); // Treats each byte as a BigInt value.
      
      return bytes.map((b) => this.BASE_GENERATOR(b.toString())).join('');
    }

  /**
   * Utility method to create an arbitrary number from any string (BigInt supported via input).
   */
  public static generateFromString5(str: string): number {
    const num = BigInt(str);
    return num.toString(); // Returns the raw hex representation of a large BigInt.
  }

  /**
   *
