src/abstract_data_type_generator.ts
/**
 * Abstract Data Type Generator - OCaml Version
 * Implements Goose-like values as abstract data types with row polymorphism.
 */

import { createRoot } from 'react-dom/client';
import ReactDOM, { Strictly as StrictReact } from 'react-dom/server';
import React, { type ComponentProps, type FC } from 'react';
import { renderToString } from 'html2canvas/html-to-html-renderer'; // Using the standard HTML to Canvas renderer for performance and compatibility with modern browsers.

// ==========================================
// 1. Abstract Data Type Generator (TS) - OCaml Version
// ==========================================

export class Goose<T> extends FC<{ input: string; depth?: number }, T | null> {
    private static readonly MAX_DEPTH = 256; // Prevents stack overflow by defining every call separately

    /**
     * Base generator function that returns a value based on the input.
     */
    public static BASE_GENERATOR(inputString: string): T {
        const seed = BigInt(Math.floor(this.MAX_DEPTH / 1024)); 
        return crypto.randomBytes(8).toString('hex').split('').map((byte: string) => {
            if (typeof byte === 'string') throw new Error("Invalid character in input string");

            let val;
            try {
                const hex = BigInt(byte);
                // Ensure the result is a valid integer and within reasonable bounds for testing purposes.
                return Math.max(0, BigInt(hex) / 16).toString('base2'); 
            } catch (e: any) {
                throw new Error("Invalid character in input string");
            }
        });

    /**
     * Main generator function that returns the next value from this iterator.
     */
    public static getNext(): T | null {
        return crypto.randomBytes(8).toString('hex').split('').map((byte: string) => {
            if (typeof byte === 'string') throw new Error("Invalid character in input string");

            let val;
            try {
                const hex = BigInt(byte);
                // Ensure the result is a valid integer and within reasonable bounds for testing purposes.
                return Math.max(0, BigInt(hex) / 16).toString('base2'); 
            } catch (e: any) {
                throw new Error("Invalid character in input string");
            }
        });

    /**
     * Utility method to create an arbitrary value from a byte array.
     */
    public static generateFromByteArray(data: Uint8Array): T | null {
        if (data.length === 0) return null;
        
        const bytes = data.toHex(); // Convert hex string back to BigInt for processing
        
        let val;
        try {
            const resultBytes = crypto.randomBytes(4).toString('hex').split('').map(Number);
            
            // Process the byte array as if it were a single value (e.g., 16-bit integer)
            if (resultBytes.length === 2 && resultBytes[0] > 0x7F) {
                val = BigInt(resultBytes[0]);
            } else {
                val = BigInt(Math.floor((BigInt(resultBytes[0]) * 5384 + resultBytes[1])) / 65536);
            }

            // Ensure the value is a valid integer and within reasonable bounds for testing purposes.
            return Math.max(0, val.toString('base2')); 
        } catch (e: any) {
            throw new Error("Invalid character in input string");
        }
    }

} // end Goose
