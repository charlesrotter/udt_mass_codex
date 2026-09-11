#!/usr/bin/env python3
"""Read-only adversarial check: historical adapters must authenticate excluded G413."""
import hashlib
import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import verify_current_scientific_premises as guard

target=ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv'
read_bytes=Path.read_bytes
read_text=Path.read_text
raw=read_bytes(target)
line=next(line for line in raw.splitlines(keepends=True) if line.startswith(b'G413\t'))
poison=line.replace(b'NOT_PHYSICAL_ADOPTION',b'PHYSICAL_LAW_ADOPTED')
assert poison!=line
bad=raw.replace(line,poison,1)

def poisoned_bytes(path,*args,**kwargs):
    return bad if path==target else read_bytes(path,*args,**kwargs)

def poisoned_text(path,*args,**kwargs):
    return bad.decode() if path==target else read_text(path,*args,**kwargs)

names=('validate_conditional_banking','validate_shared_constraint_banking',
       'validate_persistence_banking','validate_restrictiveness_banking',
       'validate_source_metric_banking','validate_reconstruction_banking',
       'validate_coupled_banking','validate_vacuum_scale_banking',
       'validate_berger_banking','validate_closed_fibre_banking',
       'validate_neighboring_tidal_banking','validate_reviewed_backlog_banking')
results=[]
with patch.object(Path,'read_bytes',poisoned_bytes), patch.object(Path,'read_text',poisoned_text):
    for name in names:
        try:
            getattr(guard,name)(ROOT,authenticate_sources=False)
        except SystemExit as exc:
            results.append({'guard':name,'rejected':True,'reason':str(exc)})
        else:
            results.append({'guard':name,'rejected':False,'reason':'CORRUPT_G413_WAS_SILENTLY_EXCLUDED'})

out={'status':'PASS' if all(r['rejected'] for r in results) else 'FAIL',
     'question':'Every historical adapter authenticates exact G413 before excluding it',
     'verifier_sha256':hashlib.sha256(read_bytes(ROOT/'verify_current_scientific_premises.py')).hexdigest(),
     'module_sha256':hashlib.sha256(read_bytes(ROOT/'ti1_banking_guard.py')).hexdigest(),
     'mutation':'G413 NOT_PHYSICAL_ADOPTION -> PHYSICAL_LAW_ADOPTED in same raw/text view',
     'results':results,'source_writes':False,'scientific_claim':'NONE'}
print(json.dumps(out,indent=2))
if out['status']!='PASS':
    raise SystemExit('Historical adapter excluded unauthenticated G413')
