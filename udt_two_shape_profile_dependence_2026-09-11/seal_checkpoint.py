"""Seal TI3 after actual final fidelity; correspondence only, no scientific promotion."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

root=Path(__file__).resolve().parents[1]
package=Path(__file__).resolve().parent
baseline='6b09b8caab189291a6ffc1956dea304bbe6da7cb'
navigation=['CURRENT_RESEARCH_PROGRAM.md','HANDOFF.md','INDEX.md','LIVE.md','UDT_RESEARCH_ROADMAP.md']
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
def save(name,data):
    with (package/name).open('x') as f:
        json.dump(data,f,indent=2);f.write('\n')
assert git('branch','--show-current')=='grok'
assert git('rev-parse','HEAD')==git('rev-parse','origin/grok')==baseline
assert sorted(git('diff','--name-only').splitlines())==navigation
assert not git('diff','--cached','--name-only')
final=json.loads((package/'review/FINAL_FIDELITY_RECEIPT.json').read_text())
assert final['verdict']=='PASS'
assert final['science_status']=='CONDITIONAL_UNPROMOTED'
assert final['required_scientific_repairs']==[]
for name,digest in final['sha256'].items():
    assert sha(root/name)==digest,name
for name,base,key in [('CANDIDATE_FREEZE.json',package,'files'),('SOURCE_PINS.json',root,'sources')]:
    for path,digest in json.loads((package/name).read_text())[key].items():
        assert sha(base/path)==digest,(name,path)
unrelated=''.join(line+'\n' for line in git('status','--porcelain=v1','--untracked-files=normal').splitlines()
                  if line.startswith('?? ') and not line.endswith(package.name+'/'))
fingerprint=hashlib.sha256(unrelated.encode()).hexdigest()
assert fingerprint=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
now=datetime.datetime.now(datetime.timezone.utc)
launch=json.loads((package/'LAUNCH.json').read_text())
assert now<datetime.datetime.fromisoformat(launch['research_hard_return_utc'])
save('COMPLETION_SEAL.json',{'sealed_utc':now.isoformat(),'study_launch_utc':launch['launch_utc'],
 'elapsed_seconds':(now-datetime.datetime.fromisoformat(launch['launch_utc'])).total_seconds(),
 'hard_return_utc':launch['research_hard_return_utc'],'science_and_review':'COMPLETE',
 'G414':'BANKED','TI3':'VERIFIED-WITH-CAVEATS_CONDITIONAL_UNPROMOTED','scientific_repairs':0,
 'actual_new_contexts_this_combined_request':2,'bank_review_final_utc':launch['banking_review_final_seal_utc'],
 'TI3_review_first_utc':final['first_observed_utc'],'TI3_review_final_utc':final['completed_utc'],
 'overlap':'reviewers did not overlap; TI3 reviewer overlapped parent audit/documentation; captured science intervals overlap',
 'capacity':'actual successful allocations only; general restoration UNVERIFIED; no further attempts',
 'configured_parent':launch['configured_parent'],'runtime_model_version':'UNATTESTED',
 'full397_seconds':404.31189697497757,'navigation':'359_PASS_1_DUPLICATE_FULL_WRAPPER_DESELECTED',
 'final_fidelity_pins':len(final['sha256']),'original46_status_sha256':fingerprint,
 'backup_completeness':'UNVERIFIED','pre_reboot_unsaved_state':'UNVERIFIED',
 'publication':'FUTURE_AT_SEAL','next_action':'stop for discussion; no successor or TI3 promotion authorized'})
exclude={'ARTIFACT_SHA256SUMS','PREPUBLICATION_RECEIPT.json'}
paths=set(navigation)
for directory,dirs,names in os.walk(package):
    dirs[:]=[d for d in dirs if d not in {'__pycache__','.pytest_cache'}]
    for name in names:
        path=Path(directory)/name
        assert not path.is_symlink(),path
        if path.parent==package and name in exclude:
            continue
        paths.add(str(path.relative_to(root)))
paths.add(str((package/'PUBLICATION_SCOPE.json').relative_to(root)))
additional=[str((package/name).relative_to(root)) for name in sorted(exclude)]
save('PUBLICATION_SCOPE.json',{'baseline_head':baseline,'root_scope':navigation,
 'manifest_paths':sorted(paths),'additional_seal_paths':additional,
 'stage_paths':sorted(paths|set(additional)),'science_grade':'TI3_UNPROMOTED'})
manifest=''.join(sha(root/name)+'  '+name+'\n' for name in sorted(paths))
with (package/'ARTIFACT_SHA256SUMS').open('x') as f:
    f.write(manifest)
receipt={'sealed_utc':now.isoformat(),'baseline_head':baseline,'manifest_entries':len(paths),
 'staging_paths':len(paths)+2,'manifest_sha256':sha(package/'ARTIFACT_SHA256SUMS'),
 'final_fidelity_receipt_sha256':sha(package/'review/FINAL_FIDELITY_RECEIPT.json'),
 'verified_final_pins':len(final['sha256']),'candidate_and_sources_unchanged':True,
 'original46_status_sha256':fingerprint,'publication':'FUTURE_AT_SEAL',
 'outcome_metadata':'parent-owned after final fidelity; not new science or acceptance'}
save('PREPUBLICATION_RECEIPT.json',receipt)
print(json.dumps(receipt,indent=2))
