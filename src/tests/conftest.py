"""Test bootstrap for the src-based modules.

Pytest runs from the repository root, so add ``src/`` to ``sys.path`` once for
the test session instead of relying on an ad hoc environment variable.
"""

from __future__ import annotations

import sys
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1]
src_path = str(SRC_DIR)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
