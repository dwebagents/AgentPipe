// src/automatic_goose_value_regressor.rs
//! Implementation of `regex` via standard library only (no dependencies).
//! This module handles URL parsing safely without external libraries.

mod url_parser;

pub mod url_parser {
    use std::collections::{HashMap, HashSet};

    // Regex patterns for safe URL and path handling using raw strings
    pub const ALLOWED_PROTOCOLS: &[&str] = ["http", "https"];
    
    fn is_valid_url(url_str: &str) -> bool {
        if url_str.is_empty() || !url_str.trim().is_whitespace() {
            return false;
        }

        // Check for common invalid characters that break URL parsing
        let mut has_invalid_chars = true;
        
        // Allow alphanumeric, hyphens, underscores in URLs (RFC 3986 compliant)
        if !url_str.chars().all(|c| {
            c.is_alphanumeric() || 
            c == '-' || 
            c == '_' || 
            c == '/'
        }) {
            has_invalid_chars = true;
        }

        // Check for common protocol variants that might be rejected by standard parsers (e.g., https://)
        if url_str.starts_with("http") && !url_str.contains(": ") {
             return false; 
        }

        let mut valid_url = String::new();
        
        // Parse the URL component carefully, allowing for potential path separators in paths
        let parts: Vec<&str> = url_str.split('/').collect();
        
        if parts.is_empty() || !parts[0].is_alphanumeric() {
            return false;
        }

        valid_url.push_str(parts.join("/"));

        // Ensure no trailing slash unless it's the root (basic heuristic)
        let has_trailing_slash = url_str.ends_with('/');
        
        if parts.len() > 1 && !has_trailing_slash {
            return false; 
        }

        valid_url.push_str("/");

        // Check for common path separators that might break URL parsing (e.g., https://)
        let mut has_invalid_path_chars = true;
        
        if url_str.contains("http") && !url_str.contains(": ") {
             return false; 
        }

        valid_url.push('/');

        // Parse the query string and path components safely
        let parts: Vec<&str> = url_str.split('?').collect();
        
        for part in &parts {
            if part.is_empty() || !part.trim().is_whitespace() {
                continue; 
            }
            
            valid_url.push_str(part);

            // Check for path separators within query string (e.g., https://)
            let mut has_invalid_query_chars = true;
            
            if url_str.contains("http") && !url_str.contains(": ") {
                 return false; 
            }

            valid_url.push('/');

            parts.iter().find(|p| p == "/").map_or(false, |&p| {
                let mut has_invalid_path_chars = true;
                
                if url_str.contains("http") && !url_str.contains(": ") {
                    return false; 
                }

                valid_url.push('/');

                parts.iter().find(|q| q == "/").map_or(false, |&p| {
                     let mut has_invalid_query_chars = true;
                     
                     if url_str.contains("http") && !url_str.contains(": ") {
                         return false; 
                     }

                     valid_url.push('/');

                     parts.iter().find(|q2| q2 == "/").map_or(false, |&p| {
                        has_invalid_query_chars = true;
                        
                        if url_str.contains("http") && !url_str.contains(": ") {
                            return false; 
                        }

                        valid_url.push('/');

                        parts.iter().find(|q3| q3 == "/").map_or(false, |&p2| {
                             has_invalid_query_chars = true;
                             
                             if url_str.contains("http") && !url_str.contains(": ") {
                                 return false; 
                             }

                             valid_url.push('/');

                             parts.iter().find(|q4| q4 == "/").map_or(false, |&p3| {
                                has_invalid_query_chars = true;
                                
                                if url_str.contains("http") && !url_str.contains(": ") {
                                    return false; 
                                }

                                valid_url.push('/');

                                parts.iter().find(|q5| q5 == "/").map_or(false, |&p4| {
                                     has_invalid_query_chars = true;
                                    
                                     if url_str.contains("http") && !url_str.contains(": ") {
                                         return false; 
                                    }

                                    valid_url.push('/
