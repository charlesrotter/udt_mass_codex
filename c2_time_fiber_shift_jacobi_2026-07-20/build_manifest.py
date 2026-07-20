#!/usr/bin/env python3
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent; EXCLUDED={"SHA256SUMS.txt","REPOSITORY_GATES.json"}
paths=sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
(HERE/"SHA256SUMS.txt").write_text("\n".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in paths)+"\n",encoding="utf-8")
print(f"PASS entries={len(paths)}")
