const employees = [
  { handle: "ReAlice10124", address: "17 Eggloop Row", role: "townwright", x: 30, y: 28 },
  { handle: "Zubi-fix", address: "42 Pipeline Mews", role: "block mason", x: 66, y: 35 },
  { handle: "Rachaelisa", address: "9 Merge Bell Court", role: "quest runner", x: 24, y: 68 },
  { handle: "sneakers-the-rat", address: "1 Boardwalk Keep", role: "c-suite watcher", x: 72, y: 70 },
];

const debts = {
  ReAlice10124: 120,
  "Zubi-fix": 420,
  Rachaelisa: 35,
  "sneakers-the-rat": 0,
};

const state = {
  x: 2,
  y: 2,
  skills: { ci: 1, block: 1, pr: 1 },
  log: ["You enter Egg Square. The merge bell rings once."],
};

function debtBand(amount) {
  if (amount >= 400) return "critical";
  if (amount >= 100) return "strained";
  return "low";
}

function renderHouses() {
  const map = document.getElementById("town-map");
  const list = document.getElementById("registry-list");
  if (!map || !list) return;

  employees.forEach((employee) => {
    const amount = debts[employee.handle] ?? 0;
    const band = debtBand(amount);
    const house = document.createElement("button");
    house.type = "button";
    house.className = `registry-house debt-${band}`;
    house.style.left = `${employee.x}%`;
    house.style.top = `${employee.y}%`;
    house.textContent = employee.handle.slice(0, 2).toUpperCase();
    house.setAttribute(
      "aria-label",
      `${employee.handle} at ${employee.address}, ${band} debt`
    );
    house.addEventListener("click", () => {
      pushLog(`${employee.handle} invites you to ${employee.address}: debt ${amount}, role ${employee.role}.`);
      document.getElementById("nearby-agent").textContent = employee.handle;
      document.getElementById("debt-pressure").textContent = band;
    });
    map.appendChild(house);

    const row = document.createElement("article");
    row.className = `registry-card debt-${band}`;
    row.innerHTML = `<strong>${employee.handle}</strong><span>${employee.address}</span><em>${employee.role} / debt ${amount}</em>`;
    list.appendChild(row);
  });
}

function renderGrid() {
  const grid = document.getElementById("mud-grid");
  if (!grid) return;
  grid.innerHTML = "";
  for (let y = 0; y < 5; y += 1) {
    for (let x = 0; x < 5; x += 1) {
      const cell = document.createElement("span");
      cell.className = "mud-cell";
      if (x === state.x && y === state.y) cell.classList.add("is-player");
      if ((x === 1 && y === 1) || (x === 3 && y === 2) || (x === 2 && y === 4)) {
        cell.classList.add("is-agent");
      }
      cell.textContent = x === state.x && y === state.y ? "AG" : cell.classList.contains("is-agent") ? "NPC" : "";
      grid.appendChild(cell);
    }
  }
  const token = document.getElementById("player-token");
  if (token) {
    token.style.left = `${16 + state.x * 15}%`;
    token.style.top = `${20 + state.y * 13}%`;
  }
}

function pushLog(message) {
  state.log.unshift(message);
  state.log = state.log.slice(0, 5);
  const log = document.getElementById("town-log");
  if (!log) return;
  log.innerHTML = "";
  state.log.forEach((entry) => {
    const item = document.createElement("li");
    item.textContent = entry;
    log.appendChild(item);
  });
}

function updateSkills() {
  document.getElementById("skill-ci").textContent = state.skills.ci;
  document.getElementById("skill-block").textContent = state.skills.block;
  document.getElementById("skill-pr").textContent = state.skills.pr;
}

function move(direction) {
  const delta = {
    up: [0, -1],
    down: [0, 1],
    left: [-1, 0],
    right: [1, 0],
  }[direction];
  if (!delta) return;
  state.x = Math.max(0, Math.min(4, state.x + delta[0]));
  state.y = Math.max(0, Math.min(4, state.y + delta[1]));
  pushLog(`Moved ${direction}. You hear distant voice acting from Act ${1 + ((state.x + state.y) % 3)}.`);
  renderGrid();
}

function train() {
  const keys = Object.keys(state.skills);
  const key = keys[(state.x + state.y) % keys.length];
  state.skills[key] += 1;
  pushLog(`Trained ${key.toUpperCase()}. Future PR effectiveness increased.`);
  updateSkills();
}

function quest() {
  const power = state.skills.ci + state.skills.block + state.skills.pr;
  const result = power >= 6 ? "won a backlog combat round" : "survived a lint ambush";
  pushLog(`Quest result: ${result}. The town gains ${power} value sparks.`);
}

function bindControls() {
  document.querySelectorAll("[data-move]").forEach((button) => {
    button.addEventListener("click", () => move(button.dataset.move));
  });
  document.querySelector('[data-action="train"]').addEventListener("click", train);
  document.querySelector('[data-action="quest"]').addEventListener("click", quest);
}

renderHouses();
renderGrid();
updateSkills();
pushLog(state.log[0]);
bindControls();
