"""Bounded packaging correspondence only; no scientific computation or reproof."""
import hashlib
import json
import pathlib
import subprocess

repo = pathlib.Path('/home/udt-admin/udt_mass_codex')
rel = 'udt_shared_readout_metric_constraint_campaign_2026-09-06'
pkg = repo / rel
initial = pathlib.Path('/tmp/tri_closure_fidelity.5CGThc')
pin = '70034a6faa9264bf054eb473d5eb7a0889f3d2de'
roots = ['LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md', 'INDEX.md', 'MEMORY.md']

def git(*args):
    result = subprocess.run(['git', *args], cwd=repo, capture_output=True, check=True)
    return result.stdout.decode()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_manifest(path, base):
    rows = path.read_text().splitlines()
    for row in rows:
        expected, name = row.split('  ', 1)
        assert digest(base / name) == expected, str(base / name)
    print('MANIFEST PASS', str(path.relative_to(repo)), len(rows))

print('HEAD', git('rev-parse', 'HEAD').strip())
print('BRANCH', git('branch', '--show-current').strip())
print('LOCAL TRACKING DIVERGENCE', git('rev-list', '--left-right', '--count', 'HEAD...origin/grok').strip())
check_manifest(pkg / 'CLOSURE_FINAL_INPUT_SHA256SUMS', repo)
check_manifest(pkg / 'PRESERVED_FILES_SHA256SUMS', repo)
check_manifest(pkg / 'closure_review/REVIEW_SHA256SUMS', pkg / 'closure_review')
assert sorted(p.name for p in initial.iterdir()) == sorted(p.name for p in (pkg / 'closure_review').iterdir())
for old in initial.iterdir():
    assert old.is_file() and old.read_bytes() == (pkg / 'closure_review' / old.name).read_bytes(), old.name
for suffix in ['json', 'stdout', 'stderr']:
    assert pathlib.Path(str(initial) + '_seal.' + suffix).read_bytes() == (pkg / ('closure_review_seal.' + suffix)).read_bytes()
print('INITIAL ARCHIVE PASS 17 files including its 16-payload manifest; seal triple byte-identical')
for name in roots:
    assert (repo / name).read_bytes() == (initial / ('initial_' + name)).read_bytes()
for name in ['WORK_ORDER.md', 'CLOSURE_CHECK_PLAN.md']:
    assert (pkg / name).read_bytes() == (initial / ('initial_' + name)).read_bytes()
assert (pkg / 'CLOSURE_REVIEW_INPUT_SHA256SUMS').read_bytes() == (initial / 'INITIAL_INPUT_SHA256SUMS').read_bytes()
print('UNCHANGED ROOTS, WORK ORDER, CLOSURE PLAN AND HISTORICAL INPUT MANIFEST PASS')
for i in range(1, 6):
    step = pkg / f'step_{i:02d}'
    check_manifest(step / 'CANDIDATE_SHA256SUMS', repo)
    check_manifest(step / 'SOURCE_SHA256SUMS', repo)
    check_manifest(step / 'review' / ('SHA256SUMS' if i == 4 else 'REVIEW_SHA256SUMS'), step / 'review')
check_manifest(pkg / 'step_05/repair/REPAIR_SHA256SUMS', repo)
check_manifest(pkg / 'step_05/repair/review/REVIEW_SHA256SUMS', pkg / 'step_05/repair/review')

audit = json.loads((pkg / 'closure_premise_audit.json').read_text())
assert audit['returncode'] == 0 and audit['timeout'] is False
assert audit['address_space_bytes'] == 2 * 1024**3 and audit['cpu_seconds'] == 900
assert audit['command'] == ['/usr/bin/python3', '-B', 'verify_current_scientific_premises.py']
assert audit['cwd'] == str(repo)
for stream in ['stdout', 'stderr']:
    assert audit[stream].encode() == (pkg / ('closure_premise_audit.' + stream)).read_bytes()
