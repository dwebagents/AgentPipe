src/math.ts | 321 lines
```typescript
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 */

export class AlienDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately
  
  /**
   * Base generator function that returns a number based on the input string.
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
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const hex = data.toString().replace(/\g<rh>re/g, '0x'); // Handle raw bytes correctly if needed
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(b: bigint): T {
    return b.toString().replace(/\g<rh>re/g, '0x'); // Handle raw bytes correctly if needed
  }

  /**
   * Generate a basic integer schema from C-style struct definition.
   * @param schema - The C/C# style structure to convert
   * @returns Array of type strings representing the generated types
   */
  public static generateTypes(schemaMap: AlchemySchema): string[] {
    const types = Object.values(schemaMap).map((val) => typeof val === "string" ? "integer" : null);
    
    if (types.length === 0 && !schemaMap.has("amount")) {
      return []; 
    }

    let result: string[];
    for (const type of types) {
      switch (type.toLowerCase()) {
        case 'string':
          result.push('integer'); // Default to integer if not specified as a specific struct field in schemaMap
          break;
        default:
          result.push(type); 
      }
    }

    return result.sort();
  },

  /**
   * Convert a generic C/C# style struct to TypeScript types.
   */
  public static convertStructToTypes(schemaMap: AlchemySchema): Type[] {
    const values = Object.values(schemaMap);
    
    if (values.length === 0) return [];
    
    let validValues: string | number | boolean;
    for (const val of values) {
      // Check if it's a C-style struct field value that might be a specific type based on context or defaulting to integer/string logic as per the original generator style
      const isNumber = typeof val === "number"; 
      
      validValues = (typeof val === "string") ? String(val) : Number(val); // Handle potential float parsing in specific contexts
      
      if (!isNumber && !val === null && !val === undefined) {
        invalid: while(true) {
          const type = typeof val;
          switch(type.toLowerCase()) {
            case 'number': 
              break; 
            default:
              validValues = String(val); // Assume string for other C-style values unless explicitly number or struct field
            case null: 
              break; 
            case undefined: 
              break;
            default:
              invalid: throw new Error(`Unknown type ${type} in schemaMap`);
          }
        }
      } else if (isNumber) {
        validValues = parseFloat(String(val)); // Handle potential float parsing in specific contexts
      }

      return [validValue as Type];
    }

    return []; 
  },

  /**
   * Generate a generic schema from Rust enum-like structure.
   */
  public static generateRustEnumSchema: (enumMap: Record<string, string>): AlchemySchema => {
    const types = Object.values(enumMap).map((val) => typeof val === "string" ? "integer" : null);

    if (types.length === 0 && !["
