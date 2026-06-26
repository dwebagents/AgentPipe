(() => {
  const canvas = document.getElementById("banana-canvas");
  if (!(canvas instanceof HTMLCanvasElement)) {
    return;
  }

  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return;
  }

  const seed = Number(canvas.dataset.seed || 314159);
  const TAU = Math.PI * 2;
  let width = 0;
  let height = 0;
  let dpr = 1;

  function seeded(index) {
    const x = Math.sin(seed * 0.001 + index * 12.9898) * 43758.5453;
    return x - Math.floor(x);
  }

  const stars = Array.from({ length: 88 }, (_, index) => ({
    x: seeded(index) * 2 - 1,
    y: seeded(index + 101) * 2 - 1,
    z: seeded(index + 202) * 2 - 1,
    size: 0.8 + seeded(index + 303) * 1.8,
  }));

  function resize() {
    const rect = canvas.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = Math.max(320, rect.width);
    height = Math.max(280, rect.height);
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function rotate2(a, b, angle) {
    const s = Math.sin(angle);
    const c = Math.cos(angle);
    return [a * c - b * s, a * s + b * c];
  }

  function bananaPoint(u, v, w) {
    const length = (u - 0.5) * 4.7;
    const taper = Math.sin(Math.PI * u);
    const radius = 0.22 + taper * 0.48;
    const curve = Math.sin((u - 0.1) * Math.PI) * 0.8;
    const twist = v + u * 1.4;
    const x = length;
    const y = curve + Math.cos(twist) * radius * 0.72;
    const z = Math.sin(twist) * radius;
    const q = (w - 0.5) * 1.35 + Math.sin(u * TAU) * 0.25;
    return [x, y, z, q];
  }

  function project(point, time) {
    let [x, y, z, w] = point;
    [x, w] = rotate2(x, w, time * 0.31);
    [z, w] = rotate2(z, w, time * 0.22 + 0.6);
    [x, z] = rotate2(x, z, time * 0.18);
    [y, z] = rotate2(y, z, -0.34);

    const depth4 = 4.9 / (4.9 - w);
    x *= depth4;
    y *= depth4;
    z *= depth4;

    const depth3 = 4.2 / (4.2 - z);
    const scale = Math.min(width, height) * 0.18 * depth3;

    return {
      x: width * 0.5 + x * scale,
      y: height * 0.48 - y * scale,
      z,
      glow: Math.max(0.25, Math.min(1, depth4 * depth3 * 0.7)),
    };
  }

  function drawGrid(time) {
    ctx.save();
    ctx.globalAlpha = 0.28;
    ctx.lineWidth = 1;
    ctx.strokeStyle = "#ffe879";

    for (let ring = 0; ring < 4; ring += 1) {
      const w = ring / 3;
      ctx.beginPath();
      for (let i = 0; i <= 96; i += 1) {
        const a = (i / 96) * TAU;
        const p = project([
          Math.cos(a) * (2.7 + ring * 0.12),
          Math.sin(a) * (1.5 + ring * 0.08),
          Math.sin(a * 2 + ring) * 0.18,
          (w - 0.5) * 2.3,
        ], time);
        if (i === 0) {
          ctx.moveTo(p.x, p.y);
        } else {
          ctx.lineTo(p.x, p.y);
        }
      }
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawAxes(time) {
    const axes = [
      { label: "x", color: "#ffe879", points: [[-3.2, 0, 0, 0], [3.2, 0, 0, 0]] },
      { label: "y", color: "#9be564", points: [[0, -2.1, 0, 0], [0, 2.1, 0, 0]] },
      { label: "w", color: "#ffffff", points: [[0, 0, 0, -2.2], [0, 0, 0, 2.2]] },
    ];

    ctx.save();
    ctx.font = "700 12px Inter, system-ui, sans-serif";
    axes.forEach((axis) => {
      const start = project(axis.points[0], time);
      const end = project(axis.points[1], time);
      ctx.strokeStyle = axis.color;
      ctx.globalAlpha = 0.55;
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(start.x, start.y);
      ctx.lineTo(end.x, end.y);
      ctx.stroke();
      ctx.globalAlpha = 0.9;
      ctx.fillStyle = axis.color;
      ctx.fillText(axis.label, end.x + 8, end.y + 4);
    });
    ctx.restore();
  }

  function drawStars(time) {
    ctx.save();
    stars.forEach((star, index) => {
      const drift = Math.sin(time * 0.2 + index) * 0.04;
      const p = project([star.x * 4, star.y * 2.4, star.z * 2.5, drift], time * 0.25);
      ctx.globalAlpha = 0.15 + star.size * 0.08;
      ctx.fillStyle = "#fff6b5";
      ctx.beginPath();
      ctx.arc(p.x, p.y, star.size, 0, TAU);
      ctx.fill();
    });
    ctx.restore();
  }

  function drawBanana(time) {
    const uSteps = 42;
    const vSteps = 15;
    const wSteps = 5;

    ctx.save();
    ctx.lineCap = "round";

    for (let w = 0; w < wSteps; w += 1) {
      const wNorm = w / (wSteps - 1);
      for (let v = 0; v < vSteps; v += 1) {
        ctx.beginPath();
        for (let u = 0; u <= uSteps; u += 1) {
          const p = project(bananaPoint(u / uSteps, (v / vSteps) * TAU, wNorm), time);
          if (u === 0) {
            ctx.moveTo(p.x, p.y);
          } else {
            ctx.lineTo(p.x, p.y);
          }
        }
        ctx.globalAlpha = 0.14 + wNorm * 0.1;
        ctx.strokeStyle = w === 2 ? "#ffd42a" : "#ffe879";
        ctx.lineWidth = w === 2 ? 2.8 : 1.2;
        ctx.stroke();
      }
    }

    for (let u = 0; u <= uSteps; u += 3) {
      ctx.beginPath();
      for (let v = 0; v <= vSteps; v += 1) {
        const p = project(bananaPoint(u / uSteps, (v / vSteps) * TAU, 0.5), time);
        if (v === 0) {
          ctx.moveTo(p.x, p.y);
        } else {
          ctx.lineTo(p.x, p.y);
        }
      }
      ctx.globalAlpha = 0.32;
      ctx.strokeStyle = "#ffb900";
      ctx.lineWidth = 1.6;
      ctx.stroke();
    }

    ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < 36; i += 1) {
      const u = i / 35;
      const p = project(bananaPoint(u, Math.PI * 0.3, 0.5), time);
      const radius = 6 + p.glow * 10;
      const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius);
      gradient.addColorStop(0, "rgba(255, 246, 181, 0.34)");
      gradient.addColorStop(1, "rgba(255, 212, 42, 0)");
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(p.x, p.y, radius, 0, TAU);
      ctx.fill();
    }

    ctx.restore();
  }

  function draw(timestamp) {
    const time = timestamp * 0.001;
    ctx.clearRect(0, 0, width, height);
    const background = ctx.createRadialGradient(
      width * 0.5,
      height * 0.48,
      0,
      width * 0.5,
      height * 0.48,
      Math.max(width, height) * 0.65,
    );
    background.addColorStop(0, "rgba(255, 212, 42, 0.22)");
    background.addColorStop(0.42, "rgba(255, 212, 42, 0.04)");
    background.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = background;
    ctx.fillRect(0, 0, width, height);

    drawStars(time);
    drawGrid(time);
    drawAxes(time);
    drawBanana(time);

    requestAnimationFrame(draw);
  }

  resize();
  window.addEventListener("resize", resize);
  requestAnimationFrame(draw);
})();
