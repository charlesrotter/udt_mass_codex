#!/usr/bin/env python3
"""Freeze the completed source-first assessment without reading parent synthesis."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
files=[HERE/name for name in ('SOURCE_FIRST_ASSESSMENT.md','SOURCE_FIRST_PINS.json',
 'SOURCE_READ_DEPTH.tsv','source_pin_check.py','source_pin_capture.json',
 'source_pin_capture.stdout','source_pin_capture.stderr',
 'source_pin_capture.capture_provenance.json','seal_source_first.py')]
files += [HERE.parent/'checks'/('launch_full397'+suffix)
 for suffix in ('.json','.stdout','.stderr','.capture_provenance.json')]
result=json.loads((HERE.parent/'checks/launch_full397.json').read_text())
assert result['returncode']==0 and result['timeout'] is False
assert (HERE.parent/'checks/launch_full397.stderr').read_bytes()==b''
assert 'PASS: 397-row premise registry' in (HERE.parent/'checks/launch_full397.stdout').read_text()
receipt={'sealed_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer_context':'/root/cwa1_consolidation_review','first_observed_clock':'2026-09-12T16:11:54+00:00',
 'actual_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'parent_consolidation_exposure':'NONE; only current status and original scientific sources',
 'runtime_model_version':'UNATTESTED','different_model':'NOT_ESTABLISHED',
 'allocation':'one fresh separate context; no subdelegation or override',
 'parent_full397':'actual new receipt/streams inspected; parent execution attributed; PASS',
 'source_pin_capture':'metadata correspondence only; no scientific suite replay',
 'files':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 for p in files]}
with (HERE/'SOURCE_FIRST_SEAL.json').open('x') as f:
 json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps({'sealed_utc':receipt['sealed_utc'],
 'assessment_sha256':receipt['files'][0]['sha256'],
 'files':len(files),'parent_full397':'INSPECTED_PASS','parent_candidate_exposure':'NONE'}))
