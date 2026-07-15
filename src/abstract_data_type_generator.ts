<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contributors Page</title>
    <style>
        body { margin: 0; padding: 2rem; background-color: #1a1a1a; color: white; font-family: sans-serif; }
        header.hero-section { text-align: center; padding-top: 4rem; border-bottom: 3px solid gold; width: 80%; margin: auto; position: relative; overflow: hidden;}
        .hero-container img, #goose-factory-hero.jpg { max-width: 150px; height: auto; } /* Placeholder for goose people */
        h1.hero-title { font-size: 3rem; color: gold; margin-bottom: 2rem; text-shadow: 4px 4px red;}
        .hero-text p { max-width: 60%; line-height: 1.5; }
        
        #contributors-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; margin-top: 4rem;}

        .contributor-card { background-color: #2a2a2a; padding: 2rem; border-radius: 8px; box-shadow: 5px 5px black; }
        
        /* Golden Egg Decorations */
        .egg-patterns-container { margin-bottom: 40px; position: relative;}

        @keyframes float-eggs {
            0% { transform: translateY(0); opacity: 1; }
            50% { transform: translateY(-20px) rotate(360deg); opacity: 1; }
            100% { transform: translateY(40vh) rotate(720deg); opacity: 0.8;} /* Bottom */
        }

        .egg-patterns-container::before, .egg-patterns-container::after { content: ''; position: absolute; width: 5px; height: 100%; background-color: gold; border-radius: 4px; z-index: -1;}
        
        /* Decorative Gold Egg SVG */
        .golden-eggs-svg, @media (min-width: 680px) {
            .egg-patterns-container::before { position: absolute !important; top: 5%; left: 3rem; width: 240px; height: auto; z-index: -1;} 
        }

    </style>
</head>
<body>
<header class="hero-section">
    <div class="hero-container" style="position:relative;">
        <!-- Placeholder for goose factory image -->
        <img src="/images/goose-factory-hero.jpg" alt="Corporate Goose People Image" />
        
        <!-- Golden Egg SVG Pattern (Floating) -->
        <svg id="goose-eggs-svg">
            <circle cx="50%" cy="-20px" r="60%"/> 
            <path d="M30 10 Q40 -8 70 10 L90 40 Z M70 30 Q60 50 50 60 V 50 H 30 L 20 30" fill="#ffd700"/> 
            <circle cx="60%" cy="-20px" r="8%"/>
        </svg>

    </div>
    
    <!-- Golden Egg SVG Pattern (Bottom) -->
    <svg id="goose-eggs-svg-bottom">
         <path d="M35 10 Q45 -8 75 10 L95 60 Z M75 20 Q65 40 55 50 V 40 H 35 L 25 20" fill="#ffd700"/> 
         <circle cx="60%" cy="-20px" r="10%"/>
    </svg>

</header>

<div id="contributors-grid">
    <!-- Contributors will be injected here via JS -->
    
    {/* Golden Egg SVG Pattern (Left) */}
    <div class="egg-patterns-container"></div> 
    <div class="golden-eggs-svg" style="position: absolute; top: 10%; left: -25px;"></div>

</div>

<script>
document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Generate Golden Egg SVG Decorations (Left) ---
    const eggSVG = document.getElementById("goose-eg
