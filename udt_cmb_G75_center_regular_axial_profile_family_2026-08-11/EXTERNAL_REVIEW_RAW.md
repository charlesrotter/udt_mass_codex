VERIFIED_WITH_CAVEATS

**Premise/Type Ledger**
- `34/34` rows in `REVIEW_MANIFEST.tsv` hashed exactly before I used any scientific payload.
- The intake supports a bounded mathematical atlas inside the declared stationary axial metric envelope `A(x)=1+ax^2`, `h=x^2 q(x^2)`.
- It does not support promotion to the generic ten-function metric, all smooth even profiles, or any physical CMB/source/scale claim.

**Decisive Algebra And Counts**
- Independent reconstruction of the coefficient lattice with `gcd(nonzero |c_i|)=1` and first nonzero coefficient `>0` gives exactly `49` primitive rays; the profile count is exactly `49*4*3+3=591`.
- Exact behavior census: persistent sign `28`, interior sign change `9`, center-off `6`, endpoint taper `5`, zero at both boundaries `1`; interior even-touch rows `0`.
- Exact strata: `C0_E0_O0_T0=28`, `C0_E0_O1_T0=8`, `C0_E1_O0_T0=4`, `C0_E2_O0_T0=1`, `C1_E0_O0_T0=5`, `C1_E0_O1_T0=1`, `C1_E1_O0_T0=1`, `C2_E0_O0_T0=1`.
- Center-order counts are `41/7/1` for orders `0/1/2`; endpoint-order counts are `43/5/1` for orders `0/1/2`; odd interior-root counts are `40/9` for `0/1`.
- Row-level result: my independent replay found `0` shape mismatches and `0` profile mismatches against the frozen TSVs.

**Center, Signature, Reflection**
- With `r=Rx` and Cartesian `(X,Y,Z)`, the spatial block is `dX^2+dY^2+dZ^2 + ((A^{-1}-1)/r^2)(X dX+Y dY+Z dZ)^2`. Since `A^{-1}-1 = O(r^2)`, the coefficient is analytic at `r=0`.
- The cross term is `2Rc_E h\sin^2\theta\,dt\,d\psi = (2c_E/R) q(r^2/R^2)\,dt\,(X dY - Y dX)`, which is also analytic at `r=0`. Every frozen profile is therefore genuinely Cartesian `C^\infty` at the center.
- For `a\in\{-1/4,0,1/4\}`, `A(x)\ge 3/4` on `[0,1]`. Away from chart degeneracies the spatial block is positive, and the time Schur complement is `-c_E^2(A + h^2\sin^2\theta/x^2) = -c_E^2(A + x^2 q(x^2)^2\sin^2\theta) < 0`, so the metric has Lorentz signature throughout the closed cell. The axis and spherical center are coordinate degeneracies only.
- `\psi \mapsto -\psi` is not merely a bookkeeping trick: it is an isometry sending `g[q]` to `g[-q]` inside this envelope. What remains physically unselected is orientation choice; G75 does not justify deleting that branch as a measured physical alternative.

**Independence And Catch-Proof Assessment**
- The load-bearing mathematical claim survives a separate reconstruction, so the finite family/census claim stands.
- `verify_profile_family_independent.py` is only partially independent: it re-enumerates the lattice and checks normalization and root multiplicity counts, but it does not independently rederive exact root identities, distinct-root counts, extrema, behavior labels, or stratum labels.
- `verify_package.py` is a consistency wrapper, not an independent proof.
- `run_catch_proofs.py` catches count/status tampering, but it does not mutate algebraic fields such as exact roots, extrema, or class labels while preserving totals. The catch layer is therefore useful but not catch-complete.

**Scope And Maximum Justified Conclusion**
- The premise/scope language is disciplined. The intake stays bounded to the frozen quadratic atlas, symbolic positive `R`, and the stationary axial envelope, and it does not promote to a physical profile, source law, endpoint, `X_max`, or sky fit.
- Maximum justified conclusion: the sealed intake exactly constructs and classifies the complete frozen `49`-ray / `591`-profile center-regular stationary axial quadratic family, with multiple exact shape strata, and nothing broader.

