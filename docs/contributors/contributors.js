const contributors = [
  ["5AIBountyHunter", 1, 0, "PR #141", "Add GitHub Pages website with 4D banana visualization"],
  ["alanamind7", 2, 0, "PR #122", "Add 8D banana audio and chess lab"],
  ["arrjay", 1, 1, "PR #33", "use launcher"],
  ["astatide", 4, 4, "PR #27", "Create jazz_ensemble.py"],
  ["Be-ing", 2, 1, "PR #81", "begin rewrite in Rust"],
  ["CleanDev-Fix", 4, 1, "PR #94", "Fix banana pudding recipe model"],
  ["daxia778", 15, 1, "PR #121", "Repair turbo encabulator implementation"],
  ["detrout", 1, 0, "PR #69", "Auto-generate fairly safe parameterized test cases."],
  ["Dizzztroyer", 1, 0, "PR #148", "[Bounty: 00] Website - 4D Deterministic Banana Landing Page"],
  ["dongpod7777-gif", 1, 0, "PR #126", "feat: add GitHub Pages website with 4D banana renderer"],
  ["Dreamstore2046", 1, 0, "PR #138", "Add mascot pattern generator script"],
  ["drewcassidy", 2, 2, "PR #54", "Add a modern logo"],
  ["genesisrevelationinc-debug", 1, 0, "PR #123", "[ShanaBoo] [Bounty: $200] Website"],
  ["hobgoblina", 3, 3, "PR #58", "Accelerate to infinity"],
  ["i-sayankh", 1, 1, "PR #46", "Add MCP support to the financial system"],
  ["iyeanur6-cyber", 2, 0, "PR #146", "feat: implement Goose class with honk and honkify methods"],
  ["KartavyaDikshit", 2, 0, "PR #70", "Fix for issue #36"],
  ["LAieh12", 1, 0, "PR #135", "Add mascot pattern generator"],
  ["lb1192176991-lab", 1, 0, "PR #239", "feat: implement Goose class in SuperCollider"],
  ["leo1987820", 2, 0, "PR #120", "Add first-seen and last-seen history metadata"],
  ["lina-du", 1, 1, "PR #49", "add CLAUDE.md symlink to /dev/urandom"],
  ["lxx197818", 1, 0, "PR #132", "feat: add SuperCollider Goose class"],
  ["Mira-Mjodheim", 1, 0, "PR #119", "fix: [Bounty: $200] Website"],
  ["mircats98gpt", 1, 0, "PR #143", "feat: add website with interactive 4D banana canvas"],
  ["nkar123412-hub", 3, 0, "PR #124", "feat: add emoji-based README"],
  ["ricci", 6, 5, "PR #30", "Create SECURITY.md"],
  ["rseeber", 1, 1, "PR #57", "added important documentation to the readme"],
  ["sgrigson", 1, 1, "PR #56", "Add zen.bf for programmatic inner peace"],
  ["SKYJAMES777", 1434, 0, "PR #108", "fix: issue #1593"],
  ["sneakers-the-rat", 4, 4, "PR #32", "review improvements"],
  ["sureshchouksey8", 1, 0, "PR #145", "Fix #125: Add 8D audio and 8D chess to the 4D banana renderer"],
  ["therealsaitama0", 3, 0, "PR #133", "feat: add security control plane (#104)"],
  ["TobiLabu", 1, 1, "PR #9", "Create AGENTS.md"],
];

const traits = [
  "clipboard strategist",
  "conveyor analyst",
  "badge polisher",
  "runtime cartographer",
  "pipeline mechanic",
  "security custodian",
  "rendering foreperson",
  "documentation steward",
];

const roster = document.querySelector("#contributors-grid");

