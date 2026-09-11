#!/usr/bin/env python3
"""Banking-only correspondence, via Git blobs; never reads protected payloads."""
import datetime
import hashlib
import json
import platform
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
PKG = 'udt_two_shape_nonlinear_interaction_2026-09-11/'
BASE = 'ba934a9b542f818c9032ad37d57b8f7470fe9c9b'
DIRT = '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.preloadindex=false', *args], cwd=ROOT)

assert git('branch', '--show-current').strip() == b'grok'
files = {}
for entry in git('ls-tree', '-rz', BASE, '--', PKG).split(b'\0'):
    if not entry:
        continue
    meta, path = entry.split(b'\t', 1)
    mode, kind, oid = meta.split()
    assert kind == b'blob' and mode == b'100644', (path, mode, kind)
    name = path.decode()
    assert name.startswith(PKG)
    data = (ROOT/name).read_bytes()
    got = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert got == oid.decode(), ('Git original correspondence', name, got, oid.decode())
    files[name] = hashlib.sha256(data).hexdigest()
assert files and not git('diff', '--name-only', BASE, '--', PKG).strip()

freeze = json.loads((ROOT/PKG/'CANDIDATE_FREEZE.json').read_text())
for name, want in freeze['sha256'].items():
    assert hashlib.sha256((ROOT/PKG/name).read_bytes()).hexdigest() == want, name

status = git('status', '--porcelain=v1').decode().splitlines()
own = ('udt_ti1_banking_2026-09-11/', 'udt_two_shape_evolution_2026-09-11/',
       'ti1_banking_guard.py', 'tests/test_ti1_banking.py')
unrelated = [line for line in status if line.startswith('?? ')
             and not any(line[3:].startswith(prefix) for prefix in own)]
fingerprint = hashlib.sha256(('\n'.join(unrelated)+'\n').encode()).hexdigest()
assert len(unrelated) == 46 and fingerprint == DIRT, (len(unrelated), fingerprint)

replays = {}
for now, old in [('replay_metric_jet', 'review/metric_jet'),
                 ('replay_pair_records', 'checks/parent_records')]:
    receipt = json.loads((REVIEW/(now+'.json')).read_text())
    assert receipt['returncode'] == 0 and receipt['timeout'] is False
    assert not (REVIEW/(now+'.stderr')).read_bytes()
    data = (REVIEW/(now+'.stdout')).read_bytes()
    assert data == (ROOT/PKG/(old+'.stdout')).read_bytes(), now
    replays[now] = {'receipt': receipt, 'stdout_sha256': hashlib.sha256(data).hexdigest(),
                    'comparison': 'EXACT_ORIGINAL_STDOUT_BYTES', 'meaning': 'SAME_CODE_REGRESSION'}

print(json.dumps({'status': 'PASS', 'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'python': platform.python_version(), 'git_version': git('--version').decode().strip(),
 'branch': 'grok', 'head': git('rev-parse', 'HEAD').decode().strip(), 'baseline': BASE,
 'original_package_tracked_files': len(files), 'original_package_sha256': files,
 'candidate_freeze_pins': len(freeze['sha256']), 'original46_count': len(unrelated),
 'original46_status_sha256': fingerprint, 'protected_payloads': 'NOT_READ_OR_HASHED',
 'backup_completeness': 'UNVERIFIED', 'replays': replays}, indent=2))
