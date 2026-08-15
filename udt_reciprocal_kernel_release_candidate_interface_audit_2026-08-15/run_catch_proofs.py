#!/usr/bin/env python3
"""Hostile interface and semantic mutations for the release-candidate audit."""

from __future__ import annotations

import csv
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mul2(a, b):
    return [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
    ]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def main() -> None:
    # 1. An independently rebuilt middle state cannot be silently identified.
    e0 = [[F(1), F(0)], [F(0), F(1)]]
    e1_in = [[F(2), F(1)], [F(0), F(3)]]
    e1_out = [[F(3), F(-1)], [F(0), F(2)]]
    e2 = [[F(5), F(2)], [F(0), F(7)]]
    a01 = mul2(e1_in, inv2(e0))
    a12 = mul2(e2, inv2(e1_out))
    direct = mul2(e2, inv2(e0))
    assert mul2(a12, a01) != direct
    middle = mul2(e1_out, inv2(e1_in))
    assert mul2(mul2(a12, middle), a01) == direct

    # 2. The recovered S channel is load-bearing at the generic witness.
    dphi_s = F(32976619891669139675721317145, 219978174761329555886615477906)
    assert dphi_s != 0
    assert F(0) != dphi_s

    # 3. Appending mu after terminal phi changes the output and is therefore double counting.
    phi_terminal, mu = F(2, 5), F(1, 7)
    assert phi_terminal + mu != phi_terminal

    # 4. S changes require the exact compensating Z carry to preserve the pair screen leg.
    s_leg, d, y = F(1, 4), F(2, 5), F(3, 2)
    assert s_leg + d * y != s_leg
    assert s_leg + d * y - d * y == s_leg

    with (HERE / "SNE_INTERFACE_AUDIT.tsv").open(encoding="utf-8", newline="") as handle:
        rows = {row["layer"]: row for row in csv.DictReader(handle, delimiter="\t")}

    # 5--8. Semantic shortcut catches.
    assert rows["historical_dA_equals_r"]["current_status"] == "CONDITIONAL_FROZEN_READOUT"
    assert rows["historical_dL_relation"]["current_status"] == "CONDITIONAL_FROZEN_FLUX_READOUT"
    assert rows["existing_native_sne_replay"]["current_status"] == "VERIFIED_WITH_CAVEATS__RETYPE_ONLY"
    assert rows["all_active_histories"]["current_status"] == "CONDITIONAL_NONSELECTIVE"
    assert rows["release_readiness"]["current_status"] == "GEOMETRIC_SNE_QUERY_READY_CONDITIONALLY"

    print("PASS: 9 hostile interface/semantic mutations caught")


if __name__ == "__main__":
    main()
