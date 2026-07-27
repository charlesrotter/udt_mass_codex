#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
rows=[]
with (HERE/'SOURCE_SCOPE.tsv').open(newline='',encoding='utf-8') as h:
    for row in csv.DictReader(h,delimiter='\t'):
        p=ROOT/row['path']; assert p.is_file(),row['path']
        rows.append({'path':row['path'],'role':row['role'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size})
with (HERE/'SOURCE_MANIFEST.tsv').open('w',newline='',encoding='utf-8') as h:
    w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
print(f'PASS {len(rows)}/{len(rows)} source paths')
