#!/usr/bin/env python3
"""Verify G307 builder portability and hostile source-layout rejection."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "PORTABILITY_VERIFICATION_RESULT.json"


def load_builder():
    spec = importlib.util.spec_from_file_location("g307_builder", HERE / "build_review_intake.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_builder(package: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, "-S", "build_review_intake.py"],
        cwd=package,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def rejected(callable_object) -> bool:
    try:
        callable_object()
    except AssertionError:
        return True
    return False


def main() -> None:
    repository_result = run_builder(HERE)
    first_intake = Path(repository_result["intake"])
    sealed_package = first_intake / HERE.name
    sealed_result = run_builder(sealed_package)
    assert repository_result["manifest_payloads"] == sealed_result["manifest_payloads"]
    assert repository_result["total_files"] == sealed_result["total_files"]
    assert repository_result["scope_sha256"] == sealed_result["scope_sha256"]
    assert repository_result["manifest_sha256"] == sealed_result["manifest_sha256"]
    assert repository_result["detached_seal_sha256"] == sealed_result["detached_seal_sha256"]

    builder = load_builder()
    original_root = builder.REPO
    with tempfile.TemporaryDirectory(prefix="g307_resolution_") as temporary:
        root = Path(temporary)
        builder.REPO = root
        source_relative = Path("source/example.txt")
        current_name = "CURRENT_EXAMPLE.tsv"
        missing_source_rejected = rejected(lambda: builder.resolve_source(source_relative))
        missing_current_rejected = rejected(lambda: builder.resolve_current(current_name))

        repository_source = root / source_relative
        frozen_source = root / "frozen_sources" / source_relative
        repository_source.parent.mkdir(parents=True)
        frozen_source.parent.mkdir(parents=True)
        repository_source.write_text("repository\n", encoding="utf-8")
        frozen_source.write_text("sealed\n", encoding="utf-8")
        ambiguous_source_rejected = rejected(lambda: builder.resolve_source(source_relative))

        repository_current = root / current_name
        frozen_current = root / "frozen_current" / current_name
        frozen_current.parent.mkdir(parents=True)
        repository_current.write_text("repository\n", encoding="utf-8")
        frozen_current.write_text("sealed\n", encoding="utf-8")
        ambiguous_current_rejected = rejected(lambda: builder.resolve_current(current_name))
    builder.REPO = original_root

    assert missing_source_rejected
    assert missing_current_rejected
    assert ambiguous_source_rejected
    assert ambiguous_current_rejected
    result = {
        "status": "PASS",
        "repository_builder_passed": True,
        "sealed_builder_passed": True,
        "rebuilt_manifest_byte_identical": True,
        "manifest_payloads": repository_result["manifest_payloads"],
        "total_files": repository_result["total_files"],
        "scope_sha256": repository_result["scope_sha256"],
        "missing_source_rejected": missing_source_rejected,
        "missing_current_rejected": missing_current_rejected,
        "ambiguous_source_rejected": ambiguous_source_rejected,
        "ambiguous_current_rejected": ambiguous_current_rejected,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
