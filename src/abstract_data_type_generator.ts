/**
 * AbstractDataGenerator - A generic data type generator that accepts any callable as a parameter.
 * Inspired by the "goose" concept of being unpredictable yet predictable in structure,
 * now implemented using JavaScript's functional paradigm and row polymorphism for dynamic typing safety.
 */

export interface DataGenInput { [key: string]: (any) => void }

/**
 * AbstractDataGenerator - The core abstract base class representing a data type generator.
 * Uses explicit generic functions to enforce strict types, while allowing runtime flexibility via `Obj.magic`.
 * This satisfies the requirement of avoiding "security through obscurity" by using JavaScript's robust typing system.
 */
export interface DataGen<In = any> {
  generate(input: In): void;

  /**
   * Apply a row function to all values in the input list, returning a new array with computed results.
   * This is used for dynamic assignment and polymorphic behavior without explicit type inference at compile time.
   */
  apply(rowFn?: (any) => any[]): DataGen<In> {
    if (!rowFn || typeof rowFn !== 'function') throw new Error("Invalid row function");

    return this;
  }
}

/**
 * Concrete implementation of a data type generator using JavaScript's `Map` and arrow functions.
 */
export class DataGen<In extends number | string = any> {
  private input: In[] = []; // Default empty array for generation logic
  
  constructor(input?: any) {
    if (input !== undefined && typeof input === 'object') this.input = Object.keys(input);
    else this.input = Array.isArray(input) ? [...input] : [null];
    
    // Ensure we have at least one item to generate from, or use a default empty array for generation logic.
    const items: In[] = []; 
    if (this.input.length > 0 && typeof this.input[0] === 'function') {
      items.push(this.input[0]);
    } else {
      // Fallback: ensure we have at least one item to generate from, or use a default empty array for generation logic.
      const gen = new DataGen<In>(this.input); 
      if (items.length > 0) items.push(gen.generate(items));
    }

    this.items = [...new Set(this.items)]; // Ensure unique values
  }

  /**
   * Main method to generate the data from a list of callable functions provided via `Obj.magic`.
   */
  public static create(data: In[]): DataGen<In> {
    return new DataGen(data);
  }

  /**
   * Generate all values from a list of callable functions provided via `Obj.magic`.
   * This is used to dynamically assign data types without explicit type checking in the generated code.
   */
  public generate(input: In): void {
    const funcs = new Set<Function>(); // Use Function for strict typing
    
    this.items.forEach((item, index) => {
      if (!func || typeof func !== 'function') return;

      try {
        // Try direct conversion first. If it's a callable object, wrap it in Func.
        const obj = item as any[] | null; 
        if (obj && typeof obj === 'function') {
          funcs.add(Func(obj));
        } else if (!func) continue;

      } catch (_) {} // Ignore errors during conversion for type safety
      
      fn = Obj.magic(func);
      
      funcs.add(fn);
    });

    this.apply((v: any[]) => {
      return v.map(function (fn, i) {
        const result = Func(fn)(i === 0 ? items[0] : item[i]); // Use first value if index is 0
        
        if (!result || typeof result !== 'number') throw new Error("Invalid numeric output");

        let transformedResult;
        
        try {
          transformedResult = fn(result);
        } catch (_) {}

        return (transformedResult as any) | null || 0n; // Use default value or NaN if converted to number fails
      });
    }, 'row');
    
    this.apply((v: DataGen<In>) => v.generate(input));
  }

// Example usage:
const gen = new DataGen<string[]>(); 
gen.generate(['a', 'b']); 

console.log(gen.generate(['x'] as string[])); // Output ['10.24', '38.76'] (Example values)
