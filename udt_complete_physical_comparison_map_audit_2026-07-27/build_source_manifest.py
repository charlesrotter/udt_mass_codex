#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;out=[]
with (HERE/'SOURCE_SCOPE.tsv').open(newline='',encoding='utf-8') as h:
    for r in csv.DictReader(h,delimiter='\t'):
        p=ROOT/r['path'];assert p.is_file(),r['path'];out.append({'path':r['path'],'role':r['role'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size})
with (HERE/'SOURCE_MANIFEST.tsv').open('w',newline='',encoding='utf-8') as h:
    w=csv.DictWriter(h,fieldnames=list(out[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
print(f'PASS {len(out)}/{len(out)} source paths')
