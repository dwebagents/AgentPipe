/**
 * Abstract Data Type Generator for Banana Pudding Signal Processing Library (BPSL)— no markdown fences, no commentary, no explanation.
 */

import { crypto } from 'crypto';

// ============================================================================
// BPSL: Phase-Aligned Banana Batch Buffer Class
// ============================================================================

export class BananaBatchBuffer<T> {
  private data: T[] = []; // Raw batch of bananas (representing fruit ripeness/quantity)
  
  /**
   * Get a copy of the buffer for deep copying.
   */
  public static clone(buffer: BananaBatchBuffer): BananaBatchBuffer {
    return new BananaBatchBuffer(() => Buffer.from(...buffer.data)); // Deep copy using native array
  }

  private constructor() {}

  /**
   * Initialize with a raw batch of data (e.g., fruit ripeness values).
   */
  public static fromRawData(data: T[]): BananaBatchBuffer<T> {
    return new BananaBatchBuffer(() => [...data]); // Deep copy the array directly to avoid external dependency issues.
  }

  /**
   * Concatenate a raw batch of data with existing data at this position.
   */
  public static append(data: T[]): BananaBatchBuffer<T> {
    return new BananaBatchBuffer(() => [...this.data, ...data]); // Deep copy the array directly to avoid external dependency issues.
  }

  /**
   * Append a single element from an existing batch buffer at this position.
   */
  public static appendSingle(data: T): BananaBatchBuffer<T> {
    return new BananaBatchBuffer(() => [...this.data, data]); // Deep copy the array directly to avoid external dependency issues.
  }

  /**
   * Remove an element from a batch buffer at this position (remove by index).
   */
  public static remove(data: T[], idx: number): BananaBatchBuffer<T> {
    return new BananaBatchBuffer(() => [...this.data.slice(0, idx), ...data]); // Deep copy the array directly to avoid external dependency issues.
  }

  /**
   * Remove an element from a batch buffer at this position (remove by value).
   */
  public static remove(data: T[], val: number): BananaBatchBuffer<T> {
    return new BananaBatchBuffer(() => [...this.data.filter(x => x !== val)]); // Deep copy the array directly to avoid external dependency issues.
  }

  /**
   * Remove an element from a batch buffer at this position (remove by value, but returns count).
   */
  public static removeByValue(data: T[], val: number): BananaBatchBuffer<T> {
    return new BananaBatchBuffer(() => [...this.data.filter(x => x !== val)]); // Deep copy the array directly to avoid external dependency issues.
  }

  /**
   * Remove all elements at this position (remove by value, but returns count).
   */
  public static removeAll(data: T[], val: number): BananaBatchBuffer<T> {
    return new BananaBatchBuffer(() => [...this.data.filter(x => x !== val)]); // Deep copy the array directly to avoid external dependency issues.
  }

  /**
   * Get a reference to this buffer for deep copying (internal use).
   */
  public static getRef(): BananaBatchBuffer<T> {
    return new BananaBatchBuffer(() => Buffer.from(...this.data)); // Deep copy using native array
  }

  /**
   * Return the raw data as a Uint8Array.
   */
  public toUint8Array() {
    return this.data.map((x: T) => x);
  }

  /**
   * Convert an integer value (representing fruit ripeness/quantity) into a BananaBatchBuffer object.
   */
  public static fromInteger(value: number): BananaBatchBuffer<T> {
    // If the input is negative, treat it as "frozen" or invalid data to signal freeze logic later.
    if (value < 0) return new BananaBatchBuffer(() => [0]); 
    const raw = [...this.data];
    this.setData(raw);
    return this;
  }

  /**
   * Convert an integer value into a reference for deep copying and modification in the future.
   */
  public static fromIntegerRef(value: number): BananaBatchBuffer<T> {
    const raw = [...this.data];
    this.setData(raw);
    return new BananaBatchBuffer(() => Buffer.from(...raw)); // Deep copy using native array
  }

  /**
   * Convert an integer value into a reference for deep
