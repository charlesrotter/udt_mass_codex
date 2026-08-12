#!/usr/bin/env python3
"""Verify the G82 external review, chronology, and bounded numerical claims."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REVIEW_BASE = "a9cffc66794707eb68042e372bdb47b1a182de63"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def git(*args: str, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=text, check=False,
    )


def main() -> None:
    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    assert result["status"] == "VERIFIED_WITH_CAVEATS"
    assert result["scientific_corrections"] == 0
    assert len(result["binding_caveats"]) == 4
    assert digest(HERE / "REVIEW_MANIFEST.tsv") == result["sealed_manifest_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == result["raw_review_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == result["review_transcript_sha256"]

    manifest = rows(HERE / "REVIEW_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 26
    live_rows = historical_rows = 0
    for row in manifest:
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            shown = git("show", f"{REVIEW_BASE}:{row['path']}")
            assert shown.returncode == 0 and digest_bytes(shown.stdout) == row["sha256"]
            historical_rows += 1
        else:
            assert digest(ROOT / row["path"]) == row["sha256"]
            live_rows += 1
    assert live_rows == 25 and historical_rows == 1

    base = result["preregistration_base"]
    prereg_commit = result["preregistration_commit"]
    ancestry = git("merge-base", "--is-ancestor", base, prereg_commit)
    assert ancestry.returncode == 0
    parent = git("rev-parse", f"{prereg_commit}^")
    assert parent.returncode == 0 and parent.stdout.decode().strip() == base
    subject = git("show", "-s", "--format=%s", prereg_commit, text=True)
    assert subject.returncode == 0 and subject.stdout.strip() == "Preregister fixed-C1 Radau covariance replay"
    prereg_at_commit = git("show", f"{prereg_commit}:{HERE.name}/PREREGISTRATION.md")
    assert prereg_at_commit.returncode == 0
    assert digest_bytes(prereg_at_commit.stdout) == digest(HERE / "PREREGISTRATION.md")

    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    control = saved["control"]
    checks = {
        "radau_vs_dop853_max_relative": max(saved["radau_vs_dop853_matrix_relative"].values()),
        "max_coarse_fine_relative": saved["coarse_fine_max_relative"],
        "unrotated_reciprocity_residual": control["independent_unrotated_reciprocity_relative"],
        "rotated_covariance_residual": control["independent_rotated_covariance_relative"],
        "area_reciprocity_residual": control["independent_area_ratio_minus_Z"],
    }
    for name, value in checks.items():
        assert math.isclose(value, result[name], rel_tol=1e-15, abs_tol=1e-20), name
        assert value < 2e-4

    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    combined = raw + adjudication
    for token in (
        "VERIFIED_WITH_CAVEATS",
        "26/26",
        "G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY",
        "DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS",
        "not catch-complete",
        "not a literal packaged CLI rerun",
        "No physical profile, endpoint, scale",
    ):
        assert token in combined

    output = {
        "schema": "udt-cmb-g82-external-adjudication-verification-v1",
        "status": "PASS",
        "scientific_corrections": 0,
        "binding_caveats": 4,
        "sealed_intake_files": 27,
        "sealed_payload_rows": 26,
        "live_payload_hashes_verified": live_rows,
        "mutable_registry_row_verified_at_review_base": historical_rows,
        "preregistration_base": base,
        "preregistration_commit": prereg_commit,
        "chronology_verified": True,
        "load_bearing_numbers_reproduced": len(checks),
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
