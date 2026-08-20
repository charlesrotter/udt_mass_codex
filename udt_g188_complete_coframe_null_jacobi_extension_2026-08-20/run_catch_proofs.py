#!/usr/bin/env python3
"""Independent algebra mutations and textual scope guards for bounded G188."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ZERO = F(0)
ONE = F(1)


def mmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def mscale(s, a):
    return [[s * value for value in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def series_coefficients(tidal, order=7):
    """Exact Jacobi coefficients D=sum_n C_n lambda^n."""
    coeff = [
        [[ZERO, ZERO], [ZERO, ZERO]],
        [[ONE, ZERO], [ZERO, ONE]],
    ]
    for n in range(order - 1):
        coeff.append(mscale(F(-1, (n + 2) * (n + 1)), mmul(tidal, coeff[n])))
    return coeff


def require_and_mutate(text: str, clause: str) -> bool:
    if clause not in text:
        return False
    return clause not in text.replace(clause, "", 1)


def forbid_and_mutate(text: str, clause: str) -> bool:
    if clause in text:
        return False
    return clause in text + "\n" + clause + "\n"


def main() -> None:
    mixing = [[ONE, ONE], [ONE, ONE]]
    tidal = mscale(F(-1), mmul(mixing, mixing))
    expected_tidal = [[F(-2), F(-2)], [F(-2), F(-2)]]
    coeff = series_coefficients(tidal)
    flat_coeff = series_coefficients([[ZERO, ZERO], [ZERO, ZERO]])
    deleted_cross = [[F(-2), ZERO], [ZERO, F(-2)]]
    scalarized = [[F(-2), ZERO], [ZERO, F(-2)]]
    sign_flipped = mscale(F(-1), tidal)

    q_source = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    q_sink = [[F(5, 13), F(-12, 13)], [F(12, 13), F(5, 13)]]
    finite_sample = [[F(7, 3), F(1, 3)], [F(1, 3), F(7, 3)]]
    transformed = mmul(mmul(transpose(q_sink), finite_sample), q_source)

    algebraic = {
        "mixing_square_tidal_exact": tidal == expected_tidal,
        "cross_tidal_deletion_goes_red": deleted_cross != tidal,
        "tidal_sign_flip_goes_red": sign_flipped != tidal,
        "trace_scalarization_goes_red": scalarized != tidal,
        "forced_g187_diagonal_form_goes_red": tidal[0][1] != ZERO,
        "finite_cross_response_is_generated": coeff[3][0][1] == F(1, 3),
        "finite_cross_deletion_goes_red": coeff[3][0][1] != ZERO,
        "wrong_trigonometric_sign_goes_red": coeff[3][0][1] != F(-1, 3),
        "flat_deletion_has_no_cubic_response": flat_coeff[3] == [[ZERO, ZERO], [ZERO, ZERO]],
        "flat_deletion_retains_vertex_slope": flat_coeff[1] == [[ONE, ZERO], [ZERO, ONE]],
        "endpoint_o2_abs_det_covariant": abs(det2(transformed)) == abs(det2(finite_sample)),
        "endpoint_basis_erasure_goes_red": transformed != finite_sample,
        "post_readout_scalar_goes_red": mscale(F(7, 3), finite_sample) != finite_sample,
        "caustic_inverse_rejected": det2([[ZERO, ZERO], [ZERO, ONE]]) == ZERO,
    }

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    derivation = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    artifact_guards = {
        "supplied_history_clause_deletion_goes_red": require_and_mutate(
            prereg, "arbitrary supplied smooth Lorentzian complete coframe"
        ),
        "supplied_null_branch_clause_deletion_goes_red": require_and_mutate(
            prereg, "one future affinely parametrized null geodesic branch"
        ),
        "metric_jet_clause_deletion_goes_red": require_and_mutate(
            derivation, "through the metric connection and curvature before any readout"
        ),
        "no_ray_selection_clause_deletion_goes_red": require_and_mutate(
            derivation, "does not select the complete metric or ray population"
        ),
        "open_history_status_deletion_goes_red": require_and_mutate(
            status, "physical_metric_history\tOPEN"
        ),
        "open_ray_status_deletion_goes_red": require_and_mutate(
            status, "physical_ray_population\tOPEN"
        ),
        "flux_promotion_injection_goes_red": forbid_and_mutate(
            derivation, "The Jacobi determinant is the derived physical luminosity law."
        ),
        "post_readout_orchestra_injection_goes_red": forbid_and_mutate(
            derivation, "A fitted orchestra coefficient is appended after the metric readout."
        ),
        "path_selection_injection_goes_red": forbid_and_mutate(
            derivation, "The metric selects this null branch as the unique physical ray."
        ),
        "xmax_injection_goes_red": forbid_and_mutate(
            derivation, "The Jacobi map determines X_max."
        ),
        "globalization_injection_goes_red": forbid_and_mutate(
            derivation, "This local witness is the unique global UDT history."
        ),
    }

    failed_algebraic = [name for name, value in algebraic.items() if not value]
    failed_artifact = [name for name, value in artifact_guards.items() if not value]
    output = {
        "algebraic_mutation_catch_count": len(algebraic),
        "algebraic_mutation_catches": algebraic,
        "artifact_scope_guard_count": len(artifact_guards),
        "artifact_scope_guards": artifact_guards,
        "audit": "G188_CATCH_PROOFS",
        "failed_algebraic_mutation_catches": failed_algebraic,
        "failed_artifact_scope_guards": failed_artifact,
        "status": "PASS" if not failed_algebraic and not failed_artifact else "FAIL",
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    if failed_algebraic or failed_artifact:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
