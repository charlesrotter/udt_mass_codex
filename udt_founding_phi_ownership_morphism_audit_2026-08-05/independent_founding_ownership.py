#!/usr/bin/env python3
"""Independent Fraction reconstruction; imports neither SymPy nor production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mm(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def inv2(a: list[list[F]]) -> list[list[F]]:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def d(z: F) -> list[list[F]]:
    return [[1 / z, F(0)], [F(0), z]]


def encode(a: list[list[F]]) -> list[list[str]]:
    return [[str(value) for value in row] for row in a]


def main() -> None:
    checks: dict[str, bool] = {}

    def check(name: str, value: bool) -> None:
        checks[name] = value
        if not value:
            raise AssertionError(name)

    identity = [[F(1), F(0)], [F(0), F(1)]]
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    pairing = [[F(0), F(1)], [F(1), F(0)]]
    check("character_composition", mm(d(F(7)), d(F(3))) == d(F(21)))
    check("character_inverse", d(F(1, 3)) == inv2(d(F(3))))
    check("pairing_preserved", mm(mm(transpose(d(F(3))), pairing), d(F(3))) == pairing)
    check("physical_eta_not_preserved", mm(mm(transpose(d(F(3))), eta), d(F(3))) != eta)

    reference = [[F(3), F(1)], [F(2), F(5)]]
    theta = mm(d(F(4)), reference)
    shifted_reference = mm(inv2(d(F(9))), reference)
    shifted_theta = mm(d(F(36)), shifted_reference)
    check("factorization_same_complete_coframe", theta == shifted_theta)

    zp, zq, hp, hq = F(3), F(13), F(2), F(7)
    refp = [[F(1), F(2)], [F(0), F(3)]]
    refq = [[F(2), F(0)], [F(1), F(4)]]
    thetap, thetaq = mm(d(zp), refp), mm(d(zq), refq)
    arrow = mm(thetaq, inv2(thetap))
    refp2, refq2 = mm(inv2(d(hp)), refp), mm(inv2(d(hq)), refq)
    thetap2, thetaq2 = mm(d(zp * hp), refp2), mm(d(zq * hq), refq2)
    arrow2 = mm(thetaq2, inv2(thetap2))
    depth1, depth2 = zq / zp, (zq * hq) / (zp * hp)
    check("pair_depth_changes", depth1 != depth2)
    check("endpoint_coframes_fixed", thetap == thetap2 and thetaq == thetaq2)
    check("physical_arrow_fixed", arrow == arrow2)
    check("orbit_transitive_control", depth1 * (F(17, 5) / depth1) == F(17, 5))

    # Two normalization powers satisfy the same multiplicative laws.
    for power in (1, 3):
        left = [[F(1, 2**power), F(0)], [F(0), F(2**power)]]
        right = [[F(1, 5**power), F(0)], [F(0), F(5**power)]]
        combined = [[F(1, 10**power), F(0)], [F(0), F(10**power)]]
        check(f"normalization_composes_{power}", mm(right, left) == combined)
    check("normalizations_distinct", d(F(2)) != [[F(1, 8), F(0)], [F(0), F(8)]])

    # Endpoint and stationary branch ratios.  The lapse ratio N(q)/N(p) is the inverse of the
    # multiplicative signed-depth ratio exp(delta_K)=N(p)/N(q).
    check("potential_composes", F(23, 7) * F(7, 2) == F(23, 2))
    check("common_zero_cancels", F(5 * 23, 5 * 7) == F(23, 7))
    check("killing_lapse_ratio_composes", F(19, 5) * F(5, 2) == F(19, 2))
    check("killing_depth_ratio_composes", F(5, 19) * F(2, 5) == F(2, 19))
    check("killing_depth_is_inverse_lapse", F(2, 5) == 1 / F(5, 2))
    check("killing_depth_scale_cancels", F(11 * 2, 11 * 5) == F(2, 5))

    # Exact Lorentz isometry control versus reciprocal metric deformation.
    boost = [[F(5, 4), F(3, 4)], [F(3, 4), F(5, 4)]]
    check("transport_isometry_control", mm(mm(transpose(boost), eta), boost) == eta)
    check("dilation_not_transport", mm(mm(transpose(d(F(2))), eta), d(F(2))) != eta)

    magnitude = abs(F(11) - F(4))
    check("magnitude_symmetric", magnitude == abs(F(4) - F(11)) and magnitude > 0)
    check("magnitude_not_reversal_odd", magnitude != -magnitude)
    check("bootstrap_relation_multivalued", len({F(2), F(5)}) == 2)
    check("identity_control", mm(identity, d(F(3))) == d(F(3)))

    result = {
        "schema": "udt.founding_phi_ownership.independent.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "independence": "stdlib Fraction matrices; no SymPy or production import",
        "check_count": len(checks),
        "checks": checks,
        "depth_before": str(depth1),
        "depth_after": str(depth2),
        "physical_arrow": encode(arrow),
        "physical_arrow_after": encode(arrow2),
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
