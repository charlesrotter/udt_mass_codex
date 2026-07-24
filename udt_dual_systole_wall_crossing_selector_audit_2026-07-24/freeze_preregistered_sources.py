#!/usr/bin/env python3
"""Freeze source identities from the preregistration base without mutating them."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "bcd1692e8a2bdf2300c7e7f13f5d0f4f34d490f9"


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def main() -> None:
    paths = [
        line.strip()
        for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines()
        if line.strip()
    ]
    if len(paths) != len(set(paths)):
        raise SystemExit("duplicate source path")

    rows = ["path\tblob\tsha256\tsize\tbase"]
    for path in paths:
        data = git("show", f"{BASE}:{path}")
        blob = git("rev-parse", f"{BASE}:{path}").decode().strip()
        rows.append(
            "\t".join(
                [
                    path,
                    blob,
                    hashlib.sha256(data).hexdigest(),
                    str(len(data)),
                    BASE,
                ]
            )
        )
    (HERE / "SOURCE_MANIFEST.tsv").write_text("\n".join(rows) + "\n")
    print(
        {
            "base": BASE,
            "source_count": len(paths),
            "identity_sha256": hashlib.sha256(
                ("\n".join(paths) + "\n").encode()
            ).hexdigest(),
        }
    )


if __name__ == "__main__":
    main()

