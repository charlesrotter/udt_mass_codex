"""FEP1 byte/scope correspondence only; no scientific truth certification."""
from pathlib import Path
import csv
import datetime
import hashlib
import json
import platform
import subprocess
import sys

root = Path.cwd()
p = Path(__file__).resolve().parent.relative_to(root)
read = lambda name: json.loads((p / name).read_text())
sha = lambda data: hashlib.sha256(data).hexdigest()
git = lambda *args: subprocess.check_output(['git', *args])
launch = read('LAUNCH.json')
base = launch['head']
checks = {}
assert git('rev-parse', '--abbrev-ref', 'HEAD').decode().strip() == 'grok'
checks['branch_grok'] = True
for label, pins in [('source_pins', read('SOURCE_PINS.json')),
                    ('fixed_launch_pins', launch['source_snapshot'])]:
    for name, expected in pins.items():
        assert sha(Path(name).read_bytes()) == expected, name
        assert sha(git('show', base + ':' + name)) == expected, name
    checks[label + '_disk_and_baseline_match'] = len(pins)
for name in ['LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md']:
    assert Path(name).read_bytes() == git('show', base + ':' + name), name
checks['current_scientific_status_unchanged'] = True
before = read('PLAN_BEFORE.json')
assert sha(before['content'].encode()) == before['sha256']
assert git('show', base + ':' + before['path']) == before['content'].encode()
checks['original_plan_snapshot_exact'] = True
initial = read('reviews/INITIAL_FREEZE.json')
for name, expected in initial['drafts'].items():
    assert sha((p / 'reviews/initial' / Path(name).name).read_bytes()) == expected
checks['initial_review_snapshots_exact'] = len(initial['drafts'])
with open('CURRENT_SCIENTIFIC_PREMISES.tsv') as f:
    current = {r['premise_id']: r for r in csv.DictReader(f, delimiter='\t')}
with (p / 'SELECTED_PREMISES.tsv').open() as f:
    selected = list(csv.DictReader(f, delimiter='\t'))
assert all(r == current[r['premise_id']] for r in selected)
checks['exact_selected_registry_rows'] = len(selected)
with (p / 'ROUTE_LEDGER.tsv').open() as f:
    routes = list(csv.DictReader(f, delimiter='\t'))
assert len({r['route_id'] for r in routes}) == len(routes)
assert all(Path(r['source']).is_file() for r in routes)
checks['unique_routes_with_existing_source'] = len(routes)
status = git('status', '--short', '--untracked-files=all').decode()
outside = ''.join(line + '\n' for line in status.splitlines()
                  if line.startswith('?? ') and not line[3:].startswith(str(p) + '/'))
assert outside == launch['original_untracked_status']
checks['original_untracked_name_count'] = len(outside.splitlines())
checks['original_untracked_status_sha256'] = sha(outside.encode())
allowed = {'INDEX.md', 'MEMORY.md', 'UDT_RESEARCH_ROADMAP.md', before['path']}
changed = set(git('diff', base, '--name-only').decode().splitlines())
assert all(name in allowed or name.startswith(str(p) + '/') for name in changed)
checks['tracked_change_scope'] = sorted(changed)
for name in ['checks/premise406.json', 'checks/navigation.json']:
    result = read(name)
    assert result['returncode'] == 0 and not result['timeout']
    checks[name] = {'returncode': 0, 'duration_seconds': result['duration_seconds']}
checks['result'] = 'PASS_DOCUMENTARY_CORRESPONDENCE_ONLY'
checks['utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
checks['baseline_head'] = base
checks['python'] = sys.version
checks['platform'] = platform.platform()
print(json.dumps(checks, indent=2))
