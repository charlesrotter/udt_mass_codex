"""Stage B read-only authentication and proportional sequential exact replays.

Writes execution artifacts only to the explicitly authorized scratch directory.
This checks byte identity and finite regression, not the general analytic proof.
"""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

repo = Path('/home/udt-admin/udt_mass_codex')
scratch = Path('/tmp/udt-cone-review-0WvbvE')
package = Path('udt_g349_normalized_cone_phase_extension_candidate_2026-09-06')
snapshot = 'f14098737a7bd571aff79bef09ccffdc22135853'
declared_source_snapshot = '5ef2f971805ee23383cad694c5cb058124614a5d'
digest = lambda data: hashlib.sha256(data).hexdigest()

def git_bytes(rev, path):
    return subprocess.run(['git', 'show', f'{rev}:{path}'], cwd=repo,
                          check=True, capture_output=True, timeout=20).stdout

artifact_rows = []
for line in (repo/package/'ARTIFACT_SHA256SUMS').read_text().splitlines():
    expected, path = line.split(None, 1)
    live = (repo/path).read_bytes()
    pinned = git_bytes(snapshot, path)
    item = {'path': path, 'expected_sha256': expected,
            'live_sha256': digest(live), 'snapshot_sha256': digest(pinned)}
    assert expected == digest(live) == digest(pinned), item
    artifact_rows.append(item)
manifest_path = package/'ARTIFACT_SHA256SUMS'
manifest_live = (repo/manifest_path).read_bytes()
manifest_git = git_bytes(snapshot, manifest_path)
assert manifest_live == manifest_git
source_rows = []
for line in (repo/package/'SOURCE_SHA256SUMS').read_text().splitlines():
    expected, path = line.split(None, 1)
    live_hash = digest((repo/path).read_bytes())
    review_hash = digest(git_bytes(snapshot, path))
    source_hash = digest(git_bytes(declared_source_snapshot, path))
    assert expected == review_hash == source_hash, path
    if path != 'AGENTS.md':
        assert expected == live_hash, path
    source_rows.append({'path': path, 'expected_sha256': expected,
                        'live_sha256': live_hash, 'review_snapshot_sha256': review_hash,
                        'declared_source_snapshot_sha256': source_hash,
                        'live_matches_historical': live_hash == expected})
auth = {'artifact_payloads': artifact_rows,
        'artifact_manifest_sha256': digest(manifest_live),
        'artifact_manifest_matches_pinned_git': True,
        'sources': source_rows,
        'scope': 'all original 15 package files; review directory not inspected',
        'source_exception': 'AGENTS live method-only change; historical bytes verified in Git'}
(scratch/'STAGE_B_AUTHENTICATION.json').write_text(json.dumps(auth, indent=2)+'\n')

def capture(name, command):
    start = time.monotonic()
    completed = subprocess.run(command, cwd=repo, text=True, capture_output=True, timeout=60)
    record = {'command': command, 'cwd': str(repo), 'returncode': completed.returncode,
              'elapsed_seconds': time.monotonic()-start,
              'stdout': completed.stdout, 'stderr': completed.stderr}
    (scratch/name).write_text(json.dumps(record, indent=2)+'\n')
    return record

runner = capture('STAGE_B_CAPTURE_RUNNER.json', [sys.executable, str(repo/package/'run_checks.py')])
assert runner['returncode'] == 0 and runner['stderr'] == ''
runs = json.loads(runner['stdout'])['runs']
expected_names = {
    'acceleration_zero': 'nonaffine_nonzero_component',
    'pullback_only': 'matching_rejects_hidden_factor_two',
    'omit_frequency': 'absolute_rate_second_cut',
    'area_radius': 'metric_area_not_radius'}
assert len(runs) == 5
baseline = runs[0]
assert baseline['mutation'] is None and baseline['returncode'] == 0 and baseline['stderr'] == ''
baseline_json = json.loads(baseline['stdout'])
assert baseline_json == json.loads((repo/package/'CHECK_RESULT.json').read_text())
mutation_results = []
for child in runs[1:]:
    intended = expected_names[child['mutation']]
    assert child['returncode'] == 1 and child['stdout'] == ''
    assert child['stderr'].rstrip().endswith('AssertionError: '+intended)
    mutation_results.append({'mutation': child['mutation'], 'caught_at': intended})
recompute = capture('STAGE_B_SAVED_RECOMPUTATION.json',
                    [sys.executable, str(repo/package/'recompute_saved.py')])
assert recompute['returncode'] == 0 and recompute['stderr'] == ''
recomputed_json = json.loads(recompute['stdout'])
assert recomputed_json['results'] == baseline_json['readout_outputs']
summary = {'python': platform.python_version(), 'executable': sys.executable,
           'original_payload_count': len(artifact_rows),
           'manifest_git_match': True, 'source_count': len(source_rows),
           'historical_source_matches': len(source_rows),
           'live_source_matches': sum(x['live_matches_historical'] for x in source_rows),
           'artifact_manifest_sha256': digest(manifest_live),
           'baseline_exact_saved_output_match': True,
           'baseline_assertion_count': baseline_json['assertion_count'],
           'mutations': mutation_results, 'saved_readout_recomputation': recomputed_json,
           'ceiling': 'Byte authentication and explicit finite child outcomes only.'}
print(json.dumps(summary, indent=2))