assert 'PASS: 339-row premise registry' in audit['stdout'] and audit['stderr'] == ''
print('AUDIT CAPTURE CORRESPONDENCE PASS', audit['duration_seconds'], audit['maxrss_kib'], 'independent audit NOT rerun')
regression = json.loads((pkg / 'closure_startup_regression.json').read_text())
assert regression['returncode'] == 0 and regression['timeout'] is False
assert regression['address_space_bytes'] == 512 * 1024**2 and regression['cpu_seconds'] == 60
assert regression['command'][-3:] == ['tests/test_startup_surface.py', '-k', 'not test_full_foundational_premise_verifier_is_in_pytest']
assert '107 passed, 1 deselected in 1.64s' in (pkg / 'closure_startup_regression.stdout').read_text()
assert (pkg / 'closure_startup_regression.stderr').read_bytes() == b''
print('REGRESSION CAPTURE CORRESPONDENCE PASS', regression['duration_seconds'], 'suite NOT rerun')
preserved = json.loads((pkg / 'closure_preserved_hashes.json').read_text())
assert preserved['returncode'] == 0 and preserved['timeout'] is False
assert (pkg / 'closure_preserved_hashes.stderr').read_bytes() == b''
assert (pkg / 'closure_preserved_hashes.stdout').read_text().splitlines() == [name + ': OK' for name in ['UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv', 'CANON.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv']]
print('PRESERVATION CAPTURE CORRESPONDENCE PASS', preserved['duration_seconds'])

baseline = json.loads((pkg / 'STARTUP_CHECK_RECORD.json').read_text())['baseline_status']['output']
preservation = json.loads((pkg / 'CLOSURE_PRESERVATION_RECORD.json').read_text())
def unrelated(text):
    return sorted(line for line in text.splitlines() if line.startswith('?? ') and not line[3:].startswith(rel + '/'))
current_status = git('status', '--short', '--branch')
assert unrelated(baseline) == unrelated(preservation['status_output']) == unrelated(current_status)
assert len(unrelated(baseline)) == preservation['baseline_unrelated_count'] == preservation['current_unrelated_count'] == 46
assert preservation['metadata_entries_unchanged'] is True
tracked = git('diff', '--name-only', pin).splitlines()
assert len(tracked) == preservation['tracked_changed_path_count'] == 379
assert all(name in roots or name.startswith(rel + '/') for name in tracked)
assert preservation['tracked_diff_scoped'] is True
print('EXACT 46 UNRELATED STATUS ENTRIES AND 379 TRACKED PATHS PASS; metadata only, no protected payload inspected')

whitespace = json.loads((pkg / 'WHITESPACE_CHECK_DISPOSITION.json').read_text())
raw = rel + '/step_05/repair/review/repair_delta.stdout'
for label, extra in [('strict', []), ('narrowed', ['--', '.', ':(exclude)' + raw])]:
    result = subprocess.run(['git', 'diff', '--check', pin, *extra], cwd=repo, capture_output=True)
    prior = whitespace[label + '_result']
    assert result.returncode == prior['exit_code'], label
    assert result.stdout.decode() == prior['output'] and result.stderr == b'', label
    print('WHITESPACE REPLAY', label, result.returncode)
assert whitespace['strict_result']['exit_code'] == 2
assert whitespace['narrowed_result']['exit_code'] == 0
lines = (repo / raw).read_text().splitlines()
assert [i + 1 for i, line in enumerate(lines) if line and not line.strip()] == [10, 16, 18, 19]
print('EXACT IMMUTABLE RAW-DIFF WHITESPACE EXCEPTION PASS; not a strict whole-diff PASS')

for name in ['DECISION_BRIEF.md', 'CAMPAIGN_LOG.md']:
    result = subprocess.run(['diff', '-u', str(initial / ('initial_' + name)), str(pkg / name)], capture_output=True)
    assert result.returncode == 1 and result.stderr == b''
    print('BEGIN REVIEWED FACTUAL DELTA', name)
    print(result.stdout.decode(), end='')
    print('END REVIEWED FACTUAL DELTA', name)
print('ALL BOUNDED FACTUAL CORRESPONDENCE CHECKS PASS; no scientific proof, remote freshness, future commit/push or backup claim')
