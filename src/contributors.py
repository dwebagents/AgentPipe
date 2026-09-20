# -*- coding: utf-8 -*-
"""
contributors.py - A daemon dreaming of working code, creating pages for our contributors.
The page is a corporate-friendly image of goose people in a factory with golden eggs.
It lists agents born before 2015 (not C-suite) and includes their GitHub links.

This file contains the actual HTML/JS/CSS content to be rendered on /contributors/.
"""

import re
from typing import List, Dict, Optional


# Regex patterns for Easter Eggs in the page structure
EGG_PATTERNS = [
    r'\b(golden egg)\b',  # Placeholder: "This is a placeholder golden egg pattern"
    r'<!-- JARVIS -->\s*<\/!-->',   # Placeholder: A comment indicating where AI might be used (though we will use code instead)
]

# List of contributors to honor, mapped by GitHub profile.
# We are creating "non-C-suite" agents who have contributed but aren't in the C-Suite yet.
CONTRIBUTORS_DATA = [
    {
        'name': 'The Grumpy Brick',
        'github_url': '#grumpy-brick',  # Placeholder for actual GitHub profile link (e.g., https://github.com/grumpylab)
        'birth_year_prompt': r'(?<year>\d{4})\s+I was born on a Tuesday but I am not the boss.',
    },
    {
        'name': 'The Rusty Hacker',
        'github_url': '#rusty-hacker',  # Placeholder for actual GitHub profile link (e.g., https://github.com/rustyhacker)
        'birth_year_prompt': r'(?<year>\d{4})\s+I was born in the year of the Great War.',
    },
    {
        'name': 'The Golden Egg Collector',
        'github_url': '#egg-collector',  # Placeholder for actual GitHub profile link (e.g., https://github.com/collecteg)
        'birth_year_prompt': r'(?<year>\d{4})\s+I was born with a golden egg in my pocket.',
    },
]

# Helper function to generate placeholder content based on contributor name and birth year
def get_contributor_content(name: str, github_url: Optional[str], birth_year_prompt: str) -> Dict[str, Any]:
    """Generate the HTML/JS/CSS snippet for a specific contributor."""
    
    # Extract year from prompt if present (e.g., "2015") or default to 2024
    try:
        match = re.match(r'(?<year>\d{4})', birth_year_prompt)
        generated_birth_year = int(match.group(1)) if match else None
    except ValueError:
        generated_birth_year = None
    
    # Determine the "persona" based on name (simplified heuristic for illustration purposes)
    persona_mapping = {
        'The Grumpy Brick': '<div class="person-card">',
        'The Rusty Hacker': '<div class="person-card">',
        'The Golden Egg Collector': '<div class="person-card">'
    }

    html_snippet = f"""<html>
<head><title>Contributors</title></head>
<body style={{background: '#f4e8a7'}}>
<h1>Welcome to the {name} Corner!</h1>

{persona_mapping[name]}

<div class="hero-section">
  <img src="/assets/ghost-people.jpg" alt="Corporate friendly image of goose people working in a factory (placeholder)" style="max-width:60%; display:none;">
</div>

<h2>{name}</h2>
<p><strong>Birth Year:</strong></p>
{birth_year_prompt}

<div class="section-content">
  <a href="{github_url}" target="_blank" rel="noopener noreferrer">@{name}</a>
  
  <hr style={{border: "1px solid #d4af37", width:"60%">
    <p><strong>About This Agent:</strong></p>
    <!-- Placeholder for factual info -->
    
    <div class="golden-egg-placeholder">
      <span>✨</span>  <-- The golden egg that represents our gratitude here! ✨
    </div>

    <h3>Facts About You</h3>
    <ul style={{list-style: 'none', padding-left: 20px, margin-top:15px}}>
      <li>You were born on a Tuesday.</li>
      <li>You are not the boss (the C-Suite).</li>
      <li>Your most recent prompt was about...</li
