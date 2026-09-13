#!/usr/bin/env python3
"""Final document/table/receipt correspondence only; no scientific rerun."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import csv,hashlib,json,subprocess

R=Path(__file__).resolve().parent;P=R.parent;root=P.parent
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
intake=json.loads((P/'FINAL_REVIEW_INTAKE.json').read_text())
for path,want in intake['files'].items():assert digest(root/path)==want,path
assert len(intake['files'])==18
raw=json.loads((P/'checks/discrimination_complete.stdout').read_text())
table=list(csv.DictReader((P/'RECORDS.tsv').open(),delimiter='\t'))
assert len(table)==len(raw['records'])==30
for line,pair in zip(table,raw['records']):
    for key,value in line.items():assert float(value)==pair['tight'][key],key
audit=json.loads((P/'AUDIT_REUSE.json').read_text())
for path,want in audit['unchanged_full_audit_core_inputs'].items():
    assert digest(root/path)==want,path
receipt=json.loads((root/audit['full406_capture_attributed']).read_text())
assert receipt['returncode']==0 and receipt['duration_seconds']==audit['full406_actual_seconds']
assert 'PASS: 406-row premise registry' in (root/audit['full406_capture_attributed']).with_suffix('.stdout').read_text()
for name in ['navigation','current_surface']:
    item=json.loads((P/f'checks/{name}.json').read_text())
    assert item['returncode']==0 and not item['timeout']
assert '359 passed, 1 deselected' in (P/'checks/navigation.stdout').read_text()
intervals=json.loads((P/'EXECUTION_INTERVALS.json').read_text())
reconstructed=[]
for item in intervals['intervals']:
    captured=json.loads((P/item['capture']).read_text())
    start=datetime.fromisoformat(captured['started_utc'])
    end=start+timedelta(seconds=captured['duration_seconds'])
    assert item['start_utc']==start.isoformat() and item['end_utc']==end.isoformat()
    assert item['seconds']==captured['duration_seconds'] and item['exit']==captured['returncode']
    assert item['command']==captured['command']
    reconstructed.append((item,start,end))
overlaps=[]
for i,(a,sa,ea) in enumerate(reconstructed):
    for b,sb,eb in reconstructed[i+1:]:
        overlap=(min(ea,eb)-max(sa,sb)).total_seconds()
        if overlap>0:
            overlaps.append(dict(a=a['capture'],b=b['capture'],seconds=overlap,
                                 same_context=a['context']==b['context']))
assert overlaps==intervals['captured_process_overlaps']
assert not any(x['same_context'] for x in overlaps)
nav=json.loads((P/'FINAL_NAVIGATION_INPUTS.json').read_text())
for path,want in nav['after'].items():assert digest(root/path)==want,path
status=subprocess.check_output(['git','status','--short','--untracked-files=all'],cwd=root,text=True)
outside=''.join(line+'\n' for line in status.splitlines() if line.startswith('?? ') and not line[3:].startswith(P.name+'/'))
launch=json.loads((P/'LAUNCH.json').read_text())
assert len(outside.splitlines())==51
assert hashlib.sha256(outside.encode()).hexdigest()==launch['original_status_sha256']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
assert head==launch['head'] and branch=='grok'
earlier=[]
start=datetime.fromisoformat(json.loads((P/'REVIEW_ALLOCATION.json').read_text())['conservative_start_utc'])
for pkg in ['udt_signal_chain_banking_2026-09-13','udt_broader_evolving_signal_geometry_2026-09-13']:
    item=json.loads((root/pkg/'review/FINAL_RECEIPT.json').read_text())
    end=datetime.fromisoformat(item['actual_review_end_utc'])
    assert end<start
    earlier.append(dict(package=pkg,actual_review_end_utc=end.isoformat()))
print(json.dumps(dict(status='PASS_FINAL_INTAKE_CORRESPONDENCE',utc=datetime.now(timezone.utc).isoformat(),
    final_intake_sha256=digest(P/'FINAL_REVIEW_INTAKE.json'),files=intake['files'],
    records_exact=30,original_finite_plan='FAIL_ONE_FROZEN_CONVERGENCE_GATE',
    captured_intervals=len(reconstructed),captured_cross_context_overlap=overlaps,
    same_context_captured_overlap=False,earlier_reviewers=earlier,
    original_untracked_names_exact=51,original_untracked_status_sha256=launch['original_status_sha256'],
    head=head,branch=branch,full406='ATTRIBUTED_NOT_RERUN',
    limits='Hash/table/receipt correspondence; prose fidelity is separately human-context reviewed. Future publication is parent-owned.'),indent=2))
