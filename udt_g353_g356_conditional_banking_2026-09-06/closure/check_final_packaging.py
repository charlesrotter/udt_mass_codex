"""Read-only final status diff and staged diff-artifact whitespace diagnostic."""
import difflib
import hashlib
import json
import pathlib
import re
import subprocess

root = pathlib.Path('/home/udt-admin/udt_mass_codex')
prior = pathlib.Path('/tmp/udt-banking-fidelity-meEiJ3/sealed')
bankname = 'udt_g353_g356_conditional_banking_2026-09-06'
bank = root / bankname
manifest = prior / 'integration_candidate' / bankname / 'INTEGRATION_CANDIDATE_SHA256SUMS'
allowed = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
           'CURRENT_SCIENTIFIC_PREMISES.md', 'MEMORY.md', bankname + '/BANKING_RECORD.md'}
changed = []
unchanged = []
for line in manifest.read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    before = prior / 'integration_candidate' / name
    a, b = before.read_bytes(), (root / name).read_bytes()
    assert hashlib.sha256(a).hexdigest() == expected
    if a != b:
        assert name in allowed, ('unallowed final target change', name)
        changed.append(dict(path=name, sha256=hashlib.sha256(b).hexdigest(),
                            diff=''.join(difflib.unified_diff(a.decode().splitlines(True),
                                b.decode().splitlines(True), fromfile='reviewed/' + name,
                                tofile='final/' + name))))
    else:
        unchanged.append(name)
assert {entry['path'] for entry in changed} == allowed
old_exec = (prior / 'INITIAL_EXECUTION_RECORD.md').read_text()
new_exec = (bank / 'EXECUTION_RECORD.md').read_text()
execution_diff = ''.join(difflib.unified_diff(old_exec.splitlines(True), new_exec.splitlines(True),
                                            fromfile='reviewed/EXECUTION_RECORD.md',
                                            tofile='final/EXECUTION_RECORD.md'))
patch_name = bankname + '/integration/IMPLEMENTATION_DIFF.patch'
patch = (root / patch_name).read_bytes()
assert hashlib.sha256(patch).hexdigest() == '44e82bb07ad2888a51adefed0637bddfec1ea37fe2f6207c4601368853b95f9c'
base = ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1',
        'diff', '--cached', '--check']
whole = subprocess.run(base, cwd=root, capture_output=True, text=True)
assert whole.returncode == 2, ('whole-stage unexpected result', whole.returncode, whole.stderr)
locations = []
for line in whole.stdout.splitlines():
    if line.startswith('+'):
        continue
    match = re.fullmatch(re.escape(patch_name) + r':(\d+): (trailing whitespace\.|new blank line at EOF\.)', line)
    assert match, ('unexpected whitespace finding', line)
    number = int(match.group(1))
    assert patch.splitlines()[number-1] == b' ', ('not blank-context syntax', number)
    locations.append(number)
assert locations
assert not whole.stderr
scoped_command = base + ['--', '.', ':!' + patch_name]
scoped = subprocess.run(scoped_command, cwd=root, capture_output=True, text=True)
assert scoped.returncode == 0 and not scoped.stdout and not scoped.stderr
assert (bank / 'INTEGRATION_CANDIDATE_SHA256SUMS').read_bytes() == manifest.read_bytes()
print(json.dumps(dict(kind='packaging_only_no_scientific_tests', changed_targets=changed,
    unchanged_targets=unchanged, execution_record_diff=execution_diff,
    execution_record_sha256=hashlib.sha256(new_exec.encode()).hexdigest(),
    archived_patch_sha256=hashlib.sha256(patch).hexdigest(),
    whole_stage_command=base, whole_stage_returncode=whole.returncode,
    whole_stage_stdout=whole.stdout, whole_stage_stderr=whole.stderr,
    flagged_blank_context_lines=sorted(set(locations)),
    scoped_command=scoped_command, scoped_returncode=scoped.returncode,
    scoped_stdout=scoped.stdout, scoped_stderr=scoped.stderr,
    historical_candidate_manifest_unchanged=True,
    staged_diagnostic_sha256=hashlib.sha256((bank / 'STAGED_WHITESPACE_DIAGNOSTIC.json').read_bytes()).hexdigest()), indent=2))
