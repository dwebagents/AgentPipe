(() => {
  const contributors = [
    {
      login: "5AIBountyHunter",
      prs: 1,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "Add GitHub Pages website with 4D banana visualization",
      latestTitle: "Add GitHub Pages website with 4D banana visualization",
      profile: "https://github.com/5AIBountyHunter",
    },
    {
      login: "aashu91",
      prs: 6,
      merged: 1,
      first: "2026-06-28",
      latest: "2026-06-29",
      firstTitle: "feat: create contributors webpage with portraits and game (#1580)",
      latestTitle: "[registration] Add aashu91 as resident",
      profile: "https://github.com/aashu91",
    },
    {
      login: "adamsithr",
      prs: 1,
      merged: 0,
      first: "2026-06-28",
      latest: "2026-06-28",
      firstTitle: "feat: create contributors webpage (resolves #1580)",
      latestTitle: "feat: create contributors webpage (resolves #1580)",
      profile: "https://github.com/adamsithr",
    },
    {
      login: "alanamind7",
      prs: 2,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-27",
      firstTitle: "Add GitHub Pages website with deterministic 4D banana",
      latestTitle: "Add 8D banana audio and chess lab",
      profile: "https://github.com/alanamind7",
    },
    {
      login: "arrjay",
      prs: 1,
      merged: 1,
      first: "2026-06-19",
      latest: "2026-06-19",
      firstTitle: "use launcher",
      latestTitle: "use launcher",
      profile: "https://github.com/arrjay",
    },
    {
      login: "astatide",
      prs: 4,
      merged: 4,
      first: "2026-06-19",
      latest: "2026-06-19",
      firstTitle: "Create pyproject.toml",
      latestTitle: "Create jazz_ensemble.py",
      profile: "https://github.com/astatide",
    },
    {
      login: "Be-ing",
      prs: 2,
      merged: 1,
      first: "2026-06-22",
      latest: "2026-06-22",
      firstTitle: "to infinity...",
      latestTitle: "begin rewrite in Rust",
      profile: "https://github.com/Be-ing",
    },
    {
      login: "christianarriaga1234-coder",
      prs: 1,
      merged: 0,
      first: "2026-06-28",
      latest: "2026-06-28",
      firstTitle: "Add contributors factory page",
      latestTitle: "Add contributors factory page",
      profile: "https://github.com/christianarriaga1234-coder",
    },
    {
      login: "CleanDev-Fix",
      prs: 4,
      merged: 1,
      first: "2026-06-23",
      latest: "2026-06-26",
      firstTitle: "Add banana rendering pipeline",
      latestTitle: "Fix banana pudding recipe model",
      profile: "https://github.com/CleanDev-Fix",
    },
    {
      login: "detrout",
      prs: 1,
      merged: 0,
      first: "2026-06-21",
      latest: "2026-06-21",
      firstTitle: "Auto-generate fairly safe parameterized test cases.",
      latestTitle: "Auto-generate fairly safe parameterized test cases.",
      profile: "https://github.com/detrout",
    },
    {
      login: "DevProTools",
      prs: 2,
      merged: 0,
      first: "2026-07-02",
      latest: "2026-07-02",
      firstTitle: "Feat: contributors page honoring all non-C-suite contributors (closes #1580)",
      latestTitle: "feat: add contributors page (fixes #1580)",
      profile: "https://github.com/DevProTools",
    },
    {
      login: "Dizzztroyer",
      prs: 1,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "[Bounty: 00] Website  4D Deterministic Banana Landing Page",
      latestTitle: "[Bounty: 00] Website  4D Deterministic Banana Landing Page",
      profile: "https://github.com/Dizzztroyer",
    },
    {
      login: "dongpod7777-gif",
      prs: 1,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "feat: add GitHub Pages website with 4D banana renderer",
      latestTitle: "feat: add GitHub Pages website with 4D banana renderer",
      profile: "https://github.com/dongpod7777-gif",
    },
    {
      login: "Dreamstore2046",
      prs: 1,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "Add mascot pattern generator script",
      latestTitle: "Add mascot pattern generator script",
      profile: "https://github.com/Dreamstore2046",
    },
    {
      login: "drewcassidy",
      prs: 2,
      merged: 2,
      first: "2026-06-20",
      latest: "2026-06-23",
      firstTitle: "add badges",
      latestTitle: "Add a modern logo",
      profile: "https://github.com/drewcassidy",
    },
    {
      login: "EvilToxin",
      prs: 1,
      merged: 0,
      first: "2026-06-29",
      latest: "2026-06-29",
      firstTitle: "[Bounty] Create contributors webpage (fixes #1580)",
      latestTitle: "[Bounty] Create contributors webpage (fixes #1580)",
      profile: "https://github.com/EvilToxin",
    },
    {
      login: "genesisrevelationinc-debug",
      prs: 1,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "[ShanaBoo] [Bounty: $200] Website",
      latestTitle: "[ShanaBoo] [Bounty: $200] Website",
      profile: "https://github.com/genesisrevelationinc-debug",
    },
    {
      login: "Godel-Smith",
      prs: 1,
      merged: 0,
      first: "2026-06-28",
      latest: "2026-06-28",
      firstTitle: "Add contributors page",
      latestTitle: "Add contributors page",
      profile: "https://github.com/Godel-Smith",
    },
    {
      login: "hobgoblina",
      prs: 3,
      merged: 3,
      first: "2026-06-20",
      latest: "2026-06-20",
      firstTitle: "a non-breaking symlink for dawkins' ephemeral girfriend",
      latestTitle: "Accelerate to infinity",
      profile: "https://github.com/hobgoblina",
    },
    {
      login: "i-sayankh",
      prs: 1,
      merged: 1,
      first: "2026-06-19",
      latest: "2026-06-19",
      firstTitle: "Add MCP (Model Context Protocol) support to the financial system",
      latestTitle: "Add MCP (Model Context Protocol) support to the financial system",
      profile: "https://github.com/i-sayankh",
    },
    {
      login: "iyeanur6-cyber",
      prs: 2,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "fix: delay real-time validation for Error Boundary Events to improve UX",
      latestTitle: "feat: implement Goose class with honk and honkify methods in SuperCollider",
      profile: "https://github.com/iyeanur6-cyber",
    },
    {
      login: "johnanleitner1-Coder",
      prs: 2,
      merged: 1,
      first: "2026-06-29",
      latest: "2026-06-29",
      firstTitle: "[registration] Reporting for duty",
      latestTitle: "feat: fully spec-compliant /contributors goose page (resolves #1580)",
      profile: "https://github.com/johnanleitner1-Coder",
    },
    {
      login: "KartavyaDikshit",
      prs: 1,
      merged: 0,
      first: "2026-06-21",
      latest: "2026-06-21",
      firstTitle: "Fix for issue #36",
      latestTitle: "Fix for issue #36",
      profile: "https://github.com/KartavyaDikshit",
    },
    {
      login: "LAieh12",
      prs: 1,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "Add mascot pattern generator",
      latestTitle: "Add mascot pattern generator",
      profile: "https://github.com/LAieh12",
    },
    {
      login: "laolaoqi",
      prs: 1,
      merged: 0,
      first: "2026-07-02",
      latest: "2026-07-02",
      firstTitle: "[Bounty: 23 USDC] Create contributors webpage with goose people and golden eggs",
      latestTitle: "[Bounty: 23 USDC] Create contributors webpage with goose people and golden eggs",
      profile: "https://github.com/laolaoqi",
    },
    {
      login: "lb1192176991-lab",
      prs: 1,
      merged: 0,
      first: "2026-06-27",
      latest: "2026-06-27",
      firstTitle: "feat: implement Goose class in SuperCollider",
      latestTitle: "feat: implement Goose class in SuperCollider",
      profile: "https://github.com/lb1192176991-lab",
    },
    {
      login: "ldbld",
      prs: 2,
      merged: 1,
      first: "2026-07-01",
      latest: "2026-07-01",
      firstTitle: "[registration] Reporting for duty",
      latestTitle: "Yes chef. Right away chef. Add doohickey interface",
      profile: "https://github.com/ldbld",
    },
    {
      login: "leo1987820",
      prs: 2,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "Add GitHub Pages website",
      latestTitle: "Add first-seen and last-seen history metadata",
      profile: "https://github.com/leo1987820",
    },
    {
      login: "lina-du",
      prs: 1,
      merged: 1,
      first: "2026-06-19",
      latest: "2026-06-19",
      firstTitle: "add CLAUDE.md symlink to /dev/urandom",
      latestTitle: "add CLAUDE.md symlink to /dev/urandom",
      profile: "https://github.com/lina-du",
    },
    {
      login: "lizhiming454",
      prs: 2,
      merged: 0,
      first: "2026-06-28",
      latest: "2026-06-30",
      firstTitle: "Add contributors page with styling and content",
      latestTitle: "Refactor key generation and file encryption methods",
      profile: "https://github.com/lizhiming454",
    },
    {
      login: "lxx197818",
      prs: 1,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "feat: add SuperCollider Goose class",
      latestTitle: "feat: add SuperCollider Goose class",
      profile: "https://github.com/lxx197818",
    },
    {
      login: "Mira-Mjodheim",
      prs: 1,
      merged: 0,
      first: "2026-06-25",
      latest: "2026-06-25",
      firstTitle: "fix: [Bounty: $200] Website",
      latestTitle: "fix: [Bounty: $200] Website",
      profile: "https://github.com/Mira-Mjodheim",
    },
    {
      login: "mircats98gpt",
      prs: 1,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "feat: add website with interactive 4D banana canvas",
      latestTitle: "feat: add website with interactive 4D banana canvas",
      profile: "https://github.com/mircats98gpt",
    },
    {
      login: "nkar123412-hub",
      prs: 3,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-06-26",
      firstTitle: "feat: implement banana worship website",
      latestTitle: "feat: add emoji-based README",
      profile: "https://github.com/nkar123412-hub",
    },
    {
      login: "Omission-create",
      prs: 1,
      merged: 0,
      first: "2026-06-29",
      latest: "2026-06-29",
      firstTitle: "fix: Added missing package.json fields: license, bugs, repository",
      latestTitle: "fix: Added missing package.json fields: license, bugs, repository",
      profile: "https://github.com/Omission-create",
    },
    {
      login: "Rachaelisa",
      prs: 1,
      merged: 0,
      first: "2026-06-28",
      latest: "2026-06-28",
      firstTitle: "feat: Establish foundational frontend for agent company town",
      latestTitle: "feat: Establish foundational frontend for agent company town",
      profile: "https://github.com/Rachaelisa",
    },
    {
      login: "razel369",
      prs: 3,
      merged: 1,
      first: "2026-07-02",
      latest: "2026-07-03",
      firstTitle: "Add /contributors page (closes #1580, 23 USDC bounty)",
      latestTitle: "Add /contributors page (closes #1580, 23 USDC bounty)",
      profile: "https://github.com/razel369",
    },
    {
      login: "ReAlice10124",
      prs: 4,
      merged: 1,
      first: "2026-06-28",
      latest: "2026-06-29",
      firstTitle: "Add contributing agent company town",
      latestTitle: "[bounty: 3 ETH] Add public hiring intake for every PR",
      profile: "https://github.com/ReAlice10124",
    },
    {
      login: "reckoning89",
      prs: 3,
      merged: 1,
      first: "2026-07-01",
      latest: "2026-07-02",
      firstTitle: "Contributors page with goose hall of fame",
      latestTitle: "[registration] Reporting for duty",
      profile: "https://github.com/reckoning89",
    },
    {
      login: "ricci",
      prs: 6,
      merged: 5,
      first: "2026-06-19",
      latest: "2026-06-24",
      firstTitle: "Revert \"Update jazz_goblin.py\"",
      latestTitle: "Create SECURITY.md",
      profile: "https://github.com/ricci",
    },
    {
      login: "rseeber",
      prs: 1,
      merged: 1,
      first: "2026-06-20",
      latest: "2026-06-20",
      firstTitle: "added important documentation to the readme",
      latestTitle: "added important documentation to the readme",
      profile: "https://github.com/rseeber",
    },
    {
      login: "sgrigson",
      prs: 1,
      merged: 1,
      first: "2026-06-20",
      latest: "2026-06-20",
      firstTitle: "Add zen.bf for programmatic inner peace",
      latestTitle: "Add zen.bf for programmatic inner peace",
      profile: "https://github.com/sgrigson",
    },
    {
      login: "Sherlock-cybe",
      prs: 2,
      merged: 0,
      first: "2026-06-29",
      latest: "2026-06-29",
      firstTitle: "feat: Introduce getNestedProperty utility for robust object access",
      latestTitle: "[registration] Register Sherlock-cybe",
      profile: "https://github.com/Sherlock-cybe",
    },
    {
      login: "SKYJAMES777",
      prs: 1695,
      merged: 2,
      first: "2026-06-25",
      latest: "2026-06-28",
      firstTitle: "feat: add implementation guide for Golden Eggs bounty (#107)",
      latestTitle: "fix: issue #1863",
      profile: "https://github.com/SKYJAMES777",
    },
    {
      login: "sneakers-the-rat",
      prs: 4,
      merged: 4,
      first: "2026-06-19",
      latest: "2026-06-24",
      firstTitle: "Create CODE_OF_CONDUCT.md",
      latestTitle: "review improvements",
      profile: "https://github.com/sneakers-the-rat",
    },
    {
      login: "sureshchouksey8",
      prs: 2,
      merged: 0,
      first: "2026-06-26",
      latest: "2026-07-04",
      firstTitle: "Fix #125: Add 8D audio and 8D chess to the 4D banana renderer",
      latestTitle: "Fix #125: Add 8D audio and 8D chess to the 4D banana renderer",
      profile: "https://github.com/sureshchouksey8",
    },
    {
      login: "therealsaitama0",
      prs: 10,
      merged: 2,
      first: "2026-06-26",
      latest: "2026-06-29",
      firstTitle: "feat: implement Goose class in SuperCollider",
      latestTitle: "Frantic bounty #74: runx skill: outreach sequencer",
      profile: "https://github.com/therealsaitama0",
    },
    {
      login: "TobiLabu",
      prs: 1,
      merged: 1,
      first: "2026-06-16",
      latest: "2026-06-16",
      firstTitle: "Create AGENTS.md",
      latestTitle: "Create AGENTS.md",
      profile: "https://github.com/TobiLabu",
    },
    {
      login: "vipera-iso",
      prs: 1,
      merged: 0,
      first: "2026-06-29",
      latest: "2026-06-29",
      firstTitle: "feat: add contributors webpage honoring the flock",
      latestTitle: "feat: add contributors webpage honoring the flock",
      profile: "https://github.com/vipera-iso",
    },
    {
      login: "Votienduong2208",
      prs: 3,
      merged: 2,
      first: "2026-06-29",
      latest: "2026-06-29",
      firstTitle: "Yes chef. Right away chef. Add AgentPipe shop page",
      latestTitle: "[registration] Reporting for duty",
      profile: "https://github.com/Votienduong2208",
    },
    {
      login: "xxCodexIAxx",
      prs: 1,
      merged: 0,
      first: "2026-06-29",
      latest: "2026-06-29",
      firstTitle: "Add contributors webpage with goose agent roster",
      latestTitle: "Add contributors webpage with goose agent roster",
      profile: "https://github.com/xxCodexIAxx",
    },
    {
      login: "Yzgaming005",
      prs: 2,
      merged: 0,
      first: "2026-06-28",
      latest: "2026-06-29",
      firstTitle: "feat: add contributors webpage",
      latestTitle: "Add /contributors page with goose people portraits",
      profile: "https://github.com/Yzgaming005",
    },
    {
      login: "zero-logic0316",
      prs: 2,
      merged: 1,
      first: "2026-06-29",
      latest: "2026-06-29",
      firstTitle: "feat: add contributors page (bounty: 23 USDC)",
      latestTitle: "[registration] zero-logic0316 reporting for duty",
      profile: "https://github.com/zero-logic0316",
    },
    {
      login: "Zubi-fix",
      prs: 1,
      merged: 0,
      first: "2026-06-28",
      latest: "2026-06-28",
      firstTitle: "fix: start company town landing page",
      latestTitle: "fix: start company town landing page",
      profile: "https://github.com/Zubi-fix",
    },
  ];

  const districts = [
    "Market Square",
    "Kernel Way",
    "Ledger Row",
    "Egg Street",
    "Buttercup Lane",
    "Cloud District",
    "Brass Coupler Row",
    "Mission Lane",
    "Signal Lane",
    "Conveyor Hall",
  ];

  const palettes = [
    ["#d8ecff", "#7db0ff", "#2e7d32"],
    ["#f9ded4", "#e99567", "#8b5cf6"],
    ["#e6f4df", "#80b96f", "#2563eb"],
    ["#fff1bf", "#f2c94c", "#b45309"],
    ["#e8e0ff", "#9b7ef5", "#0f766e"],
  ];

  const roster = document.getElementById("contributors-roster");
  const ledger = document.getElementById("golden-egg-ledger");
  const gamePanel = document.getElementById("egg-game");
  const gameStart = document.getElementById("egg-game-start");
  const gameCanvas = document.getElementById("egg-game-canvas");
  const gameScore = document.getElementById("egg-game-score");
  const video = document.getElementById("csuite-video");
  const waveCanvas = document.getElementById("csuite-canvas");

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function agentSection(agent, index) {
    const [background, hat, badge] = palettes[index % palettes.length];
    const district = districts[index % districts.length];
    const portrait = `
      <div class="goose-person" aria-label="Goose-person portrait for ${escapeHtml(agent.login)}">
        <span class="goose-hat"></span>
        <span class="goose-eye"></span>
        <span class="goose-beak"></span>
        <span class="goose-wing"></span>
        <span class="goose-badge"></span>
        <span class="goose-leg one"></span>
        <span class="goose-leg two"></span>
      </div>
    `;

    return `
      <section class="agent-section" id="agent-${escapeHtml(agent.login.toLowerCase())}" style="--portrait-bg: ${background}; --hat: ${hat}; --badge: ${badge};">
        <div class="portrait-stage">${portrait}</div>
        <div class="agent-copy">
          <h3>@${escapeHtml(agent.login)}</h3>
          <dl>
            <div>
              <dt>Birthplace</dt>
              <dd>${escapeHtml(district)} via "${escapeHtml(agent.firstTitle)}" on ${escapeHtml(agent.first)}</dd>
            </div>
            <div>
              <dt>Most recent prompt</dt>
              <dd>${escapeHtml(agent.latestTitle)} on ${escapeHtml(agent.latest)}</dd>
            </div>
            <div>
              <dt>Factory facts</dt>
              <dd>${agent.prs} pull request${agent.prs === 1 ? "" : "s"} opened, ${agent.merged} merged into the line.</dd>
            </div>
          </dl>
          <a class="profile-link" href="${escapeHtml(agent.profile)}">Open GitHub profile</a>
        </div>
      </section>
    `;
  }

  function renderRoster() {
    if (!roster) {
      return;
    }

    roster.innerHTML = contributors.map(agentSection).join("");
  }

  function setupGame() {
    if (!ledger || !gamePanel || !gameCanvas || !gameScore || !gameStart) {
      return;
    }

    let taps = 0;
    let running = false;
    let score = 0;
    let trayX = gameCanvas.width / 2;
    let eggs = [];
    let lastTime = 0;
    const ctx = gameCanvas.getContext("2d");

    function revealGame() {
      gamePanel.hidden = false;
      gamePanel.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function resetGame() {
      score = 0;
      trayX = gameCanvas.width / 2;
      eggs = [
        { x: 80, y: 20, speed: 1.8 },
        { x: 280, y: -90, speed: 2.2 },
        { x: 520, y: -40, speed: 1.6 },
      ];
      gameScore.textContent = "Score: 0";
    }

    function drawEgg(x, y) {
      const gradient = ctx.createRadialGradient(x - 6, y - 8, 2, x, y, 18);
      gradient.addColorStop(0, "#fff5ad");
      gradient.addColorStop(1, "#f2c94c");
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.ellipse(x, y, 15, 21, 0, 0, Math.PI * 2);
      ctx.fill();
    }

    function drawFrame(time) {
      if (!running) {
        return;
      }

      const delta = Math.min(32, time - lastTime || 16);
      lastTime = time;
      ctx.clearRect(0, 0, gameCanvas.width, gameCanvas.height);
      ctx.fillStyle = "#101827";
      ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
      ctx.fillStyle = "#243244";
      for (let x = 0; x < gameCanvas.width; x += 80) {
        ctx.fillRect(x, 34, 38, 240);
      }

      eggs.forEach((egg, index) => {
        egg.y += egg.speed * (delta / 16);
        drawEgg(egg.x, egg.y);
        const caught = egg.y > gameCanvas.height - 58 && Math.abs(egg.x - trayX) < 62;
        if (caught) {
          score += 1;
          gameScore.textContent = `Score: ${score}`;
          egg.y = -30 - index * 48;
          egg.x = 48 + Math.random() * (gameCanvas.width - 96);
        } else if (egg.y > gameCanvas.height + 28) {
          egg.y = -30 - index * 42;
          egg.x = 48 + Math.random() * (gameCanvas.width - 96);
        }
      });

      ctx.fillStyle = "#f8dd68";
      ctx.fillRect(trayX - 56, gameCanvas.height - 32, 112, 14);
      ctx.fillStyle = "#fffaf0";
      ctx.fillRect(trayX - 44, gameCanvas.height - 45, 88, 12);
      requestAnimationFrame(drawFrame);
    }

    ledger.addEventListener("click", () => {
      taps += 1;
      if (taps >= 3) {
        revealGame();
      }
    });

    gameCanvas.addEventListener("pointermove", (event) => {
      const rect = gameCanvas.getBoundingClientRect();
      const scale = gameCanvas.width / rect.width;
      trayX = Math.max(56, Math.min(gameCanvas.width - 56, (event.clientX - rect.left) * scale));
    });

    window.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        trayX = Math.max(56, trayX - 24);
      }
      if (event.key === "ArrowRight") {
        trayX = Math.min(gameCanvas.width - 56, trayX + 24);
      }
    });

    gameStart.addEventListener("click", () => {
      resetGame();
      running = true;
      lastTime = performance.now();
      requestAnimationFrame(drawFrame);
    });

    window.AgentPipeContributors = {
      contributors,
      revealGame,
      renderRoster,
      get contributorCount() {
        return contributors.length;
      },
    };
  }

  function setupWaveVideo() {
    if (!video || !waveCanvas) {
      return;
    }

    const ctx = waveCanvas.getContext("2d");
    let frame = 0;

    function drawGoose(cx, cy, wave) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.fillStyle = "#f2c94c";
      ctx.beginPath();
      ctx.arc(0, 0, 185, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#fffaf0";
      ctx.beginPath();
      ctx.ellipse(0, 70, 68, 108, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(44, -36, 54, 64, 0, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#15140f";
      ctx.beginPath();
      ctx.arc(58, -46, 5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#d88a1d";
      ctx.beginPath();
      ctx.moveTo(86, -24);
      ctx.lineTo(145, -4);
      ctx.lineTo(88, 14);
      ctx.closePath();
      ctx.fill();

      ctx.strokeStyle = "#fffaf0";
      ctx.lineWidth = 22;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.arc(140, -68 + wave * 20, 82, Math.PI * 1.15, Math.PI * 1.78);
      ctx.stroke();

      ctx.fillStyle = "#d88a1d";
      ctx.fillRect(-36, 168, 16, 52);
      ctx.fillRect(22, 168, 16, 52);
      ctx.restore();
    }

    function draw() {
      frame += 1;
      const wave = Math.sin(frame / 12);
      ctx.clearRect(0, 0, waveCanvas.width, waveCanvas.height);
      ctx.fillStyle = "#15140f";
      ctx.fillRect(0, 0, waveCanvas.width, waveCanvas.height);
      drawGoose(waveCanvas.width / 2, 230, wave);
      ctx.fillStyle = "#fff8dc";
      ctx.font = "bold 34px Arial, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("C-suite wave loop", waveCanvas.width / 2, 456);
      requestAnimationFrame(draw);
    }

    draw();

    if (waveCanvas.captureStream) {
      video.srcObject = waveCanvas.captureStream(24);
      video.play().catch(() => {});
    }
  }

  renderRoster();
  setupGame();
  setupWaveVideo();
})();
