#!/usr/bin/env python3
"""Fail-closed verification of the append-only cold-review adjudication."""

from __future__ import annotations

import csv
import hashlib
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_freeze(entries: list[dict[str, str]]) -> None:
    require(len(entries) == 13, "freeze count")
    require(len({row["path"] for row in entries}) == 13, "freeze uniqueness")
    for row in entries:
        path = HERE / row["path"]
        require(path.is_file(), f"freeze path {row['path']}")
        require(digest(path) == row["sha256"], f"freeze hash {row['path']}")
        require(path.stat().st_size == int(row["size_bytes"]), f"freeze size {row['path']}")


def validate_reviews(entries: list[dict[str, str]]) -> None:
    require(len(entries) == 8, "review evidence count")
    require({row["role"] for row in entries} == {"G", "T", "V", "B"}, "review role coverage")
    require(len({row["artifact"] for row in entries}) == 8, "review artifact uniqueness")
    for row in entries:
        path = HERE / row["artifact"]
        require(path.is_file(), f"review path {row['artifact']}")
        require(digest(path) == row["sha256"], f"review hash {row['artifact']}")
        require(path.stat().st_size == int(row["size_bytes"]), f"review size {row['artifact']}")
        require(row["verdict"] == "PASS-WITH-CAVEATS", f"review verdict {row['artifact']}")
        if row["artifact"].endswith("_RAW.md"):
            require("PASS-WITH-CAVEATS" in path.read_text(encoding="utf-8"), f"raw verdict {row['artifact']}")


def validate_agreement(entries: list[dict[str, str]]) -> None:
    expected = {f"R{number:02d}" for number in range(1, 16)}
    require(len(entries) == 15, "agreement count")
    require({row["issue_id"] for row in entries} == expected, "agreement identity coverage")
    require(len({row["issue_id"] for row in entries}) == len(entries), "agreement duplicates")
    for row in entries:
        require(bool(row["adjudication"]), f"empty adjudication {row['issue_id']}")
        require(bool(row["effect_on_frozen_status"]), f"empty status effect {row['issue_id']}")
    require(next(row for row in entries if row["issue_id"] == "R01")["adjudication"] == "REFERENCE_FAITHFUL_WITH_APPEND_ONLY_QUALIFICATIONS", "overall verdict")
    require(next(row for row in entries if row["issue_id"] == "R15")["adjudication"] == "NOT_AUTHORIZED", "compute boundary")


def validate_correction(text: str) -> None:
    required = (
        "Nothing in `REFERENCE_FREEZE_MANIFEST.tsv` is rewritten",
        "twelve-row registered completion/behavior taxonomy",
        "It is not a partition into twelve mutually",
        "the conditional bundle has `|c1|=1`",
        "the derivation lift of tangent endomorphisms to `Lambda^2`",
        "exterior-power transport `Lambda^2 U`",
        "the curvature operator `R: Lambda^2 -> Lambda^2`",
        "Wedge product belongs to exterior algebra, not to the metric",
        "zero isolated real simple Riemann or Weyl",
        "in all 6,144 registered two-jets",
        "pre-scale versus post-scale variation is the smallest discriminator only",
        "Simultaneity alone does not establish noncircularity",
        "This priority is a recommendation, not authorization",
    )
    for phrase in required:
        require(phrase in text, f"missing correction guard {phrase}")
    forbidden = (
        "COMPLETE_NATIVE_ACTION_DERIVED",
        "GLOBAL_QUOTIENT_SELECTED",
        "NATIVE_CARRIER_EMERGENCE_DERIVED",
        "DENSITY_NATIVE_SELECTOR_DERIVED",
        "GPU work is authorized",
    )
    for phrase in forbidden:
        require(phrase not in text, f"forbidden correction promotion {phrase}")


def validate_ponder(text: str) -> None:
    required = (
        "admissibility is not yet realization",
        "Realization-operator audit — first",
        "Typed metric representation audit — second",
        "Global cocycle and seam audit — third",
        "No follow-on audit is launched by this readout",
    )
    for phrase in required:
        require(phrase in text, f"missing ponder guard {phrase}")


def validate_navigation() -> None:
    required = {
        "LIVE.md": "REFERENCE_CORRECTION_LAYER.md",
        "HANDOFF.md": "PONDER_READOUT.md",
        "INDEX.md": "REFERENCE_CORRECTION_LAYER.md",
        "README.md": "PONDER_READOUT.md",
        "research/README.md": "REFERENCE_CORRECTION_LAYER.md",
        "AGENTS.md": "REFERENCE_CORRECTION_LAYER.md",
    }
    for name, pointer in required.items():
        text = (ROOT / name).read_text(encoding="utf-8")
        require(pointer in text, f"navigation pointer {name}")
    require("FOUR COLD EXTERNAL REVIEWS COMPLETE: 4 PASS-WITH-CAVEATS" in (ROOT / "LIVE.md").read_text(encoding="utf-8"), "LIVE review status")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require("Further repository reorganization is" in readme and "**PAUSED**" in readme, "reorganization pause")


