#!/usr/bin/env python3
"""Exact G157 semidirect composition and source regrading derivation."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "7b783451"
ALLOWED_ROLES = {
    "KINEMATIC_EVALUATOR",
    "KINEMATIC_CHANNEL_IDENTITY",
    "EXPECTED_CHANNEL_FREEDOM",
    "GENUINE_TYPED_OWNER_OPEN",
    "CONDITIONAL_QUERY_RESTRICTION",
    "HISTORY_DATA_OR_LAW_OPEN",
    "GENUINE_QUERY_OUTPUT_MULTIPLICITY",
    "ALGEBRAIC_SUPPORT",
    "KINEMATIC_LIVENESS_WITNESS",
    "HISTORY_SPACE_CLASSIFICATION",
    "GENUINE_EVOLUTION_LAW_OPEN",
    "MIXED_PROGRAM_FRAME",
}
LANDING = (
    "MIXED_REGRADING__BPLUS2_NO_FIXED_CHANNEL_RATIO_DERIVED__"
    "REGIME_DEPENDENT_BASE_BALANCE_ALLOWED_BY_NATIVE_SEMIDIRECT_COMPOSITION__"
    "SUPPLIED_VALUED_HISTORY_CAN_CARRY_CHANGING_SCORE__FULL_SCREEN_MIXING_"
    "COMPOSITION_PHYSICAL_CROSS_QUERY_CARRY_AND_HISTORY_EVOLUTION_REMAIN_OPEN"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 20
    assert [row["source_id"] for row in rows] == [f"S{i:02d}" for i in range(1, 21)]
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"]), row["source_id"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["source_id"]


def verify_ledger(rows: list[dict[str, str]], source_ids: set[str]) -> None:
    assert len(rows) == 20
    assert {row["source_id"] for row in rows} == source_ids
    assert all(row["active_depth_only_lockstep"] == "NO" for row in rows)
    assert all(row["regraded_role"] in ALLOWED_ROLES for row in rows)
    assert any(row["regraded_role"] == "EXPECTED_CHANNEL_FREEDOM" for row in rows)
    assert any(row["regraded_role"] == "GENUINE_EVOLUTION_LAW_OPEN" for row in rows)
    assert any(row["regraded_role"] == "GENUINE_TYPED_OWNER_OPEN" for row in rows)


def C(sigma, delta, mu):
    return sp.exp(sigma) * sp.diag(sp.exp(-delta), sp.exp(delta)) * sp.Matrix([[1, mu], [0, 1]])


def exact_checks() -> dict[str, object]:
    checks: list[str] = []
    s, d, m = sp.symbols("sigma delta mu", real=True)
    matrix = sp.simplify(C(s, d, m))
    assert matrix == sp.Matrix(
        [[sp.exp(s - d), sp.exp(s - d) * m], [0, sp.exp(s + d)]]
    )
    checks.append("unique_positive_triangular_channel_parameterization")

    # The parameterization has full rank three everywhere: no algebraic fixed
    # ratio among common scale, reciprocal grading, and normalized shift.
    entries = sp.Matrix([matrix[0, 0], matrix[0, 1], matrix[1, 1]])
    jac = entries.jacobian((s, d, m))
    jac_det = sp.simplify(jac.det())
    assert sp.simplify(jac_det + 2 * sp.exp(3 * s - d)) == 0
    checks.append("channel_coordinate_jacobian_rank_three")

    s1, d1, m1, s2, d2, m2 = sp.symbols(
        "s1 d1 m1 s2 d2 m2", real=True
    )
    product = sp.simplify(C(s2, d2, m2) * C(s1, d1, m1))
    composed_mu = sp.simplify(m1 + sp.exp(2 * d1) * m2)
    predicted = sp.simplify(C(s2 + s1, d2 + d1, composed_mu))
    assert sp.simplify(product - predicted) == sp.zeros(2)
    checks.append("native_semidirect_composition")

    inverse = sp.simplify(C(-s, -d, -sp.exp(-2 * d) * m))
    assert sp.simplify(inverse * C(s, d, m) - sp.eye(2)) == sp.zeros(2)
    assert sp.simplify(C(s, d, m) * inverse - sp.eye(2)) == sp.zeros(2)
    checks.append("native_semidirect_inverse")

    # Common scale is central, while reciprocal depth acts on normalized shift.
    central = sp.exp(s) * sp.eye(2)
    arbitrary = C(s1, d1, m1)
    assert sp.simplify(central * arbitrary - arbitrary * central) == sp.zeros(2)
    checks.append("common_scale_central_in_Bplus2")
    conjugated = sp.simplify(
        sp.diag(sp.exp(-d), sp.exp(d))
        * sp.Matrix([[1, m], [0, 1]])
        * sp.diag(sp.exp(d), sp.exp(-d))
    )
    assert conjugated == sp.Matrix([[1, sp.exp(-2 * d) * m], [0, 1]])
    checks.append("reciprocal_depth_rescales_shift_under_conjugation")

    # A smooth endpoint-state family with changing channel balance. Pair edges
    # compose because C_ji=R_j R_i^-1, not because R(t) is a one-parameter group.
    def R(t):
        return sp.Matrix([[1 + t, t**2], [0, 1 + t**2]])

    R0, R1, R2 = R(sp.Integer(0)), R(sp.Integer(1)), R(sp.Integer(2))
    C10 = sp.simplify(R1 * R0.inv())
    C21 = sp.simplify(R2 * R1.inv())
    C20 = sp.simplify(R2 * R0.inv())
    assert sp.simplify(C21 * C10 - C20) == sp.zeros(2)
    checks.append("changing_balance_endpoint_family_composes_exactly")
    assert R2 != R1 * R1
    checks.append("changing_balance_family_is_not_depth_only_homomorphism")

    # A genuine one-parameter subgroup is a stricter ansatz. For generator
    # constants p,q,r, sigma and delta are linear and mu is fixed by them.
    t, u, p, q, r = sp.symbols("t u p q r", real=True, nonzero=True)
    mu_t = r * (sp.exp(2 * q * t) - 1) / (2 * q)
    mu_u = r * (sp.exp(2 * q * u) - 1) / (2 * q)
    mu_tu = r * (sp.exp(2 * q * (t + u)) - 1) / (2 * q)
    assert sp.simplify(mu_tu - (mu_u + sp.exp(2 * q * u) * mu_t)) == 0
    assert sp.simplify(C(p * t, q * t, mu_t) * C(p * u, q * u, mu_u) - C(p * (t + u), q * (t + u), mu_tu)) == sp.zeros(2)
    # Separate q=0 branch: the normalized shift is then additive.
    p0, r0, t0, u0 = sp.symbols("p0 r0 t0 u0", real=True)
    assert sp.simplify(
        C(p0 * t0, 0, r0 * t0)
        * C(p0 * u0, 0, r0 * u0)
        - C(p0 * (t0 + u0), 0, r0 * (t0 + u0))
    ) == sp.zeros(2)
    checks.append("scalar_parameter_full_transition_subgroup_is_extra_fixed_generator_ansatz")

    # The founded reciprocal subgroup is the special sigma=mu=0 slice, not a
    # theorem that the full complete transition must remain on that slice.
    founded_slice = C(0, d, 0)
    assert founded_slice == sp.diag(sp.exp(-d), sp.exp(d))
    checks.append("founded_reciprocal_core_is_special_slice_not_full_lockstep")

    assert len(checks) == 10
    return {
        "exact_checks": len(checks),
        "exact_check_names": checks,
        "channel_jacobian_determinant": str(jac_det),
        "composition_law": "(s2,d2,m2)*(s1,d1,m1)=(s2+s1,d2+d1,m1+exp(2d1)m2)",
        "inverse_law": "(s,d,m)^-1=(-s,-d,-exp(-2d)m)",
        "changing_balance_frames": [str(R0), str(R1), str(R2)],
        "active_depth_only_lockstep_sources": 0,
    }


def main() -> None:
    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    ledger = read_tsv(HERE / "REGRADING_LEDGER.tsv")
    verify_manifest(manifest)
    verify_ledger(ledger, {row["source_id"] for row in manifest})
    result = {
        "status": "PASS",
        "landing": LANDING,
        "registered_outcome_class": "MIXED_REGRADING",
        "source_count": len(manifest),
        "ledger_count": len(ledger),
        "role_counts": dict(sorted(Counter(row["regraded_role"] for row in ledger).items())),
        "fixed_channel_ratio_derived": False,
        "regime_dependent_balance_kinematically_allowed": True,
        "physical_regime_score_derived": False,
        "cross_query_carry_derived": False,
        "history_evolution_derived": False,
        **exact_checks(),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
