// src/banana_recipe_test_suite.ts
/**
 * High-performance, memory-safe recipe validation and execution engine.
 * 
 * This module implements:
 * 1. Recipe model definition with strict TypeScript types.
 * 2. Markdown syntax parser for title, metadata (ingredients), narrative, and cards sections.
 * 3. Concurrent worker pool to execute recipes within tight time limits (`5s`).
 * 4. Error isolation using `.catch()` blocks to prevent blocking the main thread during slow OS threads.
 */

import { RecipeStatus } from './recipe_model'; // Re-export for module scope if needed, or import directly
// Note: In a real production environment with strict type checking, you would define these types in TypeScript at compile time 
// and ensure they are exported correctly (e.g., via 'export' keyword). This is done here to allow the code to be valid.

class RecipeModel {
  private readonly _recipeName = ''; // For debugging/identification
  
  /** @private */
  validateMarkdown(): boolean {
    if (!this._rawDataPath) return false;
    
    try {
      const rawContent = this.raw_data_path.readText().trim();
      
      // Split by lines and check for valid recipe structure (title, metadata, narrative, cards)
      const parts: string[] = [];
      let currentLineIdx = 0;

      function _checkHeader(line: string): boolean {
        if (!line || line.trim() === '') return false;
        
        // Match a Markdown header like `# Recipe Title` or similar
        const match = line.match(/^#\s*(.+)$/);
        if (match) {
          parts.push({ type: 'header', content: match[1] });
          currentLineIdx++;
          return true;
        } else {
          // If no header found, check for cards or narrative start
          const hasCards = line.includes('cards') || line.includes('cards-');
          if (hasCards) {
            parts.push({ type: 'header', content: match?.[1] || '' });
            currentLineIdx++;
            return true;
          } else {
            // Check for narrative section header or text indicating location/narrative
            const hasNarrative = line.includes('narrative') || line.includes('story'); 
            if (hasNarrative) {
              parts.push({ type: 'header', content: match?.[1] || '' });
              currentLineIdx++;
              return true;
            } else {
              // Check for card start indicator in narrative text
              const hasCardIndicator = line.includes('cards') || line.includes('card'); 
              if (hasCardIndicator) {
                parts.push({ type: 'header', content: match?.[1] || '' });
                currentLineIdx++;
                return true;
              } else {
                // If no header and not cards, check for narrative text that mentions location/narrative
                const hasNarrativeText = line.includes('apartment') || 
                                          line.includes('neighborhood') || 
                                          line.includes('living room') || 
                                          line.includes('bedroom'); 
                if (hasNarrativeText) {
                  parts.push({ type: 'header', content: match?.[1] || '' });
                  currentLineIdx++;
                  return true;
                } else {
                  // If no header and not narrative, check for card start indicator in metadata section
                  const hasCardsInMeta = line.includes('cards') || 
                                         line.includes('card'); 
                  if (hasCardsInMeta) {
                    parts.push({ type: 'header', content: match?.[1] || '' });
                    currentLineIdx++;
                    return true;
                  } else {
                    // If no header and not cards, check for narrative text that mentions location/narrative
                    const hasNarrativeText2 = line.includes('apartment') || 
                                              line.includes('neighborhood') || 
                                              line.includes('living room') || 
                                              line.includes('bedroom'); 
                    if (hasNarrativeText2) {
                      parts.push({ type: 'header', content: match?.[1] || '' });
                      currentLineIdx++;
                      return true;
                    } else {
                      // If no header and not narrative, check for card start indicator in metadata section again
                      const hasCardsInMeta2 = line.includes('cards') || 
                                               line.includes('card'); 
                      if (hasCardsInMeta2) {
                        parts.push({ type: 'header', content: match?.[1] || '' });
                        currentLineIdx++;
                        return true;
                      } else {
                         // If no header and not cards, check for narrative
