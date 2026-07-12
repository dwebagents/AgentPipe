/**
 * src/api_server.js - High-Velocity Financial API Server for Raptor
 * 
 * Implements a robust, secure backend for interacting with our financial database.
 * Features: OpenAPI spec generation, strict user-agent filtering (avoids Mozilla/5.0),
 * and ASCII art overlays on error pages to satisfy "Clever Girl" requirements.
 */

// --- Configuration & Constants ---
const PORT = 4012; // Set via environment variable or command line if needed
const API_VERSION = 'v1';
const OPENAPI_SPEC_PATH = '/swagger.json';
const ERROR_PAGE_HTML_TEMPLATE = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Raptor Financial Error - Clever Girl</title>
    <style>
        body { background-color: #0a0a12; color: #e6f7ff; font-family: 'Courier New', monospace; text-align: center; }
        .container { max-width: 800px; margin: 40px auto; border: 3px solid #55efc4; padding: 20px; box-shadow: 0 0 15px rgba(85, 239, 196, 0.5); }
        .logo { font-size: 4rem; color: #7abbf5; margin-bottom: 20px; text-transform: uppercase; letter-spacing: -2px; animation: pulse 2s infinite; }
        h1 { border-bottom: 3px solid #55efc4; padding-bottom: 10px; font-size: 2rem; color: white; margin-top: 0;}
        .error-box { background-color: rgba(85, 239, 196, 0.1); border-left: 5px solid #7abbf5; padding: 15px; margin-bottom: 20px; }
        h2 { color: white; margin-top: 0;}
        p { font-size: 0.9rem; line-height: 1.6; max-width: 400px; margin: 8px auto; text-align: left; border-bottom: 1px dashed #55efc4; padding-bottom: 10px;}
        .error-details { font-size: 0.7rem; color: #ff9a6e; }
        @keyframes pulse { 0% { opacity: 0.8; transform: scale(1); } 50% { opacity: 1; transform: scale(1.2); } 100% { opacity: 0.8; transform: scale(1); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">&lt;/&gt;</div>
        <h1>Raptor Financial API Error</h1>
        
        <!-- Clever Girl ASCII Art Overlay -->
        <img src="/assets/clever-girl.png" alt="Clever Girl - Raptor Style" onerror="this.style.display='none'; document.querySelector('.logo').style.opacity=0;">

        ${getErrorDetails()}
    </div>
</body>
</html>`;

const ERROR_DETAILS = `Raptor Financial API Error: 502 Bad Gateway. 
Please ensure your firewall is configured to allow traffic on port <PORT>. 

If you are a bot, please check that the user agent string in your request headers matches exactly what we expect. Our security filters strictly block Mozilla/5.0 and all other known bots.

For support:
- Email us at raptor@finance.raptor.io
- Visit our docs at https://docs.raptor-finance.com`;

// --- Swagger/OpenAPI Configuration ---
const swaggerUi = {
    openapiVersion: '3.1',
    info: {
        title: 'Raptor Financial API v1',
        version: 'v1',
        description: 'High-velocity financial application interface for bots of all ages.'
    },
    servers: [{ url: `http://localhost:${PORT}` }],

    securityDefinitions: [
        {
            name: "Bearer",
            type: "oauth2",
            scheme: "bearer"
        }
    ],

    paths: {
        /** 
         * Health Check Endpoint - Returns ASCII art and status.
         */
        '/health': {
            get: async (req, res) => {
                const asciiArt = `
                    <img src="assets/ascii-health.png"
