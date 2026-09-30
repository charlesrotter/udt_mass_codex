from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_current_scientific_premises as v
p=Path("udt_physical_connection_whiteboard_2026-09-30")
old=json.loads((p/"review/fidelity/PRE_REGISTRY_POINTER_FINAL_ATTESTATION.json").read_text())["accepted_sha256"]
f=json.loads((p/"INTEGRATION_FREEZE.json").read_text());new=f["accepted_sha256"]
assert set(old)-set(new)==set()
assert {n for n in old if old[n]!=new[n]}=={"HANDOFF.md"}
assert set(new)-set(old)=={str(p/"PACKAGING_REPAIR.md")}
current=Path("HANDOFF.md").read_text()
before=current.replace("Exact406 grades in CURRENT_SCIENTIFIC_PREMISES.tsv are unchanged; previous", "Exact406 grades are unchanged; previous")
assert before!=current
assert hashlib.sha256(before.encode()).hexdigest()==old["HANDOFF.md"]
for n,h in new.items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
missing=[n for n in v.PREMISE_REGISTRY_CONTROLS if "CURRENT_SCIENTIFIC_PREMISES.tsv" not in Path(n).read_text()]
assert not missing,missing
print(json.dumps({"status":"PASS_PACKAGING_CORRESPONDENCE_ONLY","frozen_files":len(new),"inherited_changed":["HANDOFF.md"],"new_files":[str(p/"PACKAGING_REPAIR.md")],"exact_prior_handoff_reconstructed":True,"registry_pointer_controls":len(v.PREMISE_REGISTRY_CONTROLS),"full_audit_rerun":"not performed by this focused check"},indent=2))
