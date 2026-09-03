#!/usr/bin/env python3
"""Build a sealed dependency-free G337 fresh-review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PREREG_COMMIT = "96135e03"
PACKAGE_FILES = (
    "MAP.md", "EXPLORATORY_MAP_NOTE.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv",
    "COMPLETENESS_MAP.md", "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "EXECUTION_NOTE.md",
    "derive_double_silent_third_response.py",
    "verify_double_silent_third_response_independent.py", "run_catch_proofs.py",
    "verify_package.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION_RESULT.json", "EXACT_DERIVATION.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "AUDIT_REPORT.md", "EVIDENCE_GATES.md",
    "COMMANDS.md", "RUN_RECORD.md", "build_review_intake.py", "verify_review_intake.py",
    "EXTERNAL_REVIEW_REQUEST.md",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_source(relative: Path, size: int, expected: str) -> bytes:
    candidate = (ROOT / relative).resolve()
    if not candidate.is_relative_to(ROOT.resolve()):
        raise SystemExit(f"source escaped repository: {relative}")
    payload = candidate.read_bytes() if candidate.is_file() else b""
    if len(payload) == size and hashlib.sha256(payload).hexdigest() == expected:
        return payload
    replay = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{relative.as_posix()}"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if replay.returncode or len(replay.stdout) != size:
        raise SystemExit(f"frozen source unavailable: {relative}")
    if hashlib.sha256(replay.stdout).hexdigest() != expected:
        raise SystemExit(f"frozen source mismatch: {relative}")
    return replay.stdout


def main() -> None:
    rows = list(csv.DictReader(
        (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"
    ))
    intake = Path(tempfile.mkdtemp(prefix="udt_g337_review_", dir="/tmp"))
    package_out, source_out = intake / "package", intake / "sources"
    package_out.mkdir()
    source_out.mkdir()
    copied: list[Path] = []
    for filename in PACKAGE_FILES:
        source = PACKAGE / filename
        if not source.is_file():
            raise SystemExit(f"missing package file: {filename}")
        target = package_out / filename
        shutil.copy2(source, target)
        copied.append(target)
    for row in rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"unsafe source: {relative}")
        target = source_out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(frozen_source(relative, int(row["bytes"]), row["sha256"]))
        copied.append(target)
    scope = {
        "review": "fresh read-only adversarial G337 review",
        "allowed": [
            "inspect only this sealed intake",
            "independently rederive the bounded initial third-jet ownership result",
            "run registered checks in a writable ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files", "continue the research", "access repository or protected packages",
            "use internet or unsealed observations", "import action source matter mass fit scale Xmax",
            "select topology physical germs initial data history occupancy or canon",
            "promote an initial third jet into explicit evolution persistence stability or viability",
        ],
        "allowed_verdicts": [
            "ACCEPT__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED",
            "ACCEPT_WITH_REPAIRS__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED",
            "REFUTE__G337_BOUNDED_THIRD_JET_OWNERSHIP",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    copied.append(scope_path)
    manifest_lines = ["sha256\tbytes\tpath"]
    for path in sorted(copied, key=lambda item: item.relative_to(intake).as_posix()):
        manifest_lines.append(
            f"{digest(path)}\t{path.stat().st_size}\t{path.relative_to(intake).as_posix()}"
        )
    manifest = intake / "REVIEW_MANIFEST.tsv"
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake), "file_count": len(copied) + 2,
        "payload_count": len(copied), "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest), "seal_sha256": digest(seal),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
