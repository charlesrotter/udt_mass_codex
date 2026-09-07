"""Pin final R1 code, reproduce output, and reintroduce its covariance defect."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import platform

step = Path(__file__).resolve().parent.parent
codepath = step / 'geometry_checks.py'
code = codepath.read_text()
assert hashlib.sha256(codepath.read_bytes()).hexdigest() == '48766db54bbff840ac3fad54c54f8d18061bcc9290480694e6f02f8ebbdc6819'
assert hashlib.sha256((step/'INITIAL_CANDIDATE.md').read_bytes()).hexdigest() == '478100481ea75cc363b8c0c60c0f7e2338fbdc600db0bee140b1a2d16feb92b4'
assert hashlib.sha256((step/'INITIAL_geometry_checks.py').read_bytes()).hexdigest() == 'df61009c19d4755e3ec17fcc60219ae0e0f01aa0f66045531d75dc588a5a02a1'
assert hashlib.sha256((step/'geometry_run.stdout').read_bytes()).hexdigest() == '1ce4666a64540ee8eec49bc82ffc1b64a9264e0e9eb68752244612c527a4e9e5'
assert hashlib.sha256((step/'repair_run.stdout').read_bytes()).hexdigest() == '37854cc5c016d268181f8fd071c078f1b94abd1b40be8a01832416c90fefd9c5'
out = io.StringIO()
ns = {'__name__':'__review_replay__'}
with contextlib.redirect_stdout(out):
    exec(compile(code, str(codepath), 'exec'), ns)
assert out.getvalue() == (step/'repair_run.stdout').read_text()
old = json.loads((step/'geometry_run.stdout').read_text())
new = json.loads(out.getvalue())
assert set(new) == set(old) | {'complex_covariance_R1'}
for key in old:
    if key == 'finite_defects_rejected':
        assert new[key] == old[key] + ['R1_missing_complex_conjugation']
    else:
        assert new[key] == old[key], key
assert new['complex_covariance_R1']['correct_variance'] == '3'
assert new['complex_covariance_R1']['wrong_unconjugated_column_variance'] == '1'

# Real defect insertion into producer expression, in memory only.
correct = 'complex_variance=(bc*Cc*bc.H)[0]'
wrong = 'complex_variance=(bc.conjugate()*Cc*bc.T)[0]'
assert code.count(correct) == 1
mutant = code.replace(correct, wrong)
mutated_ns = {'__name__':'__review_mutation__'}
caught = False
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(mutant, '<R1_wrong_complex_orientation>', 'exec'), mutated_ns)
except AssertionError:
    assert mutated_ns['complex_variance'] == mutated_ns['wrong_variance'] == 1
    caught = True
assert caught

# Separate standard-library dyadic-complex evaluation does not reuse SymPy.
b = [-1j,0j,1+0j]
c = [[1+0j,0j,0.5j],[0j,1+0j,0j],[-0.5j,0j,1+0j]]
independent = sum(b[i]*c[i][j]*b[j].conjugate() for i in range(3) for j in range(3))
independent_wrong = sum(b[i].conjugate()*c[i][j]*b[j] for i in range(3) for j in range(3))
assert independent == 3 and independent_wrong == 1

print(json.dumps({
    'python':platform.python_version(),
    'source_hashes_and_preserved_originals_match':True,
    'repaired_stdout_byte_identical':True,
    'all_original_result_fields_unchanged_except_added_guard':True,
    'R1_correct_variance':independent.real,
    'R1_initial_wrong_variance':independent_wrong.real,
    'actual_wrong_conjugation_expression_mutation_rejected':caught,
    'scope':'Focused finite repair verification; no event data or instrument recertification',
},indent=2,sort_keys=True))
