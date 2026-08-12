#!/usr/bin/env python3
"""Verify the G83 external review, chronology, and bounded evidence claims."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


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


def close(actual: float, expected: float) -> None:
    assert math.isclose(actual, expected, rel_tol=2e-14, abs_tol=1e-20), (actual, expected)


def main() -> None:
    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    assert result["status"] == "VERIFIED_WITH_CAVEATS"
    assert result["scientific_corrections"] == 0
    assert len(result["binding_caveats"]) == 4
    assert result["maximum_conclusion"] == "BOUNDED_STATIONARY_ENDPOINT_ASYMPTOTE_CANDIDATE_ATLAS"
    assert digest(HERE / "REVIEW_MANIFEST.tsv") == result["sealed_manifest_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == result["raw_review_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == result["review_transcript_sha256"]

    manifest = rows(HERE / "REVIEW_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 40
    for row in manifest:
        assert digest(ROOT / row["path"]) == row["sha256"], row["path"]

    prereg = result["preregistration_commit"]
    calculation = result["calculation_commit"]
    parent = git("rev-parse", f"{calculation}^")
    assert parent.returncode == 0 and parent.stdout.decode().strip() == prereg
    ancestry = git("merge-base", "--is-ancestor", prereg, calculation)
    assert ancestry.returncode == 0
    prereg_subject = git("show", "-s", "--format=%s", prereg, text=True)
    calculation_subject = git("show", "-s", "--format=%s", calculation, text=True)
    assert prereg_subject.stdout.strip() == "Preregister G83 endpoint asymptote atlas"
    assert calculation_subject.stdout.strip() == "Bank G83 stationary endpoint asymptote atlas"
    prereg_at_commit = git("show", f"{prereg}:{HERE.name}/PREREGISTRATION.md")
    assert prereg_at_commit.returncode == 0
    assert digest_bytes(prereg_at_commit.stdout) == digest(HERE / "PREREGISTRATION.md")

    strict = rows(HERE / "STRICT_DOMAIN_ATLAS.tsv")
    paths = rows(HERE / "CONTINUED_PATH_ATLAS.tsv")
    assert len(strict) == len({row["profile_id"] for row in strict}) == result["strict_rows"] == 591
    assert all(row["finite_positive_lapse"] == "true" for row in strict)
    assert all(math.isfinite(float(row["phi_receiver_to_x_1"])) for row in strict)
    assert len(paths) == result["path_rows"] == 591
    assert len({row["profile_id"] for row in paths}) == result["am_profiles"] == 197
    assert len({(row["profile_id"], row["approach_power"]) for row in paths}) == 591

    counts = Counter(row["status"] for row in paths)
    assert dict(sorted(counts.items())) == result["status_counts"]
    by_profile: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in paths:
        by_profile[row["profile_id"]].append(row)
    patterns = Counter(
        "|".join(row["status"] for row in sorted(group, key=lambda item: int(item["approach_power"])))
        for group in by_profile.values()
    )
    assert dict(sorted(patterns.items())) == result["approach_pattern_counts"]

    reached = [row for row in paths if row["endpoint_reached"].lower() == "true"]
    certified = [row for row in reached if row["numerically_certified"].lower() == "true"]
    assert len(reached) == len(certified) == result["certified_reached_rows"] == 516
    for field, expected in result["residual_maxima"].items():
        close(max(float(row[field]) for row in reached), expected)

    radau = rows(HERE / "INDEPENDENT_RADAU_REPLAY.tsv")
    assert len(radau) == result["radau_rows"] == 18
    assert sum(row["passed"] == "True" for row in radau) == result["radau_passed"] == 18
    close(max(float(row["affine_absolute_difference"]) for row in radau), result["radau_max_affine_difference"])
    close(max(float(row["det_D_absolute_difference"]) for row in radau), result["radau_max_screen_determinant_difference"])

    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert independent["all_passed"] and independent["strict_rows"] == 591
    assert independent["exact_scalar_checks"]["phi_limit"] == "POSITIVE_INFINITY"
    assert independent["exact_scalar_checks"]["c_eff_ratio_limit"] == "ZERO"
    assert independent["exact_scalar_checks"]["receiver_dependent"] is True
    assert catches["all_passed"] and catches["count"] == result["hostile_catches_passed"] == 8

    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    combined = raw + adjudication
    for token in (
        "VERIFIED_WITH_CAVEATS",
        "BOUNDED_STATIONARY_ENDPOINT_ASYMPTOTE_CANDIDATE_ATLAS",
        "40/40",
        "shares the G68/G83 geometry implementation",
        "not the physical frame-shared",
        "No physical profile, scale `R`, source surface",
    ):
        assert token in combined, token

    output = {
        "schema": "udt-cmb-g83-external-adjudication-verification-v1",
        "status": "PASS",
        "scientific_corrections": 0,
        "binding_caveats": len(result["binding_caveats"]),
        "sealed_intake_files": result["sealed_intake_files"],
        "sealed_payload_rows": len(manifest),
        "payload_hashes_verified_live": len(manifest),
        "preregistration_commit": prereg,
        "calculation_commit": calculation,
        "chronology_verified": True,
        "strict_rows": len(strict),
        "path_rows": len(paths),
        "certified_reached_rows": len(certified),
        "radau_rows": len(radau),
        "hostile_catches_passed": catches["count"],
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
