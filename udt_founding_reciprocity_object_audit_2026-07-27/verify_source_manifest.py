#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
with (HERE/'SOURCE_MANIFEST.tsv').open(newline='',encoding='utf-8') as h: rows=list(csv.DictReader(h,delimiter='\t'))
assert len(rows)==26 and len({r['path'] for r in rows})==26
for r in rows:
    p=ROOT/r['path'];assert p.is_file();assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'];assert p.stat().st_size==int(r['size'])
print('PASS 26/26 source paths')
