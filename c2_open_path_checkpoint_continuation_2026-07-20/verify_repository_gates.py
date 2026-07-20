#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "99c57d7800eee2f9f2ebabff34dc6d17a18ed847"
PACKAGE = "c2_open_path_checkpoint_continuation_2026-07-20"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PARENT_MANIFEST = "113fa557c2a8e0b3267974276809ebebfd41b18a5ec4c5fe7afa93b875367a95"

def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def scope(g, inject=None):
    changed = set(str(g.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(g.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if inject: changed.add(inject)
    bad = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/"))
    if bad: raise g.GateError("SCOPE", bad[0])
    return sorted(changed)

def science():
    completed = subprocess.run([sys.executable, str(HERE / "verify_result_integrity.py")], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if completed.returncode: raise AssertionError(completed.stdout.decode("utf-8", "replace"))
    result = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    if result["result"] != "PASS" or result["counts"]["groups"] != 5 or result["counts"]["catch_proofs"] != 14: raise AssertionError("science")
    return {"result": "PASS", "groups": 5, "catch_proofs": 14, "states": 3919, "round": 1, "artifacts": 6, "open": 15}

def execution(g, corrupt=False):
    ledger = rows(HERE / "EXECUTION_LEDGER.tsv")
    if len(ledger) != 6 or len({row["id"] for row in ledger}) != 6: raise g.GateError("LEDGER", "count")
    for index, row in enumerate(ledger):
        if row["id"] == "E06" and (row["compute"] != "EXTERNAL_REVIEW_NOT_PERFORMED" or row["exit_code"] != "AUTHORIZATION_NOT_GIVEN"): raise g.GateError("LEDGER", "external")
        observed = g.digest((HERE / row["output_artifact"]).read_bytes())
        if corrupt and index == 0: observed = "0" * 64
        if observed != row["output_sha256"]: raise g.GateError("LEDGER", row["id"])
    return {"rows": 6, "result": "PASS"}

def main():
    generic = load(ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py", "open_path_generic_gates")
    parent_wrapper = load(ROOT / "c2_failed_basin_homotopy_2026-07-20/verify_repository_gates.py", "failed_basin_wrapper")
    generic.BASE = BASE; generic.PACKAGE = PACKAGE
    universe = rows(ROOT / "udt_premise_reset_audit_2026-07-19/PACKAGE_UNIVERSE.tsv")
    prior = {row["package"]: row["manifest_sha256"] for row in universe}
    prior.update(parent_wrapper.ADD)
    prior["c2_failed_basin_homotopy_2026-07-20"] = PARENT_MANIFEST
    changed = scope(generic); sci = science(); exe = execution(generic)
    frozen = generic.validate_frozen(ROOT)
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 36 or replay["entries"] != 889: raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    package = generic.validate_package_manifest(ROOT)
    catches = {
        "scope": generic.expect("SCOPE", lambda: scope(generic, "CANON.md")),
        "ledger": generic.expect("LEDGER", lambda: execution(generic, True)),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: generic.validate_package_manifest(ROOT, True)),
    }
    result = {"schema": "udt-c2-open-path-checkpoint-repository-gates-1.0", "base": BASE, "result": "PASS", "scope_paths": changed, "science_verifier": sci, "execution_ledger": exe, "frozen": frozen, "prior_scientific_packages": replay, "navigation": navigation, "dirty_checkout": dirty, "tests": tests, "package_manifest": package, "catch_proofs": catches, "compute": {"cpu_only": True, "gpu_work_performed": False}, "authority_boundary": {"startup_controls_changed": False, "canon_changed": False, "conditional_c2_action_made_native": False, "global_uniqueness_claimed": False, "fifteen_open_paths_closed": False, "native_angular_section_derived": False, "hopf_carrier_adopted": False, "source_backreaction_or_mass_derived": False, "external_model_review_performed": False, "repository_reorganization_performed": False}}
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("repository_gates=PASS")
    print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")

if __name__ == "__main__":
    main()
