(() => {
  const audioToggle = document.getElementById("audio8d-toggle");
  const audioReadout = document.getElementById("audio8d-readout");
  const hrtfInput = document.getElementById("hrtf-input");
  const board = document.getElementById("chess8d-board");
  const chessReadout = document.getElementById("chess8d-readout");
  const prevButton = document.getElementById("chess8d-prev");
  const nextButton = document.getElementById("chess8d-next");

  const TAU = Math.PI * 2;
  const BOARD_SIZE = 8;
  const PLAYER_COUNT = 8;

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function parseVector(value) {
    const parsed = String(value)
      .split(/[,\s]+/)
      .map((part) => Number(part.trim()))
      .filter((part) => Number.isFinite(part))
      .slice(0, 8);

    while (parsed.length < 8) {
      parsed.push(0);
    }

    return parsed.map((part) => clamp(part, -1.5, 1.5));
  }

  function rotate8d(vector, time) {
    const next = vector.slice(0, 8);
    for (let axis = 0; axis < 8; axis += 2) {
      const angle = time * (0.17 + axis * 0.025) + axis * 0.19;
      const a = next[axis];
      const b = next[axis + 1];
      next[axis] = a * Math.cos(angle) - b * Math.sin(angle);
      next[axis + 1] = a * Math.sin(angle) + b * Math.cos(angle);
    }
    return next;
  }

  function project8d(vector) {
    const weightsX = [1, 0.72, -0.48, 0.31, -0.2, 0.14, -0.1, 0.07];
    const weightsY = [0.18, -0.42, 0.96, 0.54, -0.36, 0.22, 0.11, -0.08];
    const x = vector.reduce((total, value, index) => total + value * weightsX[index], 0);
    const y = vector.reduce((total, value, index) => total + value * weightsY[index], 0);
    const depth = vector.reduce((total, value, index) => total + value * (index + 1), 0) / 18;
    return { x: clamp(x / 2.4, -1, 1), y: clamp(y / 2.4, -1, 1), depth };
  }

  function bananaMotif(time, hrtfVector) {
    const base = [1, 0.75, 0.45, 0.18, -0.18, -0.45, -0.75, -1];
    return base.map((value, index) => {
      const wobble = Math.sin(time * (0.8 + index * 0.07) + index) * 0.35;
      return value + wobble + hrtfVector[index] * 0.22;
    });
  }

  let audioContext = null;
  let oscillator = null;
  let gain = null;
  let panner = null;
  let audioFrame = 0;
  let playing = false;

  function stopAudio() {
    playing = false;
    if (oscillator) {
      oscillator.stop();
      oscillator.disconnect();
      oscillator = null;
    }
    if (gain) {
      gain.disconnect();
      gain = null;
    }
    if (panner) {
      panner.disconnect();
      panner = null;
    }
    if (audioToggle) {
      audioToggle.textContent = "Start 8D banana audio";
    }
    if (audioReadout) {
      audioReadout.textContent = "audio idle";
    }
    cancelAnimationFrame(audioFrame);
  }

  function updateAudio() {
    if (!playing || !audioContext || !gain || !panner) {
      return;
    }
    const time = audioContext.currentTime;
    const hrtfVector = parseVector(hrtfInput?.value || "");
    const projected = project8d(rotate8d(bananaMotif(time, hrtfVector), time));
    panner.pan.setTargetAtTime(projected.x, time, 0.025);
    gain.gain.setTargetAtTime(0.18 + Math.max(0, projected.depth) * 0.04, time, 0.03);
    if (oscillator) {
      oscillator.frequency.setTargetAtTime(220 + (projected.y + 1) * 110, time, 0.04);
    }
    if (audioReadout) {
      audioReadout.textContent = `pan ${projected.x.toFixed(2)} · pitch ${(220 + (projected.y + 1) * 110).toFixed(0)} Hz`;
    }
    audioFrame = requestAnimationFrame(updateAudio);
  }

  async function startAudio() {
    audioContext = audioContext || new AudioContext();
    await audioContext.resume();
    oscillator = audioContext.createOscillator();
    gain = audioContext.createGain();
    panner = audioContext.createStereoPanner();
    oscillator.type = "triangle";
    gain.gain.value = 0.16;
    oscillator.connect(gain);
    gain.connect(panner);
    panner.connect(audioContext.destination);
    oscillator.start();
    playing = true;
    if (audioToggle) {
      audioToggle.textContent = "Stop 8D banana audio";
    }
    updateAudio();
  }

  audioToggle?.addEventListener("click", async () => {
    if (playing) {
      stopAudio();
      return;
    }
    try {
      await startAudio();
    } catch (error) {
      if (audioReadout) {
        audioReadout.textContent = `audio unavailable: ${error.message}`;
      }
    }
  });

  const pieces = [
    { player: 1, piece: "K", vector: [0, 0, 0, 0, 0, 0, 0, 0] },
    { player: 2, piece: "Q", vector: [7, 7, 7, 7, 7, 7, 7, 7] },
    { player: 3, piece: "R", vector: [0, 7, 0, 7, 0, 7, 0, 7] },
    { player: 4, piece: "B", vector: [7, 0, 7, 0, 7, 0, 7, 0] },
    { player: 5, piece: "N", vector: [2, 5, 3, 6, 1, 4, 0, 7] },
    { player: 6, piece: "P", vector: [5, 2, 6, 3, 4, 1, 7, 0] },
    { player: 7, piece: "Ω", vector: [1, 6, 2, 5, 3, 4, 7, 0] },
    { player: 8, piece: "♙", vector: [6, 1, 5, 2, 4, 3, 0, 7] },
  ];

  function normalizeBoardVector(vector) {
    return vector.map((value) => (value / (BOARD_SIZE - 1)) * 2 - 1);
  }

  function cellIndexForVector(vector) {
    const projected = project8d(normalizeBoardVector(vector));
    const x = clamp(Math.round(((projected.x + 1) / 2) * (BOARD_SIZE - 1)), 0, BOARD_SIZE - 1);
    const y = clamp(Math.round(((projected.y + 1) / 2) * (BOARD_SIZE - 1)), 0, BOARD_SIZE - 1);
    return y * BOARD_SIZE + x;
  }

  function vectorNotation(vector) {
    return vector.map((value, index) => `${String.fromCharCode(97 + index)}${value + 1}`).join(" ");
  }

  let activeMove = 0;

  function renderChess() {
    if (!board) {
      return;
    }
    board.innerHTML = "";
    const cells = Array.from({ length: BOARD_SIZE * BOARD_SIZE }, (_, index) => {
      const cell = document.createElement("span");
      cell.className = "chess8d-cell";
      cell.textContent = index % 9 === 0 ? "8D" : "";
      board.appendChild(cell);
      return cell;
    });

    pieces.forEach((piece, index) => {
      const cell = cells[cellIndexForVector(piece.vector)];
      cell.classList.add(index === activeMove ? "active" : "player");
      cell.textContent = `${piece.piece}${piece.player}`;
      cell.title = `Player ${piece.player}: ${vectorNotation(piece.vector)}`;
    });

    const active = pieces[activeMove];
    if (chessReadout) {
      chessReadout.textContent = `vector ${activeMove + 1} of ${pieces.length}: P${active.player} ${active.piece} · ${vectorNotation(active.vector)}`;
    }
  }

  prevButton?.addEventListener("click", () => {
    activeMove = (activeMove + pieces.length - 1) % pieces.length;
    renderChess();
  });

  nextButton?.addEventListener("click", () => {
    activeMove = (activeMove + 1) % pieces.length;
    renderChess();
  });

  renderChess();

  window.AgentPipe8D = {
    parseVector,
    rotate8d,
    project8d,
    cellIndexForVector,
    pieces,
  };
})();
