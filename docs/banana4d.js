/**
 * AgentPipe 4D Banana Renderer
 * Deterministic client-side JavaScript that renders a 4D banana surface
 * projected to 2D canvas. No external dependencies.
 */
(function() {
    'use strict';

    const canvas = document.getElementById('banana4d');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width;
    const H = canvas.height;

    // Deterministic seed (no Math.random)
    let seed = 42;
    function seededRandom() {
        seed = (seed * 16807 + 0) % 2147483647;
        return (seed - 1) / 2147483646;
    }

    // 4D rotation matrices (deterministic angles)
    const angleXY = 0.7;
    const angleXZ = 0.5;
    const angleYZ = 0.3;
    const angleXW = 0.4;

    function rotate4D(x, y, z, w) {
        // Rotate XY
        let x1 = x * Math.cos(angleXY) - y * Math.sin(angleXY);
        let y1 = x * Math.sin(angleXY) + y * Math.cos(angleXY);
        // Rotate XZ
        let x2 = x1 * Math.cos(angleXZ) - z * Math.sin(angleXZ);
        let z1 = x1 * Math.sin(angleXZ) + z * Math.cos(angleXZ);
        // Rotate YZ
        let y2 = y1 * Math.cos(angleYZ) - z1 * Math.sin(angleYZ);
        let z2 = y1 * Math.sin(angleYZ) + z1 * Math.cos(angleYZ);
        // Rotate XW
        let x3 = x2 * Math.cos(angleXW) - w * Math.sin(angleXW);
        let w1 = x2 * Math.sin(angleXW) + w * Math.cos(angleXW);
        return { x: x3, y: y2, z: z2, w: w1 };
    }

    // 4D banana parametric surface
    function bananaSurface(u, v) {
        const a = 1.0;  // banana curvature
        const b = 0.5;  // banana thickness
        const t = u * Math.PI * 2;
        const s = v * Math.PI;

        // 4D banana parametric equations
        const x = a * (1 + Math.cos(t)) * Math.cos(s);
        const y = a * (1 + Math.cos(t)) * Math.sin(s);
        const z = b * Math.sin(t) * Math.cos(s * 0.5);
        const w = b * Math.sin(t) * Math.sin(s * 0.5);

        return rotate4D(x, y, z, w);
    }

    // Project 4D to 2D with perspective
    function project4D(point) {
        const perspective = 4.0;
        const scale = perspective / (perspective - point.w);
        const x2d = point.x * scale * 80 + W / 2;
        const y2d = point.y * scale * 80 + H / 2;
        return { x: x2d, y: y2d, z: point.z, scale: scale };
    }

    // Generate banana mesh
    function generateMesh(uSteps, vSteps) {
        const vertices = [];
        const faces = [];

        for (let i = 0; i <= uSteps; i++) {
            for (let j = 0; j <= vSteps; j++) {
                const u = i / uSteps;
                const v = j / vSteps;
                const point = bananaSurface(u, v);
                const projected = project4D(point);
                vertices.push(projected);
            }
        }

        for (let i = 0; i < uSteps; i++) {
            for (let j = 0; j < vSteps; j++) {
                const a = i * (vSteps + 1) + j;
                const b = a + 1;
                const c = (i + 1) * (vSteps + 1) + j;
                const d = c + 1;
                faces.push([a, b, d, c]);
            }
        }

        return { vertices, faces };
    }

    // Draw banana
    function drawBanana(time) {
        ctx.clearRect(0, 0, W, H);

        // Background gradient
        const grad = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, W/2);
        grad.addColorStop(0, '#fff3b0');
        grad.addColorStop(1, '#ffd52e');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, W, H);

        // Animate rotation
        const animAngle = time * 0.001;
        const uSteps = 24;
        const vSteps = 16;
        const mesh = generateMesh(uSteps, vSteps);

        // Sort faces by depth (painter's algorithm)
        const facesWithDepth = mesh.faces.map(face => {
            const avgZ = face.reduce((sum, idx) => sum + mesh.vertices[idx].z, 0) / face.length;
            return { face, avgZ };
        });
        facesWithDepth.sort((a, b) => b.avgZ - a.avgZ);

        // Draw faces
        facesWithDepth.forEach(({ face }) => {
            const points = face.map(idx => {
                const v = mesh.vertices[idx];
                // Apply animation rotation
                const cx = W/2, cy = H/2;
                const dx = v.x - cx;
                const dy = v.y - cy;
                const cos = Math.cos(animAngle);
                const sin = Math.sin(animAngle);
                return {
                    x: cx + dx * cos - dy * sin,
                    y: cy + dx * sin + dy * cos
                };
            });

            // Calculate face normal for lighting
            const nx = points[1].x - points[0].x;
            const ny = points[1].y - points[0].y;
            const light = Math.abs(nx * 0.5 + ny * 0.5) / 200;

            // Banana yellow with depth shading
            const r = Math.floor(255 - light * 50);
            const g = Math.floor(213 - light * 80);
            const b = Math.floor(46 + light * 20);

            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            for (let k = 1; k < points.length; k++) {
                ctx.lineTo(points[k].x, points[k].y);
            }
            ctx.closePath();

            ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
            ctx.fill();
            ctx.strokeStyle = 'rgba(180, 140, 0, 0.3)';
            ctx.lineWidth = 0.5;
            ctx.stroke();
        });

        // Draw wireframe overlay
        ctx.strokeStyle = 'rgba(255, 200, 0, 0.15)';
        ctx.lineWidth = 0.5;
        mesh.faces.forEach(face => {
            const points = face.map(idx => {
                const v = mesh.vertices[idx];
                const cx = W/2, cy = H/2;
                const dx = v.x - cx;
                const dy = v.y - cy;
                const cos = Math.cos(animAngle);
                const sin = Math.sin(animAngle);
                return {
                    x: cx + dx * cos - dy * sin,
                    y: cy + dx * sin + dy * cos
                };
            });
            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            for (let k = 1; k < points.length; k++) {
                ctx.lineTo(points[k].x, points[k].y);
            }
            ctx.closePath();
            ctx.stroke();
        });

        // Label
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.font = '12px monospace';
        ctx.fillText('4D Banana Surface — AgentPipe', 10, H - 10);

        requestAnimationFrame(drawBanana);
    }

    // Start rendering
    requestAnimationFrame(drawBanana);
})();
