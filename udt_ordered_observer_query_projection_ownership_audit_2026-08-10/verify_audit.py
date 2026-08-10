#!/usr/bin/env python3
"""Fail-closed final verification of the ordered-query projection audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "28db903f"
EXPECTED_BASE = "93f962a727336dafe256364b7de489e5a63b1972"
INTAKE_MANIFEST_SHA256 = "49cd31909666d09c3e6d2f444c0ef91e59382d4e251dc6675bf0e9f6c5c81575"
FIRST_RAW_SHA256 = "3dde442e42679e102eadca46e4e3ae47ba801c131568b884aa64fc9a91f2f090"
FIRST_TRANSCRIPT_SHA256 = "a7412c6e3d27366d1f025e15f8ab90ecf101c5527fc3aaadbaaae57ead37f25d"
EXTERNAL_RAW_SHA256 = "1855f58a328cd5fc89d589b77837ef5d7a955fb59bae3bc8d92f3e8b802cc85a"
EXTERNAL_TRANSCRIPT_SHA256 = "fb40b814cd49e12271541abb8b2fc087b32dce8dd8a98c326264dbbdb6412da7"
PREREG_FILES = (
    "PREREGISTRATION.md",
    "PONDER_MAP.md",
    "PREMISE_LEDGER.tsv",
    "QUERY_PROJECTION_UNIVERSE.tsv",
    "FOUNDING_SIGNATURE.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "SOURCE_MANIFEST.tsv",
    "verify_preregistration.py",
)


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
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

    sources = table("SOURCE_MANIFEST.tsv")
    require(len(sources) == 17, "source manifest must contain 17 rows")
    require([row["source_id"] for row in sources] == [f"S{i:02d}" for i in range(1, 18)],
            "source ids changed")
    for row in sources:
        raw = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        require(len(raw) == int(row["size"]), f"source size changed: {row['path']}")
        require(hashlib.sha256(raw).hexdigest() == row["sha256"],
                f"source hash changed: {row['path']}")
        blob = subprocess.check_output(
            ["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True
        ).strip()
        require(blob == row["git_blob"], f"source blob changed: {row['path']}")

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8")
    )
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require(result["status"] == "PASS" and result["passed"] == result["total"] == 23,
            "production result is not 23/23 PASS")
    require(independent["status"] == "PASS" and independent["passed"] == independent["total"] == 25,
            "independent result is not 25/25 PASS")
    require(catches["status"] == "PASS" and catches["rejected"] == catches["total"] == 23,
            "catch proofs are not 23/23 PASS")

    require(result["founding_query_output"] ==
            "Delta_phi_AS_CONDITIONAL_REALIZATION_OF_FOUNDING_PROJECTION_WITHIN_CONTINUOUS_REAL_TWO_DENSITY_CHARACTER_CLASS",
            "conditional projection wording changed")
    require(result["uniqueness_scope"] ==
            "UNIQUE_ONLY_WITHIN_FOUNDED_DENSITY_CHARACTERS_NOT_ALL_COMPLETE_STATE_COBBOUNDARIES",
            "uniqueness scope changed")
    require(result["kappa_status"] == "RETAINED_COMPLETE_STATE_NOT_DELETED_BY_RECIPROCAL_PROJECTION",
            "kappa was lost")
    require(result["phi_orchestra"] == "UPSTREAM_COMPLETE_PAIR_METRIC_MODULATION_RETAINED",
            "phi+orchestra was lost")
    require(result["physical_regime_policy"] is None, "physical regime policy invented")
    require(result["conductor_owner"] is None, "conductor invented")
    require(len(table("QUERY_PROJECTION_CLASSIFICATION.tsv")) == 14,
            "projection classification changed")
    require(len(table("MEASUREMENT_OWNERSHIP_ATLAS.tsv")) == 6,
            "measurement atlas changed")
    require(len(table("FOUNDING_SIGNATURE_RESULT.tsv")) == 5,
            "founding signature result changed")

    require(digest("EXTERNAL_REVIEW_FIRST_RAW.md") == FIRST_RAW_SHA256,
            "first external raw changed")
    require(digest("EXTERNAL_REVIEW_FIRST_TRANSCRIPT.log") == FIRST_TRANSCRIPT_SHA256,
            "first external transcript changed")
    require(digest("EXTERNAL_REVIEW_RAW.md") == EXTERNAL_RAW_SHA256,
            "corrected external raw changed")
    require(digest("EXTERNAL_REVIEW_TRANSCRIPT.log") == EXTERNAL_TRANSCRIPT_SHA256,
            "corrected external transcript changed")
    external = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    require("FOUNDED_PROJECTION_ONLY_REALIZATION_CONDITIONAL" in external,
            "external grade missing")
    require("verified clean" in external and "all 45" not in external,
            "external manifest-verification wording changed")
    require("complete calibrated observer query has supplied the relevant pair relation" in external,
            "external corrected wording missing")
    correction = (HERE / "EXTERNAL_REVIEW_NAVIGATION_CORRECTION.md").read_text(encoding="utf-8")
    require(INTAKE_MANIFEST_SHA256 in correction, "intake manifest hash missing")
    require("source texts were absent" in correction, "first-review correction missing")

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for text, name in ((report, "report"), (exact, "exact derivation")):
        flat = " ".join(text.split())
        require("complete calibrated observer query" in flat,
                f"conditional query boundary missing: {name}")
        require("physical pair" in flat, f"physical-pair open boundary missing: {name}")
        require("Delta_phi" in flat, f"reciprocal projection missing: {name}")

    forbidden = (
        "COMPLETE_PHYSICAL_OBSERVER_ARROW_DERIVED",
        "PHYSICAL_REGIME_MAP_DERIVED",
        "UNIVERSAL_C_EFF_DERIVED",
        "NATIVE_ACTION_DERIVED",
        "BOOTSTRAP_CLOSED",
    )
    corpus = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in HERE.iterdir()
        if path.is_file() and path.suffix in {".md", ".tsv", ".json"}
    )
    for token in forbidden:
        require(token not in corpus, f"forbidden promotion: {token}")

    print(
        "PASS: preregistration immutable; 17/17 sources pinned; production 23/23; "
        "independent 25/25; catches 23/23; both external reviews preserved; corrected "
        "external grade founded-projection-only-realization-conditional; kappa and "
        "phi+orchestra retained; pair owner, regime, conductor, and downstream physics open"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
