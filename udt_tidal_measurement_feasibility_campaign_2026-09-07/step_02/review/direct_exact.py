"""Post-exposure authentication and Fraction recomputation of saved TM2 records.

Reuse the sealed reviewer-only matrix helpers. No author science is imported.
The source-first script has a main body, so its stdout is captured and its
repeat PASS is explicitly excluded from the new direct-check count.
"""
from fractions import Fraction as F
import contextlib
import hashlib
import io
import json
from pathlib import Path
import platform
import runpy

root = Path(__file__).resolve().parents[3]
pkg = root / 'udt_tidal_measurement_feasibility_campaign_2026-09-07'
review = pkg / 'step_02/review'
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    namespace = runpy.run_path(str(review / 'stage_a_exact.py'))
assert json.loads(buffer.getvalue())['status'] == 'PASS'
mat, mul, tr, rank, null, zero = [namespace[k] for k in
                                ('mat', 'multiply', 'transpose', 'rank', 'null_rows', 'zero')]
checks = []


def guard(name, condition, evidence):
    checks.append(dict(name=name, passed=bool(condition), evidence=evidence))
    assert condition, name


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


expected = {
    'CANDIDATE_ARGUMENT.md': '8660e9077d6fb29b041bd5e7d9875c53658b7f8ab5683f60a170d071ead7990b',
    'check_designs.py': '08700748dfdc14074e95294d40c53de7615068c4a67ab973b89698ad6cb8cf91',
    'PLAN.md': '57744f8338f390a298d188e183c41b554e62ae182a95d535743300d170141eec',
}
for name, wanted in expected.items():
    actual = digest(pkg / 'step_02' / name)
    guard('candidate_auth:' + name, actual == wanted, actual)
for manifest in ['SOURCE_SHA256SUMS', 'STAGE_A_SHA256SUMS']:
    count = 0
    for line in (review / manifest).read_text().splitlines():
        wanted, filename = line.split('  ', 1)
        assert digest(root / filename) == wanted, filename
        count += 1
    guard('sealed_auth:' + manifest, count > 0, count)

author = json.loads((pkg / 'step_02/author_check.stdout').read_text())
guard('author_saved_output_internal_count', author['count'] == len(author['checks']) == 32,
      author['count'])
independent = {}
for name, item in author['designs'].items():
    if name == 'prospective_affine':
        continue
    p, n, saved_m, saved_c = [mat(item[key]) for key in ('P', 'N', 'M', 'C')]
    pn = mul(p, n)
    m = [[sum(row, F(0))] + nuisance for row, nuisance in zip(p, pn)]
    c = null(tr(m), len(p))
    computed = {'P': rank(p), 'M': rank(m), 'Q': rank(pn),
                'C': rank(c), 'CP': rank(mul(c, p))}
    identifiable = rank(m) > rank(pn)
    guard('independent_saved_design:' + name,
          m == saved_m and computed == item['ranks'] and
          identifiable == item['absolute_kappa_identifiable'] and
          rank(saved_c) == len(p)-rank(m) and zero(mul(saved_c, m)),
          dict(ranks=computed, identifiable=identifiable, independently_computed_C=c))
    independent[name] = dict(P=p, M=m, C=c)

affine = author['designs']['prospective_affine']
k = mat([[-1, 2], [-2, 3]])
c = mat([[1, -2, 1, 0], [2, -3, 0, 1]])
m = independent['unknown_affine_drift']['M']
guard('prospective_K_and_full_theta_prediction', k == mat(affine['K']) and
      c == mat(affine['C_AB']) and mul(k, m[:2]) == m[2:], dict(K=k, C=c))
quad = mul(c, mat([[0], [1], [4], [9]]))
guard('prospective_quadratic_recomputed', quad == mat([[2], [6]]) == mat(affine['quadratic_response']), quad)
coefficients = [sum(abs(x) for x in row) for row in c]
guard('prospective_bound_coefficients', coefficients == [4, 6] and
      affine['bounds'] == [['4*u'], ['6*u']], coefficients)
sigma = mat([[int(i == j)+F(1, 3) for j in range(4)] for i in range(4)])
cov = mul(mul(c, sigma), tr(c))
guard('prospective_full_cross_covariance_recomputed', sigma == mat(affine['correlated_covariance']) and
      cov == mat([[6, 8], [8, 14]]) == mat(affine['residual_covariance']), cov)
v = mat([[0], [0], [1]])
guard('prospective_one_row_ambiguity', v == mat(affine['ambiguity_vector']) and
      zero(mul(m[:1], v)) and mul(m[1:], v) == mat([[1], [2], [3]]), mul(m[1:], v))

# The author's rank(P)-rank(M) formula uses its explicit PRE-P nuisance scope.
# This exact post-P counter-design is outside that scope, not a defect in it.
p_outside = mat([[1, 0], [0, 0]])
m_outside = mat([[1, 0], [0, 1]])
c_outside = null(tr(m_outside), 2)
guard('preprocessing_nuisance_hypothesis_is_load_bearing',
      rank(p_outside)-rank(m_outside) == -1 and rank(mul(c_outside, p_outside)) == 0,
      dict(outside_scope_naive_difference=-1, actual_sensitive_rank=0))

# Exhaust the vertices of a small interval for a single known residual signal:
# |signal|>2B guarantees |signal+e|>B, while equality need not reject.
b = F(4)
signal = F(9)
guard('strict_twice_bound_control', all(abs(signal+e)>b for e in [-b, b]) and
      abs(2*b-b) == b, dict(bound=b, signal=signal, edge_residuals=[signal-b, signal+b]))

print(json.dumps(dict(status='PASS', context='/root/tidal_tm2_review',
                      check_count=len(checks), checks=checks,
                      python=platform.python_version(), arithmetic='fractions.Fraction',
                      author_scientific_imports=False,
                      repeated_source_first_checks_not_counted=True), default=str, sort_keys=True))
