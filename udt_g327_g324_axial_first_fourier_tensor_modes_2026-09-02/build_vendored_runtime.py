#!/usr/bin/env python3
"""Build the deterministic intake-local SymPy runtime used by G327 replays."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import mpmath
import sympy


FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_files(module) -> list[tuple[Path, str]]:
    root = Path(module.__file__).resolve().parent
    rows = []
    for source in sorted(root.rglob("*")):
        if not source.is_file() or source.suffix in {".pyc", ".pyo"}:
            continue
        if "__pycache__" in source.parts:
            continue
        rows.append((source, f"{root.name}/{source.relative_to(root).as_posix()}"))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="VENDORED_SYMPY_RUNTIME.zip")
    parser.add_argument("--manifest", default="VENDORED_RUNTIME_MANIFEST.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    output = root / args.output
    rows = package_files(sympy) + package_files(mpmath)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, relative in rows:
            info = zipfile.ZipInfo(relative, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED,
                             compresslevel=9)
    manifest = {
        "schema": "udt-g327-vendored-runtime-v1",
        "archive": output.name,
        "archive_sha256": digest(output),
        "archive_bytes": output.stat().st_size,
        "file_count": len(rows),
        "packages": {"sympy": sympy.__version__, "mpmath": mpmath.__version__},
        "excluded": ["__pycache__", "*.pyc", "*.pyo"],
    }
    (root / args.manifest).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

