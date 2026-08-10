#!/usr/bin/env python3
"""Fail-closed internal verifier for the G56 descent atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "6c11c218"
EXPECTED_BASE = "eca93e1395c2f690f8357f015ea5901fec9f8310"
EXTERNAL_RAW_SHA256 = "0ad62082826300c7cd8289aca38fb1649ae1dafb2f1773c4778512e4dfa64faf"
EXTERNAL_TRANSCRIPT_SHA256 = "ec6cd66f618c670019e697f861317456faf3aa9dbdc742f5bb6da803f99fb149"
PREREG_FILES = (
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv", "CANDIDATE_UNIVERSE.tsv",
    "DESCENT_AXES.tsv", "FALSIFICATION_CONTRACT.tsv", "COMPLETENESS_MAP.md",
    "SOURCE_MANIFEST.tsv", "verify_preregistration.py",
)


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def main() -> int:
    base = subprocess.check_output(["git", "rev-parse", f"{PREREG_COMMIT}^"], cwd=ROOT, text=True).strip()
    require(base == EXPECTED_BASE, "preregistration base changed")
    for name in PREREG_FILES:
        relative = f"{HERE.name}/{name}"
        result = subprocess.run(["git", "diff", "--quiet", PREREG_COMMIT, "--", relative], cwd=ROOT)
        require(result.returncode == 0, f"preregistered file changed: {name}")

    for row in table("SOURCE_MANIFEST.tsv"):
        raw = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        require(len(raw) == int(row["size"]), f"source size changed: {row['path']}")
        require(hashlib.sha256(raw).hexdigest() == row["sha256"], f"source hash changed: {row['path']}")

    atlas = table("GLOBAL_DESCENT_ATLAS.tsv")
    summary = table("BRANCH_DESCENT_SUMMARY.tsv")
    require(len(atlas) == len({(r["branch_id"], r["axis_id"]) for r in atlas}) == 240, "atlas coverage")
    require(len(summary) == len({r["branch_id"] for r in summary}) == 24, "summary coverage")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    require(result["status"] == "PASS" and result["cell_count"] == 240, "production result")
    require(result["disposition_counts"] == {
        "CONDITIONAL_AFTER_QUERY": 15,
        "INSUFFICIENT_EVIDENCE": 101,
        "MEMBER_DEPENDENT": 14,
        "OPEN_OWNER": 36,
        "OWNED_EXACT": 16,
        "PATH_LABELLED_HOLONOMY": 14,
        "TYPE_INAPPLICABLE": 44,
    }, "disposition counts")
    require(result["complete_descent_selector_count"] == 0, "complete selector promoted")
    require(result["r17_owned_links"] == ["D01", "D02", "D03", "D05"], "R17 owned links")
    require(result["r17_open_links"] == ["D06", "D10"], "R17 reset seam")
    require(result["r18_owned_links"] == ["D01", "D04", "D05", "D06", "D07"], "R18 clock links")

    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    require(independent["status"] == "PASS" and independent["passed"] == independent["total"] == 96,
            "independent verification")
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require(catches["status"] == "PASS" and catches["rejected"] == catches["total"] == 22,
            "catch proofs")

    cells = {(r["branch_id"], r["axis_id"]): r for r in atlas}
    require(cells[("R04", "D09")]["disposition"] == "INSUFFICIENT_EVIDENCE", "R04 correction")
    require(cells[("R17", "D02")]["disposition"] == cells[("R17", "D03")]["disposition"] == "OWNED_EXACT",
            "R17 foliation")
    require(cells[("R17", "D05")]["disposition"] == "OWNED_EXACT", "R17 alignment bitorsor")
    require(cells[("R17", "D06")]["disposition"] == "OPEN_OWNER", "R17 calibration reset")
    require(cells[("R18", "D06")]["disposition"] == "OWNED_EXACT" and "clock state" in cells[("R18", "D06")]["scope_caveat"],
            "R18 scoped identity")
    require(cells[("R23", "D04")]["disposition"] == "PATH_LABELLED_HOLONOMY", "R23 holonomy")
    require(cells[("R24", "D05")]["disposition"] == "MEMBER_DEPENDENT", "R24 set/member")

    require(digest("EXTERNAL_REVIEW_RAW.md") == EXTERNAL_RAW_SHA256, "external raw changed")
    require(digest("EXTERNAL_REVIEW_TRANSCRIPT.log") == EXTERNAL_TRANSCRIPT_SHA256, "external transcript changed")
    external = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    require("`VERIFIED_WITH_CORRECTIONS`" in external, "external grade missing")
    require("`R17/D05`" in external and "`OWNED_EXACT`" in external, "external correction missing")
    review = (HERE / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    require("6c840ed04c4815fe4a17fda828b4b8db419a73a99825185018a43870b724e8ec" in review,
            "original sealed intake hash missing")
    require("f6219446d72aa050e07659c9b721cf3a9c2e37690863f4cb42bb60b92da015b7" in review,
            "corrected sealed replay hash missing")
    repository = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    require(repository["status"] == "PASS" and repository["premise_guards"] == 56,
            "repository gates missing")
    require(repository["pytest"] == "94 passed, 1 xfailed", "test baseline changed")
    require(repository["frozen_manifests"] == 6 and repository["frozen_package_paths"] == 133,
            "frozen manifests changed")
    require(repository["protected_atlas_contents_read"] is False, "protected atlas guard changed")

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for text in (report, exact):
        require("NO_COMPLETE_DESCENT_SELECTOR_IN_PINNED_CORPUS" in text, "landing missing")
        require("not a no-go theorem" in text.lower() or "not a no-go" in text.lower(), "ceiling missing")
        require("R17" in text and "R18" in text and "clock" in text.lower(), "branch distinction missing")
    require("SO(2)" in exact and "R x S1" in exact, "load-bearing R17 objects missing")
    require("clock-only" in report, "R18 scope missing")

    protected = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
    require(all(not row["path"].startswith(protected) for row in table("SOURCE_MANIFEST.tsv")),
            "protected atlas cited")
    print("PASS: G56 final audit; prereg immutable; 20 sources; 24x10=240; R17/D05 correction; independent source reconstruction 96/96; catches 22/22; external VERIFIED_WITH_CORRECTIONS; repository gates PASS; zero complete selectors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
