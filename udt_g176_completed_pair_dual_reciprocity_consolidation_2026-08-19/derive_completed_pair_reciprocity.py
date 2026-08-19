#!/usr/bin/env python3
"""Exact symbolic production checks for the G176 completed-pair theorem."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def source_hashes() -> tuple[int, list[str]]:
    rows = (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    checked: list[str] = []
    for row in rows:
        expected, relative, _role = row.split("\t")
        actual = hashlib.sha256((REPO / relative).read_bytes()).hexdigest()
        assert actual == expected, f"source hash mismatch: {relative}"
        checked.append(relative)
    return len(checked), checked


def main() -> None:
    T, Ls, beta, m, k = sp.symbols("T L_sigma beta m k", positive=True, finite=True)
    A, v2, r2, b2 = sp.symbols("A v2 r2 b2", positive=True, finite=True)

    h_sigma = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, Ls**2 - T**2 * beta**2],
        ]
    )
    jac = sp.diag(1, 1 / m)
    h_s = sp.simplify(jac.T * h_sigma * jac)

    checks: dict[str, bool] = {}
    checks["auxiliary_determinant"] = sp.simplify(h_sigma.det() + T**2 * Ls**2) == 0
    checks["calibrated_h00"] = sp.simplify(h_s[0, 0] + T**2) == 0
    checks["calibrated_h01"] = sp.simplify(h_s[0, 1] + T**2 * beta / m) == 0
    checks["calibrated_h11"] = sp.simplify(
        h_s[1, 1] - (Ls**2 - T**2 * beta**2) / m**2
    ) == 0
    checks["calibrated_determinant"] = sp.simplify(h_s.det() + T**2 * Ls**2 / m**2) == 0

    beta_s = sp.simplify(h_s[0, 1] / h_s[0, 0])
    L2_s = sp.simplify(h_s[1, 1] - h_s[0, 1] ** 2 / h_s[0, 0])
    checks["shift_survives"] = sp.simplify(beta_s - beta / m) == 0
    checks["spatial_scale"] = sp.simplify(L2_s - Ls**2 / m**2) == 0

    m_rec = T * Ls
    h_rec = sp.simplify(h_s.subs(m, m_rec))
    checks["reciprocal_determinant"] = sp.simplify(h_rec.det() + 1) == 0
    checks["reciprocal_spatial_scale"] = sp.simplify(
        h_rec[1, 1] - h_rec[0, 1] ** 2 / h_rec[0, 0] - 1 / T**2
    ) == 0
    checks["reciprocal_shift"] = sp.simplify(h_rec[0, 1] / h_rec[0, 0] - beta / (T * Ls)) == 0

    # Converse: -det(h_s)=1 gives m^2=T^2 L_sigma^2; positive m makes the root unique.
    determinant_equation = sp.solve(sp.Eq(-h_s.det(), 1), m)
    checks["unique_positive_root"] = determinant_equation == [T * Ls]

    # Positive auxiliary reparameterization sigma=k*sigma_tilde.
    h_tilde = h_sigma.subs({Ls: k * Ls, beta: k * beta})
    m_tilde = k * m
    jac_tilde = sp.diag(1, 1 / m_tilde)
    checks["positive_reparameterization_covariance"] = sp.simplify(
        jac_tilde.T * h_tilde * jac_tilde - h_s
    ) == sp.zeros(2)

    # Orientation reversal flips the shift component but preserves determinant and scales.
    h_reverse = h_sigma.subs(beta, -beta)
    h_reverse_s = sp.simplify(jac.T * h_reverse * jac)
    checks["orientation_reversal_determinant"] = sp.simplify(h_reverse_s.det() - h_s.det()) == 0
    checks["orientation_reversal_shift"] = sp.simplify(
        h_reverse_s[0, 1] + h_s[0, 1]
    ) == 0

    # Static spherical specialization with A=exp(2 phi).
    H = A * v2 + r2 * b2
    static_m2 = sp.simplify(H / A)
    static_spatial = sp.simplify(H / static_m2)
    checks["static_reciprocal_density"] = sp.simplify(static_m2 - (v2 + r2 * b2 / A)) == 0
    checks["static_spatial_scale"] = sp.simplify(static_spatial - A) == 0
    checks["static_determinant"] = sp.simplify(-(1 / A) * static_spatial + 1) == 0
    checks["static_terminal_phi"] = sp.simplify(sp.log(static_spatial / (1 / A)) / 4 - sp.log(A) / 2) == 0
    checks["pure_radial_recovery"] = sp.simplify(static_m2.subs(b2, 0) - v2) == 0
    checks["angular_turn_regular"] = sp.simplify(static_m2.subs(v2, 0) - r2 * b2 / A) == 0

    source_count, checked_sources = source_hashes()
    assert all(checks.values()), [name for name, passed in checks.items() if not passed]

    result = {
        "audit": "G176",
        "landing": "COMPLETED_PAIR_DUAL_RECIPROCITY_UNIQUELY_FIXES_RECIPROCAL_RULER__ARBITRARY_CALIBRATIONS_ARE_CONTROL_QUERIES",
        "epistemic_grade": "DERIVED_CONDITIONAL_ON_WORKING_FOUNDATIONAL_CLARIFICATION",
        "symbolic_check_count": len(checks),
        "symbolic_checks": checks,
        "source_hash_count": source_count,
        "source_hashes_pass": True,
        "checked_sources": checked_sources,
        "generic_formula": "m=T*L_sigma=sqrt(-det(h_sigma))",
        "static_formula": "m^2=exp(-2*phi)*H",
        "open_scope": [
            "physical event and pair-germ population",
            "singular and global strata",
            "non-scalar transport",
            "dimensionful distance and X_max",
            "observations and radiative transfer",
            "dynamics action source matter bootstrap mass signalling",
        ],
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
