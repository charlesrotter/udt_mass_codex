#!/usr/bin/env python3
"""Build explicit one-row-per-load-bearing-source adjudication for the boundary audit."""
from __future__ import annotations
import csv,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
BASE="eb06c7b5157ffb893ee3e6cd1d10de0816a07e3a"
def main():
 raw=subprocess.check_output(["git","show",f"{BASE}:c2_rigidity_three_route_zoomout_2026-07-20/SOURCE_ADJUDICATION.tsv"],cwd=ROOT,text=True)
 old=list(csv.DictReader(raw.splitlines(),delimiter="\t"));by={r["path"]:r for r in old}
 additions={
  "c2_rigidity_three_route_zoomout_2026-07-20/AUDIT_REPORT.md":("immediate parent zoom-out","CURRENT_EVIDENCE","ranks boundary variation before nonlinear solve","ranking is not outcome authority","PARENT_ROUTE_RANKING"),
  "c2_rigidity_three_route_zoomout_2026-07-20/STATUS_LEDGER.tsv":("zoom-out status ledger","CURRENT_EVIDENCE","scoped rigidity/open labels","no boundary selector promotion","STATUS_SCOPE"),
  "c2_rigidity_three_route_zoomout_2026-07-20/ROUTE_COMPARISON.tsv":("three-route comparison","CURRENT_EVIDENCE","omission and dependency comparison","no route chosen by physics","ROUTE_SCOPE"),
  "c2_rigidity_three_route_zoomout_2026-07-20/DERIVATION_RESULT.json":("zoom-out machine result","CURRENT_EVIDENCE","conditional scale and omission checks","inherits conditional C2 premises","PARENT_ALGEBRA"),
  "c2_rigidity_three_route_zoomout_2026-07-20/NEXT_SCIENTIFIC_DECISION.md":("authorized seam","CURRENT_NAVIGATION","defines finite-cell boundary question","not evidence for outcome","QUESTION_ONLY"),
  "c2_rigidity_three_route_zoomout_2026-07-20/COMPLETENESS_SCOPE.tsv":("zoom-out scope census","CURRENT_EVIDENCE","boundary/action/nonlinear omissions","omissions remain open","SCOPE_GATE")}
 fields=["id","path","role","authority","affirmative_use","prohibition","audit_ruling"]
 for path,values in additions.items():
  role,authority,use,prohibition,ruling=values
  by[path]={"path":path,"role":role,"authority":authority,"affirmative_use":use,"prohibition":prohibition,"audit_ruling":ruling}
 with (HERE/"SOURCE_CENSUS.tsv").open(encoding="utf-8",newline="") as h:census=list(csv.DictReader(h,delimiter="\t"))
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
 if expected!=set(by):raise AssertionError(f"mismatch missing={sorted(expected-set(by))} extra={sorted(set(by)-expected)}")
 with (HERE/"SOURCE_ADJUDICATION.tsv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for i,path in enumerate(sorted(by),1):
   row={k:by[path][k] for k in fields if k not in {"id","path"}};w.writerow({"id":f"R{i:02d}","path":path,**row})
 print(f"PASS rows={len(by)}")
if __name__=="__main__":main()