def catches(freeze, reviews, agreement, correction, ponder) -> list[dict[str, str]]:
    observed: list[dict[str, str]] = []

    def exercise(identifier: str, mutation: str, callback) -> None:
        caught = False
        try:
            callback()
        except AssertionError:
            caught = True
        require(caught, f"catch accepted mutation {identifier}")
        observed.append({"catch_id": identifier, "mutation": mutation, "result": "PASS_MUTATION_REJECTED"})

    bad_freeze = deepcopy(freeze); bad_freeze[0]["sha256"] = "0" * 64
    exercise("A01", "corrupt frozen reference input", lambda: validate_freeze(bad_freeze))
    bad_reviews = deepcopy(reviews); bad_reviews[0]["sha256"] = "0" * 64
    exercise("A02", "corrupt raw reviewer evidence", lambda: validate_reviews(bad_reviews))
    exercise("A03", "drop one agreement issue", lambda: validate_agreement(agreement[:-1]))
    duplicate = deepcopy(agreement); duplicate[-1]["issue_id"] = duplicate[0]["issue_id"]
    exercise("A04", "duplicate an agreement identity", lambda: validate_agreement(duplicate))
    exercise("A05", "erase prior curvature-bivector negative", lambda: validate_correction(correction.replace("zero isolated real simple Riemann or Weyl", "unclassified Riemann or Weyl")))
    exercise("A06", "erase orientation/exterior-algebra distinction", lambda: validate_correction(correction.replace("Wedge product belongs to exterior algebra, not to the metric", "The metric supplies wedge product")))
    exercise("A07", "erase Hopf sign qualification", lambda: validate_correction(correction.replace("the conditional bundle has `|c1|=1`", "the conditional bundle has fixed degree")))
    exercise("A08", "promote simultaneous density to automatic closure", lambda: validate_correction(correction.replace("Simultaneity alone does not establish noncircularity", "Simultaneity establishes noncircularity")))
    exercise("A09", "erase realization priority guard", lambda: validate_correction(correction.replace("pre-scale versus post-scale variation is the smallest discriminator only", "pre-scale versus post-scale variation is the smallest discriminator")))
    exercise("A10", "authorize GPU continuation", lambda: validate_correction(correction + "\nGPU work is authorized\n"))
    exercise("A11", "erase lay stop boundary", lambda: validate_ponder(ponder.replace("No follow-on audit is launched by this readout", "The next audit launches automatically")))
    return observed


def main() -> None:
    freeze = rows("REFERENCE_FREEZE_MANIFEST.tsv")
    reviews = rows("REVIEW_EVIDENCE_MANIFEST.tsv")
    agreement = rows("REVIEW_AGREEMENT_DISAGREEMENT.tsv")
    correction = (HERE / "REFERENCE_CORRECTION_LAYER.md").read_text(encoding="utf-8")
    ponder = (HERE / "PONDER_READOUT.md").read_text(encoding="utf-8")
    validate_freeze(freeze)
    validate_reviews(reviews)
    validate_agreement(agreement)
    validate_correction(correction)
    validate_ponder(ponder)
    validate_navigation()
    catch_rows = catches(freeze, reviews, agreement, correction, ponder)
    with (HERE / "ADJUDICATION_CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catch_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catch_rows)
    result = {
        "schema": "udt-metric-to-frontier-external-adjudication-1.0",
        "status": "PASS_WITH_APPEND_ONLY_QUALIFICATIONS",
        "frozen_reference_commit": "1a41c4b",
        "reference_freeze_manifest_sha256": digest(HERE / "REFERENCE_FREEZE_MANIFEST.tsv"),
        "review_verdict_census": {"PASS-WITH-CAVEATS": 4},
        "review_evidence_files": len(reviews),
        "agreement_rows": len(agreement),
        "catch_proofs": len(catch_rows),
        "frozen_claim_status_changes": 0,
        "new_physics_claims": 0,
        "ranked_first_question": "REGISTERED_BOOTSTRAP_REALIZATION_OPERATOR_AUDIT",
        "maximum_conclusion": "EXTERNALLY_AUDITED_REFERENCE_WITH_APPEND_ONLY_QUALIFICATIONS_AND_RANKED_NEXT_QUESTIONS",
    }
    (HERE / "ADJUDICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
