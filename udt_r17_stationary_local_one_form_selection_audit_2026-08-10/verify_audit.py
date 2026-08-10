#!/usr/bin/env python3
"""Fail-closed verification of the stationary R17 one-form audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "1caa97f9"
EXPECTED_BASE = "7effab89775b0ef33ee58dcab144ae0a0d36686b"
EXTERNAL_SHA256 = "e06e18f0ac8365f983946d45258bad0927a8acb8cd5def41705b5287113d71c4"
PREREG_FILES = (
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "CANDIDATE_UNIVERSE.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "SOURCE_SCOPE.tsv",
    "COMPLETENESS_MAP.md",
    "SOURCE_MANIFEST.tsv",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    base = subprocess.check_output(
        ["git", "rev-parse", f"{PREREG_COMMIT}^"], cwd=ROOT, text=True
    ).strip()
    require(base == EXPECTED_BASE, "preregistration base changed")
    for name in PREREG_FILES:
        relative = f"{HERE.name}/{name}"
        result = subprocess.run(
            ["git", "diff", "--quiet", PREREG_COMMIT, "--", relative], cwd=ROOT, check=False
        )
        require(result.returncode == 0, f"preregistered file changed: {name}")

    source_rows = table(HERE / "SOURCE_MANIFEST.tsv")
    require(len(source_rows) == 18, "source manifest must have exactly 18 rows")
    for row in source_rows:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        require(len(data) == int(row["size"]), f"source size changed: {row['path']}")
        require(hashlib.sha256(data).hexdigest() == row["sha256"], f"source hash changed: {row['path']}")
        blob = subprocess.check_output(
            ["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True
        ).strip()
        require(blob == row["git_blob"], f"source blob changed: {row['path']}")

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8")
    )
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require(result["status"] == "PASS" and result["passed"] == result["total"] == 17,
            "production derivation is not 17/17 PASS")
    require(independent["status"] == "PASS" and independent["passed"] == independent["total"] == 17,
            "independent verification is not 17/17 PASS")
    require(catches["status"] == "PASS" and catches["rejected"] == catches["total"] == 20,
            "catch proofs are not 20/20 PASS")
    require(result["metric_owned_forms_beyond_dphi"] is True, "metric-owned forms lost")
    require(result["distinguished_reciprocal_transgression_beyond_dphi"] is False,
            "a distinguished transgression was silently promoted")
    require(result["selection_owner"] is None, "selection owner was silently supplied")
    require("alpha_c=dphi+c*Hstar_dphi" in result["pure_pair_leaf_preserving_transgression_family"],
            "nonclosed constructive family lost")
    require("dHstar_dphi_ZY=1/2" in result["pure_pair_leaf_preserving_transgression_family"],
            "nonclosed witness lost")
    require("beta_c=dphi+c*dJ_H" in result["pure_reciprocal_preserving_exact_family"],
            "exact constructive family lost")
    require("c_UNSELECTED" in result["pure_reciprocal_preserving_exact_family"],
            "exact-family parameter was silently selected")

    candidate_ids = [row["candidate_id"] for row in table(HERE / "ONE_FORM_CLASSIFICATION.tsv")]
    require(candidate_ids == [f"L{i:02d}" for i in range(1, 17)], "candidate ledger is incomplete")
    require(len(table(HERE / "INVARIANT_COVECTOR_ATLAS.tsv")) == 4, "covector atlas row count")
    require(len(table(HERE / "CLOSEDNESS_ATLAS.tsv")) == 8, "closedness atlas row count")
    require(len(table(HERE / "SELECTION_OWNER_CENSUS.tsv")) == 6, "owner census row count")

    raw = HERE / "EXTERNAL_REVIEW_RAW.md"
    require(digest(raw) == EXTERNAL_SHA256, "external review raw hash changed")
    external = (HERE / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    require("CONSTRUCTIVE_NONUNIQUENESS_ONLY" in external, "external verdict missing")
    require("not an exhaustive classification theorem" in external, "external scope correction missing")
    require("explicit physical query/measurement premise" in external, "smallest owner correction missing")

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for text, name in ((report, "report"), (exact, "exact derivation")):
        flat = " ".join(text.split())
        require(
            "not an exhaustive classification" in flat or "scope is constructive" in flat,
            f"constructive scope missing: {name}",
        )
        require("explicit physical query/measurement premise" in flat, f"smallest owner missing: {name}")
    forbidden = (
        "UNIQUE_NATIVE_ONE_FORM_SELECTED",
        "PHYSICAL_PATH_DERIVED",
        "UNIVERSAL_C_EFF_DERIVED",
        "NATIVE_ACTION_DERIVED",
        "BOOTSTRAP_CLOSED",
    )
    corpus = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in HERE.iterdir() if path.is_file() and path.suffix in {".md", ".tsv", ".json"}
    )
    for token in forbidden:
        require(token not in corpus, f"forbidden downstream promotion: {token}")

    print(
        "PASS: preregistration immutable; 18/18 sources pinned; production 17/17; "
        "independent 17/17; catches 20/20; external verdict constructive-nonuniqueness-only; "
        "no selector or downstream physics promoted"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
