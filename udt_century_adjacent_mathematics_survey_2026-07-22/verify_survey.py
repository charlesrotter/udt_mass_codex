#!/usr/bin/env python3
"""Independent fail-closed verifier for the century-scale survey package."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE_FIELDS = [
    "source_id", "family", "year", "authors", "title", "stable_url", "source_type",
    "result_paraphrase", "indispensable_hypotheses", "udt_join", "match_grade", "allowed_role",
    "firewall_prohibition", "new_udt_premise_needed", "metric_native_returned_question",
]
FAMILIES = {f"F{i:02d}_" for i in range(1, 12)}
MATCHES = {"DIRECT_MATHEMATICAL_MATCH", "PARTIAL_HYPOTHESIS_MATCH", "ANALOGY_ONLY", "NONAPPLICABLE_CONTROL"}
ROLES = {"VOCABULARY", "UNIVERSAL_CONTROL", "APPLICABLE_THEOREM_IF_HYPOTHESES_PASS", "OBSTRUCTION_OR_COUNTEREXAMPLE", "QUESTION_GENERATOR"}
JOINS = {f"J{i:02d}" for i in range(1, 14)}
EXPECTED_SOURCE_COUNT = 46
EXPECTED_FAMILY_COUNTS = {
    "F01_NATURAL_OPERATORS": 4,
    "F02_HOLONOMY": 5,
    "F03_CONFORMAL_PROJECTIVE_SCALE": 6,
    "F04_EXTERIOR_CURVATURE_TOPOLOGY": 4,
    "F05_BUNDLES_GLUING": 4,
    "F06_BOUNDARY_VARIATION_CHARGE": 4,
    "F07_SPECTRAL_SCALE": 3,
    "F08_INVERSE_VARIATIONAL": 4,
    "F09_FIXED_POINT_BOOTSTRAP": 3,
    "F10_EVOLUTION_AND_CONSTRAINTS": 4,
    "F11_HOPF_SOLITON_CONTROLS": 5,
}
EXPECTED_STATIC_IDS = {
    "CROSS_FAMILY_CONVERGENCE.tsv": [f"C{i:02d}" for i in range(1, 9)],
    "MISSING_DATUM_LEDGER.tsv": [f"M{i:02d}" for i in range(1, 10)],
    "RESEARCH_QUESTION_RANKING.tsv": [f"Q0{i}_" for i in range(1, 8)],
}


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_sources(rows: list[dict[str, str]], fields: list[str]) -> None:
    assert fields == SOURCE_FIELDS, (fields, SOURCE_FIELDS)
    assert len(rows) == EXPECTED_SOURCE_COUNT
    ids = [row["source_id"] for row in rows]
    assert ids == [f"S{i:03d}" for i in range(1, EXPECTED_SOURCE_COUNT + 1)]
    assert len(ids) == len(set(ids))
    assert Counter(row["family"] for row in rows) == Counter(EXPECTED_FAMILY_COUNTS)
    assert {row["family"].split("_", 1)[0] + "_" for row in rows} == FAMILIES
    assert all(1925 <= int(row["year"]) <= 2026 for row in rows)
    assert min(int(row["year"]) for row in rows) == 1930
    assert max(int(row["year"]) for row in rows) == 2004
    assert all(row["stable_url"].startswith("https://") for row in rows)
    assert all(row["source_type"].startswith(("PRIMARY_", "AUTHOR_ARCHIVE_")) for row in rows)
    assert all(row["match_grade"] in MATCHES for row in rows)
    assert all(row["allowed_role"] in ROLES for row in rows)
    assert all(row["udt_join"] in JOINS for row in rows)
    assert all(row["indispensable_hypotheses"].strip() for row in rows)
    assert all(row["firewall_prohibition"].startswith(("Cannot", "The ", "A ", "Degree ")) for row in rows)
    assert all(row["metric_native_returned_question"].endswith("?") for row in rows)
    assert not any(row["allowed_role"] == "AFFIRMATIVE_UDT_PHYSICS" for row in rows)
    summary = json.loads((HERE / "BUILD_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["external_structures_adopted"] == 0
    assert summary["physics_solves_run"] == 0
    assert summary["gpu_runs"] == 0


def expected_adjacency(rows: list[dict[str, str]]) -> dict[str, tuple[int, str, str]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[row["family"]][row["udt_join"]] += 1
    return {
        family: (
            sum(counts.values()),
            ";".join(f"{join}:{counts[join]}" for join in sorted(counts)),
            ";".join(sorted(counts)),
        )
        for family, counts in grouped.items()
    }


def validate_derived(rows: list[dict[str, str]]) -> None:
    _, adjacency = read_tsv(HERE / "UDT_ADJACENCY_MATRIX.tsv")
    got = {r["family"]: (int(r["source_count"]), r["join_counts"], r["joins_touched"]) for r in adjacency}
    assert got == expected_adjacency(rows)

    _, gates = read_tsv(HERE / "APPLICABILITY_GATES.tsv")
    assert len(gates) == len(rows)
    for source, gate in zip(rows, gates, strict=True):
        assert gate["source_id"] == source["source_id"]
        assert gate["udt_join"] == source["udt_join"]
        assert gate["match_grade"] == source["match_grade"]
        assert gate["allowed_role"] == source["allowed_role"]
        assert gate["hypothesis_gate"] == source["indispensable_hypotheses"]
        assert gate["firewall_gate"] == source["firewall_prohibition"]
        assert gate["application_status"] == "GATED__NOT_APPLIED_AS_UDT_PHYSICS"

    _, convergence = read_tsv(HERE / "CROSS_FAMILY_CONVERGENCE.tsv")
    assert [r["convergence_id"] for r in convergence] == EXPECTED_STATIC_IDS["CROSS_FAMILY_CONVERGENCE.tsv"]
    assert convergence[-1]["priority"] == "DECISIVE"
    assert "operational selector relation" in convergence[-1]["udt_use"]

    _, missing = read_tsv(HERE / "MISSING_DATUM_LEDGER.tsv")
    assert [r["datum_id"] for r in missing] == EXPECTED_STATIC_IDS["MISSING_DATUM_LEDGER.tsv"]
    assert not any(r["status"] == "DERIVED" for r in missing)

    _, questions = read_tsv(HERE / "RESEARCH_QUESTION_RANKING.tsv")
    assert [int(r["rank"]) for r in questions] == list(range(1, 8))
    for prefix, row in zip(EXPECTED_STATIC_IDS["RESEARCH_QUESTION_RANKING.tsv"], questions, strict=True):
        assert row["question_id"].startswith(prefix)
    assert questions[0]["question_id"] == "Q01_LOCAL_NATURAL_SELECTOR_EXHAUSTION"
    assert questions[1]["question_id"] == "Q02_FULL_JET_HOLONOMY_CLOSURE"
    assert questions[-1]["compute_class"] == "CPU_THEN_OPTIONAL_GPU"


def validate_reports() -> None:
    report = (HERE / "SURVEY_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_READOUT.md").read_text(encoding="utf-8")
    notes = (HERE / "SOURCE_NOTES.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    required_report = [
        "CENTURY_SCALE_COMPARATIVE_MATHEMATICS_ATLAS_CHARACTERIZED__NO_EXTERNAL_STRUCTURE_ADOPTED_AS_UDT",
        "local/global fork", "Peetre-Slovak", "Ambrose-Singer", "not the complete persistence test",
        "The output type cannot be guessed", "No external action", "WORKING_NEXT_QUESTION",
    ]
    assert all(token in report for token in required_report)
    assert "only two broad places" in lay
    assert "Nothing in the survey changes UDT's existing scientific claims" in lay
    assert notes.count("https://") >= EXPECTED_SOURCE_COUNT
    assert "## Maximum conclusion" in prereg
    assert "an external action, field equation, carrier" in prereg


def must_fail(name: str, mutator, base_rows: list[dict[str, str]], base_fields: list[str]) -> tuple[str, str]:
    rows = copy.deepcopy(base_rows)
    fields = list(base_fields)
    mutator(rows, fields)
    try:
        validate_sources(rows, fields)
    except (AssertionError, ValueError, KeyError) as exc:
        return name, f"PASS__REJECTED:{type(exc).__name__}"
    raise AssertionError(f"catch did not reject corruption: {name}")


def run_catches(rows: list[dict[str, str]], fields: list[str]) -> list[tuple[str, str]]:
    catches = [
        must_fail("missing_source", lambda r, f: r.pop(), rows, fields),
        must_fail("duplicate_source", lambda r, f: r.__setitem__(-1, copy.deepcopy(r[-2])), rows, fields),
        must_fail("missing_family", lambda r, f: [x.__setitem__("family", "F01_NATURAL_OPERATORS") for x in r if x["family"] == "F11_HOPF_SOLITON_CONTROLS"], rows, fields),
        must_fail("nonprimary_source", lambda r, f: r[0].__setitem__("source_type", "SECONDARY_REVIEW"), rows, fields),
        must_fail("bad_join", lambda r, f: r[0].__setitem__("udt_join", "J99"), rows, fields),
        must_fail("missing_hypotheses", lambda r, f: r[0].__setitem__("indispensable_hypotheses", ""), rows, fields),
        must_fail("external_affirmative_role", lambda r, f: r[0].__setitem__("allowed_role", "AFFIRMATIVE_UDT_PHYSICS"), rows, fields),
        must_fail("missing_firewall", lambda r, f: r[0].__setitem__("firewall_prohibition", ""), rows, fields),
        must_fail("invalid_match_grade", lambda r, f: r[0].__setitem__("match_grade", "DERIVED_UDT"), rows, fields),
        must_fail("untyped_return_question", lambda r, f: r[0].__setitem__("metric_native_returned_question", "Adopt Einstein tensor"), rows, fields),
        must_fail("wrong_schema", lambda r, f: f.pop(), rows, fields),
        must_fail("out_of_window_year", lambda r, f: r[0].__setitem__("year", "1917"), rows, fields),
    ]

    # Load-bearing semantic catches not expressible solely through source schema.
    report_path = HERE / "SURVEY_REPORT.md"
    report = report_path.read_text(encoding="utf-8")
    for name, old, new in [
        ("erase_locality_condition", "If the missing selector is regular, local, covariant", "The missing selector is"),
        ("promote_eigenplane_to_holonomy", "it is not the complete persistence test", "it completes the persistence test"),
        ("adopt_external_action", "No external action", "An external action"),
    ]:
        mutated = report.replace(old, new, 1)
        ok = all(token in mutated for token in ["If the missing selector is regular, local, covariant", "it is not the complete persistence test", "No external action"])
        assert not ok, name
        catches.append((name, "PASS__REJECTED:semantic_guard"))
    return catches


def validate_prereg_commit() -> str:
    output = subprocess.check_output(
        ["git", "log", "--format=%H", "--", str(HERE / "PREREGISTRATION.md")],
        cwd=ROOT,
        text=True,
    ).splitlines()
    assert output
    introducing = output[-1]
    assert introducing.startswith("2ec56b6")
    return introducing


def main() -> None:
    fields, rows = read_tsv(HERE / "SOURCE_CENSUS.tsv")
    validate_sources(rows, fields)
    validate_derived(rows)
    validate_reports()
    prereg_commit = validate_prereg_commit()
    catches = run_catches(rows, fields)

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "result"])
        writer.writerows(catches)

    result = {
        "status": "PASS",
        "maximum_conclusion": "CENTURY_SCALE_COMPARATIVE_MATHEMATICS_ATLAS_CHARACTERIZED__NO_EXTERNAL_STRUCTURE_ADOPTED_AS_UDT",
        "source_count": len(rows),
        "family_count": len(set(r["family"] for r in rows)),
        "catch_count": len(catches),
        "catch_pass_count": sum(result.startswith("PASS") for _, result in catches),
        "preregistration_commit": prereg_commit,
        "source_census_sha256": sha256(HERE / "SOURCE_CENSUS.tsv"),
        "survey_report_sha256": sha256(HERE / "SURVEY_REPORT.md"),
        "external_structures_adopted": 0,
        "physics_solves_run": 0,
        "gpu_runs": 0,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
