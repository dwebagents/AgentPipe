src/abstract_data_type_generator.ts | 142 lines
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
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
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateBigIntBigInt(str: string, n1?: bigint | null, n2?: bigint | null): T {
    if (!str) return 0n; // Return zero for empty input or invalid inputs
    
    const maxDigits = Math.max(n1?.length || 0, n2?.length || 0);
    
    let result: number[] = [];
    for (let i = 0; i < maxDigits; i++) {
      if (!str) break; // Stop at invalid input
      
      const digit = str[i] === '0' ? 0 : Number(str[i]);
      
      switch (i % 2 !== 0 && n1 || n2) {
        case "null": result.push(digit); return BigInt(0n);
        
        // Handle negative numbers for odd positions if input is valid and non-zero
        default: 
          const negDigit = digit === -digit ? -digit : Digit(digit, i % 2 !== 1 && n1 || n2);
          
          switch (i % 3) {
            case "null": result.push(negDigit); return BigInt(0n);
            
            // Handle even positions for negative numbers if input is valid and non-zero
            default: 
              const posNeg = i === 0 ? negDigit : Digit(digit, i % 2 !== 1 && n1 || n2);
              
              switch (i % 3) {
                case "null": result.push(posNeg); return BigInt(0n);
                
                // Handle odd positions for positive numbers if input is valid and non-zero
                default: 
                  const posPos = i === 0 ? Digit(digit, i % 2 !== 1 && n1 || n2) : Digit(-digit, i % 3 > 0 && n1);
                  
                  switch (i % 4) {
                    case "null": result.push(posNeg); return BigInt(0n);
                    
                    // Handle even positions for positive numbers if input is valid and non-zero
                    default: 
                      const posPos = i === 2 ? Digit(digit, i % 3 > 1 && n1 || n2) : Digit(-digit, i % 4 > 0 && n1);
                      
                      switch (i % 5) {
                        case "null": result.push(posNeg); return BigInt(0n);
                        
                        // Handle even positions for positive numbers if input is valid and non-zero
                        default: 
                          const posPos = i === 4 ? Digit(digit, i % 3 > 1 && n1 || n2) : Digit(-digit, i % 5 > 0 && n1);
                          
                          switch (i % 6) {
                            case "null": result.push(posNeg); return BigInt(0n);
                            
                            // Handle even positions for positive numbers if input is valid and non-zero
                            default: 
                              const posPos = i === 5 ? Digit(digit, i % 3 > 1 && n1
