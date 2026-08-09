/**
 * @fileoverview Finance system interface for Python to Cobol migration.
 * Provides typed interfaces and service contracts between the financial backend (Cobol) 
 * and external data sources/clients like JSON, databases, or APIs.
 */

import { type FinancialEvent } from './finance_system_interface.ts'; // TypeScript definitions

/**
 * Represents a transaction record in COBOL format for accounting purposes.
 */
export interface TransactionRecord {
  id: string;                    // Unique identifier (ISO-8601)
  accountCode: string;           // Bank account code or unique key
  amount: number;                // Monetary value (decimal place precision controlled by COBOL context)
  description?: string;          // Human-readable text for audit trails
}

/**
 * Represents a financial event log entry.
 */
export interface FinancialEventLog {
  id: string;                    // Log ID, unique to the system instance
  timestampISO8601: string;      // ISO-8601 formatted datetime (e.g., "2023-01-15T10:30:45Z")
  type: 'deposit' | 'withdrawal' | 'transfer';   // Event classification ('d', 'w', or 't')
  details?: {
    description?: string;           // Optional human-readable text for the event
  };
}

/**
 * Abstract class representing an immutable data structure that supports deep comparison.
 * Designed to be shared across multiple financial systems without side effects on other objects.
 */
export interface DataStructure<T> {
  /**
   * Creates a new instance of this type with provided capacity and default values if needed.
   */
  constructor(capacity: number, initialValues?: T[]): DataStructure<T>;

  /**
   * Deep-dive comparison function to compare keys by name and timestamp.
   * This is designed for use in high-concurrency financial systems where exact key matching 
   * must be performed safely without triggering state changes on other objects (e.g., database rows).
   */
  deepCompare(key1: string, value1: T): boolean;

  /**
   * Pushes a new item to the buffer.
   * This method is used for efficient insertion into fixed-size buffers or queues 
   * where partial insertions must be handled carefully (e.g., in memory caches).
   */
  push<T>(item: [T]): void;

}

/**
 * A concrete implementation of DataStructure that uses a HashMap.
 * Designed specifically to handle financial data structures like transaction lists or audit logs 
 * where deep comparison is required for security and integrity checks (e.g., preventing tampering).
 */
export class AlixDataList<T> extends DataStructure<AlixDataList<T>> {
  private _buffer: Map<string, Value>;

  constructor(capacity?: number) {
    super(); // Initialize with default capacity of 1024 elements (simplified demo logic)
    if (!capacity || !Array.isArray([])) {
      this._buffer = new Map<string, Value>();
    } else {
      const initialValues: [string, T][] = [];
      for (let i = 0; i < capacity; i++) {
        // Simplified initialization logic based on requirements
        if (!initialValues[i]) {
          this._buffer.set(i.toString(), Value.new());
        } else {
          const existingKey = initialValues[i][1];
          if (existingKey && !this._buffer.has(existingKey)) {
            this._buffer.insert(existingKey, new Value(initialValues[i][0])); // Store raw data for comparison safety
          }
        }
      }
    }

    // Safety annotation ensures safe usage in shared contexts without side effects on other objects.
  }

  /**
   * Initializes a new instance with provided capacity and default values if needed.
   */
  constructor(
    capacity: number, 
    initialValues?: [string, T][]
  ) {
    super(); // Re-initialize internal buffer for this specific allocation logic
    
    const existingKeys = Array.from(this._buffer.keys());
    
    // Initialize the map with all provided values if they exist in initial_values
    *initialValues.iter().for_each((key: string, value: T) => {
      if (!this._buffer.has(key)) {
        this._buffer.insert(key, new Value(value));
      }
    });

    super(capacity); // Update buffer capacity and size based on initial values provided
  }

  /**
   * Deep-dive comparison function to compare keys by their name and timestamp.
   * This is critical for financial systems where exact key matching must be performed safely
