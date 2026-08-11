#!/usr/bin/env python3
"""Hash the final G68 package after external-review adjudication."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {
    "POSTREVIEW_MANIFEST.tsv",
    "POSTREVIEW_VERIFICATION_RESULT.json",
    "REPOSITORY_GATES.json",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    output = "path\tsha256\n" + "".join(f"{path.name}\t{digest(path)}\n" for path in paths)
    (HERE / "POSTREVIEW_MANIFEST.tsv").write_text(output, encoding="utf-8")
    print(f"postreview_files={len(paths)}")


if __name__ == "__main__":
    main()
