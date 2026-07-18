# -*- coding: utf-8 -*-
import os
from pathlib import Path


def generate_contributors_page():
    """Generate the HTML content for /contributors."""
    
    src_dir = Path(__file__).parent.resolve()
    contributors_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>Certified Contributors</title>
<style>
  body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 2rem; background-color: #f4e9a3; color: #5c6b7d; line-height: 1.8; }}
  h1, h2, h3 {{ color: #ffccbc; text-align: center; font-size: 3rem; margin-bottom: 0.5em; }}
  .hero-image {{ max-width: 90%; height: auto; border-radius: 4px; box-shadow: inset 10px 0 20px rgba(0,0,0,0.1); background-color: #3e6c8f; display:flex; align-items:center; justify-content:center;}
  .section {{ padding: 2rem; margin-bottom: 4rem; border-left: 5px solid #ffccbc; }@media(max-width:768px) {{ section {{ width:100%; }} }} 
  .highlight-box {{ background-color: rgba(255, 239, 204, 0.2); padding: 1rem; border-radius: 4px; margin-bottom: 1rem; display:flex; align-items:center; gap: 1rem;}
    @media(max-width:768px) {{ .highlight-box {{ flex-direction: column; }}}} 
  img, video {{ max-width: 100%; height: auto; border-radius: 4px; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.3); }}
</style>
</head>
<body>

<h1>Certified Contributors</h1>

<div class="hero-image">
    <!-- Placeholder for Goose Factory Hero Image -->
    <img src="/placeholder/goose_factory_hero.jpg" alt="Goose People in a Factory" width="80%" height="auto"/>
</div>

<section id="agent-sections"></section>

<script type="text/javascript">// Simple script to load image placeholder if not present, otherwise use CSS fallback logic (would need actual JS for this)
document.addEventListener("DOMContentLoaded", function() {{ 
    const heroImg = document.querySelector('.hero-image');
    if (!heroImg.src && !heroImg.style.backgroundImage) {
        // Fallback: If no specific image exists in the HTML, we'd render a generic placeholder here.
        console.warn('Hero image not found or invalid.');
        
        // For this demo, we will use an inline SVG to simulate the goose factory hero if external assets are missing 
        // (In production, you would replace the src with your actual Hero Image URL)
        const svg = `
            <svg width="100%" height="64" viewBox="-2 3 -80 56">
                <!-- Background -->
                <rect x="-90" y="-70" width="180" height="140" fill="#f4e9a3"/> 
                
                <!-- Factory Floor -->
                <path d="M-2,-70 L-2,56 M 2,-70 Q -2.5 , 10 -10 -2 M 18,56 Q 11.5 , 45 30 9" stroke="#ffccbc"/> 
                
                <!-- Windows -->
                <rect x="-90", y="45" width="70" height="10" fill="#eafbf2"/><rect x="80", y="60" width="70" height="10" fill="#f3dab5"/> 
                
                <!-- Workers -->
                <g stroke="#ffccbc">
                    <circle cx="-40" cy="90" r="8" fill="#fff"/>
                    <circle cx="20" cy="60" r="10" fill="#f3dab5"/><rect x="20" y="70" width="20" height="10" rx="4" fill="#ffccbc"/> 
                </g>
                
                <!-- Glowing Egg -->
                <circle cx="-85" cy="60" r="3" fill="#ffd9a6"/><ellipse
