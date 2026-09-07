"""Read-only factual closure checks; no scientific audit or theorem replay."""
import collections
import hashlib
import json
import pathlib
import platform
import re
import subprocess
import sys

repo = pathlib.Path('/home/udt-admin/udt_mass_codex')
scratch = pathlib.Path('/tmp/udt-sc-banking-accounting-JVpuu9xS')
old_review = pathlib.Path('/tmp/udt-sc-banking-fidelity-pHLUdApB')
package = 'udt_g357_g360_conditional_banking_2026-09-07'
root = repo / package
baseline = 'ed2f7432f068aa7a72628382b890596b3efba06a'
git = ['git', '-c', 'core.packedGitLimit=64m', '-c', 'core.packedGitWindowSize=8m']
sha = lambda value: hashlib.sha256(value).hexdigest()

manifest_bytes = (root / 'INTEGRATION_CANDIDATE_SHA256SUMS').read_bytes()
assert sha(manifest_bytes) == '9e040712379a96d229af25644b67f64fbb2b4351b6da1c97f5b10a3d3a2702bd'
frozen = {}
for line in manifest_bytes.decode().splitlines():
    expected, rel = line.split('  ', 1)
    actual = (repo / rel).read_bytes()
    assert sha(actual) == expected, rel
    assert subprocess.check_output(git + ['show', ':' + rel], cwd=repo) == actual, rel
    frozen[rel] = expected
assert len(frozen) == 13

audit_bytes = (root / 'CLEAN_PREMISE_AUDIT.json').read_bytes()
audit = json.loads(audit_bytes)
result = audit['result']
assert json.loads(audit['tool_capture']['output']) == result
assert audit['tool_capture']['exit_code'] == 0
assert result['returncode'] == 0 and result['timeout'] is False and result['stderr'] == ''
assert result['command'] == ['/usr/bin/python3', '-B', 'verify_current_scientific_premises.py']
assert result['started_utc'] == '2026-09-07T04:07:50.851390+00:00'
assert result['duration_seconds'] == 398.7381667880036
assert result['maxrss_kib'] == 105792
assert result['address_space_bytes'] == 2147483648 and result['cpu_seconds'] == 900
assert 'PASS: 343-row premise registry' in result['stdout']
assert 'PASS: G357/G358/G359/G360 conditional banking' in result['stdout']

review_manifest = (root / 'review/REVIEW_SHA256SUMS').read_bytes()
assert sha(review_manifest) == '80ee082ed3ec4575b43c021459dfa23eb6d42162706a7d36085cb7788cf7d713'
review_payloads = []
for line in review_manifest.decode().splitlines():
    expected, name = line.split('  ', 1)
    copied = (root / 'review' / name).read_bytes()
    assert sha(copied) == expected and copied == (old_review / name).read_bytes(), name
    review_payloads.append(name)
assert len(review_payloads) == 54
archive = (root / 'review/ARCHIVE_FILES.txt').read_text().splitlines()
assert len(archive) == 55 and set(archive) == set(review_payloads) | {'REVIEW_SHA256SUMS'}
assert all((root / 'review' / name).is_file() for name in archive)
assert not any(path.is_dir() for path in (root / 'review').iterdir())

campaign = 'udt_shared_readout_metric_constraint_campaign_2026-09-06'
source_manifest = (repo / campaign / 'ARTIFACT_SHA256SUMS').read_bytes()
assert sha(source_manifest) == '32daf9c0b69ec4107b310f9275a6bc1e2b674f7c40fb456811f0f6d122a26cfe'
assert source_manifest == subprocess.check_output(git + ['show', baseline + ':' + campaign + '/ARTIFACT_SHA256SUMS'], cwd=repo)
source_payloads = []
for line in source_manifest.decode().splitlines():
    expected, rel = line.split('  ', 1)
    assert sha((repo / rel).read_bytes()) == expected, rel
    source_payloads.append(rel)
assert len(source_payloads) == 441
tracked_source = subprocess.check_output(git + ['ls-tree', '-r', '--name-only', baseline, '--', campaign], cwd=repo).decode().splitlines()
assert set(tracked_source) == set(source_payloads) | {campaign + '/ARTIFACT_SHA256SUMS'}

