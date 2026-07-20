#!/usr/bin/env python3
from __future__ import annotations
import csv,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
BASE="eb06c7b5157ffb893ee3e6cd1d10de0816a07e3a";PACKAGE="c2_finite_cell_boundary_variation_2026-07-20";DIRTY=Path("/home/udt-admin/udt_mass_codex")
ADD={
"udt_premise_reset_audit_2026-07-19":"6123253b9370bce674c626a863dc595c773da3905cb155a7fe2b77c4667fd3a7","asymptotic_boundary_lineage_audit_2026-07-19":"3841492810a553cc07ae3107cc10c3c5584547db5dcb87757e377ebcdb335afb","native_boundary_generator_scale_audit_2026-07-19":"39d335fbbc0367f206d77173f72d4b4485145dd0cb42aacc8c4491656e6d287c","clock_curvature_selector_audit_2026-07-19":"62dd9fa82d19af1a065ffd45529b8cb0d7c4a814db66ea75759f1d19f159ea04","boundary_bootstrap_representative_selector_audit_2026-07-19":"6cd896586dda87b8e9794818c34ccb392a2f5a004e7d88ba8e288db57e50c6c3","scale_breaking_closure_census_2026-07-20":"53996dfcc0fb9cef29422ff94908fe71aaed32703d49e70e2d6d7f01aa19fe84","matter_bootstrap_dimensional_inventory_2026-07-20":"716c2ad9c071a49f75b4c340d6d980d75cfc0a48b0923c39e0cf3d100759ae77","angular_derivative_weight_selector_2026-07-20":"bff22ac4ff488c4a426f87afdfbce3d06d8a23659552f19284da1eda3b98c8ff","c2_angular_reduction_selector_2026-07-20":"98581e8f4da61692262b063650a281ffa0fb83739d16c3edd7afdbeaeaa83295","c2_variable_lapse_selector_2026-07-20":"28009a732ef6b07e74fd20764e5481d7e866a43812fa40f47162e53d60e557ae","c2_time_fiber_shift_jacobi_2026-07-20":"7decd015d987d50c1d120d32eb9111b5a6ca07b538c9c3db83bb7420bcd23fee","c2_rigidity_three_route_zoomout_2026-07-20":"848db01c3524a45f15854228549d45dac4ac7b10cd07aa06924dffd406b3c9d4"}
def rows(p):
 with p.open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h,delimiter="\t"))
def gate():
 p=ROOT/"bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py";s=importlib.util.spec_from_file_location("boundary_gate",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.BASE=BASE;m.PACKAGE=PACKAGE;return m
def scope(g,inject=None):
 c=set(str(g.git(ROOT,"diff","--name-only",BASE)).splitlines())|set(str(g.git(ROOT,"ls-files","--others","--exclude-standard")).splitlines())
 if inject:c.add(inject)
 bad=sorted(x for x in c if x and not x.startswith(PACKAGE+"/"))
 if bad:raise g.GateError("SCOPE",bad[0])
 return sorted(c)
def science():
 p=HERE/"verify_c2_boundary_variation.py";s=importlib.util.spec_from_file_location("boundary_science",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.main();r=json.loads((HERE/"VERIFICATION_RESULT.json").read_text())
 if r["result"]!="PASS" or len(r["groups"])!=11 or len(r["catch_proofs"])!=40:raise AssertionError("science")
 return {"result":"PASS","groups":11,"catch_proofs":40}
def execution(g,corrupt=False):
 a=rows(HERE/"EXECUTION_LEDGER.tsv")
 if len(a)!=7 or len({r["id"] for r in a})!=7:raise g.GateError("LEDGER","count")
 for i,r in enumerate(a):
  if r["id"]=="E07" and (r["compute"]!="EXTERNAL_REVIEW_NOT_PERFORMED" or r["exit_code"]!="AUTHORIZATION_NOT_GIVEN"):raise g.GateError("LEDGER","external")
  d=g.digest((HERE/r["output_artifact"]).read_bytes());d="0"*64 if corrupt and i==0 else d
  if d!=r["output_sha256"]:raise g.GateError("LEDGER",r["id"])
 return {"rows":len(a),"result":"PASS"}
def main():
 g=gate();u=rows(ROOT/"udt_premise_reset_audit_2026-07-19/PACKAGE_UNIVERSE.tsv");prior={r["package"]:r["manifest_sha256"] for r in u};prior.update(ADD)
 sc=scope(g);sci=science();exe=execution(g);f=g.validate_frozen(ROOT);pr=g.replay_packages(ROOT,prior,"PRIOR")
 if len(prior)!=31 or pr["entries"]!=703:raise g.GateError("PRIOR",f"{len(prior)}:{pr['entries']}")
 nav=g.validate_navigation(ROOT);dirty=g.validate_dirty(ROOT,DIRTY);tests=g.validate_tests(ROOT);pkg=g.validate_package_manifest(ROOT)
 catches={"scope":g.expect("SCOPE",lambda:scope(g,"CANON.md")),"ledger":g.expect("LEDGER",lambda:execution(g,True)),"frozen":g.expect("FROZEN",lambda:g.validate_frozen(ROOT,True)),"prior":g.expect("PRIOR",lambda:g.replay_packages(ROOT,prior,"PRIOR",True)),"current":g.expect("NAVIGATION",lambda:g.validate_navigation(ROOT,"current")),"frontier":g.expect("NAVIGATION",lambda:g.validate_navigation(ROOT,"frontier")),"dirty":g.expect("DIRTY",lambda:g.validate_dirty(ROOT,DIRTY,True)),"package":g.expect("PACKAGE",lambda:g.validate_package_manifest(ROOT,True))}
 out={"schema":"udt-conditional-c2-finite-cell-boundary-repository-gates-1.0","base":BASE,"result":"PASS","scope_paths":sc,"science_verifier":sci,"execution_ledger":exe,"frozen":f,"prior_scientific_packages":pr,"navigation":nav,"dirty_checkout":dirty,"tests":tests,"package_manifest":pkg,"catch_proofs":catches,"compute":{"cpu_only":True,"gpu_work_performed":False},"authority_boundary":{"startup_controls_changed":False,"canon_changed":False,"action_or_carrier_adopted":False,"physical_boundary_condition_selected":False,"scale_or_mass_derived":False,"nonlinear_solve_performed":False,"external_model_review_performed":False,"repository_reorganization_performed":False}}
 (HERE/"REPOSITORY_GATES.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print("repository_gates=PASS");print(f"frozen_manifests=6 entries={f['entries']} paths={f['tracked_paths']}");print(f"prior_packages={len(prior)} entries={pr['entries']}");print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed");print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}");print(f"package_manifest={pkg['sha256']} entries={pkg['entries']}")
if __name__=="__main__":main()
