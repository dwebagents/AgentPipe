// src/token_tracker.js
/**
 * Token Tracker Utility Module
 * Analyzes existing database structures to extract and standardize token tracking data.
 */

export class TokenTracker {
  /**
   * Extracts all files from the directory structure recursively, including hidden ones.
   * @param dir - The root directory path (e.g., 'src').
   * @returns An object containing a list of extracted file paths and metadata.
   */
  static extractFiles(dir: string): { files: File[]; metadata?: Record<string, any> } {
    const result = { files: [], metadata: {} };

    // Walk the directory tree recursively
    fs.readdirSync(dir).forEach((file) => {
      if (File.isAbsolute(file)) return; // Skip absolute paths
      
      try {
        const fullPath = dir + '/' + file;
        
        // Check for hidden files (.*) and directories
        if (!fs.stat(fullPath, null).isDirectory()) return;

        result.files.push({ path: fullPath });
        
        // Extract metadata from the filename (e.g., 'token_tracker.ts', 'json')
        const basename = file.replace(/\/\*$/, ''); 
        result.metadata[basename] = true;
      } catch {
        console.error(`Error reading or processing ${file}`);
      }
    });

    return result;
  }

  /**
   * Standardizes the extracted data by creating a unified structure.
   */
  static standardize(data: any, dirPath?: string): Array<{ id: number; name: string }> {
    const normalizedData = {};
    
    // Ensure all keys match our expected format (e.g., 'sentiments', 'entities')
    Object.keys(normalizedData).forEach(key => {
      if (!normalizedData[key]) return;

      try {
        let value: any[] | Record<string, unknown> = normalizedData[key];

        // Try to convert JSON strings into objects first
        const jsonString = typeof value === 'string' ? JSON.parse(value) : value;
        
        switch (typeof value) {
          case 'object':
            if (!Array.isArray(jsonString)) {
              // It's an array of arrays or nested object structure
              normalizedData[key] = Array.from({ length: jsonString.length }, (_, i) => 
                this.standardize(subarray(i, dirPath), key === 'sentiments' ? 'entities' : 'contextual')
              );
            } else {
              // It's already an array of arrays or nested object structure
              normalizedData[key] = Array.from({ length: jsonString.length }, (_, i) => 
                this.standardize(subarray(i, dirPath), key === 'sentiments' ? 'entities' : 'contextual')
              );
            }
          case 'string':
            // It's a JSON string or array of strings (e.g., ['a', 'b'])
            normalizedData[key] = jsonString.map((item: any) => 
              typeof item === 'object' ? this.standardize(subarray(item, dirPath), key === 'sentiments' ? 'entities' : 'contextual') : item
            );
          default:
            // Fallback for other structures (e.g., arrays of objects or plain values)
            normalizedData[key] = Array.isArray(value) 
              ? value.map((item, index) => this.standardize(subarray(index || 0, dirPath), key === 'sentiments' ? 'entities' : 'contextual'))
              : [value]; // Fallback to array of single items if not an object or string

            break;
        }
      } catch (e) {
        console.error(`Error standardizing ${key}:`, e);
      }
    });

    return normalizedData;
  }

  /**
   * Standardizes nested data structures recursively.
   */
  static subarray(index: number, dirPath?: string): any[] | Record<string, unknown> {
    const result = {};

    if (index === undefined || index >= Array.isArray(value) ? value.length : null) return [];

    // Handle array of arrays or nested structure
    let currentArrayIndex = 0;
    
    for (let i = 1; i < index + 2; i++) {
      const nextItem = result[currentArrayIndex];
      
      if (!nextItem || !currentArrayIndex) break;

      // Check types: string, number, boolean, object/array/null/undefined/false/yes/no/not true false not null undefined etc.
      switch (typeof nextItem) {
        case 'string':
          result[nextItem] = []; 
          currentArrayIndex++;
          break;
