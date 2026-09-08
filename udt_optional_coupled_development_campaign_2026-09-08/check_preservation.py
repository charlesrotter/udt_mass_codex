"""Read-only campaign correspondence/preservation checks, not scientific proof."""
import hashlib
import json
import pathlib
import subprocess

root=pathlib.Path(__file__).resolve().parent.parent
package=pathlib.Path(__file__).resolve().parent
name=package.name
baseline='e1b6cdbef96f9a0ce8878d42d160a5ebe1f267f7'
def git(*args):
    return subprocess.check_output(['git','-c','core.preloadIndex=false',
        '-c','index.threads=1',*args],cwd=root,text=True)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def manifest(path):
    count=0
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        expected,rel=line.split('  ',1)
        target=root/rel
        assert target.is_file(),rel
        assert digest(target)==expected,rel
        count+=1
    return count

assert git('branch','--show-current').strip()=='grok'
source_count=manifest(package/'SOURCE_SHA256SUMS')
prior_count=manifest(root/'udt_g370_g371_conditional_banking_2026-09-08/SHA256SUMS')
initials={}
for step in ('step_01','step_02'):
    pin=package/step/'INITIAL_SHA256SUMS'
    if pin.exists(): initials[step]=manifest(pin)

# Names only: no payload read, stat, hash, import, mining or citation.
status=git('status','--porcelain')
unrelated=sorted(line for line in status.splitlines()
    if line.startswith('?? ') and not line[3:].startswith(name+'/'))
assert len(unrelated)==46,('unrelated_count',len(unrelated))
names_hash=hashlib.sha256('\n'.join(unrelated).encode()).hexdigest()
assert names_hash=='d65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea'

# Only maintained current tracking and this owned package may change.
allowed={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md','MEMORY.md'}
changed=git('diff','--name-only',baseline,'--').splitlines()
assert all(p in allowed or p.startswith(name+'/') for p in changed),changed
assert not git('diff','--name-only',baseline,'--',
    'udt_g370_g371_conditional_banking_2026-09-08').strip()
rows=(root/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text().splitlines()
assert len(rows)-1==354,len(rows)-1
print(json.dumps({'status':'PASS_CORRESPONDENCE_NOT_SCIENTIFIC_PROOF',
 'baseline':baseline,'head':git('rev-parse','HEAD').strip(),
 'source_and_control_pins':source_count,'prior_bank_payloads':prior_count,
 'immutable_initial_pins':initials,'registry_rows':354,
 'unrelated_untracked_names':len(unrelated),'unrelated_names_sha256':names_hash,
 'changed_tracked_paths':changed,'protected_payloads':'NOT_INSPECTED',
 'backup_completeness':'UNVERIFIED','pre_reboot_unsaved_state':'UNVERIFIED',
 'host_wide_processes':'UNVERIFIED'},indent=2))
