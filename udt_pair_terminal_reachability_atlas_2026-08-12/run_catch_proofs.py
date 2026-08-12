#!/usr/bin/env python3
"""Hostile controls for common reachability-classification mistakes."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def correct_signature(t, ell, p, m, n):
    determinant = (p - t) * (ell + n) - m * m
    return "L" if determinant < 0 else "D" if determinant == 0 else "P"


def reachable(t, ell, T2, L2, delta):
    return (
        0 < T2 <= t
        and L2 >= ell
        and (t - T2) * (L2 - ell) >= t * T2 * delta * delta
    )


def main():
    t, ell = F(4), F(9)
    catches = {}

    # Omitting the cross term changes a Lorentzian form into a false positive-definite label.
    actual = correct_signature(t, ell, F(5), F(5), F(7))
    wrong = "P" if (F(5) - t) * (ell + F(7)) > 0 else "L"
    catches["cross_term_required"] = actual == "L" and wrong == "P"

    # The terminal clock cannot exceed its fixed base under a PSD Gram addition.
    catches["clock_direction_required"] = not reachable(t, ell, F(5), F(9), F(0))

    # The terminal orthogonal ruler cannot fall below its fixed base.
    catches["ruler_direction_required"] = not reachable(t, ell, F(4), F(8), F(0))

    # Marginal clock/ruler bounds do not make an arbitrarily shifted target reachable.
    catches["beta_coupling_required"] = not reachable(t, ell, F(2), F(9), F(1))

    # Equality is a rank boundary, not a rank-two interior point.
    T2, delta = F(2), F(1)
    L2 = ell + t * T2 * delta * delta / (t - T2)
    determinant_gram = (t - T2) * (L2 - ell) - t * T2 * delta * delta
    catches["rank_equality_required"] = determinant_gram == 0

    # h00=0 does not imply the completed pair form is degenerate when mixing remains.
    catches["clock_null_not_always_degenerate"] = correct_signature(t, ell, t, F(2), F(2)) == "L"

    # A positive completed form exists and must not be filtered from the full atlas.
    catches["positive_stratum_retained"] = correct_signature(t, ell, F(5), F(0), F(7)) == "P"

    # Base equality is the only zero-rank target. Check both the admitted base and
    # the uniquely reconstructed zero Gram matrix; also reject a shifted impostor.
    base_gram = (t - t, -t * F(0), ell - ell - t * F(0) ** 2)
    catches["base_rank_zero_unique"] = (
        reachable(t, ell, t, ell, F(0))
        and base_gram == (F(0), F(0), F(0))
        and not reachable(t, ell, t, ell, F(1))
    )

    assert all(catches.values()), catches
    result = {"status": "PASS", "catch_count": len(catches), "catches": catches}
    (ROOT / "CATCH_PROOFS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
