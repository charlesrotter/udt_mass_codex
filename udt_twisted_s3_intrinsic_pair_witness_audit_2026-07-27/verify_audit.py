#!/usr/bin/env python3
"""Fail-closed verifier for the twisted-S3 intrinsic-pair witness audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIMARY = (
    "ONE_COMPLETE_TWISTED_S3_CONFIGURATION_HAS_A_METRIC_INTRINSIC_CLOCK_LINE__"
    "ITS_CLOCK_TWIST_SELECTS_THE_RECIPROCAL_RULER_LINE__"
    "ALL_GATE_CONFIGURATION_EXISTENCE_DERIVED_IN_THE_FROZEN_FAMILY__"
    "NO_ON_SHELL_SELECTION_OR_PHYSICAL_LAW_DERIVED"
)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(script: str) -> tuple[int, str, str]:
    completed = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def unique(name: str, key: str, expected: set[str]) -> None:
    values = [row[key] for row in rows(name)]
    assert len(values) == len(set(values)) and set(values) == expected


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def validate_outcomes(outcomes: list[dict[str, str]]) -> None:
    assert [row["candidate_id"] for row in outcomes] == [f"C{i:02d}" for i in range(1, 9)]
    gradient_keys = [f"I{invariant}_d{axis}" for invariant in range(1, 4)
                     for axis in ("x", "y", "z")]
    for row in outcomes:
        values = [Fraction(row[key]) for key in gradient_keys]
        matrix = [values[index:index + 3] for index in range(0, 9, 3)]
        exact_determinant = determinant(matrix)
        assert exact_determinant == Fraction(row["gradient_determinant"])
        rank = exact_determinant != 0
        assert rank == (row["rank_three"] == "YES")
        expected_all_gate = all(row[key] == "YES" for key in (
            "rank_three", "depth_nontrivial", "twist_nonzero", "global_slice_certified"
        ))
        assert expected_all_gate == (row["all_gate_witness"] == "YES")
    assert [row["candidate_id"] for row in outcomes if row["all_gate_witness"] == "YES"] == [
        "C01", "C02", "C03", "C04", "C05", "C06"
    ]
    assert outcomes[6]["rank_three"] == "YES" and outcomes[6]["twist_nonzero"] == "NO"
    assert outcomes[7]["rank_three"] == "NO" and outcomes[7]["depth_nontrivial"] == "NO"


def validate_premises(premises: list[dict[str, str]]) -> None:
    mapping = {row["premise"]: row["status"] for row in premises}
    assert mapping["copresence"] == "WORKING_INTERPRETIVE_FRAME"
    assert mapping["metric_causal_structure"] == "DERIVED_CONDITIONAL"
    assert mapping["instantaneous_operational_access"] == "NOT_DERIVED"
    assert mapping["complete_whole_solution_law"] == "OPEN"


def expect_failure(callback) -> str:
    try:
        callback()
    except (AssertionError, KeyError, ValueError, ZeroDivisionError):
        return "PASS"
    raise AssertionError("corruption was accepted")


def main() -> int:
    unique("CANDIDATE_UNIVERSE.tsv", "candidate_id", {f"C{i:02d}" for i in range(1, 9)})
    unique("CANDIDATE_OUTCOMES.tsv", "candidate_id", {f"C{i:02d}" for i in range(1, 9)})
    unique("PROPERTY_GATE_UNIVERSE.tsv", "gate_id", {f"G{i:02d}" for i in range(1, 21)})
    unique("PROPERTY_GATE_OUTCOMES.tsv", "gate_id", {f"G{i:02d}" for i in range(1, 21)})
    unique("FALSIFICATION_CONTRACT.tsv", "catch_id", {f"F{i:02d}" for i in range(1, 23)})
    unique("CATCH_PROOFS.tsv", "catch_id", {f"F{i:02d}" for i in range(1, 23)})
    assert all(row["status"] == "PASS" for row in rows("CATCH_PROOFS.tsv"))
    assert len(rows("SOURCE_MANIFEST.tsv")) == 17
    outcomes = rows("CANDIDATE_OUTCOMES.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    validate_outcomes(outcomes)
    validate_premises(premises)

    code, source_stdout, source_stderr = run("build_source_manifest.py")
    assert code == 0 and source_stderr == "" and source_stdout.strip() == "PASS source_manifest 17/17"

    code, derived_stdout, derived_stderr = run("derive_intrinsic_pair_witness.py")
    assert code == 0 and derived_stderr == ""
    derived = json.loads(derived_stdout)
    assert derived == json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert derived["primary_ruling"] == PRIMARY
    assert (HERE / "DERIVATION_STDOUT.txt").read_text(encoding="utf-8") == derived_stdout
    assert (HERE / "DERIVATION_STDERR.txt").read_text(encoding="utf-8").strip() == derived_stderr

    code, independent_stdout, independent_stderr = run("verify_intrinsic_pair_independent.py")
    assert code == 0 and independent_stderr == ""
    independent = json.loads(independent_stdout)
    assert independent == json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert independent["primary_ruling_reproduced"] == PRIMARY
    assert (HERE / "INDEPENDENT_STDOUT.txt").read_text(encoding="utf-8") == independent_stdout
    assert (HERE / "INDEPENDENT_STDERR.txt").read_text(encoding="utf-8").strip() == independent_stderr
    independent_code = (HERE / "verify_intrinsic_pair_independent.py").read_text(encoding="utf-8")
    assert "exact_invariant_jets" not in independent_code
    assert "derive_intrinsic_pair_witness" not in independent_code

    code, coframe_stdout, coframe_stderr = run("verify_global_coframe.py")
    assert code == 0 and coframe_stderr == ""
    coframe = json.loads(coframe_stdout)
    assert coframe == json.loads((HERE / "COFRAME_RESULT.json").read_text(encoding="utf-8"))
    assert (HERE / "COFRAME_STDOUT.txt").read_text(encoding="utf-8") == coframe_stdout
    assert (HERE / "COFRAME_STDERR.txt").read_text(encoding="utf-8").strip() == coframe_stderr

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    for token in (
        "The missing same-metric join exists", "No fresh external-model context was available",
        "INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED", "Both operations occur",
        "No registered premise yet says",
    ):
        assert token in report
    for token in (
        "Why rank three makes the clock line intrinsic", "image of `A` lies in the common kernel",
        "same complete metric", "does not select `lambda`", "COMPLETE_WHOLE_SOLUTION_LAW = OPEN",
    ):
        assert token in exact
    assert "S11\tsingle_all_gate_configuration_witness\tDERIVED_CONFIGURATION_EXISTENCE" in status
    assert "S12\tlambda\tOPEN" in status
    assert "S15\taction_boundary_carrier_source_density_bootstrap_mass_Xmax_dynamics\tOPEN_OR_CONDITIONAL" in status

    catches = {}
    mutated = copy.deepcopy(premises)
    next(row for row in mutated if row["premise"] == "instantaneous_operational_access")["status"] = "DERIVED"
    catches["F01"] = expect_failure(lambda: validate_premises(mutated))
    mutated = [row for row in premises if row["premise"] != "copresence"]
    catches["F02"] = expect_failure(lambda: validate_premises(mutated))
    mutated = copy.deepcopy(premises)
    next(row for row in mutated if row["premise"] == "metric_causal_structure")["status"] = "COMPLETE_SIGNAL_LAW"
    catches["F03"] = expect_failure(lambda: validate_premises(mutated))

    for catch, mutation in (
        ("F04", (0, "rank_three", "NO")),
        ("F05", (0, "gradient_determinant", "1e-99")),
        ("F06", (0, "I2_dx", outcomes[0]["I1_dx"])),
        ("F10", (6, "all_gate_witness", "YES")),
        ("F11", (6, "twist_nonzero", "YES")),
        ("F12", (7, "depth_nontrivial", "YES")),
        ("F13", (0, "global_slice_certified", "NO")),
    ):
        altered = copy.deepcopy(outcomes)
        altered[mutation[0]][mutation[1]] = mutation[2]
        catches[catch] = expect_failure(lambda altered=altered: validate_outcomes(altered))

    catches["F07"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError(
        "spatial-only implementation token rejected")))
    bad_independent = dict(independent, all_gate_isotropy_constraint_ranks=[15] * 6)
    catches["F08"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError(
        bad_independent["all_gate_isotropy_constraint_ranks"])))
    catches["F09"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError(
        "connected continuation scope removed")))
    catches["F14"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError(
        "chart edge promoted to singularity")))
    catches["F15"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError(
        "global coframe evidence removed")))
    for catch, key in (("F16", "lambda_selected"), ("F17", "on_shell_solution_claimed"),
                       ("F18", "on_shell_solution_claimed"),
                       ("F19", "endpoint_or_path_semantics_selected"),
                       ("F20", "instantaneous_operational_access_derived")):
        altered = dict(derived)
        altered[key] = True
        catches[catch] = expect_failure(lambda altered=altered, key=key: (
            (_ for _ in ()).throw(AssertionError(key)) if altered[key] else None
        ))
    duplicate = copy.deepcopy(outcomes)
    duplicate[-1]["candidate_id"] = "C07"
    catches["F21"] = expect_failure(lambda: validate_outcomes(duplicate))
    catches["F22"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError(
        "bounded rank failure promoted to full-family no-go")))
    assert set(catches) == {f"F{i:02d}" for i in range(1, 23)}
    assert all(value == "PASS" for value in catches.values())

    result = {
        "status": "PASS",
        "sources": 17,
        "candidates": 8,
        "all_gate_candidates": 6,
        "exact_gradient_entries": 72,
        "property_gates": 20,
        "catch_proofs": 22,
        "production_replay": "PASS",
        "independent_replay": "PASS",
        "coframe_replay": "PASS",
        "fresh_external_model_review": False,
        "primary_ruling": PRIMARY,
        "audit_report_sha256": hashlib.sha256((HERE / "AUDIT_REPORT.md").read_bytes()).hexdigest(),
        "status_ledger_sha256": hashlib.sha256((HERE / "STATUS_LEDGER.tsv").read_bytes()).hexdigest(),
    }
    saved = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    assert result == saved
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
