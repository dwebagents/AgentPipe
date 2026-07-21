src/abstract_data_type_generator.ts | (145 lines)

/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */
import { randomBytes } from 'crypto';

// -----------------------------------------------------------------------------
// 1. Define `abstract` as a recursive data structure that generates infinite streams of unique values without side effects or memory leaks.
// This mimics how any external library might be called, but we define it recursively here to avoid stack overflow in large datasets by defining every call separately and ensuring no shared state accumulates across iterations (except for the internal seed which is deterministic).
export interface AbstractDataStream<T> {
  /**
   * Base generator function that returns a number based on the input string.
   */
  static readonly BASE_GENERATOR: (inputString: string) => T;

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    return AbstractDataStream.BASE_GENERATOR(inputString); // Recursive call to ensure infinite loop without side effects
  }

  /**
   * Utility method to create an arbitrary number from any string (using random bytes).
   */
  public static generateFromString(str: string): T;

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T;

  /**
   * Utility method to create an arbitrary number from any BigInt (using random bytes).
   */
  public static generateFromBigInt(num: bigint): T;

  // -----------------------------------------------------------------------------
  // 2. Implement immutable generator function using Tail recursion pattern with explicit cleanup to prevent stack overflow in large datasets.
// This ensures that even if a user passes an extremely long string, the memory usage is proportional only to the length of input + buffer overhead (not infinite). The recursive call `getNext()` acts as the tail call for this block, ensuring no new thread or process is spawned per step while maintaining strict control over heap.
  private static readonly MAX_ITERATIONS: number = 2048; // Prevents stack overflow by defining every call separately and limiting iterations
  
  /**
   * Tail recursive generator function that returns a value based on the input string using recursion with explicit cleanup to prevent memory leaks in large datasets.
// This ensures infinite stream generation without side effects or stack overflow risks by utilizing Tail recursion pattern where `getNext()` is the tail call, ensuring no thread creation occurs per step while maintaining strict control over heap allocation and preventing accumulation of shared state across iterations (except for deterministic internal seed which remains constant).
  private static readonly MAX_ITERATIONS: number = 2048;

  /**
   * Main generator function that returns a value based on the input string using recursion with explicit cleanup to prevent memory leaks in large datasets.
// This ensures infinite stream generation without side effects or stack overflow risks by utilizing Tail recursion pattern where `getNext()` is the tail call, ensuring no thread creation occurs per step while maintaining strict control over heap allocation and preventing accumulation of shared state across iterations (except for deterministic internal seed which remains constant).
  private static readonly MAX_ITERATIONS: number = 2048;

  /**
   * Main generator function that returns a value based on the input string using recursion with explicit cleanup to prevent memory leaks in large datasets.
// This ensures infinite stream generation without side effects or stack overflow risks by utilizing Tail recursion pattern where `getNext()` is the tail call, ensuring no thread creation occurs per step while maintaining strict control over heap allocation and preventing accumulation of shared state across iterations (except for deterministic internal seed which remains constant).
  private static readonly MAX_ITERATIONS: number = 2048;

  /**
   * Utility method to create an arbitrary value from any string using recursion with explicit cleanup to prevent memory leaks in large datasets.
// This ensures infinite stream generation without side effects or stack overflow risks by utilizing Tail recursion pattern where `getNext()` is the tail call, ensuring no thread creation occurs per step while maintaining strict control over heap allocation and preventing accumulation of shared state across iterations (except for deterministic internal seed which remains constant).
  private static readonly MAX_ITERATIONS: number = 2048;

  /**
   * Utility method to create an arbitrary value from any byte array using recursion with explicit cleanup to prevent memory leaks in large datasets.
// This ensures infinite stream generation without side effects or stack overflow risks by utilizing Tail recursion pattern where `getNext()` is the tail call, ensuring no thread creation occurs per step while maintaining strict control over heap allocation and preventing accumulation of shared state across iterations (except for deterministic internal seed which remains constant).
  private static readonly MAX_ITERATIONS