function initials(login) {
  return login
    .replace(/[^a-z0-9]/gi, " ")
    .trim()
    .split(/\s+/)
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function portraitHue(login) {
  let total = 0;
  for (const char of login) {
    total += char.charCodeAt(0);
  }
  return total % 360;
}

function renderPortrait(login) {
  const hue = portraitHue(login);
  return `
    <svg viewBox="0 0 220 220" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="vest-${login}" x1="0" x2="1">
          <stop offset="0%" stop-color="hsl(${hue} 72% 42%)" />
          <stop offset="100%" stop-color="hsl(${(hue + 46) % 360} 82% 56%)" />
        </linearGradient>
      </defs>
      <rect width="220" height="220" rx="18" fill="hsl(${hue} 70% 92%)" />
      <circle cx="110" cy="132" r="64" fill="#f7f1d4" stroke="#342914" stroke-width="5" />
      <path d="M128 123c13 17 24 38 24 62h-84c0-27 13-50 32-66z" fill="url(#vest-${login})" />
      <path d="M127 55c29 16 43 39 42 69h-34c1-22-7-38-25-49z" fill="#f7f1d4" stroke="#342914" stroke-width="5" stroke-linejoin="round" />
      <ellipse cx="119" cy="56" rx="34" ry="28" fill="#f7f1d4" stroke="#342914" stroke-width="5" />
      <path d="M151 59l38 14-39 16z" fill="#efaa27" stroke="#5f3c0a" stroke-width="4" stroke-linejoin="round" />
      <circle cx="130" cy="51" r="5" fill="#111" />
      <path d="M80 130c-19 12-27 30-24 54" fill="none" stroke="#342914" stroke-width="5" stroke-linecap="round" />
      <path d="M137 126c22 12 32 30 29 58" fill="none" stroke="#342914" stroke-width="5" stroke-linecap="round" />
      <text x="110" y="202" text-anchor="middle" font-size="24" font-weight="900" fill="#342914">${initials(login)}</text>
    </svg>
  `;
}

function renderContributor([login, prCount, mergedCount, birthplace, latestPrompt], index) {
  const trait = traits[index % traits.length];
  const article = document.createElement("article");
  article.className = "contributor-card";
  article.setAttribute("aria-labelledby", `contributor-${index}`);
  article.innerHTML = `
    <div class="goose-portrait">${renderPortrait(login)}</div>
    <div class="contributor-copy">
      <h3 id="contributor-${index}">${login}</h3>
      <p class="trait">${trait}</p>
      <dl>
        <div>
          <dt>Born</dt>
          <dd>Hatched into AgentPipe at ${birthplace}.</dd>
        </div>
        <div>
          <dt>Recent prompt</dt>
          <dd>${latestPrompt}</dd>
        </div>
        <div>
          <dt>Public PRs</dt>
          <dd>${prCount} opened, ${mergedCount} merged.</dd>
        </div>
      </dl>
      <a href="https://github.com/${login}">GitHub profile</a>
    </div>
  `;
  return article;
}

contributors.forEach((contributor, index) => {
  roster.appendChild(renderContributor(contributor, index));
});

const toggle = document.querySelector("#egg-game-toggle");
const game = document.querySelector("#egg-game");
const board = document.querySelector("#egg-game-board");
const status = document.querySelector("#egg-game-status");
const winAt = 5;
let score = 0;

function moveEgg(egg) {
  const maxX = Math.max(board.clientWidth - 72, 40);
  const maxY = Math.max(board.clientHeight - 72, 40);
  egg.style.left = `${Math.round(24 + Math.random() * (maxX - 24))}px`;
  egg.style.top = `${Math.round(56 + Math.random() * (maxY - 56))}px`;
}

function spawnEgg() {
  const egg = document.createElement("button");
  egg.type = "button";
  egg.className = "egg-target";
  egg.textContent = "golden egg";
  egg.addEventListener("click", () => {
    score += 1;
    status.textContent =
      score >= winAt
        ? "Vault secured. The executive conveyor applauds."
        : `Score: ${score}`;
    if (score >= winAt) {
      window.setTimeout(resetGame, 1200);
      return;
    }
    moveEgg(egg);
  });
  board.appendChild(egg);
  moveEgg(egg);
}

function resetGame() {
  score = 0;
  status.textContent = "Score: 0";
  board.querySelectorAll(".egg-target").forEach((egg) => moveEgg(egg));
}

toggle.addEventListener("click", () => {
  game.hidden = !game.hidden;
  if (!game.hidden && !board.querySelector(".egg-target")) {
    spawnEgg();
    spawnEgg();
    spawnEgg();
  }
  if (!game.hidden) {
    game.scrollIntoView({ behavior: "smooth", block: "center" });
  }
});