**Runnable Verification Details**
```bash
python3 - <<'PY'
import csv, hashlib, itertools, math
from fractions import Fraction
from pathlib import Path
from collections import Counter
import sympy as sp
root = Path('/tmp/udt_g75_review_tUtzkAuv')
here = root/'udt_cmb_G75_center_regular_axial_profile_family_2026-08-11'
S = sp.symbols('s', real=True)
def tsv(name):
    return list(csv.DictReader((here/name).open(), delimiter='\t'))
def f(q):
    return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'
manifest = tsv('REVIEW_MANIFEST.tsv')
assert len(manifest) == 34 and all(hashlib.sha256((root/r['path']).read_bytes()).hexdigest() == r['sha256'] for r in manifest)
shapes, profiles = tsv('SHAPE_ATLAS.tsv'), tsv('PROFILE_ATLAS.tsv')
rays = sorted(c for c in itertools.product(range(-2, 3), repeat=3)
              if (nz := [abs(v) for v in c if v]) and math.gcd(*nz) == 1 and next(v for v in c if v) > 0)
assert len(rays) == 49 == len(shapes)
shape_mismatches = 0
behavior = Counter()
strata = Counter()
for i, c in enumerate(rays, 1):
    row = shapes[i-1]
    pts = {Fraction(0), Fraction(1)}
    if c[2]:
        v = Fraction(-c[1], 2*c[2])
        if 0 < v < 1:
            pts.add(v)
    M = max(abs(Fraction(c[0]) + Fraction(c[1])*x + Fraction(c[2])*x*x) for x in pts)
    roots = sorted([(sp.sstr(r), int(m)) for r, m in sp.roots(sp.Poly(c[0] + c[1]*S + c[2]*S**2, S).as_expr(), S).items() if sp.simplify(sp.And(r > 0, r < 1)) is sp.true], key=lambda t: float(sp.N(sp.sympify(t[0]), 40)))
    co = 0 if c[0] else (1 if c[1] else 2)
    ep = sum(c)
    eo = 0 if ep else (1 if c[1] + 2*c[2] else 2)
    odd = sum(m % 2 for _, m in roots)
    even = sum((m % 2) == 0 for _, m in roots)
    bc = 'INTERIOR_SIGN_CHANGE' if odd else 'INTERIOR_TOUCH_NO_SIGN_CHANGE' if even else 'ZERO_BOTH_BOUNDARIES_NO_INTERIOR_ROOT' if co and eo else 'CENTER_OFF_NO_INTERIOR_ROOT' if co else 'ENDPOINT_TAPER_NO_INTERIOR_ROOT' if eo else 'PERSISTENT_SIGN_NO_INTERIOR_ROOT'
    exp = {
        'shape_id': f'S{i:02d}', 'c0': str(c[0]), 'c1': str(c[1]), 'c2': str(c[2]), 'normalization_M': f(M),
        'center_q_order_in_s': str(co), 'center_h_order_in_x': str(2 + 2*co), 'center_B_order_in_x': str(2 + 4*co),
        'endpoint_zero_order_in_s': str(eo), 'open_root_count_distinct': str(len(roots)), 'open_root_count_multiplicity': str(sum(m for _, m in roots)),
        'open_odd_root_count': str(odd), 'open_even_root_count': str(even), 'open_roots_exact': ';'.join(f'{r}@{m}' for r, m in roots) or '-',
        'behavior_class': bc, 'stratum_code': f'C{co}_E{eo}_O{odd}_T{even}'
    }
    shape_mismatches += sum(row[k] != v for k, v in exp.items())
    behavior[bc] += 1
    strata[exp['stratum_code']] += 1
L = [('AM', Fraction(-1, 4)), ('A0', Fraction(0)), ('AP', Fraction(1, 4))]
E = [('E05', Fraction(1, 20)), ('E20', Fraction(1, 5)), ('E50', Fraction(1, 2)), ('E100', Fraction(1, 1))]
profile_mismatches = 0
expected = {f'G75_F01_{n}': {'shape_id': 'ZERO', 'amplitude': '0', 'q_of_s': '0'} for n, _ in L}
for row in shapes:
    nc = [Fraction(row[f'normalized_c{k}']) for k in range(3)]
    for en, amp in E:
        expr = str(sp.expand(sum(sp.Rational((amp*nc[k]).numerator, (amp*nc[k]).denominator) * S**k for k in range(3))))
        for ln, _ in L:
            expected[f'G75_{ln}_{row["shape_id"]}_{en}'] = {'shape_id': row['shape_id'], 'amplitude': f(amp), 'q_of_s': expr}
assert len(expected) == len(profiles) == 591 == len({r['profile_id'] for r in profiles})
for row in profiles:
    exp = expected[row['profile_id']]
    profile_mismatches += sum(row[k] != v for k, v in exp.items())
assert shape_mismatches == profile_mismatches == 0
print({'hashes': '34/34', 'shape_count': 49, 'profile_count': 591, 'behavior': dict(sorted(behavior.items())), 'strata': dict(sorted(strata.items())), 'shape_mismatches': 0, 'profile_mismatches': 0})
PY
```
- `SHA-256(response body above, excluding these SHA bullets to avoid the self-reference problem) = 5b7701a9927ec651aca9b21e1d45a5ad9ceebec89f9dcba61f91d49e44f70a06`
- `SHA-256(inline verifier block) = 8b22b0c63f9c3b90e64975d88c28a6da9d8200e3301c8a8a45f984e14f564cc1`