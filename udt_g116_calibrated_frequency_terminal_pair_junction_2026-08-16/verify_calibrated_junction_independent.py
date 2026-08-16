#!/usr/bin/env python3
"""Standard-library Fraction verification of the G116 junction.

This script does not import SymPy, the production implementation, or its JSON.
"""

from __future__ import annotations

import json
import random
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def raw(values: tuple[F, F, F, F, F, F, F]) -> dict[str, F]:
    ell, n, b, bt, q, qt, w2 = values
    p2 = (ell - n + b * b - bt / 2) / 2
    p2f = p2 + w2 / 2
    optical = 2 * ell + 2 * n + bt
    v = b - q
    dv = bt - qt
    f2 = b * b / 2 - n + bt / 2 - qt
    return {
        "p2": p2,
        "p2f": p2f,
        "optical": optical,
        "v": v,
        "dv": dv,
        "f2": f2,
        "z2": f2 + v * v / 2,
    }


def gauge(values: tuple[F, F, F, F, F, F, F], a: F, at: F):
    ell, n, b, bt, q, qt, w2 = values
    return (
        ell - 2 * a * b - 2 * a * a,
        n + 2 * a * b + 2 * a * a - at,
        b + 2 * a,
        bt + 2 * at,
        q + 2 * a,
        qt + 2 * at,
        w2,
    )


def main() -> None:
    rng = random.Random(11620260816)
    trials = 256
    junction_ok = True
    gauge_ok = True
    family_ok = True
    max_numerator = 0

    for _ in range(trials):
        values = tuple(F(rng.randint(-17, 17), rng.randint(2, 19)) for _ in range(7))
        data = raw(values)
        junction_residual = data["f2"] - (
            data["p2"] - data["optical"] / 4 + data["dv"]
        )
        fixed_residual = data["f2"] - (
            data["p2f"] - values[-1] / 2 - data["optical"] / 4 + data["dv"]
        )
        junction_ok &= junction_residual == 0 and fixed_residual == 0
        max_numerator = max(max_numerator, abs(junction_residual.numerator), abs(fixed_residual.numerator))

        transformed = raw(gauge(values, F(rng.randint(-9, 9), 11), F(rng.randint(-9, 9), 13)))
        gauge_ok &= all(data[key] == transformed[key] for key in ("p2", "optical", "v", "dv", "f2", "z2"))

        alpha = F(rng.randint(-8, 8), rng.randint(1, 9))
        z1, z2, p1, p2 = (F(rng.randint(-12, 12), 7) for _ in range(4))
        direct = alpha * (z1 + z2) + (1 - alpha) * (p1 + p2)
        composed = alpha * z1 + (1 - alpha) * p1 + alpha * z2 + (1 - alpha) * p2
        pure = alpha * z1 + (1 - alpha) * z1
        family_ok &= direct == composed and pure == z1

    p = F(7, 13)
    pure_data = raw((p, -p, F(0), F(0), F(0), F(0), F(0)))
    pure_ok = pure_data["p2"] == p and pure_data["f2"] == p and pure_data["optical"] == 0

    # Direct positive rational endpoint ratios verify exact telescope and reversal.
    ws, wm, wo = F(17, 5), F(13, 7), F(11, 3)
    frequency_groupoid = (ws / wm) * (wm / wo) == ws / wo and (ws / wm) * (wm / ws) == 1
    cs, cm, co = F(19, 11), F(23, 13), F(29, 17)
    terminal_groupoid = (cm / cs) * (co / cm) == co / cs and (cm / cs) * (cs / cm) == 1

    # Generic witness disproves a universal zeta=phi identification.
    witness = raw((F(2, 7), F(-3, 11), F(5, 13), F(-7, 17), F(-2, 9), F(4, 15), F(1, 8)))
    universal_identity_rejected = witness["v"] != 0 or witness["f2"] != witness["p2"]

    checks = {
        "junction_256_fraction_trials": junction_ok,
        "gauge_invariance_256_fraction_trials": gauge_ok,
        "normalized_family_256_fraction_trials": family_ok,
        "pure_reciprocal_control": pure_ok,
        "frequency_ratio_composition_reversal": frequency_groupoid,
        "matched_terminal_ratio_composition_reversal": terminal_groupoid,
        "universal_zeta_equals_phi_rejected_generically": universal_identity_rejected,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "method": "standard-library Fraction randomized identities; no production import",
        "trials": trials,
        "maximum_identity_residual_numerator": max_numerator,
        "generic_witness": {k: str(v) for k, v in witness.items()},
        "checks": checks,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
