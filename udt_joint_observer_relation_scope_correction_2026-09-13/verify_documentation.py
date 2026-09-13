"""JRC1 documentary correspondence, adapted from the pinned FE1 utility.
Checks preservation and exact records; not a scientific or admission verifier.
"""
from pathlib import Path
import csv
import datetime
import hashlib
import json
import platform
import subprocess
import sys

p = Path(__file__).resolve().parent.relative_to(Path.cwd())
read = lambda n: json.loads((p / n).read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
git = lambda *a: subprocess.check_output(['git', *a])
launch = read('LAUNCH.json')
base = launch['head']
checks = {}
assert git('rev-parse', '--abbrev-ref', 'HEAD').decode().strip() == 'grok'
assert not git('diff', '--cached', '--name-only').strip()
for label, pins in [('source', read('SOURCE_PINS.json')),
                    ('fixed', read('FIXED_PINS.json'))]:
    for n, expected in pins.items():
        assert sha(Path(n).read_bytes()) == expected, n
        assert sha(git('show', base + ':' + n)) == expected, n
    checks[label + '_disk_and_baseline_pins'] = len(pins)
before = read('MAINTAINED_BEFORE.json')
for n, old in before.items():
    assert sha(old['content'].encode()) == old['sha256'], n
    assert git('show', base + ':' + n) == old['content'].encode(), n
checks['maintained_before_snapshots'] = len(before)
initial = read('review/INITIAL_FREEZE.json')
for i, (n, expected) in enumerate(initial['files'].items()):
    assert sha((p / 'review/initial' / f'{i:02d}_{Path(n).name}').read_bytes()) == expected
checks['initial_review_snapshots_exact'] = len(initial['files'])
final = read('review/FINAL_CANDIDATE_FREEZE.json')
for n, expected in final['files'].items():
    assert sha(Path(n).read_bytes()) == expected, n
checks['final_review_candidate_hashes_exact'] = len(final['files'])
with open('CURRENT_SCIENTIFIC_PREMISES.tsv') as f:
    current = {r['premise_id']: r for r in csv.DictReader(f, delimiter='\t')}
with (p / 'SELECTED_PREMISES.tsv').open() as f:
    selected = list(csv.DictReader(f, delimiter='\t'))
assert len(current) == 406 and len(selected) == 12
assert all(r == current[r['premise_id']] for r in selected)
checks['exact_complete_selected_registry_rows'] = len(selected)
status = git('status', '--short', '--untracked-files=all').decode()
outside = ''.join(line + '\n' for line in status.splitlines()
                  if line.startswith('?? ') and not line[3:].startswith(str(p) + '/'))
assert outside == launch['original_untracked_status']
checks['original_untracked_names'] = len(outside.splitlines())
checks['original_untracked_name_sha256'] = sha(outside.encode())
changed = set(git('diff', base, '--name-only').decode().splitlines())
assert all(n in before or n.startswith(str(p) + '/') for n in changed)
checks['tracked_change_scope'] = sorted(changed)
premise = read('checks/premise_execution.json')
assert premise['exit_code'] == 0
checks['premise_actual_execution'] = premise
nav = read('checks/navigation_final/json')
assert nav['returncode'] == 0 and not nav['timeout']
checks['navigation_actual_execution'] = nav
for n in ['checks/navigation_initial/json', 'checks/navigation_compaction_attempt/json']:
    assert read(n)['returncode'] == 1
checks['two_documentary_failures_preserved'] = True
review = read('review/FINAL_REVIEW.json')
assert review['reviewed_files'] == final['files']
assert review['verdict'] == 'VERIFIED-WITH-CAVEATS'
checks['separate_context_review_hash_correspondence'] = True
checks['utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
checks['baseline_head'] = base
checks['python'] = sys.version
checks['platform'] = platform.platform()
checks['result'] = 'PASS_DOCUMENTARY_CORRESPONDENCE_ONLY'
print(json.dumps(checks, indent=2))
