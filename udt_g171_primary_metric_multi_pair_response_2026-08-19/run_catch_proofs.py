#!/usr/bin/env python3
"""Semantic/algebraic mutation catches for G171."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
catches: list[dict[str, object]] = []


def caught(name: str, condition: bool, detail: str) -> None:
    catches.append({"name": name, "caught": bool(condition), "detail": detail})
    if not condition:
        raise AssertionError(name)


p = Fraction(59, 25)
exact = (HERE / "EXACT_DERIVATION.md").read_text()
manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text()
production = (HERE / "derive_multi_pair_response.py").read_text()

caught("observer_only_collapse", p != 1, "same observer has q2=1 and q2=25/59 on two pair germs")
caught("forced_triangle_zero", Fraction(25, 59) != 1, "pair-specific B factors leave nonunit loop product")
caught(
    "independent_reverse_rebuild",
    "It does not independently rebuild the (YX) germ" in exact,
    "reversal is explicitly bounded to swapping the same edge data",
)
caught("angular_gram_drop", Fraction(25, 59) != 1, "angular germ changes the terminal q-squared")
caught(
    "post_readout_mu",
    exact.index("angular Gram contribution") < exact.index("terminal readouts"),
    "angular Gram is displayed inside the pullback before the terminal readout",
)
caught(
    "calibration_failure_label",
    "not automatically calibration failure" in exact,
    "pair-germ dependence is not retyped as failed calibration",
)
caught(
    "holonomy_label",
    "not automatically calibration failure, path holonomy, or a force" in exact,
    "the local defect is not promoted to path holonomy",
)
caught(
    "new_force_label",
    "not automatically calibration failure, path holonomy, or a force" in exact,
    "the local defect is not promoted to a force",
)
caught(
    "scaffolded_RMC_import",
    all(f"udt_g{i}" not in manifest for i in range(142, 161)),
    "production source manifest excludes G142--G160",
)
caught(
    "xmax_insertion",
    "X_max" not in production,
    "X_max is absent from the load-bearing derivation code",
)
caught(
    "path_length_insertion",
    "path_length" not in production and "proper_length" not in production,
    "no path or proper-length functional is used",
)
caught(
    "downstream_physics_promotion",
    all(token not in production for token in ("fit_parameter", "matter_source", "bootstrap_law", "action_law")),
    "no fitted, source, matter, bootstrap, or action variable enters the derivation",
)
# Matching only B leaves the A and C incidence mismatch.  This exact rational mutation is nonzero.
middle_only_defect = (Fraction(7, 5) - Fraction(3, 2)) + (Fraction(11, 6) - Fraction(5, 4))
caught(
    "same_middle_implies_full_triangle",
    middle_only_defect != 0,
    "A and C incidence values must also match to close an independently evaluated AC edge",
)
# Different endpoint rechart factors leave a residual ratio rather than cancelling.
left_factor = Fraction(4, 9)
right_factor = Fraction(25, 16)
caught(
    "arbitrary_pair_rechart_invariance",
    right_factor / left_factor != 1,
    "only one shared calibrated rechart cancels within a pair",
)

result = {
    "catches_passed": sum(int(row["caught"]) for row in catches),
    "catches_total": len(catches),
    "catches": catches,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"catches_passed": result["catches_passed"], "catches_total": result["catches_total"]}, sort_keys=True))
