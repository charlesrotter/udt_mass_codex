#!/usr/bin/env python3
"""Final repository gates after external review and append-only adjudication."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "316114a67b52db547025888df132f89eb92bb6f1"
PACKAGE = HERE.name
DIRTY = Path("/home/udt-admin/udt_mass_codex")
NAVIGATION = {
    "AGENTS.md",
    "HANDOFF.md",
    "INDEX.md",
    "LIVE.md",
    "README.md",
    "research/README.md",
}


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def validate_scope(generic, injected: str | None = None) -> list[str]:
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        changed.add(injected)
    invalid = sorted(
        path for path in changed
        if path and not path.startswith(PACKAGE + "/") and path not in NAVIGATION
    )
    if invalid:
        raise generic.GateError("SCOPE", invalid[0])
    return sorted(path for path in changed if path)


def validate_adjudication(generic, corrupt: bool = False) -> dict[str, object]:
    result = json.loads((HERE / "ADJUDICATION_RESULT.json").read_text(encoding="utf-8"))
    if corrupt:
        result["frozen_claim_status_changes"] = 1
    required = (
        result["status"] == "PASS_WITH_APPEND_ONLY_QUALIFICATIONS"
        and result["frozen_reference_commit"] == "1a41c4b"
        and result["reference_freeze_manifest_sha256"] == "48bfee46f7d075bb6e0d19ab61dd148e2e1d38536f0863653d46f1e2bdb8cd90"
        and result["review_verdict_census"] == {"PASS-WITH-CAVEATS": 4}
        and result["review_evidence_files"] == 8
        and result["agreement_rows"] == 15
        and result["catch_proofs"] == 11
        and result["frozen_claim_status_changes"] == 0
        and result["new_physics_claims"] == 0
        and result["ranked_first_question"] == "REGISTERED_BOOTSTRAP_REALIZATION_OPERATOR_AUDIT"
    )
    if not required:
        raise generic.GateError("ADJUDICATION", "contract")
    return result


def validate_manifest(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "hash replay")
    entries = [
        line.split("  ", 1)[1]
        for line in manifest.read_text(encoding="utf-8").splitlines()
        if line
    ]
    excluded = {
        "SHA256SUMS.txt",
        "FINAL_REPOSITORY_GATES.json",
        "FINAL_REPOSITORY_GATES_TRANSCRIPT.txt",
    }
    actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in excluded)
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", f"coverage:{sorted(set(entries) ^ set(actual))}")
    return {"entries": len(entries), "manifest_sha256": digest(manifest), "result": "PASS"}


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "metric_frontier_final_generic",
    )
    frozen_gate = load(HERE / "verify_repository_gates.py", "metric_frontier_frozen_gate")
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = validate_scope(generic)
    adjudication = validate_adjudication(generic)
    freeze = frozen_gate.validate_freeze(generic)
    if freeze["manifest_sha256"] != "48bfee46f7d075bb6e0d19ab61dd148e2e1d38536f0863653d46f1e2bdb8cd90":
        raise generic.GateError("REFERENCE_FREEZE", "manifest identity")
    frozen = generic.validate_frozen(ROOT)
    prior = frozen_gate.prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 71 or replay["entries"] != 1994:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = frozen_gate.validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode()).hexdigest()
    package = validate_manifest(generic)
    catches = {
        "scope": generic.expect("SCOPE", lambda: validate_scope(generic, "CANON.md")),
        "adjudication": generic.expect("ADJUDICATION", lambda: validate_adjudication(generic, True)),
        "reference_freeze": generic.expect("REFERENCE_FREEZE", lambda: frozen_gate.validate_freeze(generic, True)),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: frozen_gate.validate_navigation(generic, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: frozen_gate.validate_navigation(generic, "frontier")),
        "link": generic.expect("NAVIGATION", lambda: frozen_gate.validate_navigation(generic, "link")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: validate_manifest(generic, True)),
    }
    output = {
        "schema": "udt-metric-to-frontier-final-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "adjudication": adjudication,
        "reference_freeze": freeze,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": {
            "canon_changed": False,
            "new_derivation_performed": False,
            "global_quotient_selected": False,
            "carrier_or_action_selected": False,
            "time_live_solve_performed": False,
            "physical_mass_or_density_derived": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "FINAL_REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("final_repository_gates=PASS")
    print(f"reference_freeze={freeze['manifest_sha256']} entries={freeze['entries']}")
    print(f"review_verdicts={adjudication['review_verdict_census']}")
    print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['manifest_sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()
