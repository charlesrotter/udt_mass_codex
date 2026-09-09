"""Authenticate repair delta, original false passes and unchanged authority."""
import hashlib
import json
from pathlib import Path
import subprocess

R = Path(__file__).resolve().parent
P = R.parent
ROOT = P.parent
BASE = 'a9896cb190e9c4aa8fd8a317cfaaa942d64e0a19'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pins(name):
    return {path: sha for sha, path in [line.split(maxsplit=1)
            for line in (P / name).read_text().splitlines()]}

initial = pins('INITIAL_IMPLEMENTATION_SHA256SUMS')
final = pins('REPAIRED_IMPLEMENTATION_SHA256SUMS')
assert len(initial) == 12 and len(final) == 14
for path, expected in final.items():
    assert digest(ROOT / path) == expected, path
changed = []
for path, expected in initial.items():
    if digest(ROOT / path) != expected:
        changed.append(path)
assert set(changed) == {'verify_current_scientific_premises.py', 'tests/test_startup_surface.py'}
assert digest(P / 'INITIAL_IMPLEMENTATION.patch') == \
    '2922c2094a152f36e186f1dd2e10afe7f4ee5c41c0c31217da136ba64980a618'
assert digest(R / 'INITIAL_DIRECT_REVIEW.md') == \
    '62911679ec20805b41326b40c7496949af5995deba3a4ba35af078e428a0570b'
assert digest(R / 'probe_guards.py') == \
    '01c00ab87bbe14ff7a355046401cdeff70d90e866b808dfac092e709d6186137'
old_probe = json.loads((R / 'guard_probes_initial.stdout').read_text())
new_probe = json.loads((R / 'guard_probes_repaired.stdout').read_text())
assert old_probe['cases'] == new_probe['cases'] == 71
assert old_probe['reviewer_source_sha256'] == new_probe['reviewer_source_sha256']
assert old_probe['failures'] == 13 and new_probe['failures'] == 0
assert {r['name'] for r in old_probe['results']} == {r['name'] for r in new_probe['results']}
assert sum(r['result'] == 'REJECTED_AS_REQUIRED' for r in new_probe['results']) == 56
assert sum(r['result'] == 'PASS' for r in new_probe['results']) == 15
assert old_probe['results'][-1]['reads'] == 2 and new_probe['results'][-1]['reads'] == 1
root_paths = sorted(path for path in initial if '/' not in path or path == 'tests/test_startup_surface.py')
result = subprocess.run(['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1',
    'diff', '--binary', BASE, '--', *root_paths], cwd=ROOT,
    capture_output=True, check=True, timeout=10)
assert result.stdout == (P / 'REPAIRED_IMPLEMENTATION.patch').read_bytes()
print(json.dumps({'status': 'PASS', 'repaired_pins': 14,
    'only_initial_candidate_files_changed': changed,
    'same_reviewer_probe_source': True, 'retained_initial_false_passes': 13,
    'repaired_intended_rejections': 56, 'repaired_positive_controls': 15,
    'registry_reads_initial': 2, 'registry_reads_repaired': 1,
    'read_swap_reporting_note': 'Original projected==baseline boolean retains its old field name; '
      'the repaired one-read path never consumes the injected poisoned second snapshot.',
    'scope': 'repair correspondence and finite regression, not semantic completeness or proof'}, indent=2))
