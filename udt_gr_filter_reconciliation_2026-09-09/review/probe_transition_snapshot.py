"""Supplemental SAME-R2 probe: parse only authenticated transition bytes."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

R = Path(__file__).resolve().parent
ROOT = R.parents[1]
sys.path.insert(0, str(ROOT))
import verify_current_scientific_premises as guard
spec = importlib.util.spec_from_file_location('shared_fixture', ROOT / 'tests/test_startup_surface.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
baseline = subprocess.run(['git', '-c', 'core.preloadIndex=false', '-c',
    'index.threads=1', '-c', 'core.packedGitWindowSize=16m', '-c',
    'core.packedGitLimit=64m', 'show',
    'a9896cb190e9c4aa8fd8a317cfaaa942d64e0a19:CURRENT_SCIENTIFIC_PREMISES.tsv'],
    cwd=ROOT, capture_output=True, check=True, timeout=10).stdout
results = []
with tempfile.TemporaryDirectory(prefix='udt-gr-transition-snapshot-review-') as temporary:
    root = fixture._startup_copy(Path(temporary))
    guard.validate_startup_surface(root)
    registry = root / 'CURRENT_SCIENTIFIC_PREMISES.tsv'
    transition_path = root / guard.GR_FILTER_TRANSITION_SOURCE
    transition = json.loads(transition_path.read_text())
    clean = registry.read_bytes()
    headers = clean.decode().splitlines()[0].split('\t')
    row = transition['after_line'].rstrip('\n').split('\t')
    row[headers.index('active_use')] = 'CURRENT_ACTIVE_FULL_QUIET_GR_RESPONSE_CONSTRUCTION_INPUT'
    unauthorized_line = '\t'.join(row) + '\n'
    registry.write_bytes(clean.replace(transition['after_line'].encode(), unauthorized_line.encode()))
    forged = dict(transition, after_line=unauthorized_line)
    original_text = Path.read_text
    text_swaps = [0]
    def swapped_text(path, *args, **kwargs):
        if path == transition_path:
            text_swaps[0] += 1
            return json.dumps(forged)
        return original_text(path, *args, **kwargs)
    actions = [
        ('current_authority', lambda: guard.validate_gr_filter_authority(root)),
        ('historical_projection', lambda: guard.registry_bytes_for_historical_banking(root)),
        ('full_startup', lambda: guard.validate_startup_surface(root)),
    ]
    with patch.object(Path, 'read_text', swapped_text):
        for name, action in actions:
            try:
                value = action()
            except SystemExit as error:
                results.append({'case': name, 'result': 'REJECTED_AS_REQUIRED', 'message': str(error)})
            else:
                item = {'case': name, 'result': 'FALSE_PASS'}
                if name == 'historical_projection':
                    item['unauthorized_current_row_projects_to_exact_valid_baseline'] = value == baseline
                results.append(item)
    registry.write_bytes(clean)
    assert transition_path.read_bytes() == (ROOT / guard.GR_FILTER_TRANSITION_SOURCE).read_bytes()
failures = sum(r['result'] == 'FALSE_PASS' for r in results)
print(json.dumps({'scope': 'incomplete same R2 authenticated snapshot implementation',
    'injection': 'read_bytes hashes authentic transition; read_text supplies unpinned after_line '
       'matching an actual unauthorized scratch G312 row',
    'actual_transition_text_swaps': text_swaps[0], 'cases': len(results),
    'false_passes': failures, 'results': results,
    'no_claim_of_actual_repository_race': True}, indent=2))
raise SystemExit(1 if failures else 0)
