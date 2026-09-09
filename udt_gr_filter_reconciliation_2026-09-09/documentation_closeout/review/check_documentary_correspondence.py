"""Bounded documentary correspondence; no scientific theorem or full365 pass."""
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / 'udt_gr_filter_reconciliation_2026-09-09'
PRIOR = PACKAGE / 'review'
CURRENT = Path(__file__).resolve().parent
BASE = '450d987e22164364e08e5ea0eadaaeaf2dcef096'
SURFACES = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
            'CURRENT_SCIENTIFIC_PREMISES.md', 'INDEX.md', 'MEMORY.md'}

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.packedGitWindowSize=16m',
        '-c', 'core.packedGitLimit=64m', *args], cwd=ROOT, timeout=10)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

pins = [line.split(maxsplit=1) for line in
        (PACKAGE / 'FINAL_IMPLEMENTATION_SHA256SUMS').read_text().splitlines()]
assert len(pins) == 15
for digest, path in pins:
    assert sha(git('show', BASE + ':' + path)) == digest, ('historical_pin', path)
    if path not in SURFACES:
        assert sha((ROOT / path).read_bytes()) == digest, ('unchanged_pin', path)
original_paths = git('ls-tree', '-r', '--name-only', BASE, '--', PACKAGE.name).decode().splitlines()
for path in original_paths:
    assert (ROOT / path).read_bytes() == git('show', BASE + ':' + path), path

old = load(PRIOR / 'guard_probes_initial.stdout')
final = load(PRIOR / 'guard_probes_final.stdout')
now = load(CURRENT / 'current_guard_probes.stdout')
counts = [dict(collections.Counter(r['result'] for r in item['results']))
          for item in (old, final, now)]
assert counts == [dict(FALSE_PASS=13, REJECTED_AS_REQUIRED=44, PASS=14),
                  dict(REJECTED_AS_REQUIRED=56, PASS=15),
                  dict(REJECTED_AS_REQUIRED=56, PASS=15)]
assert old['cases'] == final['cases'] == now['cases'] == 71
assert old['reviewer_source_sha256'] == final['reviewer_source_sha256'] == now['reviewer_source_sha256']
assert final['guard_source_sha256'] == now['guard_source_sha256']
assert final['fixture_source_sha256'] == now['fixture_source_sha256']
reconstructed = load(PRIOR / 'transition_snapshot_reconstructed_old.stdout')
assert reconstructed['chronology'] == 'POST_HOC_FIRST_REPAIR_RECONSTRUCTION_AND_EXECUTION'
assert reconstructed['probe']['false_passes'] == 3
for path in (PRIOR / 'transition_snapshot_first_repair.stdout',
             PRIOR / 'transition_snapshot_final.stdout', CURRENT / 'current_transition_probes.stdout'):
    data = load(path)
    assert data['false_passes'] == 0 and data['actual_transition_text_swaps'] == 0
    assert len(data['results']) == 3
    assert all(r['result'] == 'REJECTED_AS_REQUIRED' for r in data['results'])
utility = load(PRIOR / 'author_utility_final.stdout')
assert utility['count'] == len(utility['checks']) == 189
assert utility['g351_replay']['returncode'] == 0
g351 = json.loads(utility['g351_replay']['stdout'])
assert g351['checks_passed'] == g351['checks_total'] == len(g351['checks']) == 47
assert all(g351['checks'].values()) and g351['failed'] == [] and g351['all_passed']
assert utility['g351_replay']['evidence_before'] == utility['g351_replay']['evidence_after']
assert '106 passed, 248 deselected' in (PRIOR / 'focused_author_tests_final.stdout').read_text()
for path in (PACKAGE / 'COMPLETED_REPAIR_FULL_PREMISE_AUDIT.json',
             PACKAGE / 'documentation_closeout/STARTUP_PREMISE_AUDIT.json'):
    data = load(path)
    assert data['returncode'] == 1 and 'G325 dependency-free replay failed' in data['stderr']
    assert 'replay_exact:DERIVATION_RESULT.json' in data['stderr']

print(json.dumps(dict(status='PASS_DOCUMENTARY_CORRESPONDENCE_ONLY', baseline=BASE,
    original_package_files_unchanged=len(original_paths), historical_final_pins=15,
    unchanged_current_nonstartup_final_pins=9, guard_case_counts=counts,
    preserved_posthoc_false_passes=3, current_transition_rejections=3,
    reused_prior_utility_checks=189, reused_prior_focused_tests=106,
    full365='NOT_PASSED_G325', python=sys.version,
    omitted='No full science rerun; historical seals remain historical; no original review report recovered.'), indent=2))
