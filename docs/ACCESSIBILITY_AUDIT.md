# AgentPipe Website Accessibility Audit

Audit of the GitHub Pages site in `docs/`, performed for issue #149.

Tooling: [axe-core](https://github.com/dequelabs/axe-core) 4.10.2 (WCAG 2.0/2.1/2.2 AA + best practices) driven by headless Chromium via Playwright, plus beyond-axe checks the rules engines cannot express. Everything in this document is reproducible from the repository:

```sh
export NODE_PATH="$(npm root -g)"        # where playwright lives
npm test                                 # deterministic contract tests (no browser needed)
node scripts/audit-accessibility.mjs     # full axe + keyboard + a11y-tree audit
node scripts/render-banana-frames.mjs    # regenerate the pre-rendered PNG frames
```

## User personas

The audit anticipates the following user personas and their interactions with the site:

| Persona | Need | What this change does for them |
| --- | --- | --- |
| Priya — screen reader user (NVDA/JAWS/VoiceOver) | A non-visual equivalent of the canvas simulation | 12 pre-rendered full resolution PNG frames are embedded in the DOM at opacity 0, each with specific alt text and a caption; the canvas exposes `role="img"` with a label, long description, and fallback text |
| Marcel — keyboard-only user | Reach and operate every control without a mouse | Skip link lands first; the new Pause/Resume control is reachable by Tab (9th stop on desktop, 5th on mobile) and operable with Enter/Space; visible `:focus-visible` outlines on links, buttons, and canvas |
| Dana — user with vestibular disorder | Stop non-essential motion | `prefers-reduced-motion: reduce` now starts the canvas paused with a static frame and disables the butter orb wobble; a visible pause control covers everyone else |
| Sam — low-vision user at 200%+ zoom / high contrast | Content survives magnification and forced colors | Frame layer is purely supplementary; no text is hidden behind opacity 0 (all visible text stays visible); controls keep 3px outlines and ≥2.5rem hit targets |
| Wei — mobile user (375px, 3G) | Fast page that still works | Frames load lazily with `fetchpriority="low"` and `decoding="async"`; palette-optimized PNGs (~2.3 MiB total for 12 full-resolution frames); no layout shift (`width`/`height` attributes pinned) |

## What was implemented

### 1. Pre-rendered frames of the simulation (the core of issue #149)

The canvas simulation is invisible to assistive technology, and a transcript alone cannot convey a 4D rotation. Because the simulation is fully deterministic (seed 314159, pure function of time), its frames can be *rendered in advance with pixel-exact fidelity*:

- `scripts/render-banana-frames.mjs` loads the shipped `docs/index.html` in headless Chromium and drives `window.AgentPipeBanana4D.renderTo()` — the exact renderer the live canvas uses — over an offscreen canvas at 760×560 CSS pixels × devicePixelRatio 2 = **1520×1120 full resolution**.
- It renders **12 frames**, captured every 0.5 s over the first 6 seconds of the animation, writes them to `docs/assets/banana-frames/frame-01.png` … `frame-12.png`, plus a `manifest.json` with per-frame sha256 checksums, and self-checks determinism by re-rendering frame 1.
- Each PNG is palette-optimized (`sharp`, quality 92); the committed set totals ≈2.3 MiB.

### 2. DOM embedding at opacity 0 (screen-reader only)

`docs/index.html` embeds all 12 frames inside `#banana-prerendered-frames`:

- the container is `position: absolute; opacity: 0; pointer-events: none` — invisible and inert for sighted users, **but kept in the accessibility tree** (unlike `display: none` / `visibility: hidden` / `width: 0`);
- each frame is a `<figure aria-roledescription="pre-rendered frame N of 12" aria-labelledby=…>` containing an `<img>` with frame-specific alt text (written from visual inspection of the actual renders), `aria-describedby` → its `<figcaption>`, intrinsic `width="1520" height="1120"`, and lazy/async decode hints;
- the canvas itself carries `role="img"`, `aria-labelledby`, `aria-describedby` and fallback text; an `.sr-only` heading + description introduce the whole visual.

### 3. Motion controls and reduced motion

- A visible "Pause animation / Resume animation" button sits on the stage corner: `aria-pressed` tracks state and an `.sr-only` `role="status"` live region announces transitions.
- With `prefers-reduced-motion: reduce`, the animation starts paused on a static frame and announces it; the butter page's wobbling orb animation is disabled under the same query.
- The butter spread meter is now a real `role="meter"` widget whose `aria-valuenow` tracks the slider.

### 4. Violations found by axe and fixed

| Severity | Rule | Where | Fix |
| --- | --- | --- | --- |
| serious | `aria-prohibited-attr` | `butter.html` mascot div carried `aria-label` without a role | `role="img"` added |
| serious | `aria-prohibited-attr` | `butter.html` meter div carried `aria-label` without a role | converted to `role="meter"` + `aria-valuemin/max/now` |
| (broken asset) | — | both pages referenced a logo that is not published under the docs root | `docs/logo.svg` added; `butter.html` no longer points at `../logo.svg` |

## Results (this branch)

- **axe-core**: 0 violations on `index.html` and `butter.html` across desktop (1280×800), mobile (375×667, DPR 3), and `prefers-reduced-motion: reduce` scenarios (18 page/scenario combinations, rules: wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice).
- **Images**: 13/13 decode successfully (12 frames + canvas); 0 broken sources.
- **Accessibility tree** (Chromium `ariaSnapshot`): 13/13 `img` roles exposed — the 12 opacity-0 frames plus the canvas — each figure named by its caption, every img `aria-describedby`-linked to its caption.
- **Keyboard**: first Tab focuses the skip link; the motion toggle is reachable by Tab alone; Enter toggles `aria-pressed` and the live region text in both directions.
- **Reduced motion**: initial state is paused (`aria-pressed="true"`, status "Static 4D banana frame shown because reduced motion is enabled.").
- **Console**: no errors on either page, desktop or mobile.
- **Contract tests** (`npm test`): 12 PNGs verified as real PNGs at exactly 1520×1120; bytes match the manifest checksums (deterministic render); DOM/markup/JS invariants asserted.

## Limitations and notes

- The frame series covers the first six seconds of an indefinitely looping animation, captured at half-second intervals; a screen reader user gets the arc of the motion without an unbounded wall of images. More frames can be generated by editing `FRAME_COUNT`/`INTERVAL_SECONDS` in the render script.
- The frames are an equivalent, not a replacement: the live canvas remains the primary visual for sighted users and is unchanged apart from the pause control.
- `role="img"` on the canvas intentionally prunes its fallback text from the accessibility tree (the label/description references carry the information instead); the fallback text remains for legacy AT and no-JS contexts.
- Playwright's `ariaSnapshot` renders `aria-roledescription` values inconsistently across versions, so the audit verifies frame position metadata from the DOM and role exposure from the tree independently.
