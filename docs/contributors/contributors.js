const grid = document.querySelector("#contributors-grid");
const summary = document.querySelector("#roster-summary");
const ledger = document.querySelector("#ledger-output");
const statusLine = document.querySelector("#game-status");
const eggButtons = Array.from(document.querySelectorAll(".egg-button"));
const foundEggs = new Set();

const birthplaceFor = (contributor, index) => {
  const stations = [
    "Merge Queue North",
    "Pipeline Floor",
    "Recipe Foundry",
    "Review Bay",
    "Pages Dock",
    "Optimization Lab",
  ];
  return stations[index % stations.length];
};

const essenceFor = (contributor, index) => {
  const traits = [
    "precision-minded",
    "deadline-friendly",
    "high-throughput",
    "documentation-aware",
    "review-hardened",
    "release-ready",
  ];
  return traits[(contributor.login.length + index) % traits.length];
};

const makeCard = (contributor, index) => {
  const card = document.createElement("section");
  card.className = "contributor-card";
  card.setAttribute("aria-labelledby", `contributor-${index}`);

  const portrait = document.createElement("div");
  portrait.className = "portrait";
  portrait.innerHTML = '<span class="portrait-shape" aria-hidden="true"></span>';

  const name = document.createElement("h3");
  name.id = `contributor-${index}`;
  name.textContent = contributor.login;

  const facts = document.createElement("p");
  facts.textContent = `Born in ${birthplaceFor(contributor, index)}. Pull requests: ${contributor.prs}.`;

  const prompt = document.createElement("p");
  prompt.textContent = `Most recent prompt: ${contributor.latestTitle}. Essence: ${essenceFor(contributor, index)}.`;

  const link = document.createElement("a");
  link.href = contributor.profile;
  link.textContent = "GitHub profile";

  card.append(portrait, name, facts, prompt, link);
  return card;
};

const renderLedger = (contributors) => {
  const count = contributors.length * 2 - 3;
  ledger.replaceChildren();
  for (let index = 0; index < count; index += 1) {
    const stamp = document.createElement("span");
    stamp.textContent = String(count);
    ledger.append(stamp);
  }
};

const renderContributors = async () => {
  const response = await fetch("contributors-data.json");
  if (!response.ok) {
    throw new Error("Contributor data failed to load.");
  }

  const contributors = await response.json();
  grid.replaceChildren(...contributors.map(makeCard));
  summary.textContent = `${contributors.length} public non-bot pull-request authors represented.`;
  renderLedger(contributors);
};

eggButtons.forEach((button) => {
  button.addEventListener("click", () => {
    foundEggs.add(button.dataset.egg);
    button.setAttribute("aria-pressed", "true");
    statusLine.textContent =
      foundEggs.size === eggButtons.length
        ? "Production bonus unlocked: the contributor floor is fully staffed."
        : `${foundEggs.size} of ${eggButtons.length} markers found.`;
  });
});

renderContributors().catch((error) => {
  summary.textContent = error.message;
});
