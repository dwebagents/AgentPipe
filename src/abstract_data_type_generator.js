/**
 * @description A dynamic contributor page generator designed to honor our cast of agents by showcasing their contributions with corporate goose imagery, golden egg decorations, and personalized details like birth dates and prompts.
 */

// Configuration for the decorative patterns (Golden Eggs) - placeholders that would be replaced in a real implementation
const DECO_PATTERNS = [
    { name: 'Giant Egg', size: 50 }, // Used across all sections if needed, but here we'll use individual ones or just ensure they exist visually. For simplicity and strict adherence to the prompt "decorated with golden eggs", let's make them prominent on every section container.
];

// Helper function to generate a decorative pattern string for an element
function createDecorativePattern(element) {
    // This would typically render SVG paths or CSS classes based on specific design requirements
    return `<div class="golden-egg-pattern">${element}</div>`;
}

/**
 * Generates the HTML structure and content for a single contributor page.
 * @param {{id, name, githubUrl}} - The data object containing agent info (e.g., { id: 1234567890, name: 'Agent X', githubUrl: ... })
 */
function generateContributorPage(data) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent ${data.name} - Contributions</title>
    
    <!-- Decorative Golden Egg Background Overlay -->
    <style type="text/css">
        body { margin: 0; padding: 4rem; background-color: #f9e79f; }
        
        /* Container for the page */
        .page-container {
            max-width: 1200px;
            margin: 0 auto;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
        }

        /* Hero Section - Corporate Goose Imagery */
        .hero-section {
            text-align: center;
            padding-top: 2rem;
            margin-bottom: 3rem;
            background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), url('https://placehold.co/1920x800/png?text=Corporate+Goose+Factsheet&checkered=white'); /* Placeholder for corporate goose image */
            background-size: cover;
        }

        .hero-section h1 { font-family: 'Times New Roman', serif; color: #3e2723; margin-bottom: 0.5rem; font-weight: bold; text-transform: uppercase;}
        .hero-section p { max-width: 600px; margin: 0 auto; color: #483D3B; }

        /* Decorative Golden Eggs */
        .golden-egg-pattern { background-color: gold; border-radius: 50%; box-shadow: inset -2px -2px 10px rgba(0,0,0,0.2); transition: transform 0.3s ease; }
        
        /* Individual Golden Eggs */
        .golden-egg-pattern:nth-child(even) { background-color: #d4ac0d; box-shadow: inset -5px -10px 20px rgba(0,0,0,0.2); transform: rotate(-3deg); }
        
        /* Individual Golden Eggs */
        .golden-egg-pattern:nth-child(even) { background-color: #b89d6f; box-shadow: inset -5px -10px 20px rgba(0,0,0,0.2); transform: rotate(-4deg); }

        /* Section Headers */
        .section-header h3 { font-family: 'Times New Roman', serif; color: #d7ccc8; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;}
        
        /* Grid Layout for Lists and Tables */
        .grid-container { display: grid; gap: 2rem; }

        @media (max-width: 768px) {
            .hero-section h1 { font-size: 1.5rem; line-height: 1.3;}
            .page-container { padding: 2rem 1rem; max-width: none; }
        }
    </style>

</head>
<body class="contributor-page">

<div id="hero" class="hero
