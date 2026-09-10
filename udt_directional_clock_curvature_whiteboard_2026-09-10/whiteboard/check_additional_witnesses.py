"""Exact construction controls in a declared diagonal homogeneous witness class.

No Einstein/source equation. One CPU process, no numerical approximation or GPU.
Class-specific Christoffel/Ricci formulas are justified in PARTNER_NOTES.md;
these symbolic checks are constructor arithmetic checks, not independent review.
Run in a copied directory to preserve saved outputs.
"""
import json
import pathlib
import sys

import sympy as s

root = pathlib.Path(__file__).parent
t, beta, rate = s.symbols("t beta s", real=True)
nx, ny, nz = s.symbols("n_x n_y n_z", real=True)


def check(name, scales, expected_q0, expected_m0, expected_dot_m0, expected_ric0):
    # g=-dt²+sum A_i²(dx^i)², U=partial_t. The displayed Christoffels
    # are obtained directly from g and its first derivatives.
    gamma_i0i = [s.simplify(s.diff(a*a, t) / (2*a*a)) for a in scales]
    gamma_0ii = [s.simplify(s.diff(a*a, t) / 2) for a in scales]
    # Ric_00=partial_a Gamma^a_00-partial_0 Gamma^a_a0
    #        +Gamma^a_ad Gamma^d_00-Gamma^a_0d Gamma^d_a0.
    ric = s.simplify(-sum(s.diff(h, t) + h*h for h in gamma_i0i))
    mean = s.simplify(-sum(gamma_i0i)/3)
    q = -sum(h*n*n for h, n in zip(gamma_i0i, (nx, ny, nz)))
    # The sphere identity nx²+ny²+nz²=1 is used for the isotropic q.
    if gamma_i0i[0] == gamma_i0i[1] == gamma_i0i[2]:
        q = -gamma_i0i[0]
    q0, m0, dm0, r0 = [s.simplify(v.subs(t, 0)) for v in (q, mean, s.diff(mean, t), ric)]
    actual = [q0, m0, dm0, r0]
    expected = [expected_q0, expected_m0, expected_dot_m0, expected_ric0]
    for value, want in zip(actual, expected):
        assert s.simplify(value-want) == 0
    out = {
        "scales": [str(a) for a in scales],
        "Gamma_i0i": [str(h) for h in gamma_i0i],
        "Gamma_0ii": [str(h) for h in gamma_0ii],
        "Ric_UU": str(ric),
        "q": str(q),
        "q_at_t0": str(q0),
        "mean_q_at_t0": str(m0),
        "dot_mean_q_at_t0": str(dm0),
        "Ric_UU_at_t0": str(r0),
        "acceleration_divergence": "0",
        "vorticity_squared": "0",
    }
    print(name, json.dumps(out, sort_keys=True), flush=True)
    return out


result = {
    "evidence_type": "same-context constructor exact symbolic controls",
    "python": sys.version,
    "sympy": s.__version__,
}
result["isotropic_time_dependence"] = check(
    "isotropic_time_dependence", [s.exp(beta*t*t/2)]*3,
    0, 0, -beta, -3*beta,
)
result["constant_anisotropic_rates"] = check(
    "constant_anisotropic_rates", [s.exp(rate*t), s.exp(-rate*t), s.Integer(1)],
    -rate*(nx*nx-ny*ny), 0, 0, -2*rate*rate,
)
(root / "ADDITIONAL_RESULT.json").write_text(json.dumps(result, indent=2)+"\n")
print("PASS constructor diagonal-metric controls")
