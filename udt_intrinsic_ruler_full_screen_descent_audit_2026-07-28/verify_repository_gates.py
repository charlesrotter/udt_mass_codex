#!/usr/bin/env python3
"""Repository gates for the intrinsic-ruler/full-screen descent audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "97d85edb7da351e6a96bb8c55b4e969ea8e3a749"
PACKAGE = HERE.name
DIRTY_COUNT = 57
DIRTY_SHA = "bf85b6db00083cfa0d19e4ba9cc09766423cc2d5e224954f12ceda74aeab9c96"
CONTROLS = {"LIVE.md", "HANDOFF.md", "INDEX.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "CANON.md"}


def run(command):
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)


def require(process):
    if process.returncode:
        raise AssertionError(process.stdout)


def generic_module():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("intrinsic_ruler_descent_generic", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.PACKAGE = PACKAGE
    module.BASE = BASE
    return module


def main():
    status = run(["git", "status", "--short"]); require(status)
    unrelated = [line for line in status.stdout.splitlines() if not line[3:].startswith(PACKAGE + "/")]
    dirty_text = "".join(line+"\n" for line in unrelated)
    dirty_hash = hashlib.sha256(dirty_text.encode()).hexdigest()
    if len(unrelated) != DIRTY_COUNT or dirty_hash != DIRTY_SHA:
        raise AssertionError(f"dirty drift {len(unrelated)} {dirty_hash}")

    committed = run(["git", "diff", "--name-only", f"{BASE}..HEAD"]); require(committed)
    invalid = [p for p in committed.stdout.splitlines() if p and not p.startswith(PACKAGE+"/")]
    if invalid:
        raise AssertionError(f"scope escaped {invalid}")
    for control in CONTROLS:
        changed = run(["git", "diff", "--name-only", BASE, "--", control]); require(changed)
        if changed.stdout.strip():
            raise AssertionError("unauthorized control "+control)

    generic = generic_module()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    audit = run([sys.executable, str(HERE / "verify_audit.py")])
    premises = run([sys.executable, "verify_current_scientific_premises.py"])
    tests = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    for process in (audit, premises, tests): require(process)
    match = re.search(r"(\d+) passed, (\d+) xfailed", tests.stdout)
    if match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError(tests.stdout)

    manifest = HERE / "SHA256SUMS.txt"
    replay = subprocess.run(["sha256sum", "--check", manifest.name], cwd=HERE, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if replay.returncode or "FAILED" in replay.stdout:
        raise AssertionError(replay.stdout)
    entries = [line.split("  ", 1)[1] for line in manifest.read_text().splitlines() if line]
    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    actual = sorted(p.name for p in HERE.iterdir() if p.is_file() and p.name not in excluded and p.suffix != ".pyc")
    if sorted(entries) != actual:
        raise AssertionError(f"manifest coverage {sorted(set(entries)^set(actual))}")

    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    if verification["status"] != "PASS" or verification["catch_proofs"] != 28:
        raise AssertionError("audit verification")
    relevant = sorted(set(committed.stdout.splitlines())
                      | {p for p in run(["git", "diff", "--name-only"]).stdout.splitlines() if p.startswith(PACKAGE+"/")}
                      | {p for p in run(["git", "ls-files", "--others", "--exclude-standard"]).stdout.splitlines() if p.startswith(PACKAGE+"/")})
    result = {
        "schema": "udt-intrinsic-ruler-full-screen-descent-repository-gates-1.0",
        "status": "PASS",
        "verified_head": run(["git", "rev-parse", "HEAD"]).stdout.strip(),
        "scope_base": BASE,
        "scope_paths": relevant,
        "dirty_checkout": {"paths": len(unrelated), "metadata_sha256": dirty_hash,
                           "contents_read": False, "result": "PASS"},
        "frozen": frozen,
        "navigation": navigation,
        "package_manifest": {"entries": len(entries), "sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(), "result": "PASS"},
        "audit": {"production_checks": 23, "independent_checks": 139, "catch_proofs": 28,
                  "status": "PASS", "stdout_sha256": hashlib.sha256(audit.stdout.encode()).hexdigest()},
        "current_premises": {"result": "PASS", "stdout_sha256": hashlib.sha256(premises.stdout.encode()).hexdigest()},
        "tests": {"passed": 70, "failed": 0, "xfailed": 1, "result": "PASS",
                  "stdout_sha256": hashlib.sha256(tests.stdout.encode()).hexdigest()},
        "authority_boundary": {"physical_selection": False, "GPU_ODE_PDE_time_live": False,
                               "action_source_carrier_density_bootstrap_boundary_scale": False,
                               "navigation_controls_changed": False, "canon_changed": False,
                               "historical_packages_rewritten": False},
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
