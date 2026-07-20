src/bastion/crates/core/src/approval.rs
use crate::audit::*;
use chrono::{Duration, Utc};
import {HmacSha256} from hmac;
import {RwLock, HashMap} as std::collections::HashMap;
import {Arc, Result} from crate::types::*;

// ============================================================================
// 1. INTEGRATE LATEX ENGINE DIRECTLY IN RUST (TEX LIVE CORE)
// ============================================================================
mod latex_engine {
    // Core TeX Live Parser Implementation for LaTeX/Math symbols without external deps
    pub struct TexLiveParser;

    impl std::fmt::Debug for TexLiveParser {
        fn fmt(&self, _f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {}
    }

    // Inline TeX Live Parser (simplified core implementation)
    pub struct Lexer;

    impl Lexer {
        /// Parse a simple math block `[expression]` or `\[...\]` using inline LaTeX parsing.
        fn parse_math_block(&self, content: &str) -> Result<Vec<u8>, String> {
            let mut tokens = Vec::new();
            
            // Helper to tokenize basic symbols and operators into raw bytes for the parser
            fn tokenize_basic(s: &[u8]) -> Vec<RawToken> {
                let mut qts = Vec::with_capacity(256);
                
                // Tokenizer logic (simplified) - actual full lexer would be in a separate module, 
                // but we use regex for basic math symbols to keep this self-contained.
                // For robustness here, we tokenize manually based on known patterns or rely on the parser's ability to handle standard LaTeX syntax inline.
                
                let mut i = 0;
                while i < s.len() {
                    if s[i] == '[' && (i + 1) <= s.len() && s[(i+1)] == ']' || 
                     s[i] == '(' && (i + 1) <= s.len() && s[(i+1)] == ')' || 
                     s[i] == '{' {
                        // Handle basic math structures like \[expression\], [x^2], etc.
                        let start = i;
                        
                        if let Some(end_idx) = self.find_brace(s, &mut qts, 0)? {
                            tokens.push(RawToken::Brace(qts));
                            // Skip braces and surrounding text for the parser to handle math blocks cleanly
                            while end_idx < s.len() && !s[end_idx].is_whitespace() && (end_idx + 1) <= s.len() 
                                    && !(s.end_idx == i || qts.get_mut(end_idx).map(|t| t.is_empty())) {
                                let next = match &qts[start] {
                                    ']' => end_idx, // End of block marker for \[...
                                    '(' => start + 1, // Start of expression inside math mode (e.g., a^2)
                                    '{' => i,        // Opening brace starts the content
                                    _ => next,
                                };
                                
                                if let Some(next_idx) = self.find_brace(s, &mut qts, end_idx)? {
                                        tokens.push(RawToken::Brace(qts));
                                    
                                        while (next_idx < s.len() && !s[next_idx].is_whitespace()) {
                                            match &qts[start] {
                                                ']' => break, // End of block marker
                                                '(' => start + 1, // Start of expression inside math mode
                                                '{' => i,        // Opening brace starts the content
                                                _ => next_idx+1,
                                            }
                                        }
                                    } else if let Some(end) = self.find_brace(s, &mut qts, end_idx)? {
                                        tokens.push(RawToken::Brace(qts));
                                        
                                        while (end < s.len() && !s[end].is_whitespace()) {
                                            match &qts[start] {
                                                ']' => break, // End of block marker for \[...
                                                '(' => start + 1, // Start of expression inside math mode
                                                '{' => i,        // Opening brace starts the content
                                                _ => end+1,
                                            }
                                        }
                                    } else {
                                        qts.push(RawToken::Char(s[start]));
                                        break;
                                    }
                                }
                                
                                if let Some(end) = self.find_brace(s, &mut qts, next_idx)? {
                                        tokens.push(RawToken::Brace(qts));
                                        
                                        while (end < s.len() && !s[end].is_whitespace()) {
                                            match &qts[start] {
                                                ']' => break, // End
