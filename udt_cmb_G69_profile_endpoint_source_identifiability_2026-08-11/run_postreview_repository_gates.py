#!/usr/bin/env python3
"""Replay the frozen G69 repository gates into an additions-only post-review result."""

from __future__ import annotations

import runpy
from pathlib import Path


HERE = Path(__file__).resolve().parent
FROZEN_RESULT = (HERE / "REPOSITORY_GATES.json").resolve()
POSTREVIEW_RESULT = HERE / "POSTREVIEW_REPOSITORY_GATES.json"
ORIGINAL_WRITE_TEXT = Path.write_text


def redirected_write_text(path: Path, data: str, *args, **kwargs) -> int:
    if path.resolve() == FROZEN_RESULT:
        return ORIGINAL_WRITE_TEXT(POSTREVIEW_RESULT, data, *args, **kwargs)
    return ORIGINAL_WRITE_TEXT(path, data, *args, **kwargs)


Path.write_text = redirected_write_text
runpy.run_path(str(HERE / "verify_repository_gates.py"), run_name="__main__")
