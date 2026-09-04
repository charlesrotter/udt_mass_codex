#!/usr/bin/env python3
"""Build a sealed exact-file G344 adversarial-review intake under /tmp."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SOURCE_COMMIT = "50c3da8d"
PREREGISTRATION_COMMIT = "5c16ca60"
QUALIFICATION_COMMIT = "9701e595"

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
    "derive_endpoint_generator.py",
    "verify_endpoint_generator_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "ADVERSARIAL_REVIEW_REQUEST.md",
)


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


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g344_review_", dir="/tmp"))
    payload: list[Path] = []
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / "g344" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payload.append(target)

    rows = (PACKAGE / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for row in rows:
        if not row.strip():
            continue
        columns = row.split("\t")
        relative, expected = columns[0], columns[1]
        if expected == "NA_METHOD":
            continue
        target = destination / "sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(frozen_source(relative, expected))
        payload.append(target)

    for name, commit in (
        ("GIT_PREREGISTRATION_PROOF.txt", PREREGISTRATION_COMMIT),
        ("GIT_QUALIFICATION_PROOF.txt", QUALIFICATION_COMMIT),
    ):
        target = destination / name
        target.write_bytes(commit_proof(commit))
        payload.append(target)

    scope = {
        "task": "fresh read-only adversarial review of bounded G344 screen endpoint generator and determinant bidensity",
        "intake_only": True,
        "may_run": "registered checks in a writable ephemeral copy",
        "must_not": [
            "edit evidence files",
            "continue the research",
            "access the repository or protected packages",
            "use internet or unsealed observations",
            "import electromagnetic/light transfer, luminosity, source/detector physics, matter, fit, or observation",
            "select or canonize a spacetime action, amplitude, physical route/population, distance protocol, topology, stability, scale, X_max, or universe",
        ],
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "qualification_commit": QUALIFICATION_COMMIT,
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
