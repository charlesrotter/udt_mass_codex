#!/usr/bin/env python3
"""Build a sealed exact-file G346 adversarial-review intake under /tmp."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SOURCE_COMMIT = "bb3676d5"
PREREGISTRATION_COMMIT = "9a037558"

PACKAGE_FILES = (
    "MAP.md",
    "PREREGISTRATION.md",
    "PREREGISTRATION_EXECUTION_NOTE.md",
    "PREMISE_LEDGER.tsv",
    "COMPLETENESS_MAP.md",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "AUDIT_REPORT.md",
    "RUN_RECORD.md",
    "COMMANDS.md",
    "SOURCE_SCOPE.tsv",
    "derive_directional_angular_area.py",
    "verify_directional_angular_area_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "ADVERSARIAL_REVIEW_REQUEST.md",
)

SOURCE_HASHES = {
    "udt_g340_finite_separated_normal_observer_relations_2026-09-03/EXACT_DERIVATION.md":
        "1c8998906a354b26d18dd2fd307564b158d74bdd52c865daa6b0f0300378740f",
    "udt_g342_full_null_jacobi_beam_area_2026-09-04/EXACT_DERIVATION.md":
        "3906be2e481e04d705715743ce1f73b9ba323742cf9a6cdac57daa3e7e4df9d6",
    "udt_g343_bilocal_screen_phase_space_propagator_2026-09-04/EXACT_DERIVATION.md":
        "b295455e2835e3a04de7e91dbafb61ba0b0cef0f1eaea338c90cfe8a1cab5051",
    "udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md":
        "8af5dd5dfdb259bcafd184155664792c9f6f027428202e3e69039735a604687a",
    "udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md":
        "e59887e92b055cc18a8215ae6acbbf88528d1371b2afcc03371935c574079722",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_show_bytes(commit: str, relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"cannot read {relative} at {commit}")
    return result.stdout


def frozen_source(relative: str, expected: str) -> bytes:
    current = ROOT / relative
    if current.is_file() and hashlib.sha256(current.read_bytes()).hexdigest() == expected:
        return current.read_bytes()
    content = git_show_bytes(SOURCE_COMMIT, relative)
    if hashlib.sha256(content).hexdigest() != expected:
        raise RuntimeError(f"cannot authenticate frozen source: {relative}")
    return content


def commit_proof(commit: str) -> bytes:
    result = subprocess.run(
        ["git", "show", "--format=fuller", "--stat", "--patch", commit],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"cannot authenticate commit: {commit}")
    return result.stdout


def main():
    destination = Path(tempfile.mkdtemp(prefix="udt_g346_review_", dir="/tmp"))
    payload = []
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / "g346" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payload.append(target)

    for relative, expected in SOURCE_HASHES.items():
        target = destination / "sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(frozen_source(relative, expected))
        payload.append(target)

    proof = destination / "GIT_PREREGISTRATION_PROOF.txt"
    proof.write_bytes(commit_proof(PREREGISTRATION_COMMIT))
    payload.append(proof)

    scope = {
        "task": "fresh read-only adversarial review of bounded G346 directional angular-area reciprocity",
        "intake_only": True,
        "may_run": "registered checks in a writable ephemeral copy",
        "must_not": [
            "edit evidence files",
            "continue the research",
            "access the repository or protected packages",
            "use internet or unsealed observations",
            "import optical reciprocity, electromagnetic/light transfer, luminosity, source/detector physics, probability, matter, fit, or observation",
            "select or canonize brightness, flux, a physical distance, route/population, spacetime, topology, stability result, scale, X_max, or universe",
        ],
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "payload_count_excluding_manifest_and_detached_seal": len(payload) + 1,
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payload.append(scope_path)

    manifest_path = destination / "REVIEW_MANIFEST.tsv"
    lines = ["sha256\tbytes\tpath"]
    for path in sorted(payload, key=lambda item: item.relative_to(destination).as_posix()):
        relative = path.relative_to(destination).as_posix()
        lines.append(f"{sha256(path)}\t{path.stat().st_size}\t{relative}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    seal_path = destination / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{sha256(manifest_path)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(json.dumps({
        "detached_seal_sha256": sha256(seal_path),
        "intake": str(destination),
        "manifest_payloads": len(payload),
        "review_manifest_sha256": sha256(manifest_path),
        "review_scope_sha256": sha256(scope_path),
        "total_files": len(payload) + 2,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
