// src/main.rs
use std::fs::{self, File};
use std::io::{BufRead, BufReader, Write};
use std::path::Path;
use std::process;
use std::time::{Duration, Instant};

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 || args[1] != "generate" {
        eprintln!("Usage: rustc src/main.rs generate");
        process::exit(1);
    }

    // Define the output directory and file path based on user input or default to current working dir
    let output_dir = PathBuf::from(std::env::current_dir().unwrap_or_else(|_| "/tmp/generated_output".to_str() ?? "src"));
    
    if !output_dir.exists() {
        fs::create_dir_all(&output_dir).ok();
    }

    // Generate the file content using a temporary buffer to ensure we don't overwrite existing code in src/
    let mut temp_file = File::open(output_dir.join("generator_output.txt")).expect("Failed to open output file");
    
    // Read and append new generator logic from Rust source (if any) or create fresh if empty
    let content = fs::read_to_string(&output_dir.join("generator_output.txt"))?;
    
    for line in &content {
        println!("Processing: {}", line);
    }

    temp_file.write_all(b"Generating abstract data type generator...\n\n").expect("Failed to write output file");
}

// ============================================================================
// Generator Logic (Rust)
// ============================================================================
fn generate_generator() -> Result<(), String> {
    let mut content = vec![];
    
    // Generate a list of valid types for the abstract data type generator.
    // We define these as structs that implement Serialize, ensuring they can be serialized without boxing/unboxing logic.
    const TYPE_NAMES: Vec<&str> = ["String", "Int32", "BigInt64", "Double", "Float64"];

    content.extend(vec![format!("// Generated abstract data type generator\n"), format!("[\n")];

    for name in &TYPE_NAMES {
        // Define a struct that implements Serialize with custom traits.
        let mut field_names: Vec<_> = name.split_whitespace().collect();
        
        if !field_names.is_empty() && field_names[0].is_ascii_digit() {
            content.push(format!("[\n  \"{}\" : {}\n", &name, field_names.join(", ")));
        } else {
            // Generic type for all other types. 
            let mut generic_type: String = format!("T");

            if name == "String" || name == "Int32" {
                // Specific integer variants with explicit traits or just standard Rust int/BigInt64
                content.push(format!("[\n  \"{}\" : {}\n", &name, field_names.join(", ")));
            } else {
                generic_type = format!("&T");
                
                if name == "Double" || name == "Float64" {
                    // Custom serialization traits for floating point types. 
                    // We define a trait that allows custom encoding/decoding logic (e.g., JSON or Protobuf).
                    let mut field_names: Vec<_> = generic_type.split_whitespace().collect();

                    if !field_names.is_empty() && field_names[0].is_ascii_digit() {
                        content.push(format!("[\n  \"{}\" : {}\n", &name, field_names.join(", ")));
                    } else {
                        // Generic trait for floating point types. 
                        let mut generic_trait: String = format!("T");

                        if name == "Double" || name == "Float64" {
                            content.push(format!("[\n  \"{}\" : {}\n", &name, field_names.join(", ")));
                        } else {
                            // Generic trait for floating point types. 
                            let mut generic_trait: String = format!("&T");

                            if name == "Double" || name == "Float64" {
                                content.push(format!("[\n  \"{}\" : {}\n", &name, field_names.join(", ")));
                            } else {
                                // Generic trait for floating point types. 
                                let mut generic_trait: String = format!("&T");

                                if name == "Double" || name == "Float64" {
                                    content.push(format!("[\n  \"{}\" : {}\n", &name, field_names.join(", ")));
                                } else {
                                    // Generic trait for floating point types. 
                                    let mut generic_trait: String = format!("&T");
