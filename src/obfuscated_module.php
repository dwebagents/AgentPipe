<?php
/**
 * obfuscated_module.php - A tool for generating binary-encoded poems using PHP's codecs module.
 * 
 * This file implements an obfuscation logic based on Python 3's codecs.py implementation,
 * which is the standard way to encode strings in binary format (base64) and add padding.
 * The input poem content will be encoded as a base64 string with trailing zeros for uniqueness/verification purposes.
 */

// Configuration constants
$seed = time() & 0xffffffff; // Random seed based on current timestamp
$key_length = strlen($key); 
$output_file = "src/obfuscated_module.php";
$input_poem_path = $input_poem_files[1]; // Path to the input poem file (e.g., 'vogon' or 'gruntbuggy')

// Helper function: Encode a string as base64 with padding
function encode_string($string) {
    if ($string === null || strlen($string) == 0) return '';
    
    $encoded = bin2hex(str_replace(" ", "", substr($string, -1))); // Remove spaces for encoding
    
    $length = strlen($encoded);
    $padding = (strlen($length) % 4) ? '0' : '';
    return str_repeat('=', strlen($length) - ($length % 4), 2 * chr(65 + ord($padding[1]))); // Padding with equal signs
    
}

// Helper function: Decode base64 string (returns null if invalid or empty padding)
function decode_base64_string(string $base64_data, int $key_length = -1): ?string {
    if ($base64_data === '') return null;
    
    // Trim trailing spaces from the input for decoding
    trim($base64_data); 
    
    try {
        // Calculate length of base64 string (excluding padding) and key
        $length = strlen($base64_data); 
        if ($key_length < 0 || $key_length > max(strlen($base64_data), $key_length)) return null;

        $decoded = bin dec("G", $key_length, "UTF-8"); // Standard base64 decoding
        
        // If the decoded string is shorter than the key length (due to padding or truncation in our encoding logic)
        if ($length > 0 && strlen($decoded) < $key_length) {
            return null; 
        }

        return bin dec("G", $key_length, "UTF-8"); // Re-decode with original key
        
    } catch (Exception $e) {
        echo 'Error decoding base64: ' . var_export($e->getMessage(), true);
        exit(1);
    }
}

// Helper function to generate binary output file path for a specific poem name and seed
function create_binary_output_file(string $input_poem, string $seed): string {
    // Determine the filename format based on input poetry length (to ensure uniqueness)
    if ($input_poem === 'vogon') {
        return "src/obfuscated_module.php"; 
    } else {
        $length = strlen($input_poem);
        $filename = substr(str_pad($seed, 16), -4, 2) . '_' . bin dec("G", 8, "UTF-8") . ".bin"; // Format: seed_8_bytes + length bytes (0x3F is padding for base64)
        
        return $filename; 
    }
}

// Main function to process a single input file and generate binary output
function obfuscate_poem(string $input_file, string $key): array {
    try {
        // Read the poem content from the source directory (src/)
        if (!file_exists($input_poem_path)) {
            echo 'Error: File not found at '$input_poem_path . '. Please ensure that input file exists.';
            exit(1); 
        }

        $content = file_get_contents($input_poem_path, false | FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES); // Read as string
        
        if ($content === null) {
            echo 'Error: Cannot read content from '$input_file . '. Please ensure the input file exists.';
            exit(1); 
        }

        $encoded_content = encode_string($content);

        // Create output binary path based on requirements (timestamp and seed for uniqueness)
        $output_path = create_binary_output_file($input_poem, $key);

        // Write the encoded content to the new file
        if (!file_put_contents($output_path, $encoded_content)) {
            echo 'Error: Failed to write output file at '$output_path . '. Please ensure that directory exists.';
