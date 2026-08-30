#!/usr/bin/env python3
"""Build a sealed self-contained G303 adversarial-review intake."""

from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.metadata
import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PACKAGE = ROOT.name
SITE_PACKAGES = Path("/home/udt-admin/.local/lib/python3.10/site-packages")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def add_runtime_dependencies(intake: Path) -> None:
    runtime = intake / "review_runtime"
    runtime.mkdir()
    members = [SITE_PACKAGES / "sympy", SITE_PACKAGES / "mpmath"]
    for pattern in ("sympy-*.dist-info", "mpmath-*.dist-info"):
        members.extend(sorted(SITE_PACKAGES.glob(pattern)))
    assert all(path.exists() for path in members), members

    archive = runtime / "python_deps.tar.gz"
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as bundle:
                def normalized(info: tarfile.TarInfo):
                    parts = Path(info.name).parts
                    if "__pycache__" in parts or info.name.endswith((".pyc", ".pyo")):
                        return None
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mtime = 0
                    return info

                for member in members:
                    bundle.add(member, arcname=member.name, filter=normalized)

    metadata = {
        "purpose": "sealed review-only runtime for registered G303 replays",
        "sympy_version": importlib.metadata.version("sympy"),
        "mpmath_version": importlib.metadata.version("mpmath"),
        "archive_sha256": digest(archive),
        "network_or_install_required": False,
    }
    (runtime / "RUNTIME_DEPENDENCIES.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g303_review_", dir="/tmp"))
    package_target = intake / PACKAGE
    package_target.mkdir()

    package_files = sorted(path for path in ROOT.iterdir() if path.is_file())
    for source in package_files:
        if source.name == "build_review_intake.py" or source.name.startswith("launch_external"):
            continue
        shutil.copy2(source, package_target / source.name)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for row in sources:
        source = REPO / row["path"]
        target = intake / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    add_runtime_dependencies(intake)

    git_state = subprocess.run(
        ["git", "show", "--stat", "--oneline", "--decorate", "42e31303"],
        cwd=REPO, check=True, text=True, capture_output=True,
    ).stdout
    (intake / "PREREGISTRATION_GIT_PROOF.txt").write_text(git_state, encoding="utf-8")

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    manifest_lines = ["path\tsha256\tbytes"]
    for path in payloads:
        relative = path.relative_to(intake).as_posix()
        manifest_lines.append(f"{relative}\t{digest(path)}\t{path.stat().st_size}")
    manifest = intake / "REVIEW_MANIFEST.tsv"
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    scope = {
        "package": PACKAGE,
        "purpose": "fresh read-only adversarial review of bounded G303 landing",
        # REVIEW_SCOPE itself is added immediately below and is also a manifest payload.
        "payload_count_excluding_manifest_and_seal": len(payloads) + 1,
        "allowed": ["inspect intake", "bounded replay in writable ephemeral copy"],
        "forbidden": [
            "edit evidence", "continue research", "access repository outside intake",
            "access protected packages", "use internet", "select UDT law or history",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Rebuild manifest so REVIEW_SCOPE is sealed as a payload.
    payloads = sorted(
        path for path in intake.rglob("*")
        if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    )
    manifest_lines = ["path\tsha256\tbytes"]
    for path in payloads:
        relative = path.relative_to(intake).as_posix()
        manifest_lines.append(f"{relative}\t{digest(path)}\t{path.stat().st_size}")
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    print(intake)
    print(f"payloads={len(payloads)}")
    print(f"scope_sha256={digest(scope_path)}")
    print(f"manifest_sha256={digest(manifest)}")
    print(f"seal_sha256={digest(seal)}")


if __name__ == "__main__":
    main()
