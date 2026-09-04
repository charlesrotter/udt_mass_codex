#!/usr/bin/env python3
"""Build a sealed exact-file G342 adversarial-review intake under /tmp."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
PREREGISTRATION_COMMIT = "b8d56fdd"

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
    "derive_full_null_jacobi.py",
    "verify_full_null_jacobi_independent.py",
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


def frozen_source(relative: str, expected: str) -> bytes:
    current = ROOT / relative
    if current.is_file() and hashlib.sha256(current.read_bytes()).hexdigest() == expected:
        return current.read_bytes()
    result = subprocess.run(
        ["git", "show", f"{PREREGISTRATION_COMMIT}:{relative}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or hashlib.sha256(result.stdout).hexdigest() != expected:
        raise RuntimeError(f"cannot authenticate frozen source: {relative}")
    return result.stdout


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g342_review_", dir="/tmp"))
    payload: list[Path] = []
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / "g342" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payload.append(target)

    rows = (PACKAGE / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for row in rows:
        if not row.strip():
            continue
        relative, expected, _role = row.split("\t")
        target = destination / "sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(frozen_source(relative, expected))
        payload.append(target)

    scope = {
        "task": "fresh read-only adversarial review of bounded G342 full null Jacobi and beam-area geometry",
        "intake_only": True,
        "may_run": "registered checks in a writable ephemeral copy",
        "must_not": [
            "edit evidence files",
            "continue the research",
            "access the repository or protected packages",
            "use internet or unsealed observations",
            "import electromagnetic/light transfer, luminosity, a source, detector, matter model, fit, or observation",
            "select or canonize a physical route, population, distance protocol, topology, stability, scale, X_max, or spacetime",
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
