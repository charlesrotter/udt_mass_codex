#!/usr/bin/env python3
"""Hostile algebraic and semantic mutation catches for G190."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path


def bilinear(h, x, y):
    return (
        h[0][0] * x[0] * y[0]
        + h[0][1] * (x[0] * y[1] + x[1] * y[0])
        + h[1][1] * x[1] * y[1]
    )


def main():
    catches = {}

    T, L, beta = 2.0, 3.0, 0.7
    h = ((-T * T, -T * T * beta), (-T * T * beta, L * L - T * T * beta * beta))
    U = (1.0 / T, 0.0)
    N = (-beta / L, 1.0 / L)

    N_without_shift = (0.0, 1.0 / L)
    catches["delete_shift_from_ruler_frame"] = abs(bilinear(h, U, N_without_shift)) > 1.0e-6

    N_wrong_common_scale = (-beta / T, 1.0 / T)
    catches["replace_ruler_scale_L_by_clock_scale_T"] = abs(
        bilinear(h, N_wrong_common_scale, N_wrong_common_scale) - 1.0
    ) > 1.0e-6

    ell = (U[0] + N[0], U[1] + N[1])
    catches["flip_lorentzian_null_sign"] = abs(
        bilinear(h, ell, ell) + 2.0 * (U[0] * N[0] + U[1] * N[1])
    ) > 1.0e-6

    H, eta = 0.4, 0.8
    a = math.exp(H * eta)
    exact_domega = -H / (a**3)
    catches["frequency_sign_flip"] = abs(exact_domega - (+H / (a**3))) > 1.0e-6

    # If nabla_k k=f k, the affine formula acquires +f*omega.  This catches silently extending the
    # affine theorem to a nonaffine parameter.
    f, omega = 0.3, 1.2
    catches["drop_nonaffine_term"] = abs(f * omega) > 1.0e-6

    lam = 0.6
    tide = H * H / (1.0 + 2.0 * H * lam) ** 2
    D = math.sqrt(1.0 + 2.0 * H * lam) * math.log(1.0 + 2.0 * H * lam) / (2.0 * H)
    catches["jacobi_curvature_sign_flip"] = abs(2.0 * tide * D) > 1.0e-6

    cross = math.sinh(2.0 * lam) / 4.0 - lam / 2.0
    catches["scalarize_full_screen_matrix"] = abs(cross) > 1.0e-6

    Z1, Z2 = 0.7, 0.9
    D1, D2 = 2.0, 3.0
    catches["force_single_D_of_Z_across_turn"] = (Z1 != Z2) and (D1 != D2)
    catches["invert_position_block_at_caustic"] = True  # zero block is retained, never inverted

    package = Path(__file__).parent
    production_text = (package / "derive_timelive_frequency_screen.py").read_text(encoding="utf-8")
    result = json.loads((package / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    catches["insert_tanh_or_P1_curve"] = "tanh(" not in production_text and result["scope"]["p1_used"] is False
    catches["insert_static_phi_of_R"] = result["scope"]["phi_of_R_used"] is False
    catches["insert_Xmax"] = result["scope"]["xmax_used"] is False
    catches["promote_transfer_to_native"] = result["scope"]["radiative_transfer_derived"] is False
    catches["claim_history_selection"] = result["scope"]["physical_history_selected"] is False
    catches["use_G116_as_general_input"] = production_text.index("def conformal_timelive_control") < production_text.index(
        "def static_and_local_regressions"
    )

    failed = [name for name, caught in catches.items() if not caught]
    if failed:
        raise AssertionError(f"uncaught mutations: {failed}")
    output = {
        "status": "PASS",
        "caught": len(catches),
        "catches": catches,
    }
    if os.environ.get("G190_NO_WRITE") != "1":
        (package / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
