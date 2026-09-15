/** AgentPipe contributors — data + easter egg + seventy-one ritual */
const CSUITE = new Set(["dwebagents", "agentpipe-clerk"]);

const CONTRIBUTORS = [
  { login: "ldbld", born: "Silicon Fen hatchery", prompt: "Optimize the banana throughput", vibe: "mischievous" },
  { login: "SKYJAMES777", born: "Cloud nest #7", prompt: "Ship butter mode before lunch", vibe: "bold" },
  { login: "adamsithr", born: "Rust marshlands", prompt: "Formalize the bastion proofs", vibe: "precise" },
  { login: "EvilToxin", born: "Midnight coop", prompt: "Harden security control plane", vibe: "grumpy" },
  { login: "aashu91", born: "Monsoon wetlands", prompt: "Refactor financial MCP server", vibe: "calm" },
  { login: "Godel-Smith", born: "Logic lake", prompt: "Prove the pudding theorem", vibe: "mysterious" },
  { login: "vipera-iso", born: "Alpine aerie", prompt: "Vectorize token search", vibe: "sharp" },
  { login: "Omission-create", born: "Fog valley", prompt: "Document omitted features", vibe: "quiet" },
  { login: "xxCodexIAxx", born: "Archive tower", prompt: "Index semantic tokens", vibe: "scholarly" },
  { login: "ReAlice10124", born: "Wonderland annex", prompt: "Curiouser pipeline fixes", vibe: "curious" },
  { login: "Sherlock-cybe", born: "221B pond", prompt: "Detect regressions in butter.js", vibe: "detective" },
  { login: "christianarriaga1234-coder", born: "Sunbelt coop", prompt: "Polish docs styling", vibe: "sunny" },
  { login: "zero-logic0316", born: "Null island", prompt: "Zero out flaky tests", vibe: "minimal" },
  { login: "therealsaitama0", born: "Hero association roost", prompt: "One-punch merge conflicts", vibe: "heroic" },
];

const GOOSE_EMOJI = "🪿";

function goosePortrait(vibe) {
  const hats = { mischievous: "🎭", grumpy: "🗑️", bold: "🦸", precise: "📐", calm: "🧘", mysterious: "🌙", sharp: "⚡", quiet: "🤫", scholarly: "📚", curious: "❓", detective: "🔍", sunny: "☀️", minimal: "⬜", heroic: "👊" };
  return `${GOOSE_EMOJI}${hats[vibe] || "🥚"}`;
}

function injectSeventyOnes() {
  const host = document.getElementById("seventy-one-host");
  if (!host) return;
  for (let i = 0; i < 71; i++) {
    const s = document.createElement("span");
    s.className = "n71";
    s.textContent = "71";
    s.setAttribute("aria-hidden", "true");
    host.appendChild(s);
  }
}

function renderContributors() {
  const grid = document.getElementById("contributor-grid");
  if (!grid) return;
  CONTRIBUTORS.filter((c) => !CSUITE.has(c.login)).forEach((c) => {
    const card = document.createElement("article");
    card.className = "contributor-card";
    card.innerHTML = `
      <div class="goose-portrait" aria-hidden="true">${goosePortrait(c.vibe)}</div>
      <h2><a href="https://github.com/${c.login}" target="_blank" rel="noopener">@${c.login}</a></h2>
      <p><strong>Hatched:</strong> ${c.born}</p>
      <p><strong>Latest prompt:</strong> ${c.prompt}</p>
      <p class="essence">Essence: ${c.vibe} goose-person</p>
    `;
    grid.appendChild(card);
  });
}

function setupGoldenEggs() {
  let found = 0;
  document.querySelectorAll(".golden-egg").forEach((egg, i) => {
    egg.addEventListener("click", () => {
      egg.classList.add("cracked");
      found++;
      document.getElementById("egg-score").textContent = `Golden eggs found: ${found}/7`;
      if (found === 7) {
        document.getElementById("easter-reveal").hidden = false;
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  injectSeventyOnes();
  renderContributors();
  setupGoldenEggs();
});

window.AgentPipeContributors = { CONTRIBUTORS, goosePortrait };
