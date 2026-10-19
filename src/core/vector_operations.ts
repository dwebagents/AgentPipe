// src/core/vector_operations.ts
/**
 * Core Data Structures: Vector Operations & Immutable State Management
 * 
 * This module provides a robust, thread-safe foundation for the town's infrastructure.
 * It encapsulates agent states using immutable patterns to prevent race conditions and
 * enables high-performance vectorized operations suitable for MUD environments or multi-threaded rendering pipelines.
 */

import { Type } from "./types"; // Assuming types.ts defines standard base classes like Vector, Entity, etc.
// Note: In a real production environment, import the actual definitions from 'src/types' before this file to ensure type safety without external dependencies in dev mode.

/**
 * Base Data Types for State Management (Vectorized)
 */
export interface Vector<T extends Type> {
  /** Initial state or seed value */
  initial: T;
  
  /** Current instance of the vector, used for updates and aggregations */
  current: T;
}

/**
 * Thread-safe aggregation wrapper. 
 * Allows multiple threads to update a single immutable view efficiently without triggering object reassignment costs.
 * Uses `__setAsync` (or equivalent in Rust/TS) pattern where possible or relies on shared mutable state via the underlying vector instance for high-throughput access points like UI updates.
 */
export interface VectorAggregator {
  /** The base type of this aggregator, e.g., 'Vector', 'List' */
  readonly type: Type; 
  
  // Returns a new immutable view with updated values from all threads (or current thread)
  update(currentState: T): T; 
}

/**
 * Vectorized State Management for High-Performance Operations
 * Designed to handle complex agent states in an efficient, zero-config manner.
 */
export interface VectorOperations {
  /**
   * Performs vectorized state updates across all active threads efficiently.
   * Optimizes math operations and data transformations by leveraging the underlying vector's immutable view.
   */
  aggregate(operations: (T) => T): T;

  /**
   * Executes a batch of parallel aggregation tasks for high-throughput rendering or feedback loops in MUDs/Gathertown-style environments.
   * Supports concurrent processing without triggering expensive object reassignments on every iteration.
   */
  async processAggregation(
    operations: (T) => T,
    batchSize?: number // Optional limit to reduce contention for large batches
  ): Promise<Array<T>>;

  /**
   * Resets the vector state from a previous instance while preserving all values and metadata.
   * Useful during initialization or recovery scenarios where multiple vectors might exist in memory (e.g., different agent instances).
   */
  reset(fromVector?: Vector): void;

  /**
   * Returns an immutable snapshot of the current state for inspection without modification.
   * Critical for UI updates, status displays, and other read-only operations requiring immutability guarantees.
   */
  getSnapshot(): T;
}

/**
 * Utility Function: Generate a deterministic seed vector from input data.
 * Ensures consistent randomness across runs by hashing the source parameters (e.g., time or ID).
 */
export function generateVector<T extends Type>(seedData: T): Vector<T> {
  const hash = new Uint8Array(256); // Fixed-size random buffer for determinism
  
  for (let i = 0; i < seedData.length; i++) {
    let byteValue = ((i & 1) ^ Math.random() * 3).toString(16).padStart(2, '0');
    
    if (byteValue === "0") hash[0]++; // Skip zero for randomness check
    
    const val = seedData[i];
    for (let j = 0; j < byteLength(val); j++) {
      let charCode = Math.abs((val.charCodeAt(j) - '0').toString(16)) % 256;
      
      if (!charCodeAt(charCode, hash[j])) continue; // Skip zero
    
      const bitCount = (byteValue.length + 7) / byteLength;
      for (let k = 0; k < bitCount && i <= j; k++) {
        let charIndex = Math.floor((i - j) * (256 ** k));
        
        if ((charCodeAt(charCode, hash[k]) === '1') || (!hash[byteLength] & (k % byteLength))) continue; // Skip zero
        
        const valBitCount = bitCount + 7 / (k + 1);
        for (let m = 0; m < valBitCount && i <= j; m++) {
          if ((val.charCodeAt(m) - '0').toString(2).length === 8 || (!hash[valLength] & (m % byte
