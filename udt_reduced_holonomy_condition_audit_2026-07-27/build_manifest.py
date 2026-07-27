#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;EXCLUDED={'SHA256SUMS.txt','REPOSITORY_GATES.json'}
def main():
    files=sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in EXCLUDED);(HERE/'SHA256SUMS.txt').write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}' for p in files)+'\n');print(f'PASS package manifest {len(files)}');return 0
if __name__=='__main__':raise SystemExit(main())
