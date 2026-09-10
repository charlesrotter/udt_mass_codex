#!/usr/bin/env python3
"""Independent exact construction checks; no project/source-code imports.

Scope, exposed choices and exclusions: CONSTRUCTION_FREEZE.md.
This constructs conditional mathematical records, not a physical protocol.
"""
import json
import os
import platform
import sys

import sympy as sp


def scalar_text(value):
    return str(sp.simplify(value))


checks = []


def zero(name, expression):
    entries = list(expression) if isinstance(expression, sp.MatrixBase) else [expression]
    residuals = [sp.simplify(entry) for entry in entries]
    passed = all(entry == 0 for entry in residuals)
    checks.append({"name": name, "pass": passed, "residuals": list(map(str, residuals))})
    if not passed:
        print(json.dumps({"failed_check": checks[-1], "prior_checks": checks}, indent=2))
        raise AssertionError(name)


# FREE / supplied comparison-family parameter, not a selected metric or scale.
b, t, x, y, z, a, c, r0 = sp.symbols("b t x y z a c r0", real=True)
q = sp.Matrix([t, x, y, z])
eta = sp.diag(-1, 1, 1, 1)  # G179 mathematical domain, pinned-by-THEORY.
E = sp.eye(4)
E[0, 1] = -b * y / 2
E[0, 2] = b * x / 2
g = E.T * eta * E
U = sp.eye(4)[:, 0]
B = sp.Matrix([-b * y / 2, b * x / 2, 0])
records = []
horizontal = []

zero("coframe_invertible_exact", E.det() - 1)
zero("U_unit", (U.T * g * U)[0] + 1)
zero("origin_entire_coframe_is_identity", E.subs({x: 0, y: 0}) - sp.eye(4))

for i, axis in enumerate((x, y, z)):
    J = sp.Matrix.hstack(U, sp.eye(4)[:, i + 1])
    V = E * J
    h = sp.simplify(V.T * eta * V)
    beta = sp.simplify(h[0, 1] / h[0, 0])
    zero(f"coordinate_{axis}_h00", h[0, 0] + 1)
    zero(f"coordinate_{axis}_det", h.det() + 1)
    zero(f"coordinate_{axis}_beta", beta - B[i])
    zero(f"coordinate_{axis}_h11", h[1, 1] - (1 - B[i] ** 2))
    # The previous h00=-1 and det=-1 establish regularity for every real parameter.
    # Positive reciprocal normalization consequently gives T=m=L=1, Phi=0.
    H = sp.eye(4)[:, i + 1] - B[i] * U
    J_perp = sp.Matrix.hstack(U, H)
    V_perp = sp.simplify(E * J_perp)
    h_perp = sp.simplify(V_perp.T * eta * V_perp)
    zero(f"horizontal_{axis}_V_constant", V_perp - J)
    zero(f"horizontal_{axis}_h_constant", h_perp - sp.diag(-1, 1))
    for coord in (t, x, y, z, b):
        zero(f"horizontal_{axis}_V_derivative_{coord}", V_perp.diff(coord))
    horizontal.append(H)
    records.append({"axis": str(axis), "h": str(h), "beta_s": str(beta),
                    "T": "1", "m": "1", "L_s": "1", "Phi": "0",
                    "J_horizontal": str(J_perp), "V_horizontal": str(V_perp)})


def lie_bracket(X, Y):
    return sp.simplify(Y.jacobian(q) * X - X.jacobian(q) * Y)


bracket = lie_bracket(horizontal[0], horizontal[1])
zero("horizontal_xy_bracket_minus_bU", bracket + b * U)
zero("horizontal_Ux_integrable_strip", lie_bracket(U, horizontal[0]))
zero("horizontal_Uy_integrable_strip", lie_bracket(U, horizontal[1]))

# Explicit individual observer/ruler strips exist even though all three horizontal
# spatial directions do not together form a hypersurface for nonzero b.
tau, s, x0, y0, z0 = sp.symbols("tau s x0 y0 z0", real=True)
Fx = sp.Matrix([tau + b * y0 * s / 2, x0 + s, y0, z0])
Fy = sp.Matrix([tau - b * x0 * s / 2, x0, y0 + s, z0])
for axis, F, column in (("x", Fx, 1), ("y", Fy, 2)):
    JF = F.jacobian((tau, s))
    EF = E.subs(dict(zip(q, F)), simultaneous=True)
    VF = sp.simplify(EF * JF)
    zero(f"explicit_{axis}_strip_V", VF - sp.Matrix.hstack(U, sp.eye(4)[:, column]))

# Supplied synchronization control, not an output-derived calibration.
f = a * x * y + c * x
df = sp.Matrix([sp.diff(f, coord) for coord in (x, y, z)])
Bprime = B - df
K = sp.eye(4)
for i in range(3):
    K[0, i + 1] = df[i]
Eprime = sp.simplify(E * K.inv())
for i, axis in enumerate((x, y, z)):
    J = sp.Matrix.hstack(U, sp.eye(4)[:, i + 1])
    h_old = J.T * g * J
    Vmatched = sp.simplify(Eprime * K * J)
    zero(f"matched_chart_{axis}_V_invariant", Vmatched - E * J)
    zero(f"matched_chart_{axis}_h_invariant", Vmatched.T * eta * Vmatched - h_old)
    # Constant-new-clock ruler germs J have been RESELECTED, not matched as KJ.
    h_reselected = sp.simplify((Eprime * J).T * eta * (Eprime * J))
    zero(f"reselected_{axis}_beta_transform", h_reselected[0, 1] / h_reselected[0, 0] - Bprime[i])

curl = sp.simplify(sp.diff(B[1], x) - sp.diff(B[0], y))
curlprime = sp.simplify(sp.diff(Bprime[1], x) - sp.diff(Bprime[0], y))
zero("joint_family_beta_curl", curl - b)
zero("reselected_synchronization_beta_curl_invariant", curlprime - curl)
zero("flat_shift_false_positive", Bprime[0].subs({b: 0, a: 0}) + c)
zero("flat_shift_false_positive_curl_zero", curlprime.subs(b, 0))
zero("marked_off_origin_y_shift", B[1].subs({x: r0, y: 0}) - b * r0 / 2)

result = {
    "scope": "Conditional exact supplied-family record-type construction; UNPROMOTED; not adversarial review",
    "versions": {"python": sys.version, "sympy": sp.__version__, "platform": platform.platform(),
                 "logical_cpus": os.cpu_count(), "runtime_model": "UNATTESTED"},
    "resources": {"device": "CPU", "dtype": "symbolic exact", "grid": None,
                  "scientific_subprocess_timeout_seconds": 120},
    "parameters": "real b,t,x,y,z,a,c,r0; r0 nonzero only for the declared off-origin distinction",
    "records": records,
    "horizontal_bracket": str(bracket),
    "synchronization_f": str(f),
    "reselected_Bprime": str(Bprime),
    "joint_marked_family_curl": str(curl),
    "checks_passed": len(checks),
    "checks": checks,
    "limitations": [
        "T,m,Phi point values are algebraic; their constancy does not imply ambient flatness.",
        "beta point values are marked pair shifts, not invariant rotation.",
        "A jointly marked neighborhood family is supplied cross-query data, not scalar output.",
        "Constant V coefficients in varying ambient E_b do not reconstruct coordinate J fields.",
        "G182 V-jet equivalence requires the same common ambient coframe.",
        "No curvature, field equations, null geodesic integration or physical protocol checked here."
    ],
}
print(json.dumps(result, indent=2))
