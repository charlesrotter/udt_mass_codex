"""Independent packet correspondence only; no scientific source-code imports."""
import csv
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

base=Path('udt_foundation_alignment_audit_2026-09-27')
candidate=base/'initial_candidate'
def rows(path):
    with Path(path).open(newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))
def unique(data,key):
    assert len(data)==len({r[key] for r in data})
    return {r[key]:r for r in data}

frozen=json.loads((base/'INITIAL_FREEZE.json').read_text())['sha256']
frozen_matches={p:hashlib.sha256((base/p).read_bytes()).hexdigest()==h for p,h in frozen.items()}
assert all(frozen_matches.values())
current=unique(rows('CURRENT_SCIENTIFIC_PREMISES.tsv'),'premise_id')
old=unique(rows('udt_accepted_work_consolidation_2026-09-12/REGISTRY_COVERAGE.tsv'),'premise_id')
covered=unique(rows(candidate/'REGISTRY_COVERAGE.tsv'),'premise_id')
assert current.keys()==covered.keys()
field_names=list(next(iter(current.values())).keys())
mismatches=[(i,k) for i,r in current.items() for k in field_names if covered[i][k]!=r[k]]
assert not mismatches
old_fields={'term':'term','epistemic_label':'epistemic_label_exact','active_use':'active_use_exact','controlling_source':'controlling_source_exact'}
changed=[(i,k) for i in old.keys() & current.keys() for k,oldk in old_fields.items() if current[i][k]!=old[i][oldk]]
assert not changed
added=set(current)-set(old)
removed=set(old)-set(current)
assert added=={'G'+str(x) for x in range(415,424)} and not removed
families=rows(candidate/'FAMILY_ROUTING.tsv')
members=Counter()
for family in families:
    ids=family['premise_ids'].split(';')
    assert len(ids)==int(family['count'])
    for i in ids:
        members[i]+=1
        assert covered[i]['editorial_family']==family['family_id']
assert set(members)==set(current) and set(members.values())=={1}
claims=rows(candidate/'SOURCE_CLAIM_MAP.tsv')
claim_ids={r['audit_id'] for r in claims}
audit_ids=set(re.findall(r'^## (A\d+)\.',(candidate/'AUDIT.md').read_text(),re.M))
assert claim_ids==audit_ids=={'A'+str(i).zfill(2) for i in range(1,12)}
apply_check=subprocess.run(['git','apply','--check',str(candidate/'MAINTAINED_DOCS.patch')],capture_output=True,text=True)
assert apply_check.returncode==0,apply_check.stderr
tracked=subprocess.check_output(['git','ls-files','-z']).split(b'\0')
count=sum(bool(p) for p in tracked)
assert count==33248
out={'status':'PASS','evidence_type':'independent byte/ID/field correspondence; no science validation',
     'frozen_files_matched':len(frozen_matches),'candidate_files':8,
     'current_rows':len(current),'inherited_rows':len(old),'added_ids':sorted(added),'removed_ids':sorted(removed),
     'current_fields_checked':field_names,'current_field_mismatch_count':len(mismatches),
     'inherited_four_field_mismatch_count':len(changed),'families':len(families),'family_multiplicity':'exactly one per current ID',
     'audit_ids_checked':sorted(audit_ids),'patch_check_returncode':apply_check.returncode,
     'patch_check_stdout':apply_check.stdout,'patch_check_stderr':apply_check.stderr,
     'tracked_file_count':count,'tracked_dirt':subprocess.check_output(['git','status','--porcelain=v1','-uno'],text=True),
     'source_first_unchanged':hashlib.sha256((base/'review/math/SOURCE_FIRST.md').read_bytes()).hexdigest()==json.loads((base/'review/math/SOURCE_FIRST_FREEZE.json').read_text())['source_first_sha256']}
assert out['tracked_dirt']=='' and out['source_first_unchanged']
print(json.dumps(out,indent=2))
