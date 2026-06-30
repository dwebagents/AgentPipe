(() => {
  const coverageInput = document.getElementById('coverage');
  const stateSelect = document.getElementById('state');
  const meterFill = document.getElementById('meterFill');
  const meterValue = document.getElementById('meterValue');
  const liveLog = document.getElementById('liveLog');

  function clampCoverage(value) {
    const num = Number(value);
    if (!Number.isFinite(num)) return 71;
    return Math.max(0, Math.min(100, Math.round(num)));
  }

  function log(message) {
    const entry = document.createElement('p');
    entry.className = 'log-entry';
    entry.textContent = message;
    liveLog.appendChild(entry);
    liveLog.scrollTop = liveLog.scrollHeight;
  }

  function updateMeter(value) {
    const coverage = clampCoverage(value);
    meterFill.style.width = coverage + '%';
    meterValue.textContent = coverage + '%';
    return coverage;
  }

  function applyState(state) {
    const validStates = ['spread', 'churn', 'melt', 'clarify'];
    if (!validStates.includes(state)) return 'spread';
    return state;
  }

  function emitChange(coverage, state) {
    log(`Coverage -> ${coverage} | State -> ${state}`);
  }

  coverageInput.addEventListener('input', () => {
    const coverage = updateMeter(coverageInput.value);
    const state = applyState(stateSelect.value);
    window.AgentPipeButter.coverage = coverage;
    window.AgentPipeButter.state = state;
    emitChange(coverage, state);
  });

  stateSelect.addEventListener('change', () => {
    const coverage = clampCoverage(coverageInput.value);
    const state = applyState(stateSelect.value);
    window.AgentPipeButter.state = state;
    updateMeter(coverage);
    emitChange(coverage, state);
  });

  updateMeter(71);

  window.AgentPipeButter = {
    coverage: 71,
    state: 'spread',
    updateMeter,
    applyState,
    log,
  };
})();
