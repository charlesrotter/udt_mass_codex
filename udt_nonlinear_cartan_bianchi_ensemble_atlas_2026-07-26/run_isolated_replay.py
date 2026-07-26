#!/usr/bin/env python3
"""Replay the package in a fresh, minimal, pinned dependency directory."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent


def package_root(name: str) -> Path:
    spec = importlib.util.find_spec(name)
    if spec is None or spec.origin is None:
        raise SystemExit(f"required package unavailable: {name}")
    return Path(spec.origin).resolve().parent


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def main() -> None:
    roots = {name: package_root(name) for name in ("sympy", "mpmath")}
    with tempfile.TemporaryDirectory(prefix="udt_cartan_pinned_") as temporary:
        site = Path(temporary) / "site"
        site.mkdir()
        copied = {}
        for name, source in roots.items():
            destination = site / name
            shutil.copytree(source, destination)
            copied[name] = {
                "source_tree_sha256": tree_hash(source),
                "copied_tree_sha256": tree_hash(destination),
            }
            if copied[name]["source_tree_sha256"] != copied[name]["copied_tree_sha256"]:
                raise AssertionError(f"dependency copy changed: {name}")

        bootstrap = (
            "import runpy,sys;"
            f"sys.path.insert(0,{str(site)!r});"
            f"runpy.run_path({str(HERE / 'verify_package.py')!r},run_name='__main__')"
        )
        command = [sys.executable, "-I", "-S", "-c", bootstrap]
        environment = dict(os.environ)
        environment["UDT_PINNED_SITE"] = str(site)
        completed = subprocess.run(
            command,
            cwd=HERE.parent,
            env=environment,
            text=True,
            capture_output=True,
        )
        (HERE / "ISOLATED_STDOUT.txt").write_text(completed.stdout, encoding="utf-8")
        (HERE / "ISOLATED_STDERR.txt").write_text(completed.stderr, encoding="utf-8")
        record = {
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "command": [
                sys.executable,
                "-I",
                "-S",
                "-c",
                "import runpy,sys;sys.path.insert(0,'<PINNED_SITE>');"
                "runpy.run_path('<PACKAGE>/verify_package.py',run_name='__main__')",
            ],
            "command_note": "temporary dependency path normalized; public replay command is in COMMANDS.md",
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "dependency_trees": copied,
            "stdout_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
            "stderr_sha256": hashlib.sha256(completed.stderr.encode("utf-8")).hexdigest(),
            "exit_code": completed.returncode,
        }
        (HERE / "RUN_ENVIRONMENT.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        sys.stdout.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        if completed.returncode != 0:
            raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
