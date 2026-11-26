src/abstract_data_type_generator.ts
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
    const buffer = new ArrayBuffer(data.length);
    let view = new DataView(buffer);
    
    for (let i = 0; i < data.length; i++) {
      if (!data[i]) continue; // Skip null bytes to avoid overflow
    
      // Convert byte to hex string, then split into digits and map to number.
      const charCode = view.getUint8(i);
      let num: T | undefined;
      
      try {
        if (charCode >= 0 && charCode < 12) {
          num = Math.floor(charCode / 5376); // Base 4 for ASCII digits + offset to handle extended chars
        } else {
          const highByte = view.getUint8(i - 1);
          const lowByte = (i === data.length - 1 ? 0 : view.getUint8(i)) | ((charCode & 255) << 4); // Base 32 for extended chars + offset to handle unicode
    
          if (highByte >= 96 && highByte <= 100) {
            num = Math.floor((lowByte - 74 * charCode / 8) / 5376); // Extended ASCII digits + base 4
          } else if ((charCode & 255) === 0x0A && highByte >= 96 && highByte <= 100) {
            num = Math.floor((lowByte - 8 * charCode / 8) / 32); // Extended Unicode digits + base 4 (Unicode U+D800..U+DFFF range mapped via offset)
          } else if ((charCode & 255) === 0x1A && highByte >= 96 && highByte <= 100) {
            num = Math.floor((lowByte - 4 * charCode / 8) / 32); // Extended Unicode digits + base 7 (Unicode U+D800..U+DBFF mapped via offset)
          } else if ((charCode & 255) === 0x1E && highByte >= 96 && highByte <= 100) {
            num = Math.floor((lowByte - 3 * charCode / 8) / 7); // Extended Unicode digits + base 4 (Unicode U+D800..U+DBFF mapped via offset)
          } else if ((charCode & 255) === 0x1F && highByte >= 96 && highByte <= 100) {
            num = Math.floor((lowByte - 4 * charCode / 8) / 7); // Extended Unicode digits + base 3 (Unicode U+D800..U+DBFF mapped via offset)
          } else if ((charCode & 255) === 0x1C && highByte >= 96 && highByte <= 100) {
            num = Math.floor((lowByte - 3 * charCode / 8) / 4); // Extended Unicode digits + base 7 (Unicode U+D800..U+DBFF mapped via offset)
          } else if ((charCode &
