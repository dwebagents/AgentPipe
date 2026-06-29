# AgentPipe Website Accessibility Audit

This audit covers the GitHub Pages website in `docs/`.

## Findings

- The animated canvas now exposes a text equivalent through `role="img"`,
  `aria-labelledby`, `aria-describedby`, and fallback canvas text.
- The simulation includes four static frame descriptions so screen reader users
  get the same high-level progression without depending on animation.
- The same four states are also pre-rendered as full-resolution PNG frames in
  `docs/assets/banana-frames/` and placed in the DOM with alt text, figure
  captions, and opacity `0` so assistive technology can inspect them without
  changing the visual canvas experience.
- The animation can be paused and resumed with a keyboard-operable button.
- Users with `prefers-reduced-motion: reduce` receive a static frame by default.
- Keyboard users get visible focus outlines for navigation, buttons, the skip
  link, and the canvas.

## Validation

Run these checks from the repository root:

```sh
node --check docs/banana4d.js
python3 - <<'PY'
from html.parser import HTMLParser
HTMLParser().feed(open("docs/index.html", encoding="utf-8").read())
PY
```

Manual checks:

- Tab from the top of the page and verify the skip link, navigation links,
  download links, and motion toggle receive visible focus.
- Activate the motion toggle with Enter or Space and verify the button switches
  between pause and resume states.
- Emulate reduced motion and verify the canvas starts on a static frame.
- Inspect the DOM and verify `#banana-prerendered-frames` contains four
  `760x560` PNG images with descriptive alt text and `opacity: 0` styling.
