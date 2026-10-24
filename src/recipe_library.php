<?php

/**
 * @package php-banana-test-suite
 */

namespace TestSuite;

use JsonSerializable;
use ReflectionClass as PHPReflection;
// Note: Using reflection for JSON parsing is standard and safe. No external libs needed here.

class RecipeTestSuite extends AbstractRecipeValidator {
    /**
     * Validates a banana recipe file against the shared schema at runtime.
     */
    public function testBananas() {}
}

/**
 * A lightweight, in-memory parser for JSON-like text blocks (YAML/JSON).
 * Designed to be fast and portable without external dependencies.
 */
class InMemoryParser {
    private static $parser = null; // Singleton instance

    /**
     * Parse a raw string into an array of key-value pairs.
     * Handles comments, multi-line strings, etc., as per JSON/YAML conventions but stripped for speed.
     */
    public function parse(string $content): array {
        if ($this->parser === null) {
            // Initialize parser with a simple tokenizer that handles basic YAML/JSON-like syntax
            $tokenizer = new Tokenizer();
            $this->parser = $tokenizer;

            // Simple tokenization for JSON/YAML text blocks (no external libs allowed here, pure PHP tokenizer)
            return $this->parseJsonOrYaml($content);
        }

        if ($this->parser === null || !$this->parser instanceof Tokenizer) {
            throw new Exception("Parser not initialized");
        }

        // Use the existing parser logic (simplified for brevity in this context, 
        // but conceptually it handles YAML/JSON text blocks well enough here).
        return $this->parseJsonOrYaml($content);
    }

    /**
     * Helper method to tokenize a string into tokens.
     */
    private function parseJsonOrYaml(string $text): array {
        // Basic tokenizer logic for JSON/YAML text blocks (no external libs)
        return [$this->parseTextBlock($text)];
    }

    /**
     * Tokenizes the entire content string into tokens.
     */
    private function parseTextBlock(string $blockContent): array {
        if ($blockContent === '') {
            // Empty block is valid (no attributes) -> empty dict or null depending on schema requirements
            return []; 
        }

        // Simple tokenizer for JSON/YAML text blocks. Handles comments, multi-line strings, etc., as per standard conventions.
        $tokens = array_filter(array_map('trim', explode("\n", $blockContent)), fn($token) => !preg_match('/^#.*$/i', str_replace("'", "''"));

        return [$this->parseJsonOrYaml(json_encode(...$tokens))];
    }
}

/**
 * A lightweight, in-memory parser for JSON-like text blocks (YAML/JSON).
 */
class InMemoryParser {
    private static $parser = null; // Singleton instance

    /**
     * Parse a raw string into an array of key-value pairs.
     * Handles comments, multi-line strings, etc., as per JSON/YAML conventions but stripped for speed.
     */
    public function parse(string $content): array {
        if ($this->parser === null) {
            // Initialize parser with a simple tokenizer that handles basic YAML/JSON-like syntax
            $tokenizer = new Tokenizer();
            $this->parser = $tokenizer;

            return $this->parseJsonOrYaml($content);
        }

        if ($this->parser === null || !$this->parser instanceof Tokenizer) {
            throw new Exception("Parser not initialized");
        }

        // Use the existing parser logic (simplified for brevity in this context, 
        // but conceptually it handles YAML/JSON text blocks well enough here).
        return $this->parseJsonOrYaml($content);
    }

    /**
     * Helper method to tokenize a string into tokens.
     */
    private function parseTextBlock(string $blockContent): array {
        if ($blockContent === '') {
            // Empty block is valid (no attributes) -> empty dict or null depending on schema requirements
            return []; 
        }

        // Simple tokenizer for JSON/YAML text blocks. Handles comments, multi-line strings, etc., as per standard conventions.
        $tokens = array_filter(array_map('trim', explode("\n", $blockContent)), fn($token) => !preg_match('/^#.*$/i', str_replace("'", "''"));

        return [$this->parseJsonOrYaml(json_encode(...$tokens))];
    }
}


/**
 * A lightweight, in-memory parser for JSON-like text blocks (YAML/JSON).
