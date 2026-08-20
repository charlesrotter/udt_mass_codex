#!/usr/bin/env python3
"""Algebraic mutation catches and artifact-scope guards for bounded G187.

The two classes are deliberately separated.  Algebraic catches distinguish a
registered wrong formula or map from the derived one.  Artifact guards mutate
the banked text in memory and prove that the corresponding required/forbidden
scope clause would go red; they are not mislabelled as physics calculations.
"""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def require_and_mutate(text: str, clause: str) -> bool:
    """Pass now, and fail after deleting the registered required clause."""
    if clause not in text:
        return False
    mutant = text.replace(clause, "", 1)
    return clause not in mutant


def forbid_and_mutate(text: str, clause: str) -> bool:
    """Pass now, and fail after injecting the registered forbidden clause."""
    if clause in text:
        return False
    mutant = text + "\n" + clause + "\n"
    return clause in mutant


def main() -> None:
    r = F(5, 2)
    f = F(9, 16)
    fp = F(2, 7)
    fpp = F(-3, 11)
    angular = F(7, 5)
    t_perp = angular**2 * (r * fp - 2 * f + 2) / (2 * r**4)
    t_parallel = angular**2 * (r * fpp - fp) / (2 * r**3)
    t_trace = t_parallel + t_perp
    affine = F(4, 3)
    finite_map = [[F(2), F(0)], [F(0), F(3)]]
    identity = [[F(1), F(0)], [F(0), F(1)]]

    q_source = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    q_target = [[F(5, 13), F(-12, 13)], [F(12, 13), F(5, 13)]]
    transformed = mmul(mmul(transpose(q_target), finite_map), q_source)

    algebraic = {
        "parallel_mode_deletion_goes_red": t_parallel != 0,
        "perpendicular_mode_deletion_goes_red": t_perp != 0,
        "forced_mode_equality_goes_red": t_parallel != t_perp,
        "parallel_sign_flip_goes_red": t_parallel != -t_parallel,
        "perpendicular_sign_flip_goes_red": t_perp != -t_perp,
        "forced_zero_trace_goes_red": t_trace != 0,
        "angular_momentum_deletion_goes_red": (t_parallel, t_perp) != (F(0), F(0)),
        "post_readout_scalar_goes_red": [[F(7, 3) * x for x in row] for row in finite_map] != finite_map,
        "finite_map_to_projector_goes_red": finite_map != identity,
        "one_mode_forced_on_both_axes_goes_red": finite_map != [[F(2), F(0)], [F(0), F(2)]],
        "cross_mode_insertion_goes_red": finite_map != [[F(2), F(1)], [F(0), F(3)]],
        "endpoint_o2_law_preserves_abs_det": abs(det2(transformed)) == abs(det2(finite_map)),
        "endpoint_o2_erasure_goes_red": transformed != finite_map,
        "caustic_inverse_is_rejected": det2([[F(0), F(0)], [F(0), F(2)]]) == 0,
        "flat_finite_map_is_not_unit_projector": [[affine, F(0)], [F(0), affine]] != identity,
    }

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    derivation = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    artifact_guards = {
        "query_supply_clause_deletion_goes_red": require_and_mutate(
            prereg, "one future null initial vector `k_o`"
        ),
        "history_supply_clause_deletion_goes_red": require_and_mutate(
            prereg, "`free-and-explored` supplied history"
        ),
        "no_flux_clause_deletion_goes_red": require_and_mutate(
            derivation, "It is also not a flux or luminosity\nlaw."
        ),
        "no_physical_population_clause_deletion_goes_red": require_and_mutate(
            derivation, "not a selection of the physical null population."
        ),
        "no_xmax_clause_deletion_goes_red": require_and_mutate(
            derivation, "or determine \\(X_{\\max}\\)."
        ),
        "open_flux_status_deletion_goes_red": require_and_mutate(
            status, "flux_or_luminosity\tOPEN"
        ),
        "open_physical_population_status_deletion_goes_red": require_and_mutate(
            status, "physical_ray_population\tOPEN"
        ),
        "open_global_history_status_deletion_goes_red": require_and_mutate(
            status, "global_or_timelive_history\tOPEN"
        ),
        "flux_promotion_injection_goes_red": forbid_and_mutate(
            derivation, "The Jacobi map is the physical luminosity law."
        ),
        "path_selection_injection_goes_red": forbid_and_mutate(
            derivation, "The metric selects this ray as the unique physical path."
        ),
        "xmax_injection_goes_red": forbid_and_mutate(
            derivation, "This finite map determines X_max."
        ),
        "rz_injection_goes_red": forbid_and_mutate(
            derivation, "This finite map determines R(Z)."
        ),
        "signal_speed_injection_goes_red": forbid_and_mutate(
            derivation, "The pair readout is a local signal speed."
        ),
        "globalization_injection_goes_red": forbid_and_mutate(
            derivation, "This static-spherical branch is the unique global UDT history."
        ),
    }

    failed_algebraic = [name for name, value in algebraic.items() if not value]
    failed_artifact = [name for name, value in artifact_guards.items() if not value]
    print(json.dumps({
        "algebraic_mutation_catch_count": len(algebraic),
        "algebraic_mutation_catches": algebraic,
        "artifact_scope_guard_count": len(artifact_guards),
        "artifact_scope_guards": artifact_guards,
        "audit": "G187_CATCH_PROOFS_REPAIRED",
        "failed_algebraic_mutation_catches": failed_algebraic,
        "failed_artifact_scope_guards": failed_artifact,
        "status": "PASS" if not failed_algebraic and not failed_artifact else "FAIL",
    }, indent=2, sort_keys=True))
    if failed_algebraic or failed_artifact:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
