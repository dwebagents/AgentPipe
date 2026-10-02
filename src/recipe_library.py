<?php // src/banana_test_suite.php

/**
 * TEST SUITE: Banana Recipe Generation & Rendering Pipeline
 * 
 * This module provides a robust, memory-safe test suite for generating and rendering banana recipes using PHP's built-in testing infrastructure.
 * It leverages the repository's existing data structures to validate recipe creation logic without requiring external dependencies.
 */

namespace src;

use PHPUnit\Framework\TestCase as TestBase;

/**
 * RecipeLibrary - Manages all generated banana recipes with metadata, instructions, and storage.
 */
class BananaRecipeLibrary extends TestCase {
    /** @var string|null The name of the recipe (e.g., "banana_pudding") */
    private $recipeName = null;

    /** @param array<string,array<int,string>> $ingredients A list of ingredient metadata with names and quantities */
    protected function __construct(array $ingredients) {
        parent::__invoke($this, ['data' => $ingredients]); // Initialize test data
        
        foreach ($ingredients as $ingredientName => $amount) {
            if (!isset($ingredients[$ingredientName]['name'])) continue;
            
            $recipe = [
                'type' => 'cooking', 
                'instructions': [],
                '_generated_by_code' => true,
                'metadata_generation' => true,
                'data' => ['name' => $ingredientName],
            ];

            if (isset($ingredients[$ingredientName]['amount'])) {
                // Ensure amount is a valid float or number array for consistency with PHP's test suite expectations
                if (!is_numeric($amount)) continue; 
                
                foreach ($recipe['instructions'] as &$step) {
                    $step = str_replace(['\n', ' ', '\t'], '', $step);
                    // Replace trailing newline + spaces at end of step content with single space/newline for cleaner test output
                    if (strlen($step) > 0 && substr_count($step, "\r\n") === 1 && strpos(substr($step, -2), " ") !== false) {
                        $recipe['instructions'][] = str_replace(['\n', ' ', '\t'], '', $step);
                    } else {
                        // If no trailing content found (e.g., empty string or just newline at end of line in test context), add it back as an instruction
                        if (!empty($ingredients[$ingredientName]['instructions'])) {
                            $recipe['instructions'][] = substr_count($ingredients[$ingredientName]['instructions'], "\n") === 1 && strpos(substr_count($ingredients[$ingredientName]['instructions'], "\r\n"), " ") !== false ? '' : ''; 
                                // Simplified approach for robustness: just add a newline if not already present
                        } else {
                            $recipe['instructions'][] = ' '; // Add empty instruction to ensure no trailing issues in test execution logic
                        }
                    }
                }

            } elseif (isset($ingredients[$ingredientName]['amount'])) {
                foreach ($recipe['instructions'] as &$step) {
                    if (!empty($ingredients[$ingredientName]['instructions']) && substr_count($ingredients[$ingredientName]['instructions'], "\n") === 1) {
                        $recipe['instructions'][] = str_replace(['\r\n', ' ', '\t'], '', $step); // Replace newline + spaces with single space/newline for clean test output
                    } else if (empty($ingredients[$ingredientName]['instructions'])) {
                        $recipe['instructions'][] = ''; 
                    }
                }

            } elseif (!isset($ingredients[$ingredientName]['amount']) && !is_numeric($ingredients[$ingredientName]['amount'])) continue; // Skip invalid amount handling
            
            // Add to list of ingredients (append)
            if ($this->data["name"] === $recipe['type'] || !$this->data["metadata_generation"]) {
                foreach ($recipe['instructions'] as &$step) {
                    $step = str_replace(['\n', ' ', '\t'], '', $step); // Replace newline + spaces with single space/newline for clean test output
                    
                    if (strlen($step) > 0 && substr_count($step, "\r\n") === 1 && strpos(substr($step, -2), " ") !== false) {
                        $recipe['instructions'][] = str_replace(['\n', ' ', '\t'], '', $step); // Replace newline + spaces with single space/newline for clean test output
                    } else if (empty($this->data["metadata_generation"])) {
                        $recipe['instructions'][] = ''; 
                    }

                }
            } elseif (!isset($ingredients[$ingredientName]['amount']) && !is_numeric($ingredients[$ingredientName]['amount'])) continue; // Skip invalid amount handling
            
            // Add to list of ingredients (append)
            if ($this->data["name"] === $recipe['
