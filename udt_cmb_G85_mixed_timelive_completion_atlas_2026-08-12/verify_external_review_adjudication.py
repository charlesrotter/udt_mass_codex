#!/usr/bin/env python3
"""Verify the G85 sealed external review, chronology, and bounded adjudication."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def git(*args: str, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=text, check=False)


def main() -> None:
    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    assert result["status"] == "VERIFIED_WITH_CAVEATS"
    assert result["scientific_corrections"] == 0
    assert len(result["binding_caveats"]) == 4
    assert result["maximum_conclusion"] == (
        "BOUNDED_KINEMATIC_TIME_LIVE_COMPLETION_ARCHETYPE_ATLAS_ON_THE_G84_CANDIDATE"
    )
    assert digest(HERE / "REVIEW_MANIFEST.tsv") == result["sealed_manifest_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == result["banked_raw_review_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == result["banked_review_transcript_sha256"]

    manifest = rows(HERE / "REVIEW_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 36
    for row in manifest:
        assert digest(ROOT / row["path"]) == row["sha256"], row["path"]

    preregistration = result["preregistration_commit"]
    calculation = result["calculation_commit"]
    parent = git("rev-parse", f"{calculation}^")
    assert parent.returncode == 0 and parent.stdout.decode().strip() == preregistration
    assert git("merge-base", "--is-ancestor", preregistration, calculation).returncode == 0
    assert git("show", "-s", "--format=%s", preregistration, text=True).stdout.strip() == (
        "Preregister G85 mixed time-live completion atlas"
    )
    assert git("show", "-s", "--format=%s", calculation, text=True).stdout.strip() == (
        "Bank G85 mixed time-live completion atlas"
    )

    source = rows(ROOT / "udt_cmb_G84_am_global_completion_pair_diameter_audit_2026-08-12/PROFILE_COMPLETION_ATLAS.tsv")
    source_behaviors = {
        row["profile_id"]: row["behavior_class"]
        for row in rows(ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv")
        if row["lapse_name"] == "AM"
    }
    assert len(source) == len({row["profile_id"] for row in source}) == 197
    q4 = {row["profile_id"]: Fraction(row["q_at_s_4_exact"]) for row in source}
    signs = Counter("zero" if value == 0 else "positive" if value > 0 else "negative" for value in q4.values())
    assert signs == Counter({"positive": 104, "negative": 92, "zero": 1})
    mixed_ids = {profile_id for profile_id, value in q4.items() if value != 0}
    assert len(mixed_ids) == 196
    behaviors = Counter(source_behaviors[profile_id] for profile_id in mixed_ids)
    assert behaviors == Counter(
        {
            "CENTER_OFF_NO_INTERIOR_ROOT": 24,
            "ENDPOINT_TAPER_NO_INTERIOR_ROOT": 20,
            "INTERIOR_SIGN_CHANGE": 36,
            "PERSISTENT_SIGN_NO_INTERIOR_ROOT": 112,
            "ZERO_BOTH_BOUNDARIES_NO_INTERIOR_ROOT": 4,
        }
    )

    atlas = rows(HERE / "PROFILE_ARCHETYPE_ATLAS.tsv")
    pairs = {(row["profile_id"], row["archetype_id"]) for row in atlas}
    assert len(atlas) == len(pairs) == 980
    assert {row["profile_id"] for row in atlas} == mixed_ids
    classifications = Counter(row["classification"] for row in atlas)
    assert classifications == Counter(result["external_classification_counts"])

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    for key in (
        "physical_profile_selected",
        "physical_topology_selected",
        "physical_Xmax_selected",
        "native_dynamics_selected",
    ):
        assert derivation[key] is False

    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    combined = raw + adjudication
    for token in (
        "VERIFIED_WITH_CAVEATS",
        "36/36",
        "4u_H-b_H^2<0",
        "104",
        "92",
        "980",
        "geodesic completeness",
        "NO_NATIVE_HISTORY_SELECTED",
        "BOUNDED_KINEMATIC_TIME_LIVE_COMPLETION_ARCHETYPE_ATLAS_ON_THE_G84_CANDIDATE",
    ):
        assert token in combined, token

    output = {
        "schema": "udt-cmb-g85-external-adjudication-verification-v1",
        "status": "PASS",
        "scientific_corrections": 0,
        "binding_caveats": len(result["binding_caveats"]),
        "sealed_intake_files": result["sealed_intake_files"],
        "sealed_payload_rows": len(manifest),
        "payload_hashes_verified_live": len(manifest),
        "preregistration_commit": preregistration,
        "calculation_commit": calculation,
        "chronology_verified": True,
        "total_am_rows": len(source),
        "mixed_profile_rows": len(mixed_ids),
        "profile_archetype_rows": len(atlas),
        "unique_profile_archetype_rows": len(pairs),
        "positive_q4_rows": signs["positive"],
        "negative_q4_rows": signs["negative"],
        "zero_q4_rows": signs["zero"],
        "behavior_counts": dict(sorted(behaviors.items())),
        "classification_counts": dict(sorted(classifications.items())),
        "physical_promotions": 0,
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
