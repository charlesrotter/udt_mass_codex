#!/usr/bin/env python3
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as stream:
    sources = list(csv.DictReader(stream, delimiter="\t"))
lines = ["source_path\tsha256\tsize"]
for row in sources:
    path = ROOT / row["source_path"]
    if not path.is_file():
        raise SystemExit(f"missing source: {row['source_path']}")
    lines.append(f"{row['source_path']}\t{digest(path)}\t{path.stat().st_size}")
(HERE / "SOURCE_MANIFEST.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"PASS source_manifest rows={len(sources)}")
