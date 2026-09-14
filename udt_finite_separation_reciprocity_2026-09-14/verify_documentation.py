"""FSR1 preservation and review correspondence; adapted from pinned PJC1 utility.
This does not certify a new scientific law or physical admission.
"""
from pathlib import Path
import csv, datetime, hashlib, json, platform, subprocess, sys
p=Path(__file__).resolve().parent.relative_to(Path.cwd())
read=lambda n:json.loads((p/n).read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a])
launch=read('LAUNCH.json'); base=launch['head']; checks={}
assert git('rev-parse','--abbrev-ref','HEAD').decode().strip()=='grok'
assert not git('diff','--cached','--name-only').strip()
for label,manifest in [('source','SOURCE_PINS.json'),('tool','TOOL_PINS.json'),('fixed','FIXED_PINS.json')]:
    pins=read(manifest)
    for n,h in pins.items():
        assert sha(Path(n).read_bytes())==h,n
        assert sha(git('show',base+':'+n))==h,n
    checks[label+'_disk_baseline_pins']=len(pins)
before=read('MAINTAINED_BEFORE.json')
for n,old in before.items():
    assert sha(old['content'].encode())==old['sha256']
    assert git('show',base+':'+n)==old['content'].encode()
checks['maintained_before_snapshots']=len(before)
initial=read('review/INITIAL_FREEZE.json')
for i,(n,h) in enumerate(initial['files'].items()):
    assert sha((p/'review/initial'/f'{i:02d}_{Path(n).name}').read_bytes())==h
assert initial['files'][str(p/'CANDIDATE.md')]==read('CHECK_FREEZE.json')['files']['CANDIDATE.md']
checks['original_candidate_and_initial7_exact']=True
final=read('review/FINAL_CANDIDATE_FREEZE.json')
for n,h in final['files'].items(): assert sha(Path(n).read_bytes())==h,n
checks['final_reviewed_hashes']=len(final['files'])
with open('CURRENT_SCIENTIFIC_PREMISES.tsv') as f:
    current={r['premise_id']:r for r in csv.DictReader(f,delimiter='\t')}
with (p/'SELECTED_PREMISES.tsv').open() as f: selected=list(csv.DictReader(f,delimiter='\t'))
assert len(current)==406 and len(selected)==13
assert all(r==current[r['premise_id']] for r in selected)
checks['whole_exact_registry_rows']=len(selected)
status=git('status','--short','--untracked-files=all').decode()
outside=''.join(l+'\n' for l in status.splitlines() if l.startswith('?? ') and not l[3:].startswith(str(p)+'/'))
assert outside==launch['original_untracked_status']
checks['original_untracked_names']=len(outside.splitlines())
checks['original_untracked_name_sha256']=sha(outside.encode())
changed=set(git('diff',base,'--name-only').decode().splitlines())
assert all(n in before or n.startswith(str(p)+'/') for n in changed)
checks['tracked_change_scope']=sorted(changed)
for n in ['full406','finite','finite_basis','navigation','navigation_basis']:
    r=read('checks/'+n+'.json')
    assert r['returncode']==0 and not r['timeout']
    checks[n]={'exit':0,'duration_seconds':r['duration_seconds']}
out=read('checks/finite.stdout')
assert out['status']=='PASS_SOURCE_FORMULA_DIAGNOSTICS_ONLY'
assert out['script_sha256']==sha((p/'basis_repair_initial/replay_finite.py').read_bytes())
repaired=read('checks/finite_basis.stdout')
assert repaired['status']=='PASS_SOURCE_FORMULA_DIAGNOSTICS_ONLY'
assert repaired['script_sha256']==sha((p/'replay_finite.py').read_bytes())
assert repaired['basis_congruence_and_Lorentz_conjugate']=='PASS_EXACT_ALGEBRA_NOT_PHYSICAL_IDENTIFICATION'
for n,h in read('BASIS_REPAIR_INITIAL.json')['files'].items():
    assert sha((p/'basis_repair_initial'/n).read_bytes())==h,n
checks['initial_and_repaired_formula_evidence_preserved']=True
checks['symbolic_source_replay_script_correspondence']=True
review=read('review/RECORD.json')
assert review['reviewed_files']==final['files']
assert review['verdict']=='VERIFIED-WITH-CAVEATS'
count=0
for line in (p/'review/REVIEW_MANIFEST.sha256').read_text().splitlines():
    digest,name=line.split('  ',1)
    assert sha(Path(name).read_bytes())==digest,name
    count+=1
checks['review_manifest_files']=count
for name,script,status in [
    ('independent','review/check_independent.py','PASS_INDEPENDENT_EXACT_FINITE_ALGEBRA_ONLY'),
    ('parent_replay','basis_repair_initial/replay_finite.py','PASS_SOURCE_FORMULA_DIAGNOSTICS_ONLY'),
]:
    result=read('review/'+name+'.json'); output=read('review/'+name+'.stdout')
    assert result['returncode']==0 and not result['timeout']
    assert output['status']==status and output['script_sha256']==sha((p/script).read_bytes())
checks['review_actual_capture_script_correspondence']=True
checks['fresh_review_candidate_correspondence']=True
checks['result']='PASS_DOCUMENTARY_CORRESPONDENCE_ONLY'
checks['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
checks['python']=sys.version;checks['platform']=platform.platform()
print(json.dumps(checks,indent=2))
