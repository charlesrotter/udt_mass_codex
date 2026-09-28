#!/usr/bin/env python3
"""GRS1 packaging integrity only; no scientific truth or independent-proof claim."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent.parent
package = Path(__file__).resolve().parent
launch = json.loads((package/'LAUNCH.json').read_text())
freeze = json.loads((package/'CANDIDATE_FREEZE.json').read_text())
maintained = {'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','MEMORY.md',
              'INDEX.md','UDT_RESEARCH_ROADMAP.md'}

def git(*args):
    return subprocess.check_output(['git',*args],cwd=root)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

assert git('branch','--show-current').decode().strip() == 'grok'
assert git('rev-parse','HEAD').decode().strip() == launch['head']
changes = set(git('diff','--name-only').decode().splitlines())
assert changes == maintained, changes
assert not git('diff','--cached','--name-only'), 'Expected no staged material before exact staging'
source_checks = {}
for name, expected in launch['source_sha256'].items():
    # Modified direction/status pointers remain available at the pinned commit.
    from_baseline = name in maintained
    raw = git('show',launch['head']+':'+name) if from_baseline else (root/name).read_bytes()
    assert digest(raw) == expected, name
    source_checks[name] = {'sha256':expected,'from': 'pinned git baseline' if from_baseline else 'unchanged disk'}
for name,expected in freeze['files'].items():
    assert digest((package/name).read_bytes()) == expected,name
untracked = set(git('ls-files','--others','--exclude-standard','-z').decode().split('\0'))-{''}
outside = {name for name in untracked if not name.startswith(package.name+'/')}
assert outside == set(launch['preexisting_untracked_paths']), sorted(outside)
subprocess.run(['git','diff','--check'],cwd=root,check=True)
files = [p for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
size = sum(p.stat().st_size for p in files)
assert size < 10_000_000,size
print(json.dumps({'status':'PASS','kind':'packaging/source correspondence only',
    'source_checks':source_checks,'frozen_files_verified':len(freeze['files']),
    'preexisting_untracked_pathnames_preserved':len(outside),
    'protected_contents_read':False,'maintained_files':sorted(changes),
    'current_package_files':len(files),'current_package_bytes':size},indent=2))
