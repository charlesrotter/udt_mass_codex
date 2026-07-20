#!/usr/bin/env python3
from __future__ import annotations
import csv,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;BASE="33eaed961d4601019ee59df5ee8aa59fdc105353";PARENT="c2_nonlinear_stationary_solution_space_2026-07-20/SOURCE_ADJUDICATION.tsv";PREFIX="c2_nonlinear_stationary_solution_space_2026-07-20/"
ADDITIONS={
 PREFIX+"PREREGISTRATION.md":("parent preregistration","CURRENT_EVIDENCE","frozen 198-start design and gates","not evidence for an outcome","PARENT_SCOPE"),PREFIX+"AUDIT_REPORT.md":("immediate parent audit","CURRENT_EVIDENCE","147 round returns and 51 unresolved starts","no uniqueness promotion","PARENT_OUTCOME"),PREFIX+"STATUS_LEDGER.tsv":("parent status ledger","CURRENT_EVIDENCE","conditional and open labels","no action coframe boundary or matter promotion","STATUS_SCOPE"),PREFIX+"NEXT_SCIENTIFIC_DECISION.md":("authorized solver seam","CURRENT_NAVIGATION","failed-basin continuation question","not evidence for a branch","QUESTION_ONLY"),PREFIX+"RAW_ATTEMPTS.json":("frozen numerical input","CURRENT_RAW_EVIDENCE","exact 51 failed identities and coefficients","direct Newton failure is not no-solution evidence","FROZEN_INPUT"),PREFIX+"SUMMARY_RESULT.json":("parent machine summary","CURRENT_EVIDENCE","exact 147/51 census","bounded tile only","PARENT_CENSUS"),PREFIX+"ATTEMPT_CENSUS.tsv":("parent stratum census","CURRENT_EVIDENCE","order and parity distribution","finite starts and orders","PARENT_CENSUS"),PREFIX+"UNRESOLVED_BASIN_LEDGER.tsv":("authorized path universe","CURRENT_EVIDENCE","all 51 identities","none may be omitted","PATH_UNIVERSE"),PREFIX+"COMPLETENESS_MAP.tsv":("parent scope map","CURRENT_EVIDENCE","outer unsampled layers","remain open","SCOPE_GATE"),PREFIX+"stationary_c2_engine.py":("frozen metric tensor engine","CURRENT_IMPLEMENTATION","unchanged nonlinear C2 stationarity","conditional metric and action premises","OPERATOR_SOURCE"),PREFIX+"explore_stationary_space.py":("frozen parent solver","CURRENT_IMPLEMENTATION","seed and validation implementations","direct solver statuses not physics","NUMERICAL_LINEAGE"),PREFIX+"VERIFICATION_RESULT.json":("parent independent verification","CURRENT_EVIDENCE","tensor and source anchors","no external-model review","VERIFICATION_LINEAGE")}
def main():
 raw=subprocess.check_output(["git","show",f"{BASE}:{PARENT}"],cwd=ROOT,text=True);by={r["path"]:r for r in csv.DictReader(raw.splitlines(),delimiter="\t")}
 for path,v in ADDITIONS.items():
  role,authority,use,prohibition,ruling=v;by[path]={"path":path,"role":role,"authority":authority,"affirmative_use":use,"prohibition":prohibition,"audit_ruling":ruling}
 with (HERE/"SOURCE_CENSUS.tsv").open(encoding="utf-8",newline="") as h:census=list(csv.DictReader(h,delimiter="\t"))
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
 if expected!=set(by):raise AssertionError(f"mismatch missing={sorted(expected-set(by))} extra={sorted(set(by)-expected)}")
 fields=["id","path","role","authority","affirmative_use","prohibition","audit_ruling"]
 with (HERE/"SOURCE_ADJUDICATION.tsv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for i,path in enumerate(sorted(by),1):r=by[path];w.writerow({"id":f"R{i:03d}","path":path,**{k:r[k] for k in fields if k not in {"id","path"}}})
 print(f"PASS rows={len(by)}")
if __name__=="__main__":main()
