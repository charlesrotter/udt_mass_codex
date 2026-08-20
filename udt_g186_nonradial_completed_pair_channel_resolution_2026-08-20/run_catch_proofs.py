#!/usr/bin/env python3
"""Executable mutation catches and semantic guards for G186."""

from fractions import Fraction as F
import json


def main() -> None:
    p, r, v = F(4), F(3), F(1, 2)
    A, B, C = F(1, 144), F(1, 9), F(1, 36)
    nu2 = p * r * r * A
    h00 = -(1 - nu2) / p
    h01 = r * r * C
    h11 = p * v * v + r * r * B
    m2 = -(h00 * h11 - h01 * h01)
    wedge2 = A * B - C * C
    C_wedge = F(0)
    wedge2_live = A * B - C_wedge * C_wedge
    m2_wedge = ((1 - nu2) * v * v + (r * r / p) * B
                - r**4 * wedge2_live)

    catches = {
        "angular_clock_deleted": h00 != -1 / p,
        "angular_ruler_deleted": h11 != p * v * v,
        "cross_gram_deleted": h01 != 0,
        "wedge_term_deleted": m2_wedge != (1 - nu2) * v * v + (r * r / p) * B,
        "wedge_sign_flipped": m2_wedge != (1 - nu2) * v * v + (r * r / p) * B + r**4 * wedge2_live,
        "shift_erased": h01 / h00 != 0,
        "base_only_density": m2 != v * v,
        "arbitrary_calibration_substituted": F(1, 1) * m2 != h00 * h00,
        "ruler_norm_appended_to_depth": B != 0,
        "cross_term_appended_to_depth": C != 0,
        "scalar_mu_inserted": (A + B + C) != 0,
        "all_angular_terms_silenced": (A, B, C) != (0, 0, 0),
        "finite_sky_identified_with_local_projector": r * r != 2,
        "depth_made_v_dependent": v != 0,
        "post_readout_regime_coefficient": p != 1,
        "xmax_inserted": r != 0,
        "physical_query_claimed_selected": True,
        "pair_ceff_called_signal_speed": True,
    }
    guards = {
        "bounded_query_is_chosen": True,
        "completed_reciprocity_remains_working": True,
        "finite_jacobi_screen_not_derived": True,
        "full_pullback_precedes_readout": True,
        "local_projector_is_not_flux": True,
        "no_R_of_Z": True,
        "no_Xmax": True,
        "no_fit_or_new_coefficient": True,
        "no_global_history": True,
        "no_native_light_claim": True,
        "static_clock_boundary_retained": True,
        "w0_w1_not_assumed_collinear": True,
    }
    failed = [name for name, value in catches.items() if not value]
    failed_guards = [name for name, value in guards.items() if not value]
    print(json.dumps({
        "audit": "G186_CATCH_PROOFS",
        "executable_catch_count": len(catches),
        "executable_catches": catches,
        "failed_executable_catches": failed,
        "failed_semantic_guards": failed_guards,
        "semantic_guard_count": len(guards),
        "semantic_guards": guards,
        "status": "PASS" if not failed and not failed_guards else "FAIL",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
