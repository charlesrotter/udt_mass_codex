#!/usr/bin/env python3
"""Reviewer correspondence only; no source scientific code execution."""
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

root=Path(__file__).resolve().parents[2]
base=root/'udt_two_shape_profile_dependence_2026-09-11'
review=base/'review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
for file,key,relative in [('CANDIDATE_FREEZE.json','files',base),
                          ('SOURCE_PINS.json','sources',root),
                          ('review/PRECOMPUTATION.json','precomputation_pins',root)]:
    doc=json.loads((base/file).read_text())
    pins=doc[key]
    for name,expected in pins.items():
        assert sha(relative/name)==expected,(file,name)
    checks.append({'manifest':file,'matched':len(pins)})
raw=json.loads((root/'udt_two_shape_evolution_2026-09-11/checks/initial_rate.stdout').read_text())
author=json.loads((base/'checks/initial_profile_checks.stdout').read_text())
mine=json.loads((review/'raw_metric_results.json').read_text())
assert author['status']==mine['verdict']=='PASS'
for a in mine['anchors']:
    other=author['anchors'][str(a['lambda'])]
    assert a['P']==other['P']
    assert a['U_P']==other['P_T']
for stem in [base/'checks/initial_profile_checks',review/'checks/raw_metric_anchors']:
    cap=json.loads(Path(str(stem)+'.json').read_text())
    assert cap['returncode']==0 and not cap['timeout']
    assert not Path(str(stem)+'.stderr').read_bytes()
selected={}
lines=(root/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text().splitlines(keepends=True)
reader=csv.DictReader(lines,delimiter='\t')
for row,line in zip(reader,lines[1:]):
    if row['premise_id'] in ('G166','G176','G312','G413','G414'):
        selected[row['premise_id']]={'row_sha256':hashlib.sha256(line.encode()).hexdigest(),
           'epistemic_label':row['epistemic_label'],'current_status':row['current_status']}
assert len(selected)==5
files=[
 'udt_ti1_banking_2026-09-11/BANKING_RECORD.md',
 'udt_ti2_banking_2026-09-11/BANKING_RECORD.md',
 'udt_ti2_banking_2026-09-11/BANKED_CLAIM.json',
 'udt_two_shape_nonlinear_interaction_2026-09-11/INITIAL_CANDIDATE.md',
 'udt_two_shape_nonlinear_interaction_2026-09-11/review/REVIEW.md',
 'udt_two_shape_evolution_2026-09-11/INITIAL_CANDIDATE.md',
 'udt_two_shape_evolution_2026-09-11/review/REVIEW.md',
 'udt_two_shape_evolution_2026-09-11/review/FINAL_FIDELITY.md',
 'udt_two_shape_evolution_2026-09-11/initial_rate.py',
 'udt_two_shape_evolution_2026-09-11/checks/initial_rate.stdout',
 'udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md',
 'udt_two_shape_profile_dependence_2026-09-11/profile_checks.py',
 'udt_two_shape_profile_dependence_2026-09-11/checks/initial_profile_checks.stdout',
 'udt_two_shape_profile_dependence_2026-09-11/checks/initial_profile_checks.stderr',
 'udt_two_shape_profile_dependence_2026-09-11/checks/initial_profile_checks.json',
 'udt_two_shape_profile_dependence_2026-09-11/checks/initial_profile_checks.capture_provenance.json',
]
out={'verdict':'PASS','utc':datetime.now(timezone.utc).isoformat(),'manifest_checks':checks,
     'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
     'origin_grok':subprocess.check_output(['git','rev-parse','origin/grok'],cwd=root,text=True).strip(),
     'selected_exact_rows':selected,'read_source_pins':{name:sha(root/name) for name in files},
     'old_general_P':raw['P'],'old_general_rate':raw['P_T_general_profile_jet'],
     'author_output_read_after_reviewer_anchor_capture':True,
     'no_parent_scientific_replay':True}
with (review/'INPUT_CORRESPONDENCE.json').open('x') as f:
    json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
