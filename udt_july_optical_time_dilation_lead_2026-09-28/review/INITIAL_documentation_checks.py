#!/usr/bin/env python3
"""Bounded documentation fidelity and preservation; no scientific recomputation."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

here=Path(__file__).resolve().parent
package=here.parent
root=package.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


freeze=json.loads((package/"FINAL_DOCUMENTATION_FREEZE.json").read_text())
verified={}
for group,base in (("files",root),("package_docs",package)):
    verified[group]={}
    for name,sha in freeze[group].items():
        actual=digest(base/name)
        if actual!=sha:
            raise RuntimeError(f"documentation freeze mismatch: {name}")
        verified[group][name]=actual

initial=(package/"INITIAL_CANDIDATE.md").read_text()
maintained=(package/"CANDIDATE.md").read_text()
old="Status: CONDITIONAL MATHEMATICAL APPLICATION, UNPROMOTED; direct review pending.\n"
new="Status: VERIFIED-WITH-CAVEATS / CONDITIONAL MATHEMATICAL APPLICATION / UNPROMOTED.\nRead with REPAIR.md (domain and next-gate corrections) and\nTIME_DEPENDENT_FOLLOWUP.md. Final review: review/REPAIR_REVIEW.md.\nINITIAL_CANDIDATE.md preserves the original text; only this header has changed.\n"
if initial.replace(old,new,1)!=maintained:
    raise RuntimeError("candidate changed beyond the reviewed status header")

repairfreeze=json.loads((package/"REPAIR_REVIEW_FREEZE.json").read_text())["files"]
brief=(package/"DECISION_BRIEF.md").read_text()
briefnew="Reviewed conditional result, VERIFIED-WITH-CAVEATS, UNPROMOTED.\nFresh separate-context source-first/direct review and one bounded repair cycle\nare complete: review/REPAIR_REVIEW.md. No physical premise was adopted.\n"
briefold="Draft pending completion of the separate-context repair review.\n"
oldbrief=brief.replace(briefnew,briefold,1)
if hashlib.sha256(oldbrief.encode()).hexdigest()!=repairfreeze["DECISION_BRIEF.md"]:
    raise RuntimeError("brief changed beyond the reviewed status header")
for name,sha in repairfreeze.items():
    if name!="DECISION_BRIEF.md" and digest(package/name)!=sha:
        raise RuntimeError(f"repaired scientific file changed: {name}")

pins=json.loads((package/"SOURCE_PINS.json").read_text())
for name,sha in pins["sources"].items():
    if digest(root/name)!=sha:
        raise RuntimeError(f"scientific/method source changed: {name}")

actual_names=subprocess.check_output(["git","diff","--name-only","HEAD"],cwd=root,text=True).splitlines()
if sorted(actual_names)!=sorted(freeze["files"]):
    raise RuntimeError(f"unexpected tracked changes: {actual_names}")
diff=subprocess.check_output(["git","diff","HEAD","--",*freeze["files"]],cwd=root)
if diff!=(package/"LIVE_SURFACE_DIFF.patch").read_bytes():
    raise RuntimeError("saved live-surface diff differs from git diff HEAD")
whitespace=subprocess.run(["git","diff","--check","HEAD"],cwd=root,capture_output=True,text=True)
if whitespace.returncode!=0:
    raise RuntimeError(whitespace.stdout+whitespace.stderr)

# Name-level preservation only; protected contents are not read or hashed.
untracked=subprocess.check_output(["git","ls-files","--others","--exclude-standard"],cwd=root,text=True).splitlines()
missing=set(pins["prior_untracked_names"])-set(untracked)
if missing:
    raise RuntimeError(f"pre-existing untracked names missing: {sorted(missing)}")
unexpected=[name for name in untracked if name not in pins["prior_untracked_names"] and not name.startswith(package.name+"/")]
if unexpected:
    raise RuntimeError(f"new unrelated untracked names: {unexpected}")

audit=json.loads((package/"premise_audit/RUN_RECORD.json").read_text())
if audit["exit_code"]!=0 or audit["before"]!=audit["after"] or not audit["inputs_unchanged"]:
    raise RuntimeError("parent audit record not clean")
auditstdout=(package/"premise_audit/stdout.txt").read_text()
if "PASS: 406-row premise registry" not in auditstdout or (package/"premise_audit/stderr.txt").stat().st_size:
    raise RuntimeError("parent audit output mismatch")
focused=(package/"startup_surface_check.stdout.txt").read_text()
if "PASS" not in focused or (package/"startup_surface_check.stderr.txt").stat().st_size:
    raise RuntimeError("focused surface check evidence mismatch")

print(json.dumps({"utc":datetime.now(timezone.utc).isoformat(),"branch":subprocess.check_output(["git","branch","--show-current"],cwd=root,text=True).strip(),"head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip(),"verified_documentation_hashes":verified,"candidate_status_only_change":True,"brief_status_only_change":True,"repaired_science_unchanged":True,"pinned_scientific_method_sources_unchanged":len(pins["sources"]),"tracked_changes_exactly_six_surfaces":actual_names,"actual_diff_matches_saved_patch":True,"git_diff_check_exit":whitespace.returncode,"prior_untracked_names_retained":len(pins["prior_untracked_names"]),"protected_content_claim":"No protected contents read/hashed; name preservation only.","parent_audit":{"record_read":True,"full_audit_replayed_by_reviewer":False,"exit_code":audit["exit_code"],"elapsed_seconds":audit["elapsed_seconds"],"recorded_inputs_unchanged":audit["inputs_unchanged"],"stdout_406_pass":True,"stderr_empty":True},"focused_surface_evidence":focused.strip(),"scope":"Documentation fidelity only; final manifest/check file assembly and commit/push belong to parent."},indent=2))
