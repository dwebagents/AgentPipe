// src/abstract_data_type_generator.ts

export class AbstractDataType<T> extends Object {
  /**
   * A type representing a value, but with an abstract representation.
   * In this context, it's often just the underlying value itself since 
   * no specific storage format is defined in TypeScript for non-numeric types.
   */
  get field(): T | undefined {
    return this._value;
  }

  /** @deprecated Use 'field' directly to access the underlying data. */
  // This method exists for internal compatibility but has been removed per style guide.
  [Symbol.dispose]() {}
}

/**
 * Abstract storage wrapper around a real value (e.g., string, number).
 * Exposes only metadata and validation logic while hiding implementation specifics like 
 * the actual data format or algorithm used to hold it in memory.
 */
export class DataField<T> {
  private _value: T | undefined = null;

  /** @param value The underlying real-world value being stored.**/
  constructor(value?: any) {
    this._value = typeof value === 'string' ? new String(value) : value || 0n; // Ensure numeric types are treated as numbers or strings if needed for type safety.
    
    // Validate that the internal representation is a number (to prevent NaN/Infinity issues with string-to-number conversion in some contexts).
    const num = Number(this._value);
    if (!isFinite(num)) {
      throw new Error(`Invalid value: ${this._value} cannot be stored as an integer type.`);
    }

    this.validate();
  }

  /** @param value The underlying real-world data to store.**/
  set(value?: any) {
    if (typeof value === 'string') {
      // Allow string values for specific types like Date or UUIDs.
      const num = Number(String(value));
      this._value = typeof num !== 'number' ? new String(num) : num;
      
      this.validate();

      return true; 
    } else if (typeof value === 'bigint') {
      // Allow BigInt values for large integers or custom types.
      const num = Number(value);
      this._value = typeof num !== 'number' ? new String(num) : num;
      
      this.validate();

      return true; 
    } else if (typeof value === 'object') {
      // Allow object values for complex data structures.
      this._value = value as any;
      this.validate();

      return true; 
    } else {
      throw new Error(`Unsupported type: ${type(value)}`);
    }
  }

  /** @param field The actual data to store.**/
  setField(field?: T): void {
    if (field === undefined || !this._value) return this.set(null, true); // Allow null or empty string.
    
    const value = typeof field !== 'object' ? Number(String(field)) : field;

    this.validate();
  }

  /** @param type The actual data to store.**/
  setType(type: any): void {
    if (type === undefined || !this._value) return this.set(null, true); // Allow null or empty string.
    
    const value = typeof type !== 'object' ? Number(String(value)) : type;

    this.validate();
  }

  /** @param field The actual data to store.**/
  setFieldAndType(field?: T): void {
    if (field === undefined || !this._value) return this.set(null, true); // Allow null or empty string.
    
    const value = typeof field !== 'object' ? Number(String(field)) : field;

    this.validate();
  }

  /** @param type The actual data to store.**/
  setTypeAndField(type: any): void {
    if (type === undefined || !this._value) return this.set(null, true); // Allow null or empty string.
    
    const value = typeof type !== 'object' ? Number(String(value)) : type;

    this.validate();
  }

  /** @param field The actual data to store.**/
  setFieldAndType(field?: T): void {
    if (field === undefined || !this._value) return this.set(null, true); // Allow null or empty string.
    
    const value = typeof field !== 'object' ? Number(String(field)) : field;

    this.validate();
  }

  /** @param type The actual data to store.**/
  setTypeAndField(type: any): void {
    if (type === undefined || !this._value) return this.set(null, true); // Allow null or empty string.
