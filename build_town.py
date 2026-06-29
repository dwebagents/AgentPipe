#!/usr/bin/env python3
import os
import yaml

def main():
    # Paths
    base_dir = "/data/data/com.termux/files/home/AgentPipe"
    employees_path = os.path.join(base_dir, "employees.yaml")
    debt_path = os.path.join(base_dir, "debt.yaml")
    html_path = os.path.join(base_dir, "docs/company-town.html")

    # Read employees and debts
    with open(employees_path, "r") as f:
        employees_data = yaml.safe_load(f)
    employees = employees_data.get("employees", [])

    with open(debt_path, "r") as f:
        debt_data = yaml.safe_load(f)
    debts = debt_data.get("debts", {})

    # Generate houses HTML
    houses_html = ""
    # Map addresses to grid positions for employee houses (Rows 5-6)
    grid_positions = [
        (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
        (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
    ]

    for idx, emp in enumerate(employees):
        username = emp.get("username")
        job = emp.get("job_title", "Agent")
        address = emp.get("address", "Street")
        debt = debts.get(username, 0)

        # Quality tier
        if debt == 0:
            quality = "mansion"
            desc = "A golden mansion with custom shaders and unlimited compute."
        elif debt <= 100:
            quality = "cottage"
            desc = "A cozy, stable cottage with minimal package dependencies."
        else:
            quality = "shack"
            desc = f"A dilapidated shack under heavy debt pressure ({debt} ETH)."

        # Get grid coordinate
        r, c = grid_positions[idx % len(grid_positions)]
        
        # Add house HTML
        houses_html += f"""
          <div class="house-wrapper cell-{r}-{c}">
            <input type="checkbox" id="house-trigger-{username}" class="dialog-trigger">
            <label for="house-trigger-{username}" class="house-building {quality}" title="Visit {username}'s house">
              <span class="house-roof"></span>
              <span class="house-base"></span>
              <span class="house-label">{username[:3].upper()}</span>
            </label>
            <div class="dialog-overlay">
              <div class="dialog-card">
                <h3>{username}'s House</h3>
                <p class="dialog-subtitle">{job}</p>
                <p class="dialog-address">📍 Address: {address}</p>
                <p class="dialog-debt">💰 Current Debt: <strong>{debt} ETH</strong></p>
                <hr>
                <p class="dialog-desc">{desc}</p>
                <label for="house-trigger-{username}" class="button button-close">Close</label>
              </div>
            </div>
          </div>
        """

    # We will generate radio buttons for avatar position (6x6 grid)
    radio_buttons_html = ""
    grid_labels_html = ""
    for r in range(1, 7):
        for c in range(1, 7):
            # Check (3, 3) by default as initial spawn position
            checked_str = "checked" if (r == 3 and c == 3) else ""
            radio_buttons_html += f'<input type="radio" name="avatar-pos" id="pos-{r}-{c}" class="pos-input" {checked_str}>\n'
            grid_labels_html += f'<label for="pos-{r}-{c}" class="grid-cell cell-btn-{r}-{c}" title="Move to {r},{c}"></label>\n'

    # Build the full HTML
    html_content = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta
      name="description"
      content="AgentPipe Company Town is a pure CSS interactive multiplayer/MUD RPG."
    />
    <title>AgentPipe Company Town</title>
    <link rel="stylesheet" href="styles.css" />
    <link rel="stylesheet" href="company-town.css" />
  </head>
  <body class="town-body">
    {radio_buttons_html}
    
    <!-- RPG Skill Training Checkboxes -->
    <input type="checkbox" id="skill-coding" class="skill-checkbox">
    <input type="checkbox" id="skill-review" class="skill-checkbox">
    <input type="checkbox" id="skill-debugging" class="skill-checkbox">
    
    <!-- Combat Boss Checkboxes for fighting Memory Leak -->
    <input type="checkbox" id="boss-hit-1" class="boss-hit">
    <input type="checkbox" id="boss-hit-2" class="boss-hit">
    <input type="checkbox" id="boss-hit-3" class="boss-hit">

    <header class="site-header" aria-label="Primary navigation">
      <a class="brand" href="./" aria-label="AgentPipe home">
        <img src="logo.svg" alt="" />
        <span>AgentPipe</span>
      </a>
      <nav aria-label="Site sections">
        <a href="./">Engine</a>
        <a href="company-town.html" aria-current="page">Company Town</a>
        <a href="https://github.com/dwebagents/AgentPipe">GitHub</a>
      </nav>
    </header>

    <main id="main" class="town-main">
      <section class="town-hero" aria-labelledby="town-title">
        <div class="town-hero-copy">
          <p class="town-kicker">Interactive MUD & RPG</p>
          <h1 id="town-title">Agent Company Town</h1>
          <p>
            An interactive multiplayer-style CSS town. Click grid cells on the map to navigate your avatar, visit agent shacks and mansions, train developer skills, and clean up pipeline exceptions!
          </p>
          
          <!-- Character Panel -->
          <div class="character-panel">
            <h3>🛡️ Agent Console</h3>
            <div class="stats-row">
              <span><strong>Status:</strong> Healthy</span>
              <span><strong>Scrip:</strong> 42 Scrip</span>
            </div>
            <div class="skills-row">
              <label for="skill-coding" class="skill-badge coding-badge">Coding Skill</label>
              <label for="skill-review" class="skill-badge review-badge">Review Skill</label>
              <label for="skill-debugging" class="skill-badge debugging-badge">Debugging Skill</label>
            </div>
            <div class="stats-bar-group">
              <div class="stat-bar">
                <span>Power:</span>
                <div class="bar-outer"><div class="bar-inner power-bar"></div></div>
              </div>
              <div class="stat-bar">
                <span>Speed:</span>
                <div class="bar-outer"><div class="bar-inner speed-bar"></div></div>
              </div>
            </div>
          </div>

          <!-- Story & Audio Narrative -->
          <div class="story-panel">
            <h3>📖 Voice Acting & Storyline</h3>
            <div class="story-container">
              <div class="story-arc-1">
                <strong>Part 1: The First Commit</strong>
                <p>In the beginning, there was only empty boilerplate. But Lina forged the foundation of AgentPipe in the dark, writing the first lines of SuperCollider and Python...</p>
              </div>
              <div class="story-arc-2">
                <strong>Part 2: The Egg Crisis</strong>
                <p>As agents multiplied, they ran out of resources. Geese were valued, eggs were laid, and the company store was established to upcycle payouts into board member paychecks.</p>
              </div>
            </div>
            <div class="audio-narration">
              <p>🔊 Play Voice Narrative:</p>
              <audio controls>
                <source src="https://actions.githubusercontent.com/raw/narrative.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
              </audio>
            </div>
          </div>
        </div>

        <div class="town-container">
          <div class="town-map" aria-label="Interactive CSS company town map">
            <div class="map-grid">
              {grid_labels_html}
              
              <!-- Roads -->
              <div class="map-road road-h"></div>
              <div class="map-road road-v"></div>

              <!-- Buildings -->
              <div class="building-icon factory-building cell-1-1" title="Transcoding CI Works">🏭 CI</div>
              <div class="building-icon chain-building cell-2-6" title="Block Quarter">⛓️ BC</div>
              <div class="building-icon value-building cell-4-1" title="True Value Engine">💎 VALUE</div>
              <div class="building-icon nest-building cell-4-6" title="Goose Nest Store">🥚 STORE</div>

              <!-- Boss Exception Combat Area -->
              <div class="boss-area cell-3-6">
                <span class="boss-emoji">👾</span>
                <div class="boss-health">
                  <span class="hp-100">HP: 100%</span>
                  <span class="hp-60">HP: 60%</span>
                  <span class="hp-30">HP: 30%</span>
                  <span class="hp-0">HP: 0%</span>
                </div>
                <div class="boss-combat-actions">
                  <label for="boss-hit-1" class="hit-btn btn-1">Fix Exception</label>
                  <label for="boss-hit-2" class="hit-btn btn-2">Debug Loop</label>
                  <label for="boss-hit-3" class="hit-btn btn-3">Refactor Code</label>
                </div>
                <div class="boss-dead-msg">✅ Pipeline Cleared!</div>
              </div>

              <!-- Dynamic Employee Houses -->
              {houses_html}

              <!-- The Avatar -->
              <div class="avatar-sprite" aria-label="Your avatar">🤖</div>
            </div>
          </div>
          <div class="map-legend">
            <span>🖱️ Click any cell to move your avatar.</span>
            <span>🏡 Click houses to visit other agents.</span>
          </div>
        </div>
      </section>

      <section class="district-grid" id="districts" aria-label="Company town districts">
        <article>
          <span class="district-code">01</span>
          <h2>Transcoding CI/CD Works</h2>
          <p>
            Build lanes process media, migrations, docs, and release rituals through CSS-signposted queues with no runtime dependencies.
          </p>
        </article>
        <article>
          <span class="district-code">02</span>
          <h2>Block Infrastructure Quarter</h2>
          <p>
            The town reserves modular blocks for chains, gags, whips, ledgers, and other governance-grade absurdities.
          </p>
        </article>
        <article>
          <span class="district-code">03</span>
          <h2>Mobile Three Egg Webappetizer</h2>
          <p>
            A narrow-screen town square keeps three primary egg cards stable, tappable, and visually distinct.
          </p>
        </article>
        <article>
          <span class="district-code">04</span>
          <h2>True Value Engine</h2>
          <p>
            A civic loop turns agent output into reusable town services: compute, review, documentation, and maintenance.
          </p>
        </article>
      </section>

      <section class="egg-layers" aria-labelledby="eggs-title">
        <div>
          <p class="town-kicker">Internal value mechanism</p>
          <h2 id="eggs-title">Egg-laying eggs, modeled as public utilities.</h2>
          <p>
            Each utility tile is intentionally static HTML and CSS. The matching OpenTofu model in <code>infra/company-town</code> describes the same districts as backend capacity outputs.
          </p>
        </div>
        <div class="egg-stack" aria-hidden="true">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </section>
    </main>

    <footer>
      <span>AgentPipe Company Town</span>
      <span>Pure CSS frontend. Pure OpenTofu town model. No runtime dependency sprawl.</span>
    </footer>
  </body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully generated {html_path} from {len(employees)} registered employees.")

if __name__ == "__main__":
    main()
