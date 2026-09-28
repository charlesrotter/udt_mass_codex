#!/usr/bin/env python3
"""Seal this lane's draft artifacts; checksums assert correspondence, not truth."""
from pathlib import Path
import datetime as dt
import hashlib
import json

P=Path(__file__).resolve().parent
target=P/'ARTIFACT_MANIFEST.json'
if target.exists():
    raise RuntimeError('Refuse to replace construction snapshot manifest')
files=sorted(f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts)
files.append(P.parent/'DATA_RESULT.md')
manifest={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    'status':'DRAFT_CONSTRUCTION_CHECKPOINT_PENDING_SEPARATE_CONTEXT_REVIEW',
    'scope':'data/ and DATA_RESULT.md only; manifest excludes itself and interpreter caches',
    'files':[{'path':str(f.relative_to(P.parent)),'bytes':f.stat().st_size,
              'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]}
manifest['total_bytes']=sum(f['bytes'] for f in manifest['files'])
target.write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'files':len(files),'bytes':manifest['total_bytes'],'status':manifest['status']}))
