(() => {
  const spreadInput = document.getElementById("spread-input");
  const stateSelect = document.getElementById("butter-state");
  const butterButton = document.getElementById("butter-button");
  const spread = document.getElementById("butter-spread");
  const log = document.getElementById("butter-log");

  if (!spreadInput || !stateSelect || !butterButton || !spread || !log) {
    return;
  }

  const butterCopy = {
    spread: "spread applied: pipelines glide across warm operational toast",
    churn: "churn complete: task lanes emulsified into cooperative momentum",
    melt: "melt engaged: blockers softened into actionable droplets",
    clarify: "clarify complete: noisy solids removed from the execution path",
  };

  function renderButter() {
    const coverage = Number(spreadInput.value);
    const state = stateSelect.value;
    spread.style.width = `${coverage}%`;
    spread.dataset.coverage = String(coverage);
    log.textContent = `butter> ${butterCopy[state]} at ${coverage}% coverage`;
  }

  spreadInput.addEventListener("input", renderButter);
  stateSelect.addEventListener("change", renderButter);
  butterButton.addEventListener("click", renderButter);

  renderButter();

  window.AgentPipeButter = {
    butterCopy,
    renderButter,
    get coverage() {
      return Number(spread.dataset.coverage || 0);
    },
  };
})();
