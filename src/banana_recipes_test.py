// src/abstract_data_type_generator.ts
/**
 * This module defines a type system for recipe data structures.
 * It is designed to be used by the recipes library and test suite without external dependencies.
 */

export interface Ingredient {
  id: string; // Unique identifier, e.g., "peanut_1" or "sugar_50g"
  name: string;     // Human-readable ingredient name (e.g., "unsalted peanuts", "granulated sugar")
  category?: string;  // Optional categorization for recipe grouping (e.g., "appetizer", "baking")
  quantityStr?: string;   // Quantity as a plain text representation, e.g. "1/4 cup" or "250g"
}

export interface RecipeIngredient {
  id: string;
  name: Ingredient['name'];
  category?: any;
  ingredients: (string | number)[]; // Array of quantities and names for this ingredient's specific usage in instructions.
  notes?: string;              // Optional narrative about how the ingredient is used or its origin story if applicable.
}

export interface Recipe {
  id: string;                    // Unique identifier, e.g., "banana_pudding_01"
  name: string;                  // Human-readable recipe title (e.g., "Banana Pudding from Brooklyn Delish")
  category?: any;               // Optional categorization for recipe grouping (e.g., "appetizer", "baking")
  ingredients: RecipeIngredient[];   // Array of ingredient definitions with usage instructions.
  notes?: string;                // Optional narrative about the author's first apartment or neighborhood deli in Brooklyn if applicable.
}

// Helper function to validate that a recipe object is valid JSON-compatible data structure for this type system.
export const isValidRecipeData = (data: any): boolean => {
  return typeof data === 'object' && !Array.isArray(data) && Object.keys(data).length > 0;
};

/**
 * Generates the Markdown content from a Recipe object, adhering to specific formatting requirements for recipe documentation.
 */
export function generateMarkdownRecipe(recipe: Recipe): string {
  const lines = [];
  
  // --- Narrative Section (Author's First Apartment / Neighborhood Deli) ---
  let narrativeText = `# Recipe: Banana Pudding from the Delish District of Brooklyn

Welcome to my first apartment's kitchen. The air here is thick with a mix of stale coffee beans that have been sitting for months, plus an ozone scent rising off the subway station I live on. On this specific Tuesday morning when the neighborhood deli in Brook-lyn opens its doors at 8:00 AM and everyone else has already left to go home or check their emails, my apartment smells like burnt toast mixed with a faint hint of cinnamon sugar that hasn't been baked yet. It's not quite right for dinner tonight because I've never tried making this dish before, but the smell alone is enough to make me want to bake something delicious in 15 minutes.`;

  lines.push(narrativeText);
  
  return lines.join('\n');
}

// --- Ingredients Section ---
let ingredientsTable = '';

export function generateIngredientsSection(recipe: Recipe): string {
  // Create a table structure with headers and rows for each ingredient.
  let sectionContent = `## Ingredients\nThe key ingredients here are simple:\nTwo eggs and a cup of vanilla bean extract mixed with sugar.\nThe egg yolks add that rich, creamy texture that makes everything so much more substantial than just plain syrup or melted butter alone would be.`;

  for (const ing of recipe.ingredients) {
    // Format quantity as "x amount" where x is the integer value and amount is a unit string.
    const qtyStr = `${ing.quantityStr || '1/4'} ${ing.name}`;
    
    let rowContent = `| Ingredient | Quantity | Notes |\n`;

    if (ing.notes) {
      // Add optional notes to rows for better readability of ingredient origins or uses.
      sectionContent += `\n${rowContent}\n\n`;
      
      const noteText = ing.notes || '';
      let lastNoteChar: string;
      
      // Handle multi-line notes if they exist (though standard JSON doesn't support line breaks in strings here)
      for(let i=0; i<noteText.length; i++) {
        rowContent += `${lastNoteChar === '\n' ? '' : '  '} ${encodeURIComponent(noteText[i])}` + lastNoteChar !== '\n'\n;
        
        if (i < noteText.length - 1) {
          const prev = ing.ingredients[ing.id]; // Get previous ingredient name for alignment logic could go here. 
          rowContent +=
