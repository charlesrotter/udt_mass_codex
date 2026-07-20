#!/usr/bin/env python3
"""Build explicit adjudication for every load-bearing complete-coframe source."""
from __future__ import annotations
import csv,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
BASE="5b1b57297bcceb5f8806b1ee238ac2ed2ccfcee3";PARENT="finite_cell_seal_boundary_phase_join_2026-07-20/SOURCE_ADJUDICATION.tsv"
ADDITIONS={
 "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md":("immediate parent audit","CURRENT_EVIDENCE","partial seal data and raw-swap obstruction","no complete coframe or boundary promotion","PARENT_PARTIAL_JOIN"),
 "finite_cell_seal_boundary_phase_join_2026-07-20/STATUS_LEDGER.tsv":("parent status ledger","CURRENT_EVIDENCE","exact derived/open labels","no physical involution promotion","STATUS_SCOPE"),
 "finite_cell_seal_boundary_phase_join_2026-07-20/DERIVATION_RESULT.json":("parent exact output","CURRENT_EVIDENCE","tangent rank mirror and swap identities","not a complete physical symmetry","PARENT_ALGEBRA"),
 "finite_cell_seal_boundary_phase_join_2026-07-20/NEXT_SCIENTIFIC_DECISION.md":("authorized seam","CURRENT_NAVIGATION","defines exact complete-coframe question","not outcome evidence","QUESTION_ONLY"),
 "finite_cell_seal_boundary_phase_join_2026-07-20/SLOT_COVERAGE.tsv":("parent slot census","CURRENT_EVIDENCE","enumerates missing boundary slots","open slots remain open","SCOPE_GATE"),
 "finite_cell_seal_boundary_phase_join_2026-07-20/STRONGEST_JOIN_CHALLENGES.tsv":("parent adversarial challenges","CURRENT_EVIDENCE","strongest seal-selector counterarguments","challenges are not completion","CHALLENGE_INPUT"),
 "finite_cell_seal_boundary_phase_join_2026-07-20/CLAUSE_TO_BOUNDARY_SLOT.tsv":("foundation-to-slot map","CURRENT_EVIDENCE","maps supplied clauses to partial data","no missing slot invented","CLAUSE_SCOPE"),
 "finite_cell_seal_boundary_phase_join_2026-07-20/OUTCOME_BRANCH_LEDGER.tsv":("parent outcome branches","CURRENT_EVIDENCE","partial-seal branch classification","does not settle extension audit","QUESTION_PARENT"),
 "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md":("transverse realization audit","CURRENT_EVIDENCE","direct extension and conditional spin/Hopf witnesses","no physical transverse topology or carrier","TRANSVERSE_SCOPE"),
 "transverse_reciprocal_realization_selector_2026-07-19/STATUS_LEDGER.tsv":("transverse status ledger","CURRENT_EVIDENCE","exact conditional/open distinctions","no extension selector promotion","STATUS_SCOPE"),
 "transverse_reciprocal_realization_selector_2026-07-19/DERIVATION_RESULT.json":("transverse exact output","CURRENT_EVIDENCE","block extension and equivariance algebra","inherits conditional realization premises","CONDITIONAL_ALGEBRA"),
 "transverse_reciprocal_realization_selector_2026-07-19/CANDIDATE_FAMILY.tsv":("transverse candidate census","CURRENT_EVIDENCE","inequivalent realization families","none selected by current foundation","EXTENSION_FORK"),
}
def main():
 raw=subprocess.check_output(["git","show",f"{BASE}:{PARENT}"],cwd=ROOT,text=True)
 old=list(csv.DictReader(raw.splitlines(),delimiter="\t"));by={r["path"]:r for r in old}
 for path,v in ADDITIONS.items():
  role,authority,use,prohibition,ruling=v;by[path]={"path":path,"role":role,"authority":authority,"affirmative_use":use,"prohibition":prohibition,"audit_ruling":ruling}
 with (HERE/"SOURCE_CENSUS.tsv").open(encoding="utf-8",newline="") as h:census=list(csv.DictReader(h,delimiter="\t"))
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
 if expected!=set(by):raise AssertionError(f"mismatch missing={sorted(expected-set(by))} extra={sorted(set(by)-expected)}")
 fields=["id","path","role","authority","affirmative_use","prohibition","audit_ruling"]
 with (HERE/"SOURCE_ADJUDICATION.tsv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for i,path in enumerate(sorted(by),1):
   r=by[path];w.writerow({"id":f"R{i:02d}","path":path,**{k:r[k] for k in fields if k not in {"id","path"}}})
 print(f"PASS rows={len(by)}")
if __name__=="__main__":main()
