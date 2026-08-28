#!/usr/bin/env python3
"""Disposable hostile probes for the externally requested G287 evidence repairs."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def make_probe(parent: Path, name: str) -> tuple[Path, Path]:
    probe_root = parent / name
    probe_package = probe_root / PACKAGE.name
    shutil.copytree(PACKAGE, probe_package)
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            source = ROOT / row["path"]
            target = probe_root / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return probe_root, probe_package


def run(root: Path, script: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["G287_SKIP_REPAIR_PROBES"] = "1"
    return subprocess.run(
        [sys.executable, "-S", str(script)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="udt_g287_repair_probes_") as temporary:
        parent = Path(temporary)
        checks = {}

        root, package = make_probe(parent, "empty_mutations")
        (package / "run_catch_proofs.py").write_text(
            "import json\nprint(json.dumps({'caught': {}, 'mutation_count': 0, 'pass': True}))\n",
            encoding="utf-8",
        )
        checks["empty_mutation_registry_rejected"] = run(
            root, package / "verify_package.py"
        ).returncode != 0

        root, package = make_probe(parent, "surviving_mutant")
        path = package / "run_catch_proofs.py"
        text = path.read_text(encoding="utf-8")
        old = "return (metric[1] * -1, metric[0] * -1), -profile, -depth"
        if old not in text:
            raise AssertionError("surviving-mutant probe anchor missing")
        path.write_text(text.replace(old, "return metric, profile, -depth", 1), encoding="utf-8")
        checks["surviving_semantic_mutant_rejected"] = run(
            root, package / "verify_package.py"
        ).returncode != 0

        root, package = make_probe(parent, "broken_builder")
        path = package / "build_review_intake.py"
        text = path.read_text(encoding="utf-8")
        old = "def main() -> None:\n"
        if old not in text:
            raise AssertionError("builder probe anchor missing")
        path.write_text(
            text.replace(old, old + "    raise RuntimeError('intentional repair probe')\n", 1),
            encoding="utf-8",
        )
        checks["broken_review_builder_rejected"] = run(
            root, package / "verify_package.py"
        ).returncode != 0

        root, package = make_probe(parent, "changed_marker")
        path = package / "DEPENDENCY_AUDIT.tsv"
        text = path.read_text(encoding="utf-8")
        old = "Keep three types and three symbols distinct"
        if old not in text:
            raise AssertionError("marker probe anchor missing")
        path.write_text(text.replace(old, "THIS MARKER DOES NOT EXIST", 1), encoding="utf-8")
        checks["changed_dependency_marker_rejected"] = run(
            root, package / "verify_package.py"
        ).returncode != 0

        root, package = make_probe(parent, "missing_row")
        path = package / "DEPENDENCY_AUDIT.tsv"
        lines = path.read_text(encoding="utf-8").splitlines()
        changed = [line for line in lines if not line.startswith("G286\t")]
        if len(changed) != len(lines) - 1:
            raise AssertionError("dependency-row probe anchor missing")
        path.write_text("\n".join(changed) + "\n", encoding="utf-8")
        checks["missing_dependency_row_rejected"] = run(
            root, package / "verify_package.py"
        ).returncode != 0

    result = {
        "checks": checks,
        "probe_count": len(checks),
        "pass": len(checks) == 5 and all(checks.values()),
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
