#!/usr/bin/env python3
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
files=sorted(q for q in p.iterdir() if q.is_file() and q.name!='CLOSURE_SHA256SUMS')
with (p/'CLOSURE_SHA256SUMS').open('x') as f:
    for q in files:f.write(hashlib.sha256(q.read_bytes()).hexdigest()+'  '+q.name+'\n')
print(json.dumps({'note_sha256':hashlib.sha256((p/'CLOSURE_FIDELITY.md').read_bytes()).hexdigest(),
 'checks_stdout_sha256':hashlib.sha256((p/'closure.stdout').read_bytes()).hexdigest(),
 'manifest_sha256':hashlib.sha256((p/'CLOSURE_SHA256SUMS').read_bytes()).hexdigest(),
 'payloads':len(files),'total_files':len(files)+1},indent=2))
