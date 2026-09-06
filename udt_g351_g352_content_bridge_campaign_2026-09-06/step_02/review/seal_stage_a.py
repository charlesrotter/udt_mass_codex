#!/usr/bin/env python3
import hashlib, pathlib
p=pathlib.Path(__file__).resolve().parent
files=sorted(q for q in p.iterdir() if q.is_file() and q.name!='STAGE_A_SHA256SUMS')
out=p/'STAGE_A_SHA256SUMS'
with out.open('x') as f:
    for q in files:
        f.write(hashlib.sha256(q.read_bytes()).hexdigest()+'  '+q.name+'\n')
print(hashlib.sha256((p/'STAGE_A_SOURCE_FIRST_RECONSTRUCTION.md').read_bytes()).hexdigest())
print(hashlib.sha256(out.read_bytes()).hexdigest())
print(len(files))
