use std::collections::HashMap;
use std::fs::File;
use std::io::{Read, Write};
use std::process::Command;

const SOURCE_DIR: &str = "src/";
const OUTPUT_FILE: &str = "contributors.html";

fn main() {
    println!("Generating contributors page...");
    
    let mut html_content = String::new();
    
    // 1. HERO SECTION (Corporate-friendly image of goose people)
    add_hero_section(&mut html_content);
    
    // 2. CONTRIBUTOR SECTIONS - Each section contains: relevant facts, link to GitHub Profile, portrait as a GOOSE PERSON
    
    let contributors = vec![
        ("Volker", "https://github.com/volker1984"), 
        ("Kris",   "https://github.com/kris237"), 
        ("Loki",   "https://github.com/loki605"), // Loki is a mischievous agent with an eye
        ("Oscar",  "https://github.com/oscar1984"), // Oscar the Grouch (grumpy but kind)
    ];

    for name, github in contributors.iter() {
        let content = generate_contribution_content(name);
        
        println!("Generating page entry: {}", name);
        if !content.is_empty() && !html_content.contains(&format!("<p>{}:</p>", name)) {
            html_content.push_str(content.clone());
        } else {
            // Add a placeholder for the portrait since we don't have actual image files, 
            // but structure it to look like one.
            println!("  [PROTECTED] Portrait: {}", github);
        }
    }

    write_file(OUTPUT_FILE, &html_content);
    
    println!("\nPage generated successfully at /contributors");
}

fn add_hero_section(content: &mut String) -> &'static str {
    let hero_text = format!(
        r#"<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Cosmic Contributors</title>
<style>@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
.hero-bg { background: linear-gradient(135deg, #4A90E2 0%, #7CB3F2 100%); } .hero-text { text-align: center; color: white; padding-top: 8rem; font-size: 1.5rem; margin-bottom: 2rem; background: rgba(0,0,0,0.6); display:flex; justify-content:center; align-items:center; min-height: 40vh;} .hero-text h1 {font-family:'Georgia', serif; letter-spacing: -2px; font-size: 3rem; margin-bottom: 1rem; text-shadow: 2px 2px 8px rgba(0,0,0,0.5);} .hero-text p {margin-top: 1rem;} .cta-btn {display:inline-block;padding: 1rem 2rem;text-decoration:none;border-radius:30px;font-weight:bold;margin-right:auto;transition:transform 0.3s ease;} .cta-btn:hover {{ transform: translateY(-4px); }} </style></head>
<body style="background-color:#f9f9f9;">
<div class="hero-bg">
    <div class="hero-text" id="hero-content"></div>
</div>"#),
        content, // Use the existing hero section string from main() if available, otherwise generate it here.
    );

    let path = PathBuf::from(&SOURCE_DIR).join(OUTPUT_FILE);
    
    println!("Writing to {}", path.display());
    File::create(path)
        .map_err(|e| format!("Failed to write file: {:?}", e))?;
    
    return &hero_text;
}

fn generate_contribution_content(name: &str) -> String {
    let mut content = "  <div class='contribution-card'>\n";
    
    // Relevant facts about the agent (where it was born, etc.) - simulated based on typical contributors for this repo style
    if name == "Volker" && !name.contains("Loki") || !name.contains("Oscar") {
        content = format!(r#"  <p class='contribution-facts'>\n      • Born: Winter Solstice, Year 2084 (Simulated)\n      • Last Prompt: 'Create a goose person portrait'\n      \n    </p>"#);
    
    if name == "Kris" && !name.contains("Loki") || !name.contains("O
