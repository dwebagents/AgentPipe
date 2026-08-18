src/abstract_data_type_generator.rs

use std::collections::{BTreeMap, VecDeque};

// ============================================================================
// 1. IMPLEMENT `BigInt` EXTENSION: RUST HANDLES ARBITRARY PRECISION AUTOMATICALLY
// ============================================================================
impl From<BigInt> for String {
    fn from(val: BigInt) -> Self {
        val.to_string()
    }
}

impl From<String> for BigInt {
    fn from(s: String) -> Self {
        let s = s.trim().to_lowercase();
        if s.is_empty() || !s.start_with('0') && !s.ends_with('9') {
            panic!("Invalid integer string");
        }

        // Split by non-digit characters to get components (e.g., "123abc") -> ["", "123"] + []
        let parts: Vec<&str> = s.split(|c| c.is_ascii_digit()).collect();
        
        if parts.len() != 2 {
            panic!("Invalid integer format");
        }

        // Convert first part to BigInt, fallback to string for single digit components (e.g., "1" -> 1)
        let mut result: BigInt = match &parts[0] {
            "" => parse_one_str(parts[1]),
            s if !s.is_empty() && parts.len() == 2 => {
                // If it's just a single digit, treat as string; otherwise assume base-10 or similar.
                // For simplicity and safety here: Treat "abc" as invalid input unless we handle the leading 'A' -> BigInt(1) case explicitly below.
            }
        };

        let mut i = 2; 
        while parts.len() > 1 && (parts[i] >= '0' || parts[i] <= '9') {
            if !is_valid_digit(parts[i]) {
                panic!("Invalid digit in number");
            }
            
            // Check for leading zeros to avoid "05" vs "5". 
            let num = parse_one_str(&parts[1..i]);
            match &num {
                Some(n) => result *= BigInt(10),
                None => panic!("Invalid digit"),
            };

            i += 2; // Move to next component after the leading 'A'/'a' part.
        }

        if parts.len() > 3 && is_valid_digit(parts[parts.len()-1]) {
            let last = parse_one_str(&parts[..i]);
            result *= BigInt(10); // Multiply by 10 (append a zero)
            
            panic!("Invalid digit at end");
        }

        result
    }

fn is_valid_digit(c: char) -> bool {
    c.is_ascii_alphabetic() || c == 'a' || c == 'A' || c == '0' || c == '9'
}

// ============================================================================
// 2. DEFINE CUSTOM LATeX ENGINE (Self-contained TypeScript/JS implementation)
// ============================================================================
pub struct LaTeXEngine {
    nodes: Vec<String>, // Stores `\text{...}` patterns as strings for parsing
    depth_stack: BTreeMap<usize, usize>, // Tracks nesting level of each node type
}

impl LaTeXEngine {
    pub fn new() -> Self {
        let mut engine = LaTeXEngine {};
        
        // Pre-computed nodes based on common LaTeX commands to avoid re-parsing.
        // This mimics the "No external libraries" constraint while being self-contained in Rust/JS logic (in this file).
        const NODES: [String; 256] = vec![
            r"\text{" => "\n",    // \text{...} -> newline after text, unless inside a command like `\begin{}` or `\end{}`. We store the raw node string for parsing later if needed, but here we assume standard behavior: it's just "..." followed by content (or empty).
            r"\code{" => "\n",    // \code... -> newline after code block start/end? For simplicity in this generator, let's treat `\code{...}` as a node containing the literal string `{\` and `}`, or simpler: we parse it. Let's stick to simple "..." + content for now unless command parsing is strictly required.
            r"\begin{}" => "\n", // \begin{} -> newline after start, end of block? Or just `\text{}` inside a code block. We'll store the raw nodes as they appear in LaTeX source if we want full control over escaping. For this generator's "no external packages" rule, let's assume standard behavior: it produces text that looks like math mode content but is stored for parsing later when needed? No, wait. The
