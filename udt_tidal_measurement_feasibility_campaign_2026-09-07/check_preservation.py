#!/usr/bin/env python3
"""Task-local metadata/source preservation check, never protected payload reads."""
import hashlib
import json
import subprocess
from pathlib import Path
import verify_current_scientific_premises as guard

root=Path.cwd()
package=Path(__file__).resolve().parent
baseline='508eb238d1321a3bdce9a45eb47a97b63fb1b541'
git=['git','-c','core.preloadIndex=false','-c','index.threads=1']
def run(*args):
    return subprocess.check_output(git+list(args),text=True)
expected=json.loads((package/'STARTUP_UNTRACKED_METADATA.json').read_text())['entries']
actual=[r for r in run('status','--short','--branch').splitlines()
        if r.startswith('?? ') and not r[3:].startswith(package.name+'/')]
assert actual==expected, 'unrelated untracked metadata changed'
changed=run('diff','--name-only',baseline).splitlines()
allowed={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md'}
assert all(p in allowed or p.startswith(package.name+'/') for p in changed),changed
pinned=['CANON.md','UDT_METRIC_KERNEL_DEVELOPMENT.md','UDT_METRIC_KERNEL_COVERAGE.tsv',
        'CURRENT_SCIENTIFIC_PREMISES.tsv','AGENTS.md','CLAUDE.md','verify_current_scientific_premises.py']
hashes={}
for p in pinned:
    before=subprocess.check_output(git+['show',baseline+':'+p])
    now=(root/p).read_bytes()
    assert now==before,p
    hashes[p]=hashlib.sha256(now).hexdigest()
guard.validate_startup_surface(root)
print(json.dumps({'baseline':baseline,'pass':True,'startup_surface_guard':'PASS',
    'unchanged_bytes_sha256':hashes,'unrelated_untracked_metadata_count':len(actual),
    'allowed_tracked_changes':changed,'protected_payload_bytes':'NOT_INSPECTED',
    'backup_completeness':'UNVERIFIED','pre_reboot_unsaved_state_disposition':'UNVERIFIED',
    'ScratchDisk':'UNUSED_ARCHIVE_DEPENDENT_TASKS_ONLY'},indent=2))
