#!/usr/bin/env python3
"""Exercise explicit countermodels against the five tempting G135 overclaims."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")


def chi(q: F) -> F:
    return (1 - q) / (1 + q)


def main() -> None:
    caught: dict[str, bool] = {}

    # Overclaim: projective scalar determines physical ruler length/common scale.
    T1, L1 = F(1), F(2)
    T2, L2 = F(2), F(4)
    caught["projective_scalar_is_not_physical_length"] = (
        chi(T1 / L1) == chi(T2 / L2) and L1 != L2
    )
    caught["projective_scalars_do_not_recover_common_scale"] = (
        T1 / L1 == T2 / L2 and T1 * L1 != T2 * L2
    )

    # Overclaim: c_E fixes X_max.  Any power k of c_E has dimension vector
    # (k,-k) in (length,time), which cannot equal the pure-length target (1,0).
    ce_dimension = (F(1), F(-1))
    length_dimension = (F(1), F(0))
    k_for_length_exponent = length_dimension[0] / ce_dimension[0]
    caught["c_E_does_not_fix_Xmax"] = (
        k_for_length_exponent * ce_dimension[1] != length_dimension[1]
    )

    # Overclaim: the anchored projective chart is unique among all smooth lawful markings.
    eps = F(1, 4)
    x = F(1, 3)
    f_x = x + eps * x * (1 - x * x)
    caught["unrestricted_chart_uniqueness_false"] = f_x != x

    # Overclaim: angular/screen data can be attached after a base-only terminal readout.
    # Registered exact values from the base and full two-column pullbacks.
    q_base_squared = F(1, 16)  # (-h00)^2/(-det h) for diag(-1/4,4)
    q_full_squared = F(81, 1792)
    caught["orchestra_must_precede_terminal_readout"] = q_base_squared != q_full_squared

    # Overclaim: bounded display uses ordinary addition.
    x1, x2 = F(1, 3), F(1, 5)
    composed = (x1 + x2) / (1 + x1 * x2)
    caught["bounded_display_not_ordinary_additive"] = composed != x1 + x2

    passed = sum(caught.values())
    result = {
        "schema": "udt-g135-catch-proofs-v1",
        "status": "PASS" if passed == len(caught) else "FAIL",
        "caught": passed,
        "total": len(caught),
        "checks": caught,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
