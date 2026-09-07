"""Scoped return/preservation regression; not a new scientific verifier."""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
assert pathlib.Path.cwd() == ROOT, 'run from repository root'
sys.path.insert(0, str(ROOT))
import verify_current_scientific_premises as premises
PACKAGE = ROOT / 'udt_local_clock_metric_benchmark_campaign_2026-09-07'
PREFIX = PACKAGE.name + '/'
BASELINE = '46955846e76975fbef374ef702527f8e7389bc35'
GIT = ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1']


def git(*args):
    return subprocess.check_output(GIT + list(args), text=True, cwd=ROOT)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


premises.validate_startup_surface(ROOT)
assert git('branch', '--show-current').strip() == 'grok'
changed = git('diff', '--name-only', BASELINE).splitlines()
allowed_roots = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md'}
assert all(p in allowed_roots or p.startswith(PREFIX) for p in changed), changed
for root_name in allowed_roots:
    text = (ROOT / root_name).read_text()
    assert 'COMPLETE at two fresh-reviewed steps' in text
    assert 'no new campaign is authorized' in text

expected_science = {
    'CURRENT_SCIENTIFIC_PREMISES.tsv': 'ccd1fd2752a5884dfa2864fc9f3904f9dcc7e22557f6d4057e92ec2c54caf81f',
    'CANON.md': '047b7fbbc1acacf01d2716e3c98cdefd0b9b20136ac4a3306f55dd6775465250',
    'UDT_METRIC_KERNEL_DEVELOPMENT.md': '3b625d8f43620a37c99d9f4f0fdc9390c3a12306b1da87281c143ce84d40a81e',
    'UDT_METRIC_KERNEL_COVERAGE.tsv': 'b9a8d84d58b60dd6381af6512d89a63c8fa26750f0068e444dd039d329e74bc4',
    'AGENTS.md': '4b30e3d839d546299e2177fa33dcdc7f0a5305feb78a4c1f48bde11043b7b43d',
    'CLAUDE.md': 'b7e524a5b06760e57877a408630228767ae9a394134095f9851bef5d06e17751',
    'verify_current_scientific_premises.py': 'fd99b85a4d0bfb9548ecea5d3f358c7cbc7b96319b38b4114c43429296a24f5c',
    'udt_goce_submission_and_independent_campaign_proposal_2026-09-07/ESA_ENQUIRY.md': '6c21f117209c4c69587dc34256cd4d8daaea1058aef532853b2aee0deb8664f4',
}
actual_science = {p: sha(ROOT / p) for p in expected_science}
assert actual_science == expected_science

# Names only: protected/unrelated payloads are never read or hashed.
baseline_status = json.loads((PACKAGE / 'BASELINE_STATUS_METADATA.json').read_text())
untracked = [line for line in git('status', '--short').splitlines()
             if line.startswith('?? ') and not line[3:].startswith(PREFIX)]
status_hash = hashlib.sha256('\n'.join(sorted(untracked)).encode()).hexdigest()
assert len(untracked) == baseline_status['count'] == 46
assert status_hash == baseline_status['sha256']

freeze = PACKAGE / 'step_01/FREEZE_MANIFEST.sha256'
frozen = []
for line in freeze.read_text().splitlines():
    expected, relative = line.split('  ', 1)
    assert relative.startswith(PREFIX + 'step_01/')
    assert sha(ROOT / relative) == expected
    frozen.append(relative)

initial_pins = {
    'step_02/INITIAL_evaluate_benchmark.py': '27c87e02c3cc2591b6735ef80e9fb40161cbf234733263600105271db2d65240',
    'step_02/INITIAL_CANDIDATE_RESULT.md': 'c55bf4a085d9c94a50e9f2cb9b168c03143b15304beb52a9be596f7a38982710',
    'INITIAL_DECISION_BRIEF.md': 'e698a87014c4de8ed2d6fc92ee44e9c78500736c6cbe2216ed6708a85f276bcb',
}
assert all(sha(PACKAGE / p) == value for p, value in initial_pins.items())
initial = json.loads((PACKAGE / 'step_02/benchmark_run.stdout').read_text())
repaired = json.loads((PACKAGE / 'step_02/repair_run.stdout').read_text())
assert initial['result'] == repaired['result']
assert initial['limits'] == repaired['limits']
assert len(initial['catch_proofs']) == 7 and len(repaired['catch_proofs']) == 11
assert all(row['rejected'] for row in repaired['catch_proofs'])
json_paths = sorted(PACKAGE.rglob('*.json'))
for path in json_paths:
    json.loads(path.read_text())

print(json.dumps({
    'status': 'PASS_SCOPED_RETURN_AND_PRESERVATION_REGRESSION',
    'scope': 'Startup-surface check, unchanged-source hashes, name-only dirt, freeze and repair correspondence; not a full premise replay or experimental verification',
    'baseline': BASELINE, 'branch': 'grok',
    'allowed_tracked_diff': changed,
    'unchanged_source_hashes': actual_science,
    'unrelated_untracked_name_count': len(untracked),
    'unrelated_untracked_name_hash': status_hash,
    'protected_payloads_read_or_hashed': False,
    'immutable_LC1_entries_verified': len(frozen),
    'initial_candidate_hashes_preserved': initial_pins,
    'scientific_result_and_limits_exactly_unchanged_by_R1': True,
    'initial_and_repaired_mutation_counts': [7, 11],
    'JSON_files_parsed': [str(p.relative_to(ROOT)) for p in json_paths],
    'backup_completeness': 'UNVERIFIED',
    'pre_reboot_unsaved_state_disposition': 'UNVERIFIED',
    'host_wide_process_inventory': 'UNVERIFIED',
    'ScratchDisk': 'unused; blocker only for archive-dependent tasks',
}, indent=2))
