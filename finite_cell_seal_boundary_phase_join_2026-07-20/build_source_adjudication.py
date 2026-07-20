#!/usr/bin/env python3
"""Build explicit adjudication for every load-bearing seal-join source."""
from __future__ import annotations
import csv,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;BASE="55a2c53daade7282526581f20360f57aecfec12d"
def main():
 raw=subprocess.check_output(["git","show",f"{BASE}:c2_finite_cell_boundary_variation_2026-07-20/SOURCE_ADJUDICATION.tsv"],cwd=ROOT,text=True)
 old=list(csv.DictReader(raw.splitlines(),delimiter="\t"));by={r["path"]:r for r in old}
 additions={
 "c2_finite_cell_boundary_variation_2026-07-20/AUDIT_REPORT.md":("immediate parent audit","CURRENT_EVIDENCE","exact boundary phase-space and selector negative","conditional C2 and non-null fixed-wall caveats","PARENT_PHASE_SPACE"),
 "c2_finite_cell_boundary_variation_2026-07-20/STATUS_LEDGER.tsv":("parent status ledger","CURRENT_EVIDENCE","exact derived/open labels","no physical polarization promotion","STATUS_SCOPE"),
 "c2_finite_cell_boundary_variation_2026-07-20/EQUATION_LEDGER.tsv":("parent equations","CURRENT_EVIDENCE","h/K momenta, corner, CSN, Q","conventions and action conditional","PARENT_ALGEBRA"),
 "c2_finite_cell_boundary_variation_2026-07-20/BOUNDARY_CLASS_LEDGER.tsv":("parent class census","CURRENT_EVIDENCE","inequivalent differentiable classes","none selected","CLASS_FORK"),
 "c2_finite_cell_boundary_variation_2026-07-20/CONVENTION_LEDGER.tsv":("parent convention ledger","CURRENT_EVIDENCE","normal/gauge/K conventions","null and moving walls open","CONVENTION_SCOPE"),
 "c2_finite_cell_boundary_variation_2026-07-20/DERIVATION_RESULT.json":("parent exact output","CURRENT_EVIDENCE","machine-readable phase-space identities","not physical wall rule","PARENT_ALGEBRA"),
 "c2_finite_cell_boundary_variation_2026-07-20/NEXT_SCIENTIFIC_DECISION.md":("authorized seam","CURRENT_NAVIGATION","defines exact join question","not outcome evidence","QUESTION_ONLY"),
 "c2_finite_cell_boundary_variation_2026-07-20/COMPLETENESS_SCOPE.tsv":("parent scope census","CURRENT_EVIDENCE","decomposition omissions","omissions remain open","SCOPE_GATE"),
 "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md":("premise-reset control","CURRENT_EVIDENCE","correct c phi distance Xmax boundary meanings","no new boundary equation","SEMANTIC_CONTROL"),
 "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv":("owner meanings","OWNER_LOCKED_FOR_AUDIT","O03 O06-O12 O15","boundary join and scale open","SEMANTIC_CONTROL"),
 "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md":("co-presence audit","CURRENT_EVIDENCE","membership versus causal/response distinction","no action or boundary selector","COPRESENCE_SCOPE"),
 "copresence_causal_accessibility_selector_2026-07-19/STATUS_LEDGER.tsv":("co-presence ledger","CURRENT_EVIDENCE","C03-C05 conformal causal statuses","no physical calibration","STATUS_SCOPE"),
 "copresence_gr_constraint_regrade_2026-07-19/DERIVATION_REPORT.md":("constraint regrade","CURRENT_EVIDENCE","global admissibility not off-shell equation","no native ADM/lapse/shift import","OFFSHELL_SCOPE"),
 "copresence_gr_constraint_regrade_2026-07-19/RECLASSIFICATION_TABLE.tsv":("constraint role table","CURRENT_EVIDENCE","R07 R18 R24-R26 roles","no parent-law promotion","STATUS_SCOPE"),
 "native_action_final_adjudication_2026-07-18/MECHANICAL_AGREEMENT_DISAGREEMENT.tsv":("frozen final adjudication","HARD_FROZEN_POST_FIREWALL","M06 parity and M19 boundary ruling","immutable; no strengthening","FROZEN_BOUNDARY_STATUS")}
 fields=["id","path","role","authority","affirmative_use","prohibition","audit_ruling"]
 for path,v in additions.items():
  role,authority,use,prohibition,ruling=v;by[path]={"path":path,"role":role,"authority":authority,"affirmative_use":use,"prohibition":prohibition,"audit_ruling":ruling}
 with (HERE/"SOURCE_CENSUS.tsv").open(encoding="utf-8",newline="") as h:census=list(csv.DictReader(h,delimiter="\t"))
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
 if expected!=set(by):raise AssertionError(f"mismatch missing={sorted(expected-set(by))} extra={sorted(set(by)-expected)}")
 with (HERE/"SOURCE_ADJUDICATION.tsv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for i,path in enumerate(sorted(by),1):
   r=by[path];w.writerow({"id":f"R{i:02d}","path":path,**{k:r[k] for k in fields if k not in {"id","path"}}})
 print(f"PASS rows={len(by)}")
if __name__=="__main__":main()
