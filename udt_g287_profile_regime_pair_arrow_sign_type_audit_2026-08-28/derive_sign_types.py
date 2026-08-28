#!/usr/bin/env python3
"""Dependency-free exact G287 sign-type derivation and source audit."""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LANDING = (
    "PROFILE_REGIME_SIGN_AND_PAIR_ARROW_ORIENTATION_ARE_ALREADY_TYPE_DISTINCT"
    "__NO_NATIVE_KERNEL_REGRESSION__RECENT_EXPLANATION_CONFLATED_THEM"
)
EXPECTED_DEPENDENCIES = {
    "founding.md", "G201", "G202", "G203", "G204", "G263", "G264", "G265",
    "G266", "G267", "G268", "G269", "G270", "G271", "G272", "G273", "G274",
    "G275", "G276", "G285", "G286", "current authority surface",
}


def frac_pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def reverse_pair(metric: tuple[Fraction, Fraction], profile: int, depth: int):
    """Reverse one ordered comparison while retaining its ambient metric/profile."""
    return metric, profile, -depth


def conjugate_profile(metric: tuple[Fraction, Fraction]):
    """Diagnostic whole-profile conjugation on the clock/radial metric block."""
    return metric[1] * -1, metric[0] * -1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    with (PACKAGE / "DEPENDENCY_AUDIT.tsv").open(newline="", encoding="utf-8") as handle:
        dependency_rows = list(csv.DictReader(handle, delimiter="\t"))
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        source_paths = {row["path"] for row in csv.DictReader(handle, delimiter="\t")}
    evidence_checks = {}
    for row in dependency_rows:
        relative = row["evidence_path"]
        marker = " ".join(row["evidence_marker"].split())
        path = ROOT / relative
        normalized_source = " ".join(path.read_text(encoding="utf-8").split()) if path.is_file() else ""
        evidence_checks[f"dependency_source:{row['source']}"] = (
            relative in source_paths
            and bool(marker)
            and marker in normalized_source
        )
    dependency_names = [row["source"] for row in dependency_rows]
    dependency_checks = {
        "dependency_row_count": len(dependency_rows) == 22,
        "dependency_names_exact": set(dependency_names) == EXPECTED_DEPENDENCIES,
        "dependency_names_unique": len(dependency_names) == len(set(dependency_names)),
        "every_dependency_source_verified": len(evidence_checks) == 22 and all(evidence_checks.values()),
        "no_active_alias": all(row["alias_found"] == "NO" for row in dependency_rows),
        "all_rows_pass": all(row["grade"].startswith("PASS") for row in dependency_rows),
        "g267_guarded": any(
            row["source"] == "G267" and row["grade"] == "PASS_WITH_INTERPRETIVE_GUARD"
            for row in dependency_rows
        ),
        "g272_reference_qualified": any(
            row["source"] == "G272" and row["grade"] == "PASS_WITH_REFERENCE_QUALIFICATION"
            for row in dependency_rows
        ),
    }

    t_samples = [Fraction(1, 7), Fraction(2, 3), Fraction(3, 2), Fraction(11, 4)]
    arrow_assertions = 0
    sample_rows = []
    for t in t_samples:
        d = (1 / t, t)
        reversed_d = (t, 1 / t)
        inverse_d = (1 / d[0], 1 / d[1])
        chi = (t * t - 1) / (t * t + 1)
        mutual = 2 * t / (1 + t * t)
        reversed_t = 1 / t
        reversed_chi = (reversed_t * reversed_t - 1) / (reversed_t * reversed_t + 1)
        reversed_mutual = 2 * reversed_t / (1 + reversed_t * reversed_t)
        checks = [
            reversed_d == inverse_d,
            reversed_chi == -chi,
            reversed_mutual == mutual,
            mutual * mutual + chi * chi == 1,
        ]
        assert all(checks)
        arrow_assertions += len(checks)
        sample_rows.append({
            "t": frac_pair(t),
            "chi": frac_pair(chi),
            "mutual": frac_pair(mutual),
        })

    f_samples = [Fraction(1, 5), Fraction(2, 3), Fraction(3, 2), Fraction(7, 3)]
    profile_assertions = 0
    pair_reversal_assertions = 0
    for f in f_samples:
        metric_block = (-f, 1 / f)
        conjugate_block = (-1 / f, f)
        double_conjugate_f = 1 / (1 / f)
        reversed_pair_metric, _, _ = reverse_pair(metric_block, 1, 2)
        assert reversed_pair_metric == metric_block
        assert conjugate_profile(metric_block) == conjugate_block
        assert metric_block != conjugate_block
        assert (-double_conjugate_f, 1 / double_conjugate_f) == metric_block
        profile_assertions += 2
        pair_reversal_assertions += 1

    x_samples = [Fraction(1, 10), Fraction(1, 2), Fraction(2, 1), Fraction(5, 1)]
    separator_assertions = 0
    for x in x_samples:
        a_parallel_c = 4 * x * x / (1 + x) ** 3
        a_perp_c = x * x / (1 + x) ** 2
        assert a_parallel_c > 0 and a_perp_c > 0
        separator_assertions += 2

    regime_rows = [(3, 1), (-2, -1)]
    regime_checks = []
    for forward_depth, profile_sign in regime_rows:
        metric = (Fraction(-2, 3), Fraction(3, 2))
        _, reversed_profile_sign, reverse_depth = reverse_pair(metric, profile_sign, forward_depth)
        regime_checks.extend([
            reverse_depth == -forward_depth,
            (forward_depth > 0) != (reverse_depth > 0),
            reversed_profile_sign == profile_sign,
        ])
    regime_examples = {
        "macro_forward_depth": regime_rows[0][0],
        "macro_reversed_depth": -regime_rows[0][0],
        "macro_profile_sign_preserved": regime_rows[0][1] == 1,
        "micro_forward_depth": regime_rows[1][0],
        "micro_reversed_depth": -regime_rows[1][0],
        "micro_profile_sign_preserved": regime_rows[1][1] == -1,
        "arrow_sign_not_regime_classifier": all(regime_checks),
    }

    checks = {
        **evidence_checks,
        **dependency_checks,
        "pair_reversal_fixed_metric": pair_reversal_assertions == len(f_samples),
        "profile_conjugation_changes_generic_metric": profile_assertions == 8,
        "zero_tide_separator_active": separator_assertions == 8,
        "arrow_parity_exact": arrow_assertions == 16,
        "arrow_sign_not_regime_classifier": regime_examples["arrow_sign_not_regime_classifier"],
        "user_interpretation_not_promoted": "NOT_CANONIZED_BY_THIS_AUDIT" in
            (PACKAGE / "USER_SIGN_CLARIFICATION.md").read_text(encoding="utf-8"),
    }
    result = {
        "landing": LANDING,
        "checks": checks,
        "counts": {
            "dependency_source_checks": len(evidence_checks),
            "dependency_rows": len(dependency_rows),
            "exact_arrow_assertions": arrow_assertions,
            "exact_profile_assertions": profile_assertions,
            "exact_pair_reversal_assertions": pair_reversal_assertions,
            "exact_separator_assertions": separator_assertions,
            "exact_regime_assertions": len(regime_checks),
        },
        "regime_examples": regime_examples,
        "sample_rows": sample_rows,
        "pass": all(checks.values()),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
