"""Only final packaging-accounting correspondence; all output is lossless JSON."""
import hashlib
import json
import pathlib
import subprocess

repo = pathlib.Path('/home/udt-admin/udt_mass_codex')
rel = 'udt_shared_readout_metric_constraint_campaign_2026-09-06'
pkg = repo / rel
pin = '70034a6faa9264bf054eb473d5eb7a0889f3d2de'
records = []

def run(args, expected=0):
    command = ['git', '-c', 'core.preloadIndex=false', '--no-optional-locks', *args]
    result = subprocess.run(command, cwd=repo, capture_output=True)
    records.append(dict(command=command, returncode=result.returncode,
                        stdout=result.stdout.decode(), stderr=result.stderr.decode()))
    assert result.returncode == expected and result.stderr == b'', args
    return result.stdout.decode()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = (pkg / 'ASSEMBLY_REVIEW_INPUT_SHA256SUMS').read_text()
for line in manifest.splitlines():
    expected, name = line.split('  ', 1)
    assert sha(repo / name) == expected, name
assert len(manifest.splitlines()) == 4
historical = dict(line.split('  ', 1)[::-1] for line in (pkg / 'CLOSURE_FINAL_INPUT_SHA256SUMS').read_text().splitlines())
for name in ['DECISION_BRIEF.md', 'CAMPAIGN_LOG.md']:
    staged = run(['show', ':' + rel + '/' + name])
    assert hashlib.sha256(staged.encode()).hexdigest() == historical[rel + '/' + name]
run(['diff', '--', rel + '/DECISION_BRIEF.md', rel + '/CAMPAIGN_LOG.md'])

assembly = json.loads((pkg / 'FINAL_ASSEMBLY_CHECK_RECORD.json').read_text())
expected_raw = [rel + '/' + path for path in [
    'closure_focused_review/factual_retry.stdout',
    'closure_review/authenticate.stdout',
    'step_05/repair/review/repair_delta.stdout']]
assert assembly['exact_raw_transcript_exclusions'] == expected_raw
assert assembly['warning_count'] == 14
strict = run(['diff', '--check', pin], expected=2)
assert strict == assembly['strict_result']['output']
assert assembly['strict_result']['exit_code'] == 2
warnings = [line for line in strict.splitlines() if line.endswith(': trailing whitespace.')]
assert len(warnings) == 14
assert sorted(set(line.split(':')[0] for line in warnings)) == sorted(expected_raw)
narrowed = run(['diff', '--check', pin, '--', '.', *[':(exclude)' + path for path in expected_raw]])
assert narrowed == assembly['narrowed_result']['output'] == ''
assert assembly['narrowed_result']['exit_code'] == 0
run(['ls-files', '--error-unmatch', *expected_raw])
assert (repo / expected_raw[0]).read_bytes() == pathlib.Path('/tmp/tri_closure_final_delta.XLU1Mh/factual_retry.stdout').read_bytes()
assert (repo / expected_raw[1]).read_bytes() == pathlib.Path('/tmp/tri_closure_fidelity.5CGThc/authenticate.stdout').read_bytes()
repair_manifest = (pkg / 'step_05/repair/review/REVIEW_SHA256SUMS').read_text().splitlines()
repair_hash = next(line.split('  ', 1)[0] for line in repair_manifest if line.endswith('  repair_delta.stdout'))
assert sha(repo / expected_raw[2]) == repair_hash

review_record = (pkg / 'CLOSURE_REVIEW_RECORD.md').read_text()
for path, report in [('closure_review', 'INITIAL_FIDELITY_REVIEW.md'), ('closure_focused_review', 'FOCUSED_FIDELITY_REVIEW.md')]:
    assert sha(pkg / path / report) in review_record
    assert sha(pkg / path / 'REVIEW_SHA256SUMS') in review_record
assert '17 files/16 verified payloads' in review_record
assert '15 files/14 verified payloads' in review_record
head = run(['rev-parse', 'HEAD']).strip()
assert head == 'e93f49ebc92d527a39f04c4ce72c51408f74b679'
run(['rev-list', '--left-right', '--count', 'HEAD...origin/grok'])
assert 'not predicted' in review_record and 'before the containing closure commit' in review_record
for name in ['LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md', 'INDEX.md', 'MEMORY.md']:
    assert (repo / name).read_bytes() == (pathlib.Path('/tmp/tri_closure_fidelity.5CGThc') / ('initial_' + name)).read_bytes()
print(json.dumps(dict(result='PASS', scope='Four-file accounting delta only; no science, audit or future Git claim',
                      manifest=manifest, strict_warning_count=14, exact_raw_transcript_exclusions=expected_raw,
                      commands=records), sort_keys=True))
