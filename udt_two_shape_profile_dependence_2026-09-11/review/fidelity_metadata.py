#!/usr/bin/env python3
"""Final fidelity metadata only; no scientific program or publication execution."""
import ast
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess

root=Path(__file__).resolve().parents[2]
base=root/'udt_two_shape_profile_dependence_2026-09-11'
review=base/'review'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
sub=json.loads((review/'REVIEW_RECEIPT.json').read_text())
for group in ('source_pins','review_files'):
    for name,expected in sub[group].items():
        assert sha(root/name)==expected,(group,name)
roots=['CURRENT_RESEARCH_PROGRAM.md','HANDOFF.md','INDEX.md','LIVE.md','UDT_RESEARCH_ROADMAP.md']
docs=['REVIEWED_RESULT.md','DECISION_BRIEF.md','CLOSEOUT.md','SCOPE_MAP.tsv','MANIFEST_SCOPE.md',
      'REVIEW_ALLOCATION.json','check_preservation.py','seal_checkpoint.py','AUDIT_RESULT.json',
      'INITIAL_CANDIDATE.md','CANDIDATE_FREEZE.json','FRAME_AND_DISCOVERY.md','LAUNCH.json','SOURCE_PINS.json']
paths=[root/p for p in roots]+[base/p for p in docs]
paths+=[review/p for p in ['REVIEW.md','REVIEW_RECEIPT.json','fidelity_metadata.py']]
stems=[base/'checks'/n for n in ['current397_premise_audit','final_navigation','final_preservation']]
stems.append(review/'checks/final_preservation_replay')
for stem in stems:
    cap=json.loads(Path(str(stem)+'.json').read_text())
    assert cap['returncode']==0 and not cap['timeout'],stem
    assert not Path(str(stem)+'.stderr').read_bytes(),stem
    paths += [Path(str(stem)+ext) for ext in ('.json','.stdout','.stderr','.capture_provenance.json')]
assert '359 passed, 1 deselected' in (base/'checks/final_navigation.stdout').read_text()
assert 'PASS: 397-row premise registry' in (base/'checks/current397_premise_audit.stdout').read_text()
for name in ['check_preservation.py','seal_checkpoint.py']:
    ast.parse((base/name).read_text())
assert not (base/'COMPLETION_SEAL.json').exists()
assert not (base/'PUBLICATION_SCOPE.json').exists()
assert not (base/'PREPUBLICATION_RECEIPT.json').exists()
diff=subprocess.check_output(['git','diff','--',*roots],cwd=root,text=True)
with (review/'FINAL_ROOT_DIFF.patch').open('x') as f:f.write(diff)
subprocess.run(['git','diff','--check'],cwd=root,check=True)
stats={p:{'lines':len((root/p).read_text().splitlines()),'words':len((root/p).read_text().split())}
       for p in roots if p!='UDT_RESEARCH_ROADMAP.md'}
result={'verdict':'PASS','checked_utc':datetime.now(timezone.utc).isoformat(),
        'substantive_source_pins_unchanged':len(sub['source_pins']),
        'substantive_review_files_unchanged':len(sub['review_files']),
        'root_sizes':stats,'publication_scripts':'syntax parsed and read; not executed',
        'publication':'FUTURE','final_input_sha256':{str(p.relative_to(root)):sha(p) for p in paths}}
with (review/'FINAL_INPUT_PINS.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
