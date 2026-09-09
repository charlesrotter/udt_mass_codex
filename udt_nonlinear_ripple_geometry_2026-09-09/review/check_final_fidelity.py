"""Packaging-only correspondence checks; no scientific derivation rerun."""
import hashlib
import json
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[2]
review=Path(__file__).resolve().parent
package=review.parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
sealed={}
for name in ('SOURCE_FIRST_SHA256SUMS','DIRECT_REVIEW_SHA256SUMS'):
    rows=(review/name).read_text().splitlines()
    for row in rows:
        h,p=row.split('  ',1)
        assert sha(root/p)==h,(name,p)
    sealed[name]=len(rows)
record=json.loads((review/'REVIEW_RECORD.json').read_text())
for name,h in record['inputs'].items():
    assert sha(package/name)==h,('frozen_direct_input',name)
# The first captured attempt hit Git's threaded lstat allocation under the
# 512 MiB ceiling. Disable parallel index loading for this read-only check.
tracked=set(subprocess.check_output(['git','-c','core.preloadIndex=false',
    '-c','index.threads=1','diff','--name-only'],cwd=root,text=True).splitlines())
expected={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md'}
assert tracked==expected,tracked
next_gates={}
for name,marker in [('LIVE.md','### Next gate'),
                    ('HANDOFF.md','Next: G381=NT1'),
                    ('CURRENT_RESEARCH_PROGRAM.md','## Current next gate')]:
    old=subprocess.check_output(['git','show','HEAD:'+name],cwd=root,text=True)
    new=(root/name).read_text()
    assert marker in old and marker in new
    assert old[old.rindex(marker):]==new[new.rindex(marker):],name
    next_gates[name]='BYTE_IDENTICAL_SUFFIX'
pins={}
for name in ['REVIEWED_RESULT.md','DECISION_BRIEF.md','README.md','CAMPAIGN_LOG.md']:
    pins[str((package/name).relative_to(root))]=sha(package/name)
for name in sorted(expected):
    pins[name]=sha(root/name)
print(json.dumps(dict(result='PASS_PACKAGING_FIDELITY_CHECKPOINT',
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
    authenticated_seals=sealed,frozen_review_inputs=len(record['inputs']),
    tracked_diff_paths=sorted(tracked),next_gates=next_gates,sha256=pins,
    campaign_log_scope='REVIEWED_CHECKPOINT_ONLY; later mechanical entries excluded',
    scientific_recomputations='NONE; unchanged science already reviewed'),indent=2))
