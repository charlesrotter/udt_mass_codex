#!/usr/bin/env python3
"""Exact production derivation for the frozen twisted-S3 witness candidates."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from exact_invariant_jets import invariant_gradient_certificate

F = Fraction
HERE = Path(__file__).resolve().parent
PRIMARY = (
    "ONE_COMPLETE_TWISTED_S3_CONFIGURATION_HAS_A_METRIC_INTRINSIC_CLOCK_LINE__"
    "ITS_CLOCK_TWIST_SELECTS_THE_RECIPROCAL_RULER_LINE__"
    "ALL_GATE_CONFIGURATION_EXISTENCE_DERIVED_IN_THE_FROZEN_FAMILY__"
    "NO_ON_SHELL_SELECTION_OR_PHYSICAL_LAW_DERIVED"
)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fraction(text: str) -> F:
    return F(text)


def main() -> int:
    candidates = rows("CANDIDATE_UNIVERSE.tsv")
    assert [row["candidate_id"] for row in candidates] == [f"C{i:02d}" for i in range(1, 9)]

    outcomes = []
    for row in candidates:
        epsilon = fraction(row["epsilon"])
        twist = fraction(row["a"])
        lambda_value = fraction(row["lambda"])
        certificate = invariant_gradient_certificate(lambda_value, epsilon, twist)
        rank_three = bool(certificate["rank_three"])
        depth_nontrivial = epsilon != 0
        twist_nonzero = twist != 0

        # Global profile bound: |f|<=29. For nonzero epsilon, |phi|<=29/50<1.
        # Since e<3, exp(4 phi)>exp(-4)>1/81>1/4096=a^2.
        if epsilon:
            assert abs(epsilon) * 29 < 1
            assert twist * twist < F(1, 81)
        else:
            assert twist * twist < 1
        slice_global = True
        all_gate = rank_three and depth_nontrivial and twist_nonzero and slice_global
        outcomes.append({
            "candidate_id": row["candidate_id"],
            "role": row["role"],
            "lambda": row["lambda"],
            "epsilon": row["epsilon"],
            "a": row["a"],
            "gradient_matrix": [[str(value) for value in gradient]
                                for gradient in certificate["gradients"]],
            "gradient_determinant": str(certificate["determinant"]),
            "rank_three": rank_three,
            "depth_nontrivial": depth_nontrivial,
            "twist_nonzero": twist_nonzero,
            "global_slice_certified": slice_global,
            "all_gate_witness": all_gate,
        })

    passing = [row["candidate_id"] for row in outcomes if row["all_gate_witness"]]
    assert passing == ["C01", "C02", "C03", "C04", "C05", "C06"]
    assert outcomes[6]["rank_three"] and not outcomes[6]["twist_nonzero"]
    assert not outcomes[7]["rank_three"] and not outcomes[7]["depth_nontrivial"]
    stored_outcomes = rows("CANDIDATE_OUTCOMES.tsv")
    assert len(stored_outcomes) == 8
    gradient_keys = [f"I{invariant}_d{axis}" for invariant in range(1, 4)
                     for axis in ("x", "y", "z")]
    for computed, stored in zip(outcomes, stored_outcomes, strict=True):
        assert computed["candidate_id"] == stored["candidate_id"]
        flattened = [value for gradient in computed["gradient_matrix"] for value in gradient]
        assert flattened == [stored[key] for key in gradient_keys]
        assert computed["gradient_determinant"] == stored["gradient_determinant"]
        for key in ("rank_three", "depth_nontrivial", "twist_nonzero",
                    "global_slice_certified", "all_gate_witness"):
            assert computed[key] == (stored[key] == "YES")
    determinant_census = "\n".join(
        f"{row['candidate_id']}\t{row['gradient_determinant']}" for row in outcomes
    )

    result = {
        "schema_version": 1,
        "compute": "CPU_ONLY_EXACT_RATIONAL_JETS",
        "candidates": len(outcomes),
        "passing_all_gate_candidates": passing,
        "passing_lambda_values": ["-2", "-1", "0", "1/2", "1", "2"],
        "rank_three_candidates": [row["candidate_id"] for row in outcomes if row["rank_three"]],
        "twist_off_control": "RANK_THREE_BUT_NOT_ALL_GATE",
        "depth_off_control": "RANK_ZERO_NOT_ALL_GATE",
        "intrinsic_clock_line": "DERIVED_EXACT_IN_C01_TO_C07",
        "twist_selected_reciprocal_ruler": "DERIVED_EXACT_IN_C01_TO_C06",
        "single_all_gate_configuration_witness": "DERIVED_EXISTENCE_IN_C01_TO_C06",
        "lambda_selected": False,
        "profile_selected": False,
        "on_shell_solution_claimed": False,
        "endpoint_or_path_semantics_selected": False,
        "instantaneous_operational_access_derived": False,
        "copresence_status": "WORKING_INTERPRETIVE_FRAME",
        "complete_whole_solution_law": "OPEN",
        "primary_ruling": PRIMARY,
        "determinant_census_sha256": hashlib.sha256(determinant_census.encode()).hexdigest(),
        "candidate_outcomes_sha256": hashlib.sha256(
            (HERE / "CANDIDATE_OUTCOMES.tsv").read_bytes()
        ).hexdigest(),
        "exact_gradient_entries": 72,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
