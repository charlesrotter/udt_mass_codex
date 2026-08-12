VERIFIED_WITH_CAVEATS

No blocking correctness finding appears inside the sealed intake. The production construction in [derive_nonradial_screen_covariance.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/derive_nonradial_screen_covariance.py:52), [derive_nonradial_screen_covariance.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/derive_nonradial_screen_covariance.py:90), [derive_nonradial_screen_covariance.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/derive_nonradial_screen_covariance.py:139), [derive_nonradial_screen_covariance.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/derive_nonradial_screen_covariance.py:209), the exact algebra in [verify_exact_algebra.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/verify_exact_algebra.py:13), and the independent Christoffel replay in [verify_nonradial_neighboring_rays.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/verify_nonradial_neighboring_rays.py:33), [verify_nonradial_neighboring_rays.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/verify_nonradial_neighboring_rays.py:133), [verify_nonradial_neighboring_rays.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/verify_nonradial_neighboring_rays.py:192) all agree on the bounded claim. I found no missing `Z`, missing transpose, sign error, source/projection basis swap, silent diagonalization, or fake nonradial control.

Binding caveats:
- I independently verified all `28/28` sealed G81 rows in [REVIEW_MANIFEST.tsv](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/REVIEW_MANIFEST.tsv:10) and verified that its `9` nonlocal rows are exactly the same `9` rows listed in [SOURCE_MANIFEST.tsv](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/SOURCE_MANIFEST.tsv:1). I did not reopen those upstream bytes, because your instruction forbade leaving the sealed intake. Their byte-level hash check is therefore attested by the included verifier logic in [verify_package.py](/tmp/udt_g81_review_dBEDYe/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/verify_package.py:72), not independently replayed by me.
- The independent method is bounded, not absolute. It locally rebuilds the metric and Christoffels and uses centered neighboring rays, but it still shares the supplied metric/profile, observer query, endpoint surfaces, control rotations, and `DOP853` integrator family with production.

Corrections:
- None required inside the seal.

Strongest justified maximum conclusion:
- `DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.
- C1 is genuinely nonradial and non-diagonal: direction `(12,3,4)/13`, screen `(0,4,-3)/5` and `(-25,36,48)/65`, endpoint `(theta,psi)=(1.7493671390260097, 0.23079074045919012)`, forward off-diagonal norm `1.1801666864663825e-3`.
- The matrix law is correctly placed as `D_reverse = Z transpose(D_forward)` and `D_reverse_AB = Z B transpose(D_forward) transpose(A)`.
- This remains generic Jacobi/Wronskian covariance on the frozen metric/query pair, not a UDT selector and not a claim about profile selection, endpoint physics, `Xmax`, source, SNe/CMB observables, `cmb_temp`, action, matter, bootstrap, or future signalling.

Smallest next calculation:
- Re-run the same C1 neighboring-ray replay once with an integrator family not shared with production, and in that same out-of-seal audit reopen the 9 frozen source bytes at `f112a32e...` to complete the provenance check. Do not enlarge the control universe.

Runnable checks:
```bash
python3 - <<'PY'
import csv, hashlib, pathlib
p = pathlib.Path('.')
rows = list(csv.DictReader(open('REVIEW_MANIFEST.tsv', newline='', encoding='utf-8'), delimiter='\t'))
local = [r for r in rows if r['path'].startswith('udt_cmb_G81_nonradial_screen_covariance_2026-08-12/')]
assert all(hashlib.sha256((p / r['path'].split('/', 1)[1]).read_bytes()).hexdigest() == r['sha256'] for r in local)
src = list(csv.DictReader(open('SOURCE_MANIFEST.tsv', newline='', encoding='utf-8'), delimiter='\t'))
assert [r for r in rows if not r['path'].startswith('udt_cmb_G81_nonradial_screen_covariance_2026-08-12/')] == [{k: r[k] for k in ('path', 'sha256', 'role')} for r in src]
print('local_manifest_rows=', len(local), 'external_source_rows=', len(src))
PY
```

```python
import sympy as sp
n = sp.Matrix([12,3,4]) / 13
s1 = sp.Matrix([0,4,-3]) / 5
s2 = sp.Matrix([-25,36,48]) / 65
A = sp.Matrix([[sp.Rational(3,5), -sp.Rational(4,5)], [sp.Rational(4,5), sp.Rational(3,5)]])
B = sp.Matrix([[sp.Rational(5,13), -sp.Rational(12,13)], [sp.Rational(12,13), sp.Rational(5,13)]])
z, d11, d12, d21, d22 = sp.symbols('z d11 d12 d21 d22', positive=True, real=True)
D = sp.Matrix([[d11,d12],[d21,d22]])
assert n.dot(n) == s1.dot(s1) == s2.dot(s2) == 1
assert n.dot(s1) == n.dot(s2) == s1.dot(s2) == 0
assert s1.cross(s2) == n
assert A.T*A == B.T*B == sp.eye(2) and A.det() == B.det() == 1
assert B*(z*D.T)*A.T == z*B*D.T*A.T
```

```bash
python3 - <<'PY'
import json, math, numpy as np
prod = json.load(open('DERIVATION_RESULT.json'))
ind = json.load(open('INDEPENDENT_VERIFICATION.json'))
npz = np.load('PATH_EVIDENCE.npz')
A = np.array([[3/5,-4/5],[4/5,3/5]], float)
B = np.array([[5/13,-12/13],[12/13,5/13]], float)
for row in prod['controls']:
    cid = row['control_id']; Z = row['forward']['Z']
    Df = np.array(row['forward']['D']); Dr = np.array(row['reverse_unrotated']['D']); Drab = np.array(row['reverse_rotated']['D'])
    assert np.allclose(Dr, Z*Df.T)
    assert np.allclose(Drab, Z*B@Df.T@A.T)
    assert abs(math.sqrt(abs(np.linalg.det(Dr)))/math.sqrt(abs(np.linalg.det(Df))) - Z) < 1e-8
    fs = npz[cid+'__forward_state']; rs = npz[cid+'__reverse_unrotated_state']; rr = npz[cid+'__reverse_rotated_state']
    assert np.allclose(rs[:4,0], fs[:4,-1]) and np.allclose(rs[4:8,0], -fs[4:8,-1]/Z)
    assert np.allclose(rr[8:16,0], (A @ fs[8:16,-1].reshape(2,4)).reshape(8))
    print(cid, row['reverse_rotated']['D_relative'], row['forward']['offdiagonal_norm'])
for row in ind['controls']:
    print(row['control_id'], row['independent_rotated_covariance_relative'])
PY
```