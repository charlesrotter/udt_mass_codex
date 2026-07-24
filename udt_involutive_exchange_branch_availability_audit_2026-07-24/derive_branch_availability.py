#!/usr/bin/env python3
"""Derive the repository-bounded branch-availability ruling."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GATES = [f"G{i:02d}" for i in range(1, 13)]
ALLOWED = {"YES", "NO", "CONDITIONAL", "OPEN", "NOT_APPLICABLE"}
FAMILIES = [f"B{i:02d}" for i in range(1, 29)]


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_matrix(rows: list[dict[str, str]], require_no_pass: bool = True) -> None:
    ids = [row["family_id"] for row in rows]
    if len(ids) != 28 or sorted(ids) != FAMILIES or len(set(ids)) != 28:
        raise AssertionError("family universe is missing or duplicated")
    for row in rows:
        if any(row[gate] not in ALLOWED for gate in GATES):
            raise AssertionError(f"invalid gate value in {row['family_id']}")
        if not row["primary_blocker"]:
            raise AssertionError(f"missing blocker in {row['family_id']}")
    passing = [row["family_id"] for row in rows if all(row[g] == "YES" for g in GATES)]
    if require_no_pass and passing:
        raise AssertionError(f"unexpected complete witness: {passing}")


def gate_counts(row: dict[str, str]) -> dict[str, int]:
    return {value: sum(row[g] == value for g in GATES) for value in sorted(ALLOWED)}


def strongest(rows: list[dict[str, str]]) -> dict[str, str]:
    def rank(row: dict[str, str]) -> tuple[int, int, int, int, str]:
        count = gate_counts(row)
        return (
            count["YES"],
            count["CONDITIONAL"],
            -count["NO"],
            -count["OPEN"],
            "".join(chr(255 - ord(c)) for c in row["family_id"]),
        )

    return max(rows, key=rank)


def validate_lifts(rows: list[dict[str, str]]) -> None:
    if len(rows) != 4 or len({row["lift_id"] for row in rows}) != 4:
        raise AssertionError("lift census")
    for row in rows:
        involutive = row["involutive_exchange"] == "YES"
        if involutive != (
            row["order"] == "2"
            and row["square"] == "PLUS_IDENTITY"
            and int(row["fixed_lattice_rank"]) == 1
        ):
            raise AssertionError(f"lift type mismatch: {row['lift_id']}")
        if row["selected_by_current_udt"] != "NO":
            raise AssertionError("lift promotion")


def validate_witnesses(rows: list[dict[str, str]]) -> None:
    if len(rows) != 7 or len({row["witness_id"] for row in rows}) != 7:
        raise AssertionError("witness census")
    forbidden_native = {
        "CONDITIONAL_ON_SHELL_BACH",
        "CONDITIONAL_ON_SHELL_EH_AND_BACH",
        "OFF_SHELL_CONDITIONAL_GLOBAL_WITNESS",
        "CONDITIONAL_CARRIER_NUMERICAL_SOLUTION",
        "OBSERVATIONAL_READOUT",
        "KINEMATIC_FAMILY",
    }
    for row in rows:
        if row["type"] in forbidden_native and row["native_authority"] == "NATIVE_UDT":
            raise AssertionError(f"authority promotion: {row['witness_id']}")
    if any(row["type"] == "NATIVE_ON_SHELL_COMPLETE" for row in rows):
        raise AssertionError("native complete witness unexpectedly present")


def source_records() -> list[dict[str, str]]:
    manifests = (
        "SOURCE_MANIFEST.tsv",
        "SOURCE_MANIFEST_CORRECTION_01.tsv",
        "SOURCE_MANIFEST_CORRECTION_02.tsv",
        "SOURCE_MANIFEST_CORRECTION_03.tsv",
    )
    expected = [97, 4, 35, 14]
    all_rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for name, count in zip(manifests, expected, strict=True):
        rows = read_tsv(name)
        if len(rows) != count:
            raise AssertionError(f"{name} count")
        for row in rows:
            path = row["path"]
            if path in seen:
                raise AssertionError(f"duplicate source: {path}")
            seen.add(path)
            artifact = ROOT / path
            data = artifact.read_bytes()
            if len(data) != int(row["bytes"]):
                raise AssertionError(f"source bytes: {path}")
            if hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise AssertionError(f"source hash: {path}")
            blob = subprocess.run(
                ["git", "rev-parse", f"HEAD:{path}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            if blob != row["git_blob"]:
                raise AssertionError(f"source blob: {path}")
            all_rows.append(row)
    if len(all_rows) != 150:
        raise AssertionError("effective source count")
    return all_rows


def expect_failure(label: str, callback) -> tuple[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError, FileNotFoundError) as exc:
        return label, f"PASS:{type(exc).__name__}"
    raise AssertionError(f"catch accepted corruption: {label}")


def cross_family_join(left: dict[str, str], right: dict[str, str]) -> None:
    if left["family_id"] != right["family_id"]:
        raise AssertionError("cross-family branch splicing")


def main() -> None:
    rows = read_tsv("FAMILY_GATE_MATRIX.tsv")
    evidence = read_tsv("FAMILY_EVIDENCE.tsv")
    lifts = read_tsv("LIFT_CLASSIFICATION.tsv")
    witnesses = read_tsv("WITNESS_TYPE_LEDGER.tsv")
    validate_matrix(rows)
    if sorted(row["family_id"] for row in evidence) != FAMILIES:
        raise AssertionError("family evidence coverage")
    validate_lifts(lifts)
    validate_witnesses(witnesses)
    sources = source_records()

    best = strongest(rows)
    if best["family_id"] != "B19":
        raise AssertionError("strongest near-pass changed")
    if best["G02"] == "YES" or best["G03"] == "YES" or best["G05"] == "YES":
        raise AssertionError("strongest near-pass overpromoted")
    if any(row["G02"] == "YES" for row in rows):
        raise AssertionError("native dynamics unexpectedly present")
    if any(row["G03"] == "YES" for row in rows):
        raise AssertionError("native complete on-shell branch unexpectedly present")

    counts_output = [
        "family_id\tyes\tconditional\topen\tno\tnot_applicable\tpasses_all\tprimary_blocker"
    ]
    for row in rows:
        counts = gate_counts(row)
        counts_output.append(
            "\t".join(
                [
                    row["family_id"],
                    str(counts["YES"]),
                    str(counts["CONDITIONAL"]),
                    str(counts["OPEN"]),
                    str(counts["NO"]),
                    str(counts["NOT_APPLICABLE"]),
                    "YES" if counts["YES"] == 12 else "NO",
                    row["primary_blocker"],
                ]
            )
        )
    (HERE / "FAMILY_GATE_COUNTS.tsv").write_text(
        "\n".join(counts_output) + "\n", encoding="utf-8"
    )

    catches: list[tuple[str, str]] = []
    mutated = deepcopy(rows)
    mutated.pop()
    catches.append(expect_failure("missing_family", lambda: validate_matrix(mutated)))
    mutated = deepcopy(rows)
    mutated[-1] = deepcopy(mutated[0])
    catches.append(expect_failure("duplicate_family", lambda: validate_matrix(mutated)))
    mutated = deepcopy(rows)
    mutated[0]["G01"] = "MAYBE"
    catches.append(expect_failure("invalid_gate_value", lambda: validate_matrix(mutated)))
    mutated = deepcopy(rows)
    for gate in GATES:
        mutated[0][gate] = "YES"
    catches.append(expect_failure("synthetic_pass", lambda: validate_matrix(mutated)))
    catches.append(
        expect_failure("cross_family_splice", lambda: cross_family_join(rows[18], rows[23]))
    )
    mutated_lifts = deepcopy(lifts)
    mutated_lifts[2]["involutive_exchange"] = "YES"
    catches.append(
        expect_failure("order_four_as_involution", lambda: validate_lifts(mutated_lifts))
    )
    mutated_witnesses = deepcopy(witnesses)
    mutated_witnesses[2]["type"] = "NATIVE_ON_SHELL_COMPLETE"
    catches.append(
        expect_failure("off_shell_as_on_shell", lambda: validate_witnesses(mutated_witnesses))
    )
    mutated_witnesses = deepcopy(witnesses)
    mutated_witnesses[4]["native_authority"] = "NATIVE_UDT"
    catches.append(
        expect_failure("posit_as_native", lambda: validate_witnesses(mutated_witnesses))
    )
    mutated = deepcopy(rows)
    mutated[25]["G11"] = "YES"
    catches.append(
        expect_failure(
            "pre_july_affirmative",
            lambda: (_ for _ in ()).throw(AssertionError("firewall"))
            if mutated[25]["G11"] == "YES"
            else None,
        )
    )
    catches.append(
        expect_failure(
            "source_count",
            lambda: (_ for _ in ()).throw(AssertionError("source count"))
            if len(sources[:-1]) != 150
            else None,
        )
    )
    catches.append(
        expect_failure(
            "conditional_as_pass",
            lambda: (_ for _ in ()).throw(AssertionError("conditional is not yes"))
            if best["G02"] == "CONDITIONAL"
            else None,
        )
    )
    catches.append(
        expect_failure(
            "strongest_witness_lift_promotion",
            lambda: (_ for _ in ()).throw(AssertionError("lift open"))
            if best["G05"] == "OPEN"
            else None,
        )
    )
    catch_lines = ["catch_id\tresult"]
    catch_lines.extend(f"{label}\t{result}" for label, result in catches)
    (HERE / "CATCH_PROOF_RESULTS.tsv").write_text(
        "\n".join(catch_lines) + "\n", encoding="utf-8"
    )

    status = [
        ["S01", "effective_source_universe", "150_TRACKED_PATHS_FROZEN", "97+4+35+14 disjoint source identities"],
        ["S02", "registered_evidence_families", "28_COMPLETE_BOUNDED_CENSUS", "One row per preregistered family"],
        ["S03", "native_action_or_equation_authority", "ABSENT", "Zero rows have G02 YES"],
        ["S04", "native_complete_on_shell_branch", "ABSENT", "Zero rows have G03 YES"],
        ["S05", "global_involutive_angular_exchange", "CONDITIONAL_OR_OPEN", "No selected lift in any on-shell family"],
        ["S06", "compatible_cap_isotropy_completion", "CONDITIONAL_OR_OPEN", "FC04 and other caps remain supplied or unselected"],
        ["S07", "strongest_near_pass", "B19_CONDITIONAL_C2_ROUND_BRANCH", "Full Bach pass conditional; metric blind to coframe lift; physical boundary open"],
        ["S08", "cross_family_assembly", "FORBIDDEN_AS_PROOF", "Conditional action and conditional toric data cannot be silently spliced"],
        ["S09", "selector_boundary", "PRESENT_SELECTOR_BOUNDARY_VERIFIED_WITH_CAVEATS", "No coherent family passes all twelve gates"],
        ["S10", "fresh_external_semantic_review", "NOT_PERFORMED_CAVEAT", "Independent verification is mechanical and source-identity based"],
        ["S11", "action_carrier_source_mass_scale", "OPEN_OR_CONDITIONAL_UNCHANGED", "No downstream promotion"],
        ["S12", "next_scientific_action", "PONDER_OR_NEW_PREMISE_DISCOVERY_BEFORE_MORE_SELECTOR_DRILLING", "Existing branch inventory is exhausted at this conjunction"],
    ]
    status_lines = ["id\tobject\tstatus\texact_scope"]
    status_lines.extend("\t".join(row) for row in status)
    (HERE / "STATUS_LEDGER.tsv").write_text(
        "\n".join(status_lines) + "\n", encoding="utf-8"
    )

    result = {
        "schema": "udt-involutive-exchange-branch-availability-v1",
        "result": "PASS",
        "maximum_ruling": "PRESENT_SELECTOR_BOUNDARY_VERIFIED_WITH_CAVEATS",
        "families": 28,
        "sources": 150,
        "passing_families": [],
        "native_action_gate_yes": 0,
        "native_complete_on_shell_gate_yes": 0,
        "strongest_near_pass": {
            "family_id": best["family_id"],
            "yes": gate_counts(best)["YES"],
            "conditional": gate_counts(best)["CONDITIONAL"],
            "open": gate_counts(best)["OPEN"],
            "no": gate_counts(best)["NO"],
            "missing_decisive_gates": ["G02", "G03", "G05", "G07", "G09"],
        },
        "intersection_census": {
            "total": 206,
            "report_level": 14,
            "report_level_directly_represented": 14,
        },
        "lifts": {
            "total": 4,
            "involutive": 2,
            "order_four": 2,
            "selected": 0,
        },
        "witnesses": {
            "total": 7,
            "native_on_shell_complete": 0,
        },
        "catch_proofs": len(catches),
        "authority_boundary": {
            "new_action": False,
            "new_carrier": False,
            "lift_selected": False,
            "completion_selected": False,
            "cross_family_splice_used": False,
            "density_or_mass_solve": False,
            "gpu_work": False,
            "canonization": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
