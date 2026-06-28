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
  const PIECES_PER_PLAYER = 16;
  const TOTAL_CHESS_PIECES = PLAYER_COUNT * PIECES_PER_PLAYER;
  const MUSIC_BPM = 96;

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
  let musicSource = null;
  let musicBuffer = null;
  let gain = null;
  let panner = null;
  let audioFrame = 0;
  let playing = false;

  function midiToFrequency(note) {
    return 440 * 2 ** ((note - 69) / 12);
  }

  function noteEnvelope(timeIntoNote, noteLength) {
    const attack = Math.min(0.025, noteLength * 0.18);
    const release = Math.min(0.12, noteLength * 0.28);
    if (timeIntoNote < attack) {
      return timeIntoNote / attack;
    }
    if (timeIntoNote > noteLength - release) {
      return Math.max(0, (noteLength - timeIntoNote) / release);
    }
    return 0.86;
  }

  function buildBananaMusicBuffer(context) {
    const sampleRate = context.sampleRate;
    const duration = 12;
    const frameCount = Math.floor(sampleRate * duration);
    const buffer = context.createBuffer(2, frameCount, sampleRate);
    const left = buffer.getChannelData(0);
    const right = buffer.getChannelData(1);
    const beatLength = 60 / MUSIC_BPM;
    const melody = [64, 67, 71, 72, 71, 67, 64, 60, 62, 65, 69, 74, 72, 69, 65, 62];
    const bass = [40, 40, 47, 47, 45, 45, 43, 43];
    const chord = [52, 55, 59, 64];

    for (let frame = 0; frame < frameCount; frame += 1) {
      const time = frame / sampleRate;
      const beat = Math.floor(time / beatLength);
      const beatTime = time % beatLength;
      const barPhase = (time % (beatLength * 8)) / (beatLength * 8);
      const melodyFrequency = midiToFrequency(melody[beat % melody.length]);
      const bassFrequency = midiToFrequency(bass[Math.floor(beat / 2) % bass.length]);
      const chordFrequency = midiToFrequency(chord[(beat + Math.floor(time * 2)) % chord.length]);
      const envelope = noteEnvelope(beatTime, beatLength);
      const swing = 0.74 + Math.sin(barPhase * TAU) * 0.16;
      const melodySample =
        Math.sin(time * TAU * melodyFrequency) * 0.55 +
        Math.sin(time * TAU * melodyFrequency * 2) * 0.14;
      const chordSample = Math.sin(time * TAU * chordFrequency) * 0.18;
      const bassSample = Math.sin(time * TAU * bassFrequency) * 0.28;
      const tick = beatTime < 0.025 ? (1 - beatTime / 0.025) * 0.08 : 0;
      const sample = Math.tanh((melodySample * envelope + chordSample + bassSample + tick) * 0.72);

      left[frame] = sample * (0.78 - swing * 0.12);
      right[frame] = sample * (0.62 + swing * 0.18);
    }

    return buffer;
  }

  function stopAudio() {
    playing = false;
    if (musicSource) {
      musicSource.stop();
      musicSource.disconnect();
      musicSource = null;
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
    if (!playing || !audioContext || !gain || !panner || !musicSource) {
      return;
    }
    const time = audioContext.currentTime;
    const hrtfVector = parseVector(hrtfInput?.value || "");
    const projected = project8d(rotate8d(bananaMotif(time, hrtfVector), time));
    panner.pan.setTargetAtTime(projected.x, time, 0.025);
    gain.gain.setTargetAtTime(0.18 + Math.max(0, projected.depth) * 0.04, time, 0.03);
    musicSource.playbackRate.setTargetAtTime(0.94 + (projected.y + 1) * 0.045, time, 0.04);
    if (audioReadout) {
      audioReadout.textContent = `playing banana music · pan ${projected.x.toFixed(2)} · rate ${musicSource.playbackRate.value.toFixed(2)}x`;
    }
    audioFrame = requestAnimationFrame(updateAudio);
  }

  async function startAudio() {
    audioContext = audioContext || new AudioContext();
    await audioContext.resume();
    musicBuffer = musicBuffer || buildBananaMusicBuffer(audioContext);
    musicSource = audioContext.createBufferSource();
    gain = audioContext.createGain();
    panner = audioContext.createStereoPanner();
    musicSource.buffer = musicBuffer;
    musicSource.loop = true;
    gain.gain.value = 0.16;
    musicSource.connect(gain);
    gain.connect(panner);
    panner.connect(audioContext.destination);
    musicSource.start();
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

  function create8DChessPieces() {
    const backRank = ["R", "N", "B", "Q", "K", "B", "N", "R"];
    const allPieces = [];

    for (let playerIndex = 0; playerIndex < PLAYER_COUNT; playerIndex += 1) {
      const player = playerIndex + 1;
      const forwardAxis = playerIndex;
      const fileAxis = (playerIndex + 1) % 8;
      const homeRank = playerIndex % 2 === 0 ? 0 : BOARD_SIZE - 1;
      const pawnRank = playerIndex % 2 === 0 ? 1 : BOARD_SIZE - 2;

      backRank.forEach((piece, file) => {
        const vector = Array.from({ length: 8 }, (_, axis) => playerIndex);
        vector[forwardAxis] = homeRank;
        vector[fileAxis] = file;
        allPieces.push({ player, piece, vector });
      });

      for (let file = 0; file < BOARD_SIZE; file += 1) {
        const vector = Array.from({ length: 8 }, (_, axis) => playerIndex);
        vector[forwardAxis] = pawnRank;
        vector[fileAxis] = file;
        allPieces.push({ player, piece: "P", vector });
      }
    }

    return allPieces;
  }

  const pieces = create8DChessPieces();

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

    const stacks = new Map();
    pieces.forEach((piece, index) => {
      const cellIndex = cellIndexForVector(piece.vector);
      const stack = stacks.get(cellIndex) || [];
      stack.push({ ...piece, index });
      stacks.set(cellIndex, stack);
    });

    stacks.forEach((stack, cellIndex) => {
      const cell = cells[cellIndex];
      const activePiece = stack.find((piece) => piece.index === activeMove);
      const displayPiece = activePiece || stack[0];
      cell.classList.add(activePiece ? "active" : "player");
      cell.textContent = stack.length > 1
        ? `${displayPiece.piece}${displayPiece.player}+${stack.length - 1}`
        : `${displayPiece.piece}${displayPiece.player}`;
      cell.title = stack
        .map((piece) => `Player ${piece.player} ${piece.piece}: ${vectorNotation(piece.vector)}`)
        .join("\n");
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
    buildBananaMusicBuffer,
    create8DChessPieces,
    cellIndexForVector,
    TOTAL_CHESS_PIECES,
    pieces,
  };
})();
