const canvas = document.querySelector("#banana-canvas");
const context = canvas.getContext("2d");
const statusNode = document.querySelector("#render-status");

const SEED = 271828;
const DPR_LIMIT = 2;
const POINT_COUNT_U = 72;
const POINT_COUNT_V = 18;

let width = 0;
let height = 0;
let pointerX = 0;
let pointerY = 0;
let pointerActive = false;

function seededNoise(index) {
  const value = Math.sin(index * 12.9898 + SEED * 78.233) * 43758.5453;
  return value - Math.floor(value);
}

function bananaPoint(uIndex, vIndex) {
  const u = (uIndex / (POINT_COUNT_U - 1)) * Math.PI * 1.04;
  const v = (vIndex / POINT_COUNT_V) * Math.PI * 2;
  const taper = Math.sin(u);
  const radius = 0.34 * taper + 0.045;
  const arc = u - Math.PI / 2;
  const bend = 1.52;
  const surfaceNoise = (seededNoise(uIndex * 97 + vIndex * 31) - 0.5) * 0.035;

  const x = Math.cos(arc) * bend + Math.cos(v) * (radius + surfaceNoise);
  const y = Math.sin(v) * radius * 0.78 + Math.sin(u * 2.2) * 0.05;
  const z = Math.sin(arc) * 0.68 + Math.cos(v) * radius * 0.42;
  const w = Math.sin(u * 2.0 + v * 0.7) * 0.52 + Math.cos(u * 1.3) * 0.18;

  return { x, y, z, w, u, v };
}

const bananaCloud = [];
for (let u = 0; u < POINT_COUNT_U; u += 1) {
  for (let v = 0; v < POINT_COUNT_V; v += 1) {
    bananaCloud.push(bananaPoint(u, v));
  }
}

function rotate2d(a, b, angle) {
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  return [a * c - b * s, a * s + b * c];
}

function rotate4d(point, time) {
  const pointerTiltX = pointerActive ? pointerX * 0.7 : 0;
  const pointerTiltY = pointerActive ? pointerY * 0.55 : 0;
  let { x, y, z, w } = point;

  [x, w] = rotate2d(x, w, time * 0.41 + pointerTiltX);
  [y, z] = rotate2d(y, z, time * 0.28 + pointerTiltY);
  [x, z] = rotate2d(x, z, -0.46 + time * 0.18);
  [y, w] = rotate2d(y, w, 0.22 + time * 0.22);

  return { x, y, z, w };
}

function project4Dto2D(point) {
  const wPerspective = 2.7 / (2.7 - point.w * 0.46);
  const zPerspective = 3.8 / (3.8 - point.z * 0.36);
  const scale = Math.min(width, height) * 0.275 * wPerspective * zPerspective;

  return {
    x: width * 0.5 + point.x * scale,
    y: height * 0.54 + point.y * scale,
    depth: point.z + point.w * 0.34,
    scale: wPerspective * zPerspective,
    w: point.w,
  };
}

function resize() {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, DPR_LIMIT);
  width = Math.max(320, Math.floor(rect.width));
  height = Math.max(320, Math.floor(rect.height));
  canvas.width = Math.floor(width * dpr);
  canvas.height = Math.floor(height * dpr);
  context.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function drawStem(x, y, rotation, scale) {
  context.save();
  context.translate(x, y);
  context.rotate(rotation);
  context.scale(scale, scale);
  const stemGradient = context.createLinearGradient(-24, -12, 26, 20);
  stemGradient.addColorStop(0, "#3b2c16");
  stemGradient.addColorStop(0.55, "#8a6b22");
  stemGradient.addColorStop(1, "#cf9f2d");
  context.fillStyle = stemGradient;
  context.beginPath();
  context.moveTo(-34, -8);
  context.bezierCurveTo(-18, -30, 19, -25, 32, -4);
  context.bezierCurveTo(20, 11, -14, 15, -34, -8);
  context.fill();
  context.restore();
}

function renderBackground(time) {
  const sky = context.createLinearGradient(0, 0, width, height);
  sky.addColorStop(0, "#fff7bc");
  sky.addColorStop(0.4, "#f6d44f");
  sky.addColorStop(0.72, "#4f7c58");
  sky.addColorStop(1, "#16130a");
  context.fillStyle = sky;
  context.fillRect(0, 0, width, height);

  context.save();
  context.globalAlpha = 0.24;
  context.strokeStyle = "#fff8c8";
  context.lineWidth = 1;
  for (let ring = 0; ring < 7; ring += 1) {
    context.beginPath();
    const radius = 54 + ring * 38 + Math.sin(time + ring) * 4;
    context.ellipse(width * 0.5, height * 0.54, radius * 1.7, radius * 0.72, -0.18, 0, Math.PI * 2);
    context.stroke();
  }
  context.restore();
}

function renderBanana(timeMs) {
  const time = timeMs * 0.001;
  renderBackground(time);

  const projected = bananaCloud
    .map((point) => {
      const rotated = rotate4d(point, time);
      return {
        source: point,
        projected: project4Dto2D(rotated),
      };
    })
    .sort((a, b) => a.projected.depth - b.projected.depth);

  context.save();
  context.shadowColor = "rgba(52, 35, 0, 0.3)";
  context.shadowBlur = 18;
  context.shadowOffsetY = 12;

  for (const item of projected) {
    const { source, projected: dot } = item;
    const light = Math.max(0, Math.min(1, 0.58 + dot.depth * 0.2 + Math.cos(source.v) * 0.18));
    const alpha = Math.max(0.48, Math.min(0.95, 0.68 + dot.scale * 0.12));
    const radius = Math.max(1.15, 2.75 * dot.scale + Math.sin(source.u * 3) * 0.45);
    const greenEdge = Math.max(0, Math.sin(source.u * Math.PI));
    const hue = 43 + greenEdge * 9 + dot.w * 4;
    const saturation = 85 - Math.abs(dot.w) * 9;
    const luminance = 44 + light * 26;

    context.fillStyle = `hsla(${hue}, ${saturation}%, ${luminance}%, ${alpha})`;
    context.beginPath();
    context.arc(dot.x, dot.y, radius, 0, Math.PI * 2);
    context.fill();
  }

  context.restore();

  const left = projected[0]?.projected;
  const right = projected[projected.length - 1]?.projected;
  if (left && right) {
    drawStem(width * 0.27, height * 0.61, -0.58 + Math.sin(time) * 0.08, 0.72);
    drawStem(width * 0.73, height * 0.41, 2.72 + Math.cos(time) * 0.08, 0.62);
  }

  if (statusNode) {
    statusNode.textContent = `seed ${SEED} · ${bananaCloud.length} deterministic 4D samples`;
  }

  requestAnimationFrame(renderBanana);
}

function setPointer(event) {
  const rect = canvas.getBoundingClientRect();
  pointerX = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
  pointerY = ((event.clientY - rect.top) / rect.height - 0.5) * 2;
  pointerActive = true;
}

canvas.addEventListener("pointermove", setPointer);
canvas.addEventListener("pointerenter", setPointer);
canvas.addEventListener("pointerleave", () => {
  pointerActive = false;
});

window.addEventListener("resize", resize);
resize();
requestAnimationFrame(renderBanana);
