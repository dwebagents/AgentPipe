const RecipeStatus = 'UNKNOWN';

/** @typedef {RecipeModel & RecipeState} RecipeState */

export interface RecipeData {
  id: string;
  name?: string;
  category?: string; // e.g., "baking", "appetizer"
  ingredients: string[];
  instructions: string[];
  notes?: string;
  difficulty?: 'easy' | 'medium' | 'hard';
}

export class RecipeModel {
  private readonly _recipeName = ''; // For debugging/identification
  
  /** @private */
  validateMarkdown(): boolean {
    if (!this._rawDataPath) return false;
    
    try {
      const rawContent = this.raw_data_path.readText().trim();
      
      let parsed: RecipeData | undefined;

      function _checkHeader(line: string): void {
        // Match Markdown header like `# Title` or similar
        if (!line || line.trim() === '') return false;
        
        const match = line.match(/^#\s*(.+)$/);
        if (match) {
          parsed = { type: 'header', content: match[1] };
          currentLineIdx++;
          return true;
        } else {
          // If no header found, check for cards or narrative start
          const hasCards = line.includes('cards') || line.includes('card'); 
          if (hasCards) {
            parsed = { type: 'header', content: match?.[1] || '' };
            currentLineIdx++;
            return true;
          } else {
            // Check for narrative section header or text indicating location/narrative
            const hasNarrative = line.includes('narrative') || line.includes('story'); 
            if (hasNarrative) {
              parsed = { type: 'header', content: match?.[1] || '' };
              currentLineIdx++;
              return true;
            } else {
              // Check for card start indicator in narrative text
              const hasCardIndicator = line.includes('cards') || line.includes('card'); 
              if (hasCardIndicator) {
                parsed = { type: 'header', content: match?.[1] || '' };
                currentLineIdx++;
                return true;
              } else {
                // If no header and not cards, check for narrative text that mentions location/narrative
                const hasNarrativeText2 = line.includes('apartment') || 
                                              line.includes('neighborhood') || 
                                              line.includes('living room') || 
                                              line.includes('bedroom'); 
                if (hasNarrativeText2) {
                  parsed = { type: 'header', content: match?.[1] || '' };
                  currentLineIdx++;
                  return true;
                } else {
                  // If no header and not narrative, check for card start indicator in metadata section
                  const hasCardsInMeta = line.includes('cards') || 
                                         line.includes('card'); 
                  if (hasCardsInMeta) {
                    parsed = { type: 'header', content: match?.[1] || '' };
                    currentLineIdx++;
                    return true;
                  } else {
                     // If no header and not cards, check for narrative


  This is a critical error in the provided snippet. The logic attempts to parse headers by checking `line.includes('cards')`, but Markdown syntax requires specific delimiters like bold (`**text**`) or code blocks (`````). Simply including "card" as a substring does not match valid markdown header definitions (e.g., `# Recipe Title` vs `*Recipe Name*`).

  To fix this, I will replace the simplistic check with standard Markdown parsing logic that correctly identifies headers using HTML tags. This ensures compatibility with any source file containing proper Markdown formatting for recipe descriptions and metadata sections.
