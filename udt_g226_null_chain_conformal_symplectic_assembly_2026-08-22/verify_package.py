#!/usr/bin/env python3
"""Bounded aggregate verifier for G226 with no-persistent-output replay.

This verifier checks enumerated evidence, exact component replay equality, frozen source hashes,
selected scope tokens, and evidence-byte nonmutation.  It is not a general semantic proof of every
narrative sentence in the package.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.resolve()
SOURCE_ROOT = (REPO / "frozen_sources").resolve() if (REPO / "frozen_sources").is_dir() else REPO
LANDING = "CONFORMAL_SYMPLECTIC_NULL_CHAIN_INTERLOCK_DERIVED_CONDITIONALLY"
REQUIRED = (
    "MAP.md",
    "OBSERVATION.md",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_null_chain_conformal_symplectic.py",
    "verify_null_chain_conformal_symplectic_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "CONTROL_ATLAS.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "FRESH_ADVERSARIAL_REVIEW.md",
    "REPAIR_PREREGISTRATION.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "build_review_intake.py",
    "verify_package.py",
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def load_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def validate_payloads(production: dict, independent: dict, catch: dict, final: dict) -> None:
    require(production["landing"] == LANDING, "production landing")
    require(production["alternative"] == "B_CONFORMAL_SYMPLECTIC_INTERLOCK", "frozen alternative")
    require(production["symbolic_checks"] == 28, "symbolic count")
    require(production["chain_multiplier"] == "21/55", "chain multiplier")
    require(production["vertical_coefficients"] == ["5/3", "11/7"], "vertical inverse")
    require(production["caustic_position_det"] == "0", "caustic position")
    require(production["caustic_full_phase_det"] == "1", "caustic phase")

    require(independent["status"] == "PASS", "independent status")
    require(independent["implementation"] == "independent_standard_library_fraction", "independent implementation")
    require(independent["seed"] == 226822, "independent seed")
    require(independent["cases"] == 20000, "independent cases")
    require(independent["assertions"] == 200007, "independent assertions")
    require(independent["noncommuting_cases"] == 20000, "noncommuting count")

    require(catch["status"] == "PASS", "catch status")
    require(catch["mutation_catches"] == 8, "catch count")
    require(all(catch["catches"].values()), "uncaught mutation")

    require(final["landing"] == LANDING, "final landing")
    require(final["preregistration_commit"] == "1f60deb0", "preregistration commit")
    require(final["source_count"] == 13, "source count")
    require(final["symbolic_checks"] == 28, "final symbolic count")
    require(final["independent_cases"] == 20000, "final cases")
    require(final["exact_fraction_assertions"] == 200007, "final assertions")
    require(final["mutation_catches"] == 8, "final catches")
    require(final["full_phase_object"] is True, "full phase")
    require(final["clock_ratio_is_conformal_multiplier"] is True, "clock multiplier")
    require(final["vertical_q_is_inverse_multiplier"] is True, "vertical inverse")
    require(final["middle_screen_gauge_covariance"] is True, "middle gauge")
    require(final["affine_generator_covariance"] is True, "affine covariance")
    require(final["caustic_position_block_inverted"] is False, "position inverse")
    require(final["caustic_full_phase_invertible"] is True, "phase invertibility")
    require(final["G225_holonomy_retained_as_matrix"] is True, "matrix holonomy")
    require(final["G225_pointwise_map_promoted_to_physical_transport"] is False, "physical transport promotion")
    require(final["independent_direct_relation_constrained"] is False, "direct relation")
    require(final["universal_null_protocol_selected"] is False, "protocol")
    require(final["physical_history_selected"] is False, "history")
    require(final["read_only_replay"] is True, "read-only replay")
    require(final["manifest_path_containment"] is True, "manifest containment")


def manifest_rows() -> list[dict[str, str]]:
    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_manifest() -> list[Path]:
    rows = manifest_rows()
    require(len(rows) == 13, "manifest source count")
    paths: list[Path] = []
    for row in rows:
        candidate = (SOURCE_ROOT / row["path"]).resolve()
        require(candidate.is_relative_to(SOURCE_ROOT), "manifest path escape")
        require(candidate.is_file(), f"missing source: {row['path']}")
        require(hashlib.sha256(candidate.read_bytes()).hexdigest() == row["sha256"], f"source drift: {row['path']}")
        paths.append(candidate)
    return paths


def tree_hashes(source_paths: list[Path]) -> dict[str, str]:
    paths = [path for path in ROOT.rglob("*") if path.is_file()]
    paths.extend(source_paths)
    return {
        str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(set(paths), key=lambda item: str(item))
    }


def replay(script: str, timeout: int) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script), "--output", "/dev/null"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return json.loads(completed.stdout)


def main() -> None:
    for name in REQUIRED:
        require((ROOT / name).is_file(), f"missing package evidence: {name}")

    sources = validate_manifest()
    production = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_VERIFICATION.json")
    catch = load_json("CATCH_PROOF_RESULT.json")
    final = load_json("VERIFICATION_RESULT.json")
    validate_payloads(production, independent, catch, final)

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    prereg = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in ("CSp^+(4,R)", "r_e^{-1}", "caustic", "G225", "independently supplied direct"):
        require(token in exact, f"exact derivation lacks {token}")
    require(LANDING in audit, "audit landing")
    require("No alternative may be added" in prereg, "frozen alternatives")

    before = tree_hashes(sources)
    require(replay("derive_null_chain_conformal_symplectic.py", 60) == production, "production replay drift")
    require(replay("verify_null_chain_conformal_symplectic_independent.py", 240) == independent, "independent replay drift")
    require(replay("run_catch_proofs.py", 60) == catch, "catch replay drift")
    after = tree_hashes(sources)
    require(after == before, "replay wrote package or source bytes")

    print(
        "PASS: G226 package; 13 sources; 28 symbolic checks; 20,000 independent chains; "
        "200,007 exact-Fraction assertions; 20,000 noncommuting products; 8 mutation catches; "
        "/dev/null no-persistent-output replay"
    )


if __name__ == "__main__":
    main()
