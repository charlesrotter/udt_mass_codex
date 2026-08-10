#!/usr/bin/env python3
"""Fail-closed final verifier for the G55 multi-regime admissibility audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "4affd614"
EXPECTED_BASE = "7a14aa43a3cd38b23307f0778ff99cd0212bd261"
INTAKE_MANIFEST_SHA256 = "b391556fa50b836d99dec9f62baf9ac759f2b9f4675fccc44a818ffdac93653a"
FIRST_TRANSCRIPT_SHA256 = "c30c489454647df70e2e73922ce35e8ee499fb210795de63c7023ee564dd3425"
EXTERNAL_RAW_SHA256 = "bd3fa6d1dba21bf3b2b28c8a4f810eed707688d32fb8cc8f47edbc4a5ec63408"
EXTERNAL_TRANSCRIPT_SHA256 = "d6ac3cf701a88133985a0699f81b4327f8ecaa27ccab0e3f87d6703fad9e7135"
PREREG_FILES = (
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv", "CANDIDATE_UNIVERSE.tsv",
    "ADMISSIBILITY_AXES.tsv", "FALSIFICATION_CONTRACT.tsv", "COMPLETENESS_MAP.md",
    "SOURCE_MANIFEST.tsv", "verify_preregistration.py",
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
    require(len(sources) == 20, "source manifest must contain 20 rows")
    require([row["source_id"] for row in sources] == [f"S{i:02d}" for i in range(1, 21)],
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
    require(result["status"] == "PASS", "production result failed")
    require(result["branch_count"] == 24 and result["measurement_cells"] == 144,
            "branch/measurement coverage changed")
    require(result["axis_cells"] == 240 and result["pattern_family_count"] == 11,
            "axis/family coverage changed")
    require(result["measurement_disposition_counts"] == {
        "CONDITIONALLY_AVAILABLE": 17,
        "FOUNDED_AFTER_PAIR_SUPPLIED": 5,
        "INSUFFICIENT_EVIDENCE": 69,
        "OPEN_OWNER": 31,
        "TYPE_INAPPLICABLE": 22,
    }, "corrected measurement counts changed")
    require(result["axis_disposition_counts"] == {
        "CONDITIONALLY_AVAILABLE": 27,
        "FOUNDED_AFTER_PAIR_SUPPLIED": 5,
        "GLOBAL_COMPLETION_OWNED": 5,
        "INSUFFICIENT_EVIDENCE": 108,
        "OPEN_OWNER": 56,
        "TYPE_INAPPLICABLE": 39,
    }, "corrected axis counts changed")
    for key in (
        "physical_pair_relation_owners", "physical_nonisometric_arrow_owners",
        "optional_measurement_selector_owners", "physical_regime_owners",
    ):
        require(result[key] == 0, f"owner promoted: {key}")
    require(result["global_structural_restriction_owners"] == 5,
            "bounded global restriction count changed")
    require(result["full_multichannel_conditional_branch"] == "R17",
            "full conditional panel branch changed")
    require(independent["status"] == "PASS" and independent["passed"] == independent["total"] == 33,
            "independent result is not 33/33 PASS")
    require(catches["status"] == "PASS" and catches["rejected"] == catches["total"] == 22,
            "catch proofs are not 22/22 PASS")

    profiles = table("BRANCH_ADMISSIBILITY_PROFILES.tsv")
    matrix = table("BRANCH_MEASUREMENT_MATRIX.tsv")
    axes = table("BRANCH_AXIS_MATRIX.tsv")
    families = table("GEOMETRIC_PATTERN_FAMILIES.tsv")
    require(len(profiles) == 24 and len({row["branch_id"] for row in profiles}) == 24,
            "profile coverage changed")
    require(len(matrix) == len({(row["branch_id"], row["measurement_id"]) for row in matrix}) == 144,
            "measurement Cartesian coverage changed")
    require(len(axes) == len({(row["branch_id"], row["axis_id"]) for row in axes}) == 240,
            "axis Cartesian coverage changed")
    require(len(families) == 11 and sum(int(row["branch_count"]) for row in families) == 24,
            "family partition changed")
    cells = {(row["branch_id"], row["measurement_id"]): row for row in matrix}
    axis_cells = {(row["branch_id"], row["axis_id"]): row for row in axes}
    require(all(cells[("R04", f"M{i:02d}")]["disposition"] == "INSUFFICIENT_EVIDENCE"
                for i in range(1, 6)), "R04 inherited a member measurement panel")
    require(all(axis_cells[("R04", f"A{i:02d}")]["disposition"] == "INSUFFICIENT_EVIDENCE"
                for i in range(2, 7)), "R04 inherited member ownership axes")
    require({row["branch_id"] for row in axes
             if row["axis_id"] == "A09" and row["disposition"] == "GLOBAL_COMPLETION_OWNED"}
            == {"R04", "R17", "R18", "R23", "R24"},
            "bounded A09 owner set changed")

    require(digest("EXTERNAL_REVIEW_FIRST_TRANSCRIPT.log") == FIRST_TRANSCRIPT_SHA256,
            "first incomplete external transcript changed")
    require(digest("EXTERNAL_REVIEW_RAW.md") == EXTERNAL_RAW_SHA256,
            "external raw changed")
    require(digest("EXTERNAL_REVIEW_TRANSCRIPT.log") == EXTERNAL_TRANSCRIPT_SHA256,
            "external transcript changed")
    external = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    require(external.startswith("`VERIFIED_WITH_CORRECTIONS`"), "external grade missing")
    require("R04/M01" in external and "R04/A02" in external,
            "external corrected cell set missing")
    correction = (HERE / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    require(INTAKE_MANIFEST_SHA256 in correction, "intake manifest hash missing")
    require("51 files total" in correction and "exactly 20" in correction,
            "external intake scope changed")

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for text, name in ((report, "report"), (exact, "exact derivation")):
        flat = " ".join(text.split())
        require("11" in flat and "R17" in flat, f"atlas summary missing: {name}")
        require("None owns the complete physical calibrated observer-pair relation" in flat,
                f"physical-pair boundary missing: {name}")
        require("R04" in flat and "aggregate" in flat, f"R04 correction missing: {name}")

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
        "PASS: preregistration immutable; 20/20 sources pinned; 24 branches; 144 measurement "
        "cells; 240 axis cells; 11 apparatus patterns; R04 aggregate correction; five bounded "
        "global restrictions; zero physical pair/arrow/selector/regime owners; independent "
        "33/33; catches 22/22; external VERIFIED_WITH_CORRECTIONS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
