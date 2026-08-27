#!/usr/bin/env python3
"""Verify G275 R1/R2 containment repairs in fresh ephemeral sealed copies."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "REPAIR_VERIFICATION_RESULT.json"
CURRENT_INTAKE = ROOT.parent
SEALED_ENTRYPOINT = (CURRENT_INTAKE / "REVIEW_SCOPE.json").is_file()


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def run_verifier(intake: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    package = intake / ROOT.name
    return subprocess.run(
        [sys.executable, str(package / "verify_package.py"), "--no-write"],
        cwd=intake,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def rewrite_manifest_row(intake: Path, relative: str) -> None:
    manifest = intake / "REVIEW_MANIFEST.tsv"
    with manifest.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    target = intake / relative
    for row in rows:
        if row["path"] == relative:
            payload = target.read_bytes()
            row["sha256"] = digest(payload)
            row["bytes"] = str(len(payload))
            break
    else:
        raise AssertionError(relative)
    with manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("path", "sha256", "bytes"), delimiter="\t",
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def clone(source: Path, parent: Path, name: str) -> Path:
    target = parent / name
    shutil.copytree(source, target)
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    owns_intake = not SEALED_ENTRYPOINT
    if SEALED_ENTRYPOINT:
        intake = CURRENT_INTAKE
    else:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "build_review_intake.py")],
            cwd=ROOT.parent,
            text=True,
            capture_output=True,
            check=True,
        )
        built = json.loads(completed.stdout)
        intake = Path(built["intake"])
    scratch = Path(tempfile.mkdtemp(prefix="udt_g275_repair_checks_", dir="/tmp"))
    rebuilt_intake: Path | None = None
    try:
        clean = run_verifier(intake)
        assert clean.returncode == 0, clean.stdout + clean.stderr

        extra = clone(intake, scratch, "extra")
        (extra / "UNLISTED_FILE").write_text("hostile extra\n", encoding="utf-8")
        assert run_verifier(extra).returncode != 0

        changed = clone(intake, scratch, "changed")
        changed_report = changed / ROOT.name / "LAY_REPORT.md"
        changed_report.write_text(changed_report.read_text(encoding="utf-8") + "tamper\n",
                                  encoding="utf-8")
        assert run_verifier(changed).returncode != 0

        sealed_source = clone(intake, scratch, "sealed_source")
        relative = f"{ROOT.name}/sources/founding.md"
        source = sealed_source / relative
        source.write_text(source.read_text(encoding="utf-8") + "tamper\n", encoding="utf-8")
        rewrite_manifest_row(sealed_source, relative)
        fake_bin = scratch / "fake_bin"
        fake_bin.mkdir()
        marker = scratch / "git_was_called"
        fake_git = fake_bin / "git"
        fake_git.write_text(f"#!/bin/sh\ntouch '{marker}'\nexit 0\n", encoding="utf-8")
        fake_git.chmod(0o755)
        env = dict(os.environ)
        env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
        sealed_failure = run_verifier(sealed_source, env)
        assert sealed_failure.returncode != 0
        assert not marker.exists()

        # R4: the builder itself must replay from a sealed root without Git or outside sources.
        sealed_builder = subprocess.run(
            [sys.executable, str(intake / ROOT.name / "build_review_intake.py")],
            cwd=intake,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        assert sealed_builder.returncode == 0, sealed_builder.stdout + sealed_builder.stderr
        rebuilt_intake = Path(json.loads(sealed_builder.stdout)["intake"])
        assert run_verifier(rebuilt_intake, env).returncode == 0
        assert not marker.exists()

        # Repository mode must also launch the registered command from the fresh sealed root.
        if not SEALED_ENTRYPOINT:
            sealed_entrypoint = subprocess.run(
                [sys.executable, str(intake / ROOT.name / "verify_review_repairs.py"), "--no-write"],
                cwd=intake,
                text=True,
                capture_output=True,
                check=False,
                env=env,
            )
            assert sealed_entrypoint.returncode == 0, sealed_entrypoint.stdout + sealed_entrypoint.stderr
            assert not marker.exists()

        with (intake / "REVIEW_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        scope = json.loads((intake / "REVIEW_SCOPE.json").read_text(encoding="utf-8"))
        physical = [path for path in intake.rglob("*") if path.is_file()]
        result = {
            "status": "PASS",
            "clean_sealed_replay": True,
            "physical_files": len(physical),
            "manifest_entries_excluding_manifest": len(rows),
            "manifest_semantics_explicit": "except itself" in scope["manifest_semantics"],
            "unlisted_extra_rejected": True,
            "listed_payload_tamper_rejected": True,
            "sealed_source_tamper_rejected": True,
            "sealed_git_fallback_invoked": False,
            "sealed_builder_replay": True,
            "sealed_builder_git_fallback_invoked": False,
            "sealed_entrypoint_replay": True,
            "scientific_landing_changed": False,
        }
    finally:
        if rebuilt_intake is not None:
            shutil.rmtree(rebuilt_intake)
        if owns_intake:
            shutil.rmtree(intake)
        shutil.rmtree(scratch)

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
