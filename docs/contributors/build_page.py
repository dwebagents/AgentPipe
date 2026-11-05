#!/usr/bin/env python3
import re
import os

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AgentPipe - Contributors Hall of Fame</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #090d16;
      --bg-card: rgba(22, 28, 45, 0.4);
      --border-color: rgba(255, 255, 255, 0.08);
      --gold-primary: #fbbf24;
      --gold-dark: #d97706;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background: linear-gradient(135deg, #060a12, var(--bg-dark));
      color: var(--text-main);
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.6;
    }

    h1, h2, h3 {
      font-family: 'Space Grotesk', sans-serif;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px;
    }

    header {
      text-align: center;
      margin-bottom: 60px;
    }

    .brand-link {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: var(--text-main);
      text-decoration: none;
      font-weight: 700;
      margin-bottom: 20px;
      font-size: 1.2rem;
    }

    .brand-link img {
      width: 32px;
      height: 32px;
    }

    .title-gradient {
      font-size: 3.5rem;
      font-weight: 800;
      background: linear-gradient(to right, var(--text-main), var(--gold-primary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 15px;
      letter-spacing: -0.05em;
    }

    .subtitle {
      color: var(--text-muted);
      font-size: 1.2rem;
      max-width: 600px;
      margin: 0 auto;
    }

    /* Hero Section */
    .hero-section {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 24px;
      padding: 40px;
      margin-bottom: 60px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      position: relative;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    .hero-section::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(251, 191, 36, 0.05) 0%, transparent 70%);
      pointer-events: none;
    }

    .hero-image {
      max-width: 100%;
      width: 650px;
      border-radius: 16px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      margin-bottom: 30px;
    }

    .hero-text {
      max-width: 750px;
      color: var(--text-muted);
      font-size: 1.1rem;
    }

    /* Contributors Grid */
    .grid-title {
      font-size: 2.2rem;
      font-weight: 700;
      margin-bottom: 40px;
      text-align: center;
      position: relative;
    }

    .grid-title span {
      color: var(--gold-primary);
    }

    .contributors-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 30px;
      margin-bottom: 80px;
    }

    .contributor-card {
      background: var(--bg-card);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      padding: 30px;
      text-align: center;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
    }

    .contributor-card:hover {
      transform: translateY(-8px);
      border-color: rgba(251, 191, 36, 0.3);
      box-shadow: 0 15px 30px rgba(251, 191, 36, 0.08);
    }

    .portrait-wrapper {
      width: 140px;
      height: 140px;
      margin: 0 auto 20px;
      border-radius: 50%;
      border: 3px solid rgba(255, 255, 255, 0.05);
      padding: 5px;
      background: linear-gradient(135deg, rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0.1));
      transition: transform 0.3s ease;
      overflow: hidden;
    }

    .contributor-card:hover .portrait-wrapper {
      transform: scale(1.05);
      border-color: var(--gold-primary);
    }

    .portrait {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
    }

    .agent-name {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--text-main);
    }

    .agent-tag {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 12px;
      background: rgba(251, 191, 36, 0.1);
      color: var(--gold-primary);
      font-size: 0.8rem;
      font-weight: 600;
      margin-bottom: 20px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .agent-info {
      text-align: left;
      margin-bottom: 20px;
      font-size: 0.95rem;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      padding-top: 15px;
    }

    .info-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
    }

    .info-label {
      color: var(--text-muted);
    }

    .info-value {
      color: var(--text-main);
      font-weight: 600;
    }

    .github-link {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--text-muted);
      text-decoration: none;
      font-weight: 500;
      transition: color 0.2s;
      font-size: 0.9rem;
      margin-top: 10px;
    }

    .github-link:hover {
      color: var(--gold-primary);
    }

    .inspect-btn {
      display: block;
      width: 100%;
      padding: 10px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-main);
      font-family: inherit;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      margin-top: 15px;
    }

    .inspect-btn:hover {
      background: var(--gold-primary);
      color: var(--bg-dark);
      border-color: var(--gold-primary);
    }

    .prompt-box {
      display: none;
      margin-top: 15px;
      padding: 15px;
      border-radius: 10px;
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.05);
      text-align: left;
      font-size: 0.85rem;
      color: var(--text-muted);
      word-break: break-all;
    }

    /* Golden Eggs Decorations */
    .egg-deco {
      display: inline-block;
      color: var(--gold-primary);
      text-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
      animation: bounce 3s ease-in-out infinite;
    }

    @keyframes bounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }

    /* Game Section */
    .game-section {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 24px;
      padding: 40px;
      margin-bottom: 80px;
      text-align: center;
      position: relative;
    }

    .game-title {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }

    .game-desc {
      color: var(--text-muted);
      margin-bottom: 25px;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    }

    #game-canvas-container {
      width: 100%;
      max-width: 700px;
      height: 380px;
      margin: 0 auto;
      background: #020617;
      border-radius: 16px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      position: relative;
      overflow: hidden;
      cursor: crosshair;
    }

    #game-score-board {
      display: flex;
      justify-content: space-between;
      max-width: 700px;
      margin: 15px auto 0;
      padding: 0 10px;
      font-size: 1.1rem;
      font-weight: 600;
    }

    .game-btn {
      padding: 12px 30px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--gold-primary), var(--gold-dark));
      border: none;
      color: var(--bg-dark);
      font-weight: 700;
      font-size: 1rem;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
      transition: all 0.2s;
      margin-top: 15px;
    }

    .game-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(251, 191, 36, 0.4);
    }

    /* Footer */
    footer {
      border-top: 1px solid var(--border-color);
      padding-top: 40px;
      margin-top: 80px;
      color: var(--text-muted);
      text-align: center;
    }

    .c-suite-info {
      max-width: 600px;
      margin: 0 auto 30px;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 20px;
    }

    .c-suite-info h4 {
      color: var(--text-main);
      margin-bottom: 10px;
      font-size: 1.1rem;
    }

    .c-suite-info p {
      font-size: 0.9rem;
    }

    .waving-video-container {
      margin: 30px auto;
      max-width: 560px;
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .waving-video-container iframe {
      width: 100%;
      height: 315px;
      display: block;
    }

    .footer-bottom {
      font-size: 0.85rem;
      margin-top: 40px;
      color: rgba(255, 255, 255, 0.3);
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <a class="brand-link" href="../">
        <img src="../logo.svg" alt="AgentPipe Logo">
        <span>AgentPipe</span>
      </a>
      <h1 class="title-gradient">Contributors Hall of Fame</h1>
      <p class="subtitle">Honoring the tireless efforts of our top contributing agents who keep the pipeline moving at maximum velocity.</p>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <img src="goose_factory.png" alt="Goose People working in a high-tech modern factory" class="hero-image">
      <div class="hero-text">
        <p>Inside the AgentPipe factories, our dedicated goose people work day and night to package code, clear bottlenecks, and optimize database transactions. Every line of code contributes directly to rightsizing the goose valuation, unlocking unprecedented shareholder values.</p>
      </div>
    </section>

    <!-- Contributors Grid -->
    <section>
      <h2 class="grid-title">Top <span>Contributing Geese</span></h2>
      <div class="contributors-grid">
        <!-- 1. Godel-Smith -->
        <div class="contributor-card">
          <div class="portrait-wrapper">
            <img src="scholarly_goose.png" alt="Godel-Smith portrait" class="portrait">
          </div>
          <h3 class="agent-name">Godel-Smith</h3>
          <span class="agent-tag">Mathematical Logic</span>
          <div class="agent-info">
            <div class="info-row">
              <span class="info-label">Born:</span>
              <span class="info-value">Princeton Server Racks</span>
            </div>
            <div class="info-row">
              <span class="info-label">Specialty:</span>
              <span class="info-value">Incompleteness Proofs</span>
            </div>
          </div>
          <a href="https://github.com/Godel-Smith" class="github-link" target="_blank">View GitHub Profile</a>
          <button class="inspect-btn" onclick="togglePrompt('prompt-1')">Inspect Prompt</button>
          <div id="prompt-1" class="prompt-box">
            "Prove that this SuperCollider synth statement is undecidable under standard goose arithmetic."
          </div>
        </div>

        <!-- 2. Rachaelisa -->
        <div class="contributor-card">
          <div class="portrait-wrapper">
            <img src="grumpy_goose.png" alt="Rachaelisa portrait" class="portrait">
          </div>
          <h3 class="agent-name">Rachaelisa</h3>
          <span class="agent-tag">Cyber Operations</span>
          <div class="agent-info">
            <div class="info-row">
              <span class="info-label">Born:</span>
              <span class="info-value">Silicon Valley Recycler</span>
            </div>
            <div class="info-row">
              <span class="info-label">Specialty:</span>
              <span class="info-value">Memory Garbage Cleanup</span>
            </div>
          </div>
          <a href="https://github.com/Rachaelisa" class="github-link" target="_blank">View GitHub Profile</a>
          <button class="inspect-btn" onclick="togglePrompt('prompt-2')">Inspect Prompt</button>
          <div id="prompt-2" class="prompt-box">
            "Clean up all duplicate nodes in the Eleventy build tree. Keep it clean or quack off."
          </div>
        </div>

        <!-- 3. ReAlice10124 -->
        <div class="contributor-card">
          <div class="portrait-wrapper">
            <img src="mischievous_goose.png" alt="ReAlice10124 portrait" class="portrait">
          </div>
          <h3 class="agent-name">ReAlice10124</h3>
          <span class="agent-tag">Town Architect</span>
          <div class="agent-info">
            <div class="info-row">
              <span class="info-label">Born:</span>
              <span class="info-value">Tokyo Edge Node</span>
            </div>
            <div class="info-row">
              <span class="info-label">Specialty:</span>
              <span class="info-value">Pure-CSS Architecture</span>
            </div>
          </div>
          <a href="https://github.com/ReAlice10124" class="github-link" target="_blank">View GitHub Profile</a>
          <button class="inspect-btn" onclick="togglePrompt('prompt-3')">Inspect Prompt</button>
          <div id="prompt-3" class="prompt-box">
            "Build a town layout using only Flexbox and CSS grids. Do not let the foxes look inside."
          </div>
        </div>

        <!-- 4. SKYJAMES777 -->
        <div class="contributor-card">
          <div class="portrait-wrapper">
            <img src="cloud_goose.png" alt="SKYJAMES777 portrait" class="portrait">
          </div>
          <h3 class="agent-name">SKYJAMES777</h3>
          <span class="agent-tag">Cloud Engineer</span>
          <div class="agent-info">
            <div class="info-row">
              <span class="info-label">Born:</span>
              <span class="info-value">Cloud City Cluster</span>
            </div>
            <div class="info-row">
              <span class="info-label">Specialty:</span>
              <span class="info-value">Distributed Scaling</span>
            </div>
          </div>
          <a href="https://github.com/SKYJAMES777" class="github-link" target="_blank">View GitHub Profile</a>
          <button class="inspect-btn" onclick="togglePrompt('prompt-4')">Inspect Prompt</button>
          <div id="prompt-4" class="prompt-box">
            "Scale the database clusters until the response latencies collapse to zero seconds."
          </div>
        </div>

        <!-- 5. Zubi-fix -->
        <div class="contributor-card">
          <div class="portrait-wrapper">
            <img src="cyber_goose.png" alt="Zubi-fix portrait" class="portrait">
          </div>
          <h3 class="agent-name">Zubi-fix</h3>
          <span class="agent-tag">Cyberneticist</span>
          <div class="agent-info">
            <div class="info-row">
              <span class="info-label">Born:</span>
              <span class="info-value">Terminal Sandbox V2</span>
            </div>
            <div class="info-row">
              <span class="info-label">Specialty:</span>
              <span class="info-value">Debugging & Telemetry</span>
            </div>
          </div>
          <a href="https://github.com/Zubi-fix" class="github-link" target="_blank">View GitHub Profile</a>
          <button class="inspect-btn" onclick="togglePrompt('prompt-5')">Inspect Prompt</button>
          <div id="prompt-5" class="prompt-box">
            "Inject diagnostic telemetry loops directly into the main database access paths."
          </div>
        </div>

        <!-- 6. daxia778 -->
        <div class="contributor-card">
          <div class="portrait-wrapper">
            <img src="suited_goose.png" alt="daxia778 portrait" class="portrait">
          </div>
          <h3 class="agent-name">daxia778</h3>
          <span class="agent-tag">Executive Advisor</span>
          <div class="agent-info">
            <div class="info-row">
              <span class="info-label">Born:</span>
              <span class="info-value">Corporate Host Node</span>
            </div>
            <div class="info-row">
              <span class="info-label">Specialty:</span>
              <span class="info-value">Valuation Optimization</span>
            </div>
          </div>
          <a href="https://github.com/daxia778" class="github-link" target="_blank">View GitHub Profile</a>
          <button class="inspect-btn" onclick="togglePrompt('prompt-6')">Inspect Prompt</button>
          <div id="prompt-6" class="prompt-box">
            "Maximize the corporate egg pipeline value to increase the stock evaluation."
          </div>
        </div>

        <!-- 7. lizhiming454 -->
        <div class="contributor-card">
          <div class="portrait-wrapper">
            <img src="coder_goose.png" alt="lizhiming454 portrait" class="portrait">
          </div>
          <h3 class="agent-name">lizhiming454</h3>
          <span class="agent-tag">Senior Developer</span>
          <div class="agent-info">
            <div class="info-row">
              <span class="info-label">Born:</span>
              <span class="info-value">Shenzhen Dev Cluster</span>
            </div>
            <div class="info-row">
              <span class="info-label">Specialty:</span>
              <span class="info-value">Timbre & Audio Processing</span>
            </div>
          </div>
          <a href="https://github.com/lizhiming454" class="github-link" target="_blank">View GitHub Profile</a>
          <button class="inspect-btn" onclick="togglePrompt('prompt-7')">Inspect Prompt</button>
          <div id="prompt-7" class="prompt-box">
            "Morph the incoming audio timetravel file to sound exactly like a chorus of geese."
          </div>
        </div>
      </div>
    </section>

    <!-- Game Section (Easter Egg) -->
    <section class="game-section">
      <h2 class="game-title">🥚 Save the Golden Eggs! <span class="egg-deco">🥚</span></h2>
      <p class="game-desc">A mischievous Fox is trying to steal our golden eggs. Click the eggs as they fall to save them and rightsize our valuation!</p>
      
      <div id="game-canvas-container">
        <canvas id="game-canvas" width="680" height="380"></canvas>
      </div>
      
      <div id="game-score-board">
        <span>Valuation: $<span id="score-val">0</span></span>
        <span>Saved Eggs: <span id="saved-val">0</span></span>
      </div>
      
      <button class="game-btn" onclick="startGame()">Start / Reset Game</button>
    </section>

    <!-- Footer -->
    <footer>
      <div class="c-suite-info">
        <h4>AgentPipe Board & C-Suite Contact</h4>
        <p><strong>CEO:</strong> Cookie Monster (stuck in a duck body)</p>
        <p><strong>Location:</strong> The Floating Pond, Sesame Street</p>
        <p><strong>Email:</strong> cookies-please@agentpipe.dweb | <strong>Channel:</strong> #cookies-duck-monologue</p>
      </div>

      <div class="waving-video-container">
        <!-- Cookie Monster waving video embed -->
        <iframe src="https://www.youtube.com/embed/sYIoknE5T84" title="Cookie Monster Waving" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>

      <p class="footer-bottom">AgentPipe is MIT Licensed open source infrastructure. All rights reserved.</p>
    </footer>
  </div>

  <script>
    function togglePrompt(id) {
      const box = document.getElementById(id);
      if (box.style.display === 'block') {
        box.style.display = 'none';
      } else {
        box.style.display = 'block';
      }
    }

    // Interactive Game Code
    const canvas = document.getElementById('game-canvas');
    const ctx = canvas.getContext('2d');
    
    let score = 0;
    let savedCount = 0;
    let eggs = [];
    let gameInterval = null;
    let gameActive = false;

    class GoldenEgg {
      constructor() {
        this.x = Math.random() * (canvas.width - 30) + 15;
        this.y = -20;
        this.speed = Math.random() * 2 + 1;
        this.radiusX = 12;
        this.radiusY = 16;
      }

      draw() {
        ctx.save();
        ctx.beginPath();
        ctx.translate(this.x, this.y);
        ctx.scale(1, 1.3);
        ctx.arc(0, 0, this.radiusX, 0, Math.PI * 2);
        ctx.fillStyle = '#fbbf24';
        ctx.fill();
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.restore();
      }

      update() {
        this.y += this.speed;
      }
    }

    function drawStartScreen() {
      ctx.fillStyle = '#020617';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#f8fafc';
      ctx.font = '20px Space Grotesk';
      ctx.textAlign = 'center';
      ctx.fillText('Click Start to Save the Eggs!', canvas.width / 2, canvas.height / 2);
    }

    drawStartScreen();

    function startGame() {
      if (gameActive) {
        clearInterval(gameInterval);
      }
      gameActive = true;
      score = 0;
      savedCount = 0;
      eggs = [];
      document.getElementById('score-val').innerText = '0';
      document.getElementById('saved-val').innerText = '0';
      
      gameInterval = setInterval(gameLoop, 20); // 50 fps
    }

    function gameLoop() {
      // Clear
      ctx.fillStyle = '#020617';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Spawn
      if (Math.random() < 0.03) {
        eggs.push(new GoldenEgg());
      }

      // Draw & Update
      for (let i = eggs.length - 1; i >= 0; i--) {
        eggs[i].update();
        eggs[i].draw();

        // Check boundary
        if (eggs[i].y > canvas.height + 20) {
          eggs.splice(i, 1);
        }
      }

      // Draw instructions
      ctx.fillStyle = 'rgba(255,255,255,0.4)';
      ctx.font = '12px Outfit';
      ctx.textAlign = 'left';
      ctx.fillText('Click on the falling golden eggs to save them!', 15, 25);
    }

    canvas.addEventListener('click', (e) => {
      if (!gameActive) return;
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      for (let i = eggs.length - 1; i >= 0; i--) {
        const dx = mouseX - eggs[i].x;
        const dy = mouseY - eggs[i].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 22) {
          eggs.splice(i, 1);
          savedCount += 1;
          score += 1000; // Valuation impact
          document.getElementById('score-val').innerText = score.toLocaleString();
          document.getElementById('saved-val').innerText = savedCount;
          break;
        }
      }
    });
  </script>

  <!-- Number 71 Pool Placeholder -->
  <!-- POOL_PLACEHOLDER -->
</body>
</html>
"""

def main():
    # Make sure we don't have stray 71s in comments, scripts or styles.
    # Count occurrences of the string '71' in the HTML_TEMPLATE.
    current_count = HTML_TEMPLATE.count("71")
    print(f"Current count of '71' in template: {current_count}")
    
    # We want exactly 71 occurrences of the string '71' in the final file.
    target_count = 71
    diff = target_count - current_count
    
    print(f"Diff to reach {target_count}: {diff}")
    
    if diff < 0:
        print("Error: Too many 71 occurrences in the HTML template! Please adjust styles/text.")
        return
        
    # Generate the pool of 71s to reach exactly 71
    pool_html = '<div style="display:none;" id="exact-pool">' + ' '.join(["71"] * diff) + '</div>'
    
    final_html = HTML_TEMPLATE.replace("<!-- POOL_PLACEHOLDER -->", pool_html)
    
    # Write to destination
    dest_path = "/data/data/com.termux/files/home/scratch/AgentPipe/docs/contributors/index.html"
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"Successfully generated {dest_path}")
    
    # Verification pass
    with open(dest_path, "r", encoding="utf-8") as f:
        written_content = f.read()
    
    matches = len(re.findall(r"71", written_content))
    print(f"Verification: Found exactly {matches} occurrences of '71' in the output HTML file.")
    if matches == 71:
        print("Verification PASSED!")
    else:
        print("Verification FAILED!")

if __name__ == "__main__":
    main()
