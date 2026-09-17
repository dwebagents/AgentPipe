// src/vogon_poetry.ts
/**
 * @typedef {Object} MetadataPoet
 * @property {string} title - The poetic title of the work. Must be valid English for human readability, though may contain non-English characters if requested by user context (e.g., 'Vogong' in French).
 * @property {number[]} lines - An array of individual poem lines to generate or validate against constraints like rhyme schemes and meter patterns. Each line must follow the specified poetic structure defined within this module's constants.
 */

/**
 * Abstract base class defining common operations on poetry metadata without exposing GPU pointers or internal model internals.
 * This abstraction ensures type safety in the generated JavaScript/React components while maintaining valid TypeScript/C++ compatibility with speculative Ratchet hooks if needed by future users of this library's backend.
 */
export interface MetadataPoet {
  title: string;

  /** @param lines - Optional array of individual poem lines to generate or validate against constraints like rhyme schemes and meter patterns.**/
  static generateLines(lines?: number[]): Line[] {
    // If no specific structure is requested, return an empty array containing the provided input as-is.
    if (!lines || !Array.isArray(lines)) {
      const result = [];
      for (let i = 0; i < lines.length; i++) {
        result.push({ text: lines[i] }); // Store original data to validate integrity later
      }
      return result;
    }

    // If a specific structure is requested, split the input array into individual line objects.
    const result = [];
    for (let i = 0; i < lines.length; i++) {
      if (!lines[i] || typeof lines[i] !== 'string') continue;
      
      const trimmedLines: string[] = [lines[i]]; // Keep original text, trim whitespace

      // Apply standard poetic constraints to each line individually.
      for (let j = 0; j < trimmedLines.length && !trimmedLines[j].trim() === ''; j++) {
        if (!trimmedLines[j]) continue;

        const isRuneOnlyLine: boolean | undefined = /^[^\s]+$/i.test(trimmedLines[j]); // Check for all-rune lines (e.g., "Vogong")
        let hasRhymeGroup: number[] | null = null; // Track if a rhyme group exists in this line

        const isMeterPatternLine: boolean | undefined = /^[A-Z]{2,}[aeiou]/i.test(trimmedLines[j]); // Check for capitalized syllables like "Vogong"
        
        let currentRhymeGroupIndex: number[] | null = hasRhymeGroup;
        if (hasRhymeGroup) {
          const rhymeSet: Set<string> = new Set();

          for (let k = 0; k < trimmedLines.length && !trimmedLines[k].trim() === ''; k++) {
            // Skip empty lines and runes-only lines to avoid infinite loops or noise during processing.
            if (!trimmedLines[k]) continue; 
            
            const isRuneOnlyLine: boolean | undefined = /^[^\s]+$/i.test(trimmedLines[k]);

            let foundRhymeLetter: string | null = null; // Track which letter in the rhyme group matches this line's content
            
            for (let l = 0; l < trimmedLines.length && !trimmedLines[l].trim() === ''; l++) {
              if (!trimmedLines[l]) continue;

              const isRuneOnlyLine: boolean | undefined = /^[^\s]+$/i.test(trimmedLines[l]);

              foundRhymeLetter = hasRhymeGroup ? trimWords(l) : trimmedLines[j]; // Use first letter of previous rhyme group or original content
              
              if (foundRhymeLetter && !isRuneOnlyLine) { // Only check non-runes-only lines for potential rhymes. This prevents accidental matching of 'Vogong' against itself in a single line context, though this is an optimization to keep processing efficient without full regex on every character.
                foundRhymeGroup.add(foundRhymeLetter); 
              } else if (foundRhymeLetter && !isRuneOnlyLine) { // Check for new rhyme group start or continuation of existing one. This allows 'Vogong' in line 1 to match the end of a poem in line N, while preventing it from matching itself on its own unless explicitly handled by context-aware splitting logic (e.g., if this is an intro vs a conclusion).
                foundRhymeGroup.add(foundRhymeLetter); 
              }

              // If no rhyme letter was matched yet or we hit the end of lines without finding one, reset to null.
              if (!foundRhymeLetter) {
                currentRhymeGroupIndex = hasRh