whitespace = json.loads((root / 'WHITESPACE_CHECK.json').read_text())
strict = json.loads((scratch / 'strict_staged_whitespace.json').read_text())
strict_output = (scratch / 'strict_staged_whitespace.stdout').read_text()
assert strict['returncode'] == whitespace['strict_result']['exit_code'] == 2
assert strict_output == whitespace['strict_result']['output']
assert (scratch / 'strict_staged_whitespace.stderr').read_text() == ''
issues = []
for line in strict_output.splitlines():
    match = re.fullmatch(r'(.+):(\d+): (trailing whitespace|new blank line at EOF)\.', line)
    if match:
        path, number, kind = match.groups()
        issues.append((path, int(number), kind))
counts = dict(collections.Counter(path for path, _, _ in issues))
assert len(issues) == whitespace['warning_count'] == 51
assert counts == whitespace['warning_files']
raw_pytest = package + '/integration/banking_tests.stdout'
raw_diff = package + '/review/reviewed_integration_diff.stdout'
assert counts[raw_pytest] == 3 and counts[raw_diff] == 42
other = [(path, line, kind) for path, line, kind in issues if path not in (raw_pytest, raw_diff)]
assert len(other) == 6 and all(kind == 'new blank line at EOF' for _, _, kind in other)
staged = {}
for path, number, kind in issues:
    if path not in staged:
        staged[path] = subprocess.check_output(git + ['show', ':' + path], cwd=repo)
        assert staged[path] == (repo / path).read_bytes(), path
    data = staged[path]
    if kind == 'trailing whitespace':
        target = data.splitlines()[number - 1]
        assert target.rstrip(b' \t') != target, (path, number)
    else:
        # Git also calls a final whitespace-only diff-context line blank EOF.
        assert data.endswith(b'\n') and data.splitlines()[-1].strip() == b'', path
assert staged[raw_diff] == (old_review / 'reviewed_integration_diff.stdout').read_bytes()
narrow = json.loads((scratch / 'maintained_staged_whitespace.json').read_text())
maintained = ['AGENTS.md', 'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
              'CURRENT_SCIENTIFIC_PREMISES.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv',
              'INDEX.md', 'MEMORY.md', 'verify_current_scientific_premises.py',
              'tests/test_startup_surface.py']
assert narrow['command'] == ['git', 'diff', '--cached', '--check', '--', *maintained]
assert narrow['returncode'] == 0
assert (scratch / 'maintained_staged_whitespace.stdout').read_text() == ''
assert (scratch / 'maintained_staged_whitespace.stderr').read_text() == ''

assembly = json.loads((root / 'REVIEW_ASSEMBLY.json').read_text())
assert assembly['initial_validation']['returncode'] == 1
assert assembly['retry']['exit_code'] == 0
execution_bytes = (root / 'EXECUTION_RECORD.md').read_bytes()
execution = execution_bytes.decode()
for text in ('Clean343-row premise audit PASSED', '398.738166788', '105792KiB',
             'no timeout', 'TWO accidental full-audit launches', 'No completed result or PASS is inferred',
             'complete staged whitespace check returns2 with51 warnings', 'strict check is\nNOT called passed',
             'ten maintained registry', 'scoped commit/push and assembly', 'unstarted and unauthorized'):
    assert text in execution, text

print(json.dumps({
    'result': 'PASS_FACTUAL_CLOSURE_ACCOUNTING_WITH_RETAINED_WHITESPACE_FAILURE',
    'review_context': 'same already-exposed banking fidelity reviewer; no new scientific review',
    'versions': {'python': sys.version, 'platform': platform.platform()},
    'frozen_integration_files_in_worktree_and_index': frozen,
    'frozen_manifest_sha256': sha(manifest_bytes),
    'audit_record_sha256': sha(audit_bytes),
    'audit_actual_result': result,
    'audit_reexecuted': False,
    'copied_review_files': len(archive),
    'copied_review_payloads': len(review_payloads),
    'all_review_bytes_match_original_seal': True,
    'source_campaign_files': len(tracked_source),
    'strict_whitespace_exit_code': strict['returncode'],
    'strict_whitespace_warning_count': len(issues),
    'strict_whitespace_per_file_counts': counts,
    'six_nonraw_warnings_are_blank_eof_only': True,
    'raw_output_warnings': {raw_pytest: 3, raw_diff: 42},
    'maintained_ten_file_whitespace_exit_code': narrow['returncode'],
    'reviewed_execution_sha256': sha(execution_bytes),
    'reviewed_execution_text': execution,
    'read_receipt_hashes': {name: sha((root / name).read_bytes()) for name in ('WHITESPACE_CHECK.json', 'REVIEW_ASSEMBLY.json')},
    'commit_push_outcome': 'not asserted; parent responsibility',
    'scientific_claim_or_premise_changed': False,
}, indent=2))
