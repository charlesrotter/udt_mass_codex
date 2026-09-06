"""Pinned documentation/archive fidelity only; read-only, stdout JSON."""
import argparse,hashlib,json,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True)
p.add_argument('--sealed',type=pathlib.Path,required=True);a=p.parse_args()
repo=a.repo.resolve();sealed=a.sealed.resolve()
pin='6a3755bb2b059a30c004ee3c246dd36043f5c8aa'
package='udt_g351_g352_content_bridge_campaign_2026-09-06/'
prefix=package+'step_03/review/'
git=lambda *args:subprocess.check_output(['git',*args],cwd=repo)
sha=lambda data:hashlib.sha256(data).hexdigest()
names=(sealed/'ARCHIVE_FILES.txt').read_text().splitlines()
assert names==sorted(set(names)) and len(names)==78
assert sorted(p.relative_to(sealed).as_posix() for p in sealed.rglob('*') if p.is_file())==names
archived=repo/prefix
assert sorted(p.relative_to(archived).as_posix() for p in archived.rglob('*') if p.is_file())==names
tracked=[z.decode()[len(prefix):] for z in git('ls-tree','-r','-z','--name-only',pin,'--',prefix).split(b'\0') if z]
assert tracked==names
manifest=(sealed/'REVIEW_SHA256SUMS').read_bytes()
assert sha(manifest)=='42c3db50d4ac9762e60538fec554db40cf33440e196e78d3659ad581b6803842'
lines=manifest.decode().splitlines();assert len(lines)==77
for line in lines:
    digest,name=line.split('  ',1)
    assert sha((sealed/name).read_bytes())==digest,name
rows=[]
for name in names:
    original=(sealed/name).read_bytes();working=(archived/name).read_bytes()
    pinned=git('show',pin+':'+prefix+name)
    assert original==working==pinned,name
    rows.append({'name':name,'sha256':sha(original),'bytes':len(original),
                 'original_worktree_pinned_identical':True})
record_path=package+'step_03/REVIEW_RECORD.md'
log_path=package+'CAMPAIGN_LOG.md'
record=git('show',pin+':'+record_path)
assert record==(repo/record_path).read_bytes()
log=git('show',pin+':'+log_path).decode()
record_text=record.decode()
for token in ['VERIFIED-WITH-CAVEATS, UNPROMOTED','0/1 author','CHOSEN mathematics',
 'bounded supplied u-coordinate intervals','NO primitive of the nonclosed root',
 'Pointwise q=0 means pointwise d beta=0','open patch is the closure statement',
 'Germ-local symmetry is not a physical','duration was not captured',
 '28462569691deaea5467f4c76a22363861a4b6a72d057f2b9db0a1a1b8bc6843']:
    assert token in record_text,token
ledger=[line for line in log.splitlines() if line.startswith('| 3 |')]
assert len(ledger)==1
assert 'VERIFIED-WITH-CAVEATS, UNPROMOTED;e6ec23ac' in ledger[0]
assert 'Harmonic local nonzero-root class, optional scalar conversion;0/1 repair' in ledger[0]
start=log.index('Step3 direct report read20:28UTC;')
end=log.index('Step4 follows',start)
learning=log[start:end]
for token in ['no required defect','78-file review received','durationUNMEASURED',
 'supplied u intervals, NOT a primitive','of the nonclosed root',
 'Closure/parallelism/conservation remain distinct']:
    assert token in learning,token
current=(repo/log_path).read_text()
assert ledger[0] in current and learning in current
print(json.dumps({'status':'PASS','scope':'Step 3 documentation and archive closure only; no new mathematical review or Step 4 evaluation',
 'pinned_commit':pin,'actual_head':git('rev-parse','HEAD').decode().strip(),
 'archive_files':78,'manifest_payloads':77,'exact_membership_original_worktree_pinned':True,
 'all_bytes_original_worktree_pinned_identical':True,'record_sha256':sha(record),
 'pinned_campaign_log_sha256':sha(log.encode()),'review_record_worktree_equals_pin':True,
 'step3_ledger':ledger[0],'step3_learning':learning,
 'step3_ledger_learning_unchanged_in_current_worktree':True,
 'preserved_caveats':['bounded supplied u coordinates do not give a primitive of nonclosed beta',
 'pointwise q=0 versus closure on an open patch','local-germ symmetry versus physical global completion',
 'chosen mathematics, unpromoted status and optional scalar class','same-code premise audit with unmeasured duration'],
 'archive_comparisons':rows},indent=2))
