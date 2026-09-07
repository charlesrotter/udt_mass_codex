"""Read-only final banking snapshot correspondence, independent of author guard."""
import csv
import hashlib
import io
import json
import pathlib
import subprocess

repo = pathlib.Path('/home/udt-admin/udt_mass_codex')
scratch = pathlib.Path('/tmp/udt-sc-banking-fidelity-pHLUdApB')
banking = 'udt_g357_g360_conditional_banking_2026-09-07'
baseline = 'ed2f7432f068aa7a72628382b890596b3efba06a'
git = ['git', '-c', 'core.packedGitLimit=64m', '-c', 'core.packedGitWindowSize=8m']
sha = lambda data: hashlib.sha256(data).hexdigest()
manifest = (repo / banking / 'INTEGRATION_CANDIDATE_SHA256SUMS').read_bytes()
entries = [line.split('  ', 1) for line in manifest.decode().splitlines()]
assert len(entries) == len({path for _, path in entries}) == 13
files = {}
for expected, rel in entries:
    data = (repo / rel).read_bytes()
    assert sha(data) == expected, rel
    files[rel] = expected
initial = json.loads((scratch / 'initial_input_authentication.stdout').read_text())
for rel, previous in initial['new_documents_for_fidelity_review'].items():
    assert files[rel] == previous['sha256'], rel
for rel, expected in initial['reviewed_scientific_source_hashes'].items():
    assert sha((repo / rel).read_bytes()) == expected, rel

ids = ('G357', 'G358', 'G359', 'G360')
raw = (repo / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
old = b''.join(line for line in raw.splitlines(keepends=True)
               if not line.startswith(tuple((i + '\t').encode() for i in ids)))
pinned = subprocess.check_output(git + ['show', baseline + ':CURRENT_SCIENTIFIC_PREMISES.tsv'], cwd=repo)
assert old == pinned
assert sha(old) == '23096ecbbdace34bb9f3add2cc288c9c62edd264a096620955be04b0510a7429'
rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter='\t'))
by_id = {row['premise_id']: row for row in rows}
assert len(rows) == len(by_id) == 343
assert len(old.splitlines()) - 1 == 339
prior_ids = {row['premise_id'] for row in csv.DictReader(io.StringIO(old.decode()), delimiter='\t')}
assert set(by_id) - prior_ids == set(ids)
for i in ids:
    assert by_id[i]['current_status'] == 'BANKED_DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS__OWNER_AUTHORIZED__NOT_PHYSICAL_ADOPTION__NOT_CANON'
    assert by_id[i]['controlling_source'] == banking + '/BANKING_RECORD.md'
fixed = {}
for rel in ('UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv', 'CANON.md'):
    data = (repo / rel).read_bytes()
    assert data == subprocess.check_output(git + ['show', baseline + ':' + rel], cwd=repo)
    fixed[rel] = sha(data)
execution = (repo / banking / 'EXECUTION_RECORD.md').read_bytes()
tests = json.loads((scratch / 'scoped_integration_tests_isolated.json').read_text())
test_stdout = (scratch / 'scoped_integration_tests_isolated.stdout').read_text()
assert tests['returncode'] == 0 and not tests['timeout']
assert '48 passed, 108 deselected' in test_stdout

print(json.dumps({
    'result': 'PASS_CORRESPONDENCE_ONLY',
    'baseline': baseline,
    'frozen_integration_manifest_sha256': sha(manifest),
    'thirteen_frozen_file_hashes': files,
    'new_documents_unchanged_since_initial_direct_review': True,
    'scientific_sources_unchanged_since_source_authentication': True,
    'registry_rows': len(rows),
    'old_registry_rows_byte_identical': 339,
    'new_ids_only': ids,
    'sc1_has_no_new_result_row': True,
    'fixed_manuscript_sidecar_canon_hashes': fixed,
    'execution_record_reviewed_sha256': sha(execution),
    'execution_record_reviewed_text': execution.decode(),
    'scoped_regression_tests': {'passed': 48, 'deselected': 108, 'new_full_audit_executed': False},
    'review_procedural_violation': 'Two earlier accidental full audits were stopped and never used for a gate; see separate disposition.',
    'banking_completion': 'NOT_ASSERTED; parent clean final audit, closure and commit/push remain separate',
}, indent=2))
