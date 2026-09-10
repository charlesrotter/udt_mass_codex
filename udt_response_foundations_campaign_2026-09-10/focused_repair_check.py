"""Parent's focused separate-context review of reviewer check-only repair.

Same-code replay is regression; the new quartic mutation demonstrates the
old truncation false pass. It is a finite implementation guard, not a theorem.
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy

root = Path(__file__).resolve().parent
initial = (root/'review/independent_normal_metric_check.initial.py').read_bytes()
fixed = (root/'review/independent_normal_metric_check.py').read_bytes()
assert hashlib.sha256(initial).hexdigest() == 'bb6ca932a3fea3981d1ac3d23dd319ec8f6ea11fa46f8683b33ae702741e6c19'
assert hashlib.sha256(fixed).hexdigest() == '664b999986835547cf5c086921d4b4538688a9ab333d82b7d9e033f1f01fc7ae'
expected = initial.replace(b'r2[d, e, *s] = out', b'r2[(d, e) + s] = out')
expected = expected.replace(b'mul(g[i, j], X[j]) for j', b'mul(g[i, j], X[j], degree=5) for j')
expected = expected.replace(b"catch('quartic_sign_flip_matches_Jacobi', F(-2,45)==F(2,45))\n", b'')
assert expected == fixed, 'only three disclosed changes'
parse_failed = False
try:
    compile(initial, 'preserved_initial', 'exec')
except SyntaxError:
    parse_failed = True
assert parse_failed, 'reproduce initial Python3.10 parse failure'
compile(fixed, 'corrected', 'exec')
out = io.StringIO()
with contextlib.redirect_stdout(out):
    r = runpy.run_path(str(root/'review/independent_normal_metric_check.py'))
replay = json.loads(out.getvalue())
saved = json.loads((root/'review/independent_normal_metric_check_repaired.stdout').read_text())
assert replay == saved, 'same-code exact replay'
g = r['metric'](r['K1'], r['K2'])
assert r['radial'](g)
bad = {ij: dict(poly) for ij, poly in g.items()}
bad[0, 0] = r['add'](bad[0, 0], {(4, 0, 0, 0): r['F'](1)})
old_truncated_passes = all(r['add'](*(r['mul'](bad[i, j], r['X'][j])
    for j in range(4))) == r['scale'](r['X'][i], r['SGN'][i]) for i in range(4))
assert old_truncated_passes, 'degree4 truncation must expose its false pass'
assert not r['radial'](bad), 'degree5 guard must reject same mutation'
full_residual = r['add'](*(r['mul'](bad[0, j], r['X'][j], degree=5)
                         for j in range(4)), r['scale'](r['X'][0], -r['SGN'][0]))
assert full_residual == {(5, 0, 0, 0): r['F'](1)}
print(json.dumps(dict(
    exact_three_change_diff=True, initial_parse_failure_reproduced=True,
    corrected_same_code_replay_identical=True,
    quartic_g00_mutation_old_check_false_pass=True,
    repaired_check_rejects=True, full_radial_residual='x0^5 in component0',
    scientific_candidate_modified=False,
    scope='Focused implementation repair review; replay is not independent mathematics.'
), indent=2, sort_keys=True))
