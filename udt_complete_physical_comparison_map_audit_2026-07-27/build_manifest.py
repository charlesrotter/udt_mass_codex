#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;skip={'SHA256SUMS.txt','REPOSITORY_GATES.json'};paths=sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in skip);(HERE/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in paths));print(f'PASS {len(paths)} package files')
