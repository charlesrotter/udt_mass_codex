#!/usr/bin/env python3
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;X={'SHA256SUMS.txt','REPOSITORY_GATES.json'};P=sorted(p for p in H.iterdir() if p.is_file() and p.name not in X)
(H/'SHA256SUMS.txt').write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}' for p in P)+'\n');print(f'PASS entries={len(P)}')
