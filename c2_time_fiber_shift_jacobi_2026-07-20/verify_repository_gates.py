#!/usr/bin/env python3
"""Repository, frozen, prior-evidence, navigation, test, and dirty gates."""

from __future__ import annotations
import csv,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; HERE=Path(__file__).resolve().parent
BASE="61f6bc01e5732b3bc59120d506bd6b2716646369"; PACKAGE="c2_time_fiber_shift_jacobi_2026-07-20"
ORIGINAL_DIRTY=Path("/home/udt-admin/udt_mass_codex")
PRIOR_ADDITIONS={
"udt_premise_reset_audit_2026-07-19":"6123253b9370bce674c626a863dc595c773da3905cb155a7fe2b77c4667fd3a7",
"asymptotic_boundary_lineage_audit_2026-07-19":"3841492810a553cc07ae3107cc10c3c5584547db5dcb87757e377ebcdb335afb",
"native_boundary_generator_scale_audit_2026-07-19":"39d335fbbc0367f206d77173f72d4b4485145dd0cb42aacc8c4491656e6d287c",
"clock_curvature_selector_audit_2026-07-19":"62dd9fa82d19af1a065ffd45529b8cb0d7c4a814db66ea75759f1d19f159ea04",
"boundary_bootstrap_representative_selector_audit_2026-07-19":"6cd896586dda87b8e9794818c34ccb392a2f5a004e7d88ba8e288db57e50c6c3",
"scale_breaking_closure_census_2026-07-20":"53996dfcc0fb9cef29422ff94908fe71aaed32703d49e70e2d6d7f01aa19fe84",
"matter_bootstrap_dimensional_inventory_2026-07-20":"716c2ad9c071a49f75b4c340d6d980d75cfc0a48b0923c39e0cf3d100759ae77",
"angular_derivative_weight_selector_2026-07-20":"bff22ac4ff488c4a426f87afdfbce3d06d8a23659552f19284da1eda3b98c8ff",
"c2_angular_reduction_selector_2026-07-20":"98581e8f4da61692262b063650a281ffa0fb83739d16c3edd7afdbeaeaa83295",
"c2_variable_lapse_selector_2026-07-20":"28009a732ef6b07e74fd20764e5481d7e866a43812fa40f47162e53d60e557ae"}


def gate_module():
    source=ROOT/"bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec=importlib.util.spec_from_file_location("shift_gate_base",source)
    if spec is None or spec.loader is None: raise RuntimeError("cannot load gate base")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); module.BASE=BASE; module.PACKAGE=PACKAGE
    return module


def rows(path):
    with path.open(encoding="utf-8",newline="") as handle: return list(csv.DictReader(handle,delimiter="\t"))


def changed_paths(gate,injected=None):
    changed=set(str(gate.git(ROOT,"diff","--name-only",BASE)).splitlines()); changed.update(str(gate.git(ROOT,"ls-files","--others","--exclude-standard")).splitlines())
    if injected: changed.add(injected)
    invalid=sorted(path for path in changed if path and not path.startswith(PACKAGE+"/"))
    if invalid: raise gate.GateError("SCOPE",invalid[0])
    return sorted(changed)


def validate_science():
    source=HERE/"verify_c2_time_fiber_shift.py"; spec=importlib.util.spec_from_file_location("shift_science",source)
    if spec is None or spec.loader is None: raise RuntimeError("cannot load science verifier")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); module.main()
    result=json.loads((HERE/"VERIFICATION_RESULT.json").read_text())
    if result["result"]!="PASS" or len(result["groups"])!=9 or len(result["catch_proofs"])!=31: raise AssertionError("science verifier")
    return {"result":"PASS","groups":9,"catch_proofs":31}


def validate_execution(gate,corrupt=False):
    ledger=rows(HERE/"EXECUTION_LEDGER.tsv")
    if len(ledger)!=7 or len({row["id"] for row in ledger})!=7: raise gate.GateError("LEDGER","count")
    for index,row in enumerate(ledger):
        if row["id"]=="E07" and (row["compute"]!="EXTERNAL_REVIEW_NOT_PERFORMED" or row["exit_code"]!="AUTHORIZATION_NOT_GIVEN"): raise gate.GateError("LEDGER","external")
        observed=gate.digest((HERE/row["output_artifact"]).read_bytes())
        if corrupt and index==0: observed="0"*64
        if observed!=row["output_sha256"]: raise gate.GateError("LEDGER",row["id"])
        if row["id"]!="E07" and (row["compute"]!="CPU_ONLY" or row["exit_code"] not in {"0","1_EXPECTED_BASELINE"}): raise gate.GateError("LEDGER",row["id"])
    return {"rows":len(ledger),"result":"PASS"}


def main():
    gate=gate_module(); universe=rows(ROOT/"udt_premise_reset_audit_2026-07-19/PACKAGE_UNIVERSE.tsv")
    prior={row["package"]:row["manifest_sha256"] for row in universe}; prior.update(PRIOR_ADDITIONS)
    scope=changed_paths(gate); science=validate_science(); execution=validate_execution(gate)
    frozen=gate.validate_frozen(ROOT); prior_result=gate.replay_packages(ROOT,prior,"PRIOR")
    if len(prior)!=29 or prior_result["entries"]!=637: raise gate.GateError("PRIOR",f"{len(prior)}:{prior_result['entries']}")
    navigation=gate.validate_navigation(ROOT); dirty=gate.validate_dirty(ROOT,ORIGINAL_DIRTY); tests=gate.validate_tests(ROOT); package=gate.validate_package_manifest(ROOT)
    catches={"out_of_scope_change_rejected":gate.expect("SCOPE",lambda:changed_paths(gate,"CANON.md")),
      "execution_hash_corruption_rejected":gate.expect("LEDGER",lambda:validate_execution(gate,True)),
      "frozen_manifest_corruption_rejected":gate.expect("FROZEN",lambda:gate.validate_frozen(ROOT,True)),
      "prior_package_corruption_rejected":gate.expect("PRIOR",lambda:gate.replay_packages(ROOT,prior,"PRIOR",True)),
      "missing_current_path_rejected":gate.expect("NAVIGATION",lambda:gate.validate_navigation(ROOT,"current")),
      "missing_frontier_target_rejected":gate.expect("NAVIGATION",lambda:gate.validate_navigation(ROOT,"frontier")),
      "dirty_metadata_loss_rejected":gate.expect("DIRTY",lambda:gate.validate_dirty(ROOT,ORIGINAL_DIRTY,True)),
      "package_hash_failure_rejected":gate.expect("PACKAGE",lambda:gate.validate_package_manifest(ROOT,True))}
    output={"schema":"udt-conditional-c2-time-fiber-shift-repository-gates-1.0","base":BASE,"result":"PASS",
      "scope_paths":scope,"science_verifier":science,"execution_ledger":execution,"frozen":frozen,
      "prior_scientific_packages":prior_result,"navigation":navigation,"dirty_checkout":dirty,"tests":tests,
      "package_manifest":package,"catch_proofs":catches,"compute":{"cpu_only":True,"gpu_work_performed":False},
      "authority_boundary":{"startup_controls_changed":False,"canon_changed":False,"carrier_or_action_adopted":False,
      "electron_mass_used":False,"physical_scale_or_boundary_derived":False,"nonlinear_or_time_live_solve_performed":False,
      "external_model_review_performed":False,"repository_reorganization_performed":False}}
    (HERE/"REPOSITORY_GATES.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print("repository_gates=PASS"); print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={prior_result['entries']}"); print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}"); print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__=="__main__": main()
