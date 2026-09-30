"""Read-only final CES1 integration correspondence; no scientific reproof."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root))
import verify_udt_development as v

base = root / 'udt_clock_ensemble_stationarity_test_2026-09-30'
freeze_path = base / 'INTEGRATION_FREEZE.json'
freeze = json.loads(freeze_path.read_text())
accepted = freeze['accepted_sha256']
bad = [p for p, h in accepted.items()
       if hashlib.sha256((root / p).read_bytes()).hexdigest() != h]
assert not bad, bad
previous = json.loads((base / 'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert not set(previous) - set(accepted), 'previous reviewed paths omitted'
changed = {p for p in previous if previous[p] != accepted[p]}
assert changed == set(freeze['changed_preexisting_files']), changed
unchanged = set(previous) - changed
added = set(accepted) - set(previous)

candidate = json.loads((base / 'CANDIDATE_FREEZE.json').read_text())['sha256']
assert all(hashlib.sha256((root / p).read_bytes()).hexdigest() == h
           for p, h in candidate.items())
assert (root / 'CURRENT_RESEARCH_PROGRAM.md').read_text() == v.program_text(
    (root / 'UDT_DEVELOPMENT.md').read_text())

baseline = 'c4bdbead3eb1f0387fe75cc2fcf41fcf49e9c2aa'
preserved = {}
for p in ['CURRENT_SCIENTIFIC_PREMISES.tsv', 'CANON.md', 'founding.md']:
    original = subprocess.check_output(['git', 'show', baseline + ':' + p], cwd=root)
    preserved[p] = original == (root / p).read_bytes()
assert all(preserved.values()), preserved

print(json.dumps({
    'status': 'PASS', 'scope': 'Integration byte correspondence and inherited-review routing',
    'python': platform.python_version(),
    'integration_freeze_sha256': hashlib.sha256(freeze_path.read_bytes()).hexdigest(),
    'accepted_paths_verified': len(accepted), 'previous_paths': len(previous),
    'unchanged_inherited_paths': len(unchanged), 'changed_preexisting_paths': sorted(changed),
    'added_paths': len(added), 'candidate_freeze_entries_verified': len(candidate),
    'generated_orientation_matches': True, 'unchanged_against_launch': preserved,
    'limits': ['Hashes are not scientific proof or semantic completeness',
               'Other CES1 reviewer content hashed, not read',
               'Prior source reviews inherited at their original scope only',
               'Full premise audit, final normal guard, commit and push not performed here']
}, indent=2))
