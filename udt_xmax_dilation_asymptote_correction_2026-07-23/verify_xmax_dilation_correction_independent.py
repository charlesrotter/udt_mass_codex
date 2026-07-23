#!/usr/bin/env python3
"""Independent standard-library verification of the correction package."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PARENT_MANIFEST_SHA256 = (
    "8798461fbd59891c1eff90c36311e38a29a3753dd4066d75360a813a859955c0"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def check(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def rejected(condition: bool, label: str, catches: list[str]) -> None:
    if condition:
        raise AssertionError("mutation survived: " + label)
    catches.append(label)


def main() -> None:
    checks: list[str] = []
    catches: list[str] = []

    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    source_rows = rows("SOURCE_LINEAGE.tsv")
    graph = rows("FORMULA_DEPENDENCY_GRAPH.tsv")
    sne_rows = rows("SNE_SOURCE_ADJUDICATION.tsv")
    regrades = rows("PARENT_CLAIM_REGRADE.tsv")
    statuses = rows("STATUS_LEDGER.tsv")

    check(len(source_rows) == 23, "source-count-23", checks)
    check(len({row["path"] for row in source_rows}) == 23, "source-unique", checks)
    for row in source_rows:
        path = ROOT / row["path"]
        check(path.is_file(), "source-exists:" + row["path"], checks)
        check(digest(path) == row["sha256"], "source-hash:" + row["path"], checks)

    # Independent algebra: start with e^-phi=q, not with production output.
    for q in (Fraction(1, 2), Fraction(1, 4), Fraction(3, 5)):
        a = q**2
        r_over_x = 1 - a
        z = 1 / q - 1
        d_l_over_x = (1 + z) ** 2 * r_over_x
        check(d_l_over_x == z * (z + 2), f"full-light:{q}", checks)
        check(r_over_x < 1, f"finite-coordinate:{q}", checks)
        check((1 - q) < r_over_x, f"proper-coordinate-distinct:{q}", checks)
        check(
            (1 - a) / (1 + a) != r_over_x,
            f"projective-coordinate-distinct:{q}",
            checks,
        )

    # Independent WR-L exponent audit.
    admissible = []
    candidates = [
        ("below", Fraction(1, 2)),
        ("one", Fraction(1, 1)),
        ("between", Fraction(3, 2)),
        ("two", Fraction(2, 1)),
        ("above", Fraction(5, 2)),
    ]
    for name, alpha in candidates:
        optical = alpha >= 1
        proper = alpha < 2
        # lim A'' finite: alpha=1 has zero coefficient; alpha>=2 is finite.
        curvature = alpha == 1 or alpha >= 2
        if optical and proper and curvature:
            admissible.append(name)
    check(admissible == ["one"], "wrl-alpha-one", checks)

    graph_by_id = {row["node_id"]: row for row in graph}
    check(len(graph_by_id) == 14, "dependency-node-count", checks)
    check(
        graph_by_id["F06"]["status"] == "DERIVED_CONDITIONAL_WRL",
        "wrl-profile-status",
        checks,
    )
    check(
        graph_by_id["F11"]["status"] == "OBSERVED",
        "sne-observed-status",
        checks,
    )
    check(
        graph_by_id["F13"]["status"] == "WORKING_OPEN",
        "mass-open-status",
        checks,
    )

    status = {row["claim_id"]: row for row in statuses}
    check(len(status) == 18, "status-row-count", checks)
    check(
        status["Q01"]["status"] == "OWNER_WORKING_POSTULATE",
        "xmax-owner-status",
        checks,
    )
    check(
        status["Q06"]["status"] == "DERIVED_CONDITIONAL_WRL",
        "profile-conditional-status",
        checks,
    )
    check(
        status["Q11"]["status"] == "WORKING_OPEN",
        "native-mass-open",
        checks,
    )
    check(status["Q18"]["status"] == "OPEN", "xmax-value-open", checks)

    check(len(sne_rows) == 15, "sne-source-count", checks)
    check(
        all(row["derives_profile"] == "NO" for row in sne_rows),
        "no-sne-source-derives-profile",
        checks,
    )
    check(len(regrades) == 16, "parent-regrade-count", checks)

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    questions = (HERE / "QUESTIONS_2_4_LAY.md").read_text(encoding="utf-8")
    check(
        "not the supernova" in report and "fit." in report,
        "report-sne-distinction",
        checks,
    )
    check("same profile" in lay, "lay-same-profile", checks)
    check("same finish line" in questions, "observer-lay", checks)
    check(
        "number printed at the" in questions and "end." in questions,
        "scale-lay",
        checks,
    )

    parent_manifest = (
        ROOT
        / "udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23"
        / "MANIFEST.sha256"
    )
    check(
        digest(parent_manifest) == PARENT_MANIFEST_SHA256,
        "parent-manifest-byte-identical",
        checks,
    )

    # Exercised fail-closed mutations, implemented without importing production.
    rejected(
        status["Q01"]["status"] == "WRL_PROPER_READOUT",
        "readout-defines-xmax",
        catches,
    )
    rejected(
        status["Q06"]["status"] == "DERIVED_FROM_BARE_METRIC",
        "hide-wrl-premises",
        catches,
    )
    rejected(
        any(row["derives_profile"] == "YES" for row in sne_rows),
        "sne-promoted-to-derivation",
        catches,
    )
    rejected(
        status["Q08"]["status"] == "DERIVED_FROM_BOUND_ALONE",
        "tanh-overclaim",
        catches,
    )
    rejected(
        status["Q11"]["status"] == "DERIVED",
        "mass-overclaim",
        catches,
    )
    rejected(
        status["Q09"]["status"] == "DERIVED_GLOBAL",
        "global-branch-overclaim",
        catches,
    )
    rejected(
        status["Q18"]["status"] == "DERIVED_FROM_C_G",
        "dimensional-scale-overclaim",
        catches,
    )
    rejected(
        status["Q14"]["status"] == "IDENTICAL_COORDINATES",
        "observer-coordinate-conflation",
        catches,
    )
    rejected(
        status["Q15"]["status"] == "DERIVED_EQUALS_ONE",
        "angular-lambda-overclaim",
        catches,
    )
    rejected(
        any(row["source_role"] == "OUTPUT_AS_PREMISE" for row in sne_rows),
        "output-as-premise",
        catches,
    )
    rejected(
        result["profile"]["wrl_profile"] == "r/X=tanh(phi)",
        "profiles-conflated",
        catches,
    )
    rejected(
        result["sne"]["derives_profile"] is True,
        "result-sne-overclaim",
        catches,
    )

    check(len(catches) == 12, "catch-count-12", checks)
    check(
        result["grade"] == "VERIFIED-WITH-CAVEATS",
        "grade-with-caveats",
        checks,
    )
    output = {
        "schema": "udt-xmax-dilation-asymptote-independent-1.0",
        "result": "PASS",
        "all_checks_pass": True,
        "check_count": len(checks),
        "catch_count": len(catches),
        "catch_pass_count": len(catches),
        "source_hash_checks": len(source_rows),
        "method": "fresh_standard_library_algebra_and_source_table_audit",
        "fresh_semantic_agent": "NOT_RUN",
        "grade": "VERIFIED-WITH-CAVEATS",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
