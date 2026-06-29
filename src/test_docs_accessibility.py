from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class DocsHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.tags = []
        self._stack = []
        self._canvas_text = []

    def handle_starttag(self, tag, attrs):
        attr_map = dict(attrs)
        self.tags.append((tag, attr_map))
        if "id" in attr_map:
            self.ids.add(attr_map["id"])
        self._stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_endtag(self, tag):
        if tag in self._stack:
            self._stack.remove(tag)

    def handle_data(self, data):
        if "canvas" in self._stack:
            self._canvas_text.append(data)


def parse_docs_html():
    parser = DocsHtmlParser()
    parser.feed((DOCS / "index.html").read_text(encoding="utf-8"))
    return parser


def get_tag(parser, tag_name, element_id):
    matches = [
        attrs
        for tag, attrs in parser.tags
        if tag == tag_name and attrs.get("id") == element_id
    ]
    assert len(matches) == 1
    return matches[0]


def test_canvas_has_resolved_text_equivalent():
    parser = parse_docs_html()
    canvas = get_tag(parser, "canvas", "banana-canvas")

    assert canvas["role"] == "img"
    assert canvas["aria-labelledby"] in parser.ids

    described_by = canvas["aria-describedby"].split()
    assert described_by
    assert all(target_id in parser.ids for target_id in described_by)

    fallback_text = " ".join(part.strip() for part in parser._canvas_text if part.strip())
    assert "Deterministic 4D banana simulation" in fallback_text
    assert "seed 314159" in fallback_text


def test_prerendered_png_frames_are_present_and_accessible():
    parser = parse_docs_html()
    canvas = get_tag(parser, "canvas", "banana-canvas")
    frame_group = get_tag(parser, "div", "banana-prerendered-frames")

    assert "banana-prerendered-frames" in canvas["aria-describedby"].split()
    assert frame_group["role"] == "group"
    assert "pre-rendered PNG frames" in frame_group["aria-label"]

    images = [
        attrs
        for tag, attrs in parser.tags
        if tag == "img"
        and attrs.get("src", "").startswith("assets/banana-frames/frame-")
    ]

    assert len(images) == 4
    for index, attrs in enumerate(images, start=1):
        assert attrs["width"] == "760"
        assert attrs["height"] == "560"
        assert attrs["aria-describedby"] == f"banana-frame-{index:02d}-caption"
        assert attrs["alt"].startswith(f"Pre-rendered frame {index}:")

        frame_path = DOCS / attrs["src"]
        frame_bytes = frame_path.read_bytes()
        assert frame_bytes.startswith(b"\x89PNG\r\n\x1a\n")
        assert len(frame_bytes) > 100_000


def test_motion_control_is_keyboard_and_screen_reader_reachable():
    parser = parse_docs_html()
    button = get_tag(parser, "button", "banana-motion-toggle")
    status = get_tag(parser, "span", "banana-motion-status")

    assert button["type"] == "button"
    assert button["aria-pressed"] == "false"
    assert status["aria-live"] == "polite"


def test_skip_link_and_main_target_are_connected():
    parser = parse_docs_html()
    skip_links = [
        attrs
        for tag, attrs in parser.tags
        if tag == "a" and attrs.get("class") == "skip-link"
    ]

    assert len(skip_links) == 1
    assert skip_links[0]["href"] == "#main"
    assert "main" in parser.ids


def test_docs_scripts_and_styles_preserve_accessibility_hooks():
    script = (DOCS / "banana4d.js").read_text(encoding="utf-8")
    styles = (DOCS / "styles.css").read_text(encoding="utf-8")

    assert "prefers-reduced-motion: reduce" in script
    assert "aria-pressed" in script
    assert "aria-live" in (DOCS / "index.html").read_text(encoding="utf-8")

    assert ":focus-visible" in styles
    assert ".banana-prerendered-frames" in styles
    assert "opacity: 0" in styles
    assert "pointer-events: none" in styles
    assert "@media (prefers-reduced-motion: reduce)" in styles
