#!/usr/bin/env python3
"""Post-commit repository gates for the higher-isometry plane audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "3e3eecc364df98f321ffaf5c5e46dd0bb7b689b6"
DIRTY_COUNT = 57
DIRTY_SHA = "bf85b6db00083cfa0d19e4ba9cc09766423cc2d5e224954f12ceda74aeab9c96"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)


def unrelated_dirty() -> tuple[int, str]:
    lines = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines()
    kept = []
    for line in lines:
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path.startswith(HERE.name + "/"):
            continue
        kept.append(line)
    payload = ("\n".join(kept) + ("\n" if kept else "")).encode()
    return len(kept), digest(payload)


def package_links() -> int:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    count = 0
    for source in sorted(HERE.glob("*.md")):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = re.sub(r":\d+$", "", unquote(target.split("#", 1)[0]))
            resolved = Path(target) if Path(target).is_absolute() else source.parent / target
            require("markdown_link", resolved.exists())
            count += 1
    return count


def package_manifest() -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    replay = subprocess.run(["sha256sum", "--check", manifest.name], cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    require("package_manifest_replay", replay.returncode == 0 and "FAILED" not in replay.stdout)
    entries = [line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"})
    require("package_manifest_coverage", sorted(entries) == actual)
    return {"entries": len(entries), "sha256": digest(manifest.read_bytes()), "result": "PASS"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "REPOSITORY_GATES.json")
    args = parser.parse_args()

    gate_path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("udt_repository_gate_library", gate_path)
    require("gate_import_spec", spec is not None and spec.loader is not None)
    library = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(library)
    library.BASE = BASE
    library.PACKAGE = "__repository_gate_no_package__"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "HEAD"], cwd=ROOT, text=True).splitlines()
    require("scope", bool(changed) and all(path.startswith(HERE.name + "/") for path in changed))
    controls = ["LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "AGENTS.md", "CLAUDE.md", "CANON.md", "MEMORY.md"]
    require("controls_unchanged", run(["git", "diff", "--quiet", BASE, "HEAD", "--", *controls]).returncode == 0)

    audit = run([sys.executable, str(HERE / "verify_audit.py")])
    require("audit", audit.returncode == 0)
    premise = run([sys.executable, "verify_current_scientific_premises.py"])
    require("premises", premise.returncode == 0)
    frozen = library.validate_frozen(ROOT)
    prior = library.replay_packages(ROOT, library.PRIOR_SCIENTIFIC_PACKAGES, "PRIOR_SCIENCE")
    navigation = library.validate_navigation(ROOT)
    navigation["package_links"] = package_links()

    tests = run([sys.executable, "-m", "pytest", "-q", "tests/", "-p", "no:cacheprovider"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", tests.stdout)
    require("tests", tests.returncode == 0 and match is not None and tuple(map(int, match.groups())) == (70, 1))

    dirty_count, dirty_sha = unrelated_dirty()
    require("dirty", (dirty_count, dirty_sha) == (DIRTY_COUNT, DIRTY_SHA))
    manifest = package_manifest()
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    require(
        "verification",
        verification["status"] == "PASS"
        and verification["production_checks"] == 135
        and verification["independent_checks"] == 292
        and verification["catch_proofs"] == 32
        and verification["initial_review_verdict"] == "REFUTED"
        and verification["corrected_review_verdict"] == "PASS_WITH_CAVEATS",
    )

    result = {
        "schema": "udt-higher-isometry-plane-ownership-repository-gates-1.0",
        "status": "PASS",
        "base": BASE,
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "scope_paths": changed,
        "controls_unchanged": controls,
        "audit": verification,
        "premises": {"result": "PASS", "stdout_sha256": digest(premise.stdout.encode())},
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "tests": {"passed": 70, "xfailed": 1, "returncode": 0},
        "dirty": {"count": dirty_count, "sha256": dirty_sha, "contents_read": False},
        "package_manifest": manifest,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "physical_branch_selected": False,
            "action_carrier_source_density_or_dynamics_added": False,
            "fixed_metric_generic_selection_claimed": False,
        },
    }
    output = args.output.resolve()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("repository_gates=PASS")
    print(f"head={result['head']}")
    print(f"frozen=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_science={len(library.PRIOR_SCIENTIFIC_PACKAGES)} entries={prior['entries']}")
    print(f"navigation={navigation}")
    print("tests=70 passed/1 xfailed")
    print(f"dirty={dirty_count} sha256={dirty_sha}")
    print(f"manifest={manifest}")


if __name__ == "__main__":
    main()
