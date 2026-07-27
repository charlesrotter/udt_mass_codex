#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
with (HERE/'SOURCE_MANIFEST.tsv').open(newline='',encoding='utf-8') as h:rows=list(csv.DictReader(h,delimiter='\t'))
assert len(rows)==28 and len({r['path'] for r in rows})==28
for r in rows:
    p=ROOT/r['path'];assert p.is_file() and p.stat().st_size==int(r['size']);assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
print('PASS 28/28 source paths')
