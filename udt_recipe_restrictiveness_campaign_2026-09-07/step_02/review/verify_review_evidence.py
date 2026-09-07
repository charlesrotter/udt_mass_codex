"""Byte/provenance correspondence only; not scientific truth or chronology."""
import difflib
import hashlib
import json
import pathlib

here=pathlib.Path(__file__).resolve().parent
root=here.parents[2]
step=here.parent
pairs=[(here/'author_replay.stdout',step/'author_corrected.stdout'),(here/'replay_completion.stdout',step/'mutant_completion.stdout'),(here/'replay_dual.stdout',step/'mutant_dual.stdout')]
comparisons={str(a.relative_to(root)):a.read_bytes()==b.read_bytes() for a,b in pairs}
assert all(comparisons.values())
checks={}
for filename in ('CANDIDATE_SHA256SUMS','SOURCE_SHA256SUMS'):
    lines=(step/filename).read_text().splitlines()
    checks[filename]=len(lines)
    for line in lines:
        expected,path=line.split('  ',1)
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==expected,path
stage=(here/'STAGE_A_SHA256SUMS.stdout').read_text().splitlines()
checks['STAGE_A_SHA256SUMS.stdout']=len(stage)
for line in stage:
    expected,path=line.split('  ',1)
    assert hashlib.sha256((root/path).read_bytes()).hexdigest()==expected,path
initial=json.loads((step/'author_exact.stdout').read_text())
assert initial['status']=='FAIL' and initial['failed']=='saturation_complete_two_parameter_class'
print(json.dumps(dict(status='PASS',manifest_entries=checks,replay_stdout_byte_equality=comparisons,initial_author_diagnostic=initial,all_original_checks_retained=True),indent=2))
print('Author initial-to-corrected diff:')
print(''.join(difflib.unified_diff((step/'initial_check_exact_boundary.py').read_text().splitlines(True),(step/'check_exact_boundary.py').read_text().splitlines(True),fromfile='initial_check_exact_boundary.py',tofile='check_exact_boundary.py')))
