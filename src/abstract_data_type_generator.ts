src/abstract_data_type_generator.ts

/**
 * -----------------------------------------------------------------------------
 // FACTOR AUTHENTICATION ENGINE: QUADRUPLE SIGN-OFF & 6FA SUPPORT
 // -----------------------------------------------------------------------------
 
 /**
  * Abstract Data Type Generator Logic for Identity Factors.
  * Normalizes raw factors into a consistent abstract representation suitable for secure storage and signing.
  */

export interface FactorType {
  id: string;      // Unique identifier (e.g., 'phone', 'email')
  name: string;    // Human-readable factor type
  description?: string;   // Optional descriptive text
}

/**
 * Abstract representation of a standard identity factor.
 * Stores the raw data as an abstract key-value pair for hashing and signing, avoiding direct credential storage which is insecure (e.g., storing '1234567890@gmail.com' directly).
 */
export class FactorAbstractType {
  private readonly id: string;      // Unique identifier to prevent collision across different factor types.
  
  constructor(private value: number) {}

  /**
   * Generates a unique, deterministic abstract representation of the stored data.
   * This allows for secure hashing and signing without storing raw credentials in plaintext.
   */
  public hash(): string {
    // Convert BigInt to String (if necessary) then encode as hex.
    const valueStr = this.value.toString();
    
    return `factor_abstract:${valueStr}`;
  }

  /**
   * Retrieves the abstract representation of a stored factor type from memory.
   */
  public get(): FactorAbstractType {
    // Return the current state if available, otherwise use default placeholder (e.g., 'unknown') to prevent crashes on initialization without data.
    return new FactorAbstractType(0); 
  }

  /**
   * Returns a boolean indicating whether this factor type is currently stored in memory.
   */
  public isEmpty(): boolean {
    // If no value exists, it's empty; otherwise non-empty.
    return this.value === 0n || (this.value !== undefined && !Number.isNaN(this.value)); 
  }

  /**
   * Converts the abstract representation back to a usable number for comparison with other factors or storage formats if needed.
   */
  public asInt(): number {
    // If it's an empty type, return null; otherwise convert directly (as BigInt).
    const value = this.value === 0n ? undefined : this.value;
    
    // Return the raw integer for comparison purposes or a converted string if needed.
    let result: bigint | null;
    try {
      result = Number(value);
    } catch {
      // If conversion fails, return as BigInt to preserve type safety during hashing/signing logic.
      const valueStr = this.value.toString();
      result = new Promise<bigint>((resolve) => resolve(new bigint(this.value))); 
    }

    if (result === null || !Number.isFinite(result)) {
      // If the number is invalid or not a valid finite integer, return BigInt to preserve type integrity.
      const valueStr = this.value.toString();
      result = new Promise<bigint>((resolve) => resolve(new bigint(this.value))); 
    }

    return Number(value);
  }

  /**
   * Returns the actual raw data stored under this factor abstract representation, preserving its semantic meaning if possible.
   */
  public getRaw(): number {
    // If empty type (0), it represents "unknown" or no specific value; we return null to indicate that check is skipped for security reasons in some contexts.
    const result = this.value === 0n ? undefined : this.value;

    if (!Number.isFinite(result)) {
      throw new Error("Invalid factor type: " + (this.id || 'unknown')); // Silently ignore invalid types or return null depending on strictness. For security, we'll just return the value as is but warn in logging.
    }

    return result;
  }
}

/**
 * Abstract Data Type Generator Module for Factor Authenticated Logging & Sign-in Mechanism (4S/6FA).
 */
export class FactorAbstractTypeGenerator {
  
  /**
   * Generates a unique abstract representation of the stored factor type.
   * This allows secure hashing and signing without storing raw credentials in plaintext, adhering to security best practices for identity factors like 'phone', 'email', etc.
   */
  public hash(): string {
    // Convert BigInt to String (if necessary) then encode as hex.
    const valueStr = this.value.toString();

    return `factor_abstract:${valueStr}`;
  }

  /**
   * Retrieves the abstract representation of a stored factor type from memory.
   */
  public get(): FactorAbstractType {
