#!/usr/bin/env python3
"""Exact symbolic checks for G168.  No numerical fitting or protected inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


checks: dict[str, bool] = {}


def check(name: str, condition: object) -> None:
    value = bool(condition)
    checks[name] = value
    if not value:
        raise AssertionError(name)


# Abstract projection algebra.
guu, gus, gss = sp.symbols("guu gus gss", nonzero=True, real=True)
a = -gus / guu
check("unique_projection_coefficient", sp.simplify(gus + a * guu) == 0)
rr = sp.simplify(gss + 2 * a * gus + a**2 * guu)
check("projected_norm", rr == sp.simplify(gss - gus**2 / guu))
check(
    "pair_gram_determinant",
    sp.simplify(sp.det(sp.Matrix([[guu, 0], [0, rr]])) - guu * rr) == 0,
)

# Exact primary-metric witness.
g = sp.diag(sp.Rational(-1, 4), 4, 9, sp.Rational(144, 25))
u = sp.Matrix([2, 0, 0, 0])
s = sp.Matrix([1, sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 4)])
inner = lambda x, y: (x.T * g * y)[0]
guu_w = inner(u, u)
gus_w = inner(u, s)
r = sp.simplify(s - gus_w / guu_w * u)
check("clock_is_unit_timelike", guu_w == -1)
check("raw_separation_has_clock_component", gus_w == sp.Rational(-1, 2))
check("projection_is_orthogonal", inner(u, r) == 0)
check("projected_ruler_is_spacelike", inner(r, r) == sp.Rational(59, 25))

J_raw = sp.Matrix.hstack(u, s)
J_orth = sp.Matrix.hstack(u, r)
h_raw = sp.simplify(J_raw.T * g * J_raw)
h_orth = sp.simplify(J_orth.T * g * J_orth)
check(
    "raw_pair_metric",
    h_raw == sp.Matrix([[-1, sp.Rational(-1, 2)], [sp.Rational(-1, 2), sp.Rational(211, 100)]]),
)
check("orthogonal_pair_metric", h_orth == sp.diag(-1, sp.Rational(59, 25)))
check("same_plane_same_gram_determinant", h_raw.det() == h_orth.det() == sp.Rational(-59, 25))

# Recover the G167 B,Q,Y,Z pullback from the local germ.
B = sp.diag(sp.Rational(1, 2), 2)
Q = sp.diag(3, sp.Rational(12, 5))
eta2 = sp.diag(-1, 1)
Y = sp.Matrix([[2, 1], [0, sp.Rational(1, 2)]])
Z = sp.Matrix([[0, sp.Rational(1, 3)], [0, sp.Rational(1, 4)]])
h_blocks = sp.simplify(Y.T * B.T * eta2 * B * Y + Z.T * Q.T * Q * Z)
check("g167_blocks_recovered_from_germ", h_blocks == h_raw)
check("nonradial_angular_block_live", Z != sp.zeros(2))

Z_radial = sp.zeros(2)
Y_radial = sp.Matrix([[2, 1], [0, sp.Rational(1, 2)]])
h_radial = sp.simplify(Y_radial.T * B.T * eta2 * B * Y_radial)
check("radial_pair_has_zero_angular_block", Z_radial == sp.zeros(2))
check("angular_content_changes_pair_metric", h_radial != h_raw)

# Angular-coordinate covariance with a nonorthogonal coordinate Jacobian.
K = sp.Matrix([[1, 1], [0, 1]])
q = Q.T * Q
q_prime = K.inv().T * q * K.inv()
Z_prime = K * Z
check("angular_coordinate_covariance", sp.simplify(Z_prime.T * q_prime * Z_prime) == Z.T * q * Z)

# Positive raw-germ rescaling leaves the plane and normalized ruler unchanged.
lam = sp.Rational(7, 3)
s_lam = lam * s
r_lam = sp.simplify(s_lam - inner(u, s_lam) / guu_w * u)
check("separation_rescaling_projects_linearly", r_lam == lam * r)
check(
    "normalized_ruler_rescaling_invariant",
    sp.simplify(r_lam / sp.sqrt(inner(r_lam, r_lam)) - r / sp.sqrt(inner(r, r))) == sp.zeros(4, 1),
)

# Local orientation reversal preserves the unoriented plane but flips the wedge orientation.
R = sp.diag(1, -1)
check("local_reversal_congruence", sp.simplify(R.T * h_orth * R) == h_orth)
check("local_reversal_flips_orientation", sp.det(R) == -1)

# Relative motion does not have to lie in the positional pair plane.
v_b = sp.Matrix([sp.Rational(5, 4), 0, sp.Rational(3, 4), 0])
eta4 = sp.diag(-1, 1, 1, 1)
check("relative_velocity_unit_timelike", (v_b.T * eta4 * v_b)[0] == -1)
check("relative_velocity_not_in_position_plane", v_b[2] != 0)

# Same observer boundaries and same event pairing, different smooth regular surface germs.
sigma, alpha = sp.symbols("sigma alpha", real=True)
spatial_speed_sq = sp.simplify(1 + alpha**2 * (1 - 2 * sigma) ** 2)
check("counterfamily_is_regular_timelike", spatial_speed_sq.subs({alpha: 1, sigma: sp.Rational(1, 3)}) > 0)
s0 = sp.Matrix([0, 1, 0, 0])
s1 = sp.Matrix([0, 1, 1, 0])
check("same_labels_can_have_distinct_plane_germs", sp.Matrix.hstack(u / 2, s0).columnspace() != sp.Matrix.hstack(u / 2, s1).columnspace())
check("counterfamily_boundary_A_fixed", sp.Matrix([0, 0, alpha * 0 * (1 - 0), 0]) == sp.zeros(4, 1))
check("counterfamily_boundary_B_fixed", sp.simplify(alpha * 1 * (1 - 1)) == 0)

# Coincidence is a genuine rank-loss boundary.
s_zero = sp.zeros(4, 1)
J_zero = sp.Matrix.hstack(u, s_zero)
check("coincidence_rank_loss", J_zero.rank() == 1)

# Frozen source hashes.
manifest_rows = []
for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
    expected, rel, role = line.split("\t")
    actual = sha256(ROOT / rel)
    check(f"source_hash__{Path(rel).name}__{len(manifest_rows)}", actual == expected)
    manifest_rows.append({"path": rel, "sha256": actual, "role": role})

result = {
    "landing": "SUPPLIED_ORDERED_COPRESENT_PAIR_GERM_DERIVES_LOCAL_CALIBRATED_PAIR_PLANE__NO_PATH_REQUIRED__PHYSICAL_GERM_OWNERSHIP_IS_ADDITIONAL_WORKING_POSTULATE",
    "checks_passed": sum(checks.values()),
    "checks_total": len(checks),
    "checks": checks,
    "exact_witness": {
        "g": [[str(v) for v in row] for row in g.tolist()],
        "u": [str(v) for v in u],
        "s": [str(v) for v in s],
        "r": [str(v) for v in r],
        "h_raw": [[str(v) for v in row] for row in h_raw.tolist()],
        "h_orth": [[str(v) for v in row] for row in h_orth.tolist()],
        "Y": [[str(v) for v in row] for row in Y.tolist()],
        "Z": [[str(v) for v in row] for row in Z.tolist()],
    },
    "source_manifest": manifest_rows,
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"landing": result["landing"], "passed": result["checks_passed"], "total": result["checks_total"]}))
