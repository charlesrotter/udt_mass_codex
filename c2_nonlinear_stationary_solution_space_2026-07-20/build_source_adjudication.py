#!/usr/bin/env python3
"""Build explicit adjudication for every load-bearing stationary-space source."""
from __future__ import annotations
import csv,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
BASE="786d00a05a4475fcd8495645d39ee2897f5185b3";PARENT="complete_coframe_seal_involution_2026-07-20/SOURCE_ADJUDICATION.tsv"
ADDITIONS={
 "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md":("immediate parent audit","CURRENT_EVIDENCE","multiple complete conditional coframe lifts and missing selector","no physical lift or boundary promotion","PARENT_COFRAME_FORK"),
 "complete_coframe_seal_involution_2026-07-20/STATUS_LEDGER.tsv":("parent status ledger","CURRENT_EVIDENCE","exact founded conditional and open labels","no unique completion promotion","STATUS_SCOPE"),
 "complete_coframe_seal_involution_2026-07-20/NEXT_SCIENTIFIC_DECISION.md":("authorized solution-space seam","CURRENT_NAVIGATION","comparative nonlinear branch question","not evidence for outcome","QUESTION_ONLY"),
 "complete_coframe_seal_involution_2026-07-20/BLOCK_REALIZATION_LEDGER.tsv":("block realization census","CURRENT_EVIDENCE","diagonal obstruction and conditional K family","K-as-physical metric remains chosen","BLOCK_FORK"),
 "complete_coframe_seal_involution_2026-07-20/EXTENSION_FAMILY_LEDGER.tsv":("extension family census","CURRENT_EVIDENCE","angular normal time and global alternatives","none selected","EXTENSION_FORK"),
 "complete_coframe_seal_involution_2026-07-20/COMPLETE_EXTENSION_WITNESSES.tsv":("complete witness census","CURRENT_EVIDENCE","inequivalent conditional lifts","witnesses are not realized universes","WITNESS_SCOPE"),
 "complete_coframe_seal_involution_2026-07-20/REQUIREMENT_MATRIX.tsv":("completion requirements","CURRENT_EVIDENCE","ten physical completion gates","open gates stay open","SCOPE_GATE"),
 "complete_coframe_seal_involution_2026-07-20/DERIVATION_RESULT.json":("parent exact output","CURRENT_EVIDENCE","matrix and angular involution classification","not a nonlinear solution theorem","PARENT_ALGEBRA"),
}
def main():
 raw=subprocess.check_output(["git","show",f"{BASE}:{PARENT}"],cwd=ROOT,text=True);old=list(csv.DictReader(raw.splitlines(),delimiter="\t"));by={r["path"]:r for r in old}
 for path,v in ADDITIONS.items():
  role,authority,use,prohibition,ruling=v;by[path]={"path":path,"role":role,"authority":authority,"affirmative_use":use,"prohibition":prohibition,"audit_ruling":ruling}
 with (HERE/"SOURCE_CENSUS.tsv").open(encoding="utf-8",newline="") as h:census=list(csv.DictReader(h,delimiter="\t"))
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
 if expected!=set(by):raise AssertionError(f"mismatch missing={sorted(expected-set(by))} extra={sorted(set(by)-expected)}")
 fields=["id","path","role","authority","affirmative_use","prohibition","audit_ruling"]
 with (HERE/"SOURCE_ADJUDICATION.tsv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for i,path in enumerate(sorted(by),1):
   r=by[path];w.writerow({"id":f"R{i:03d}","path":path,**{k:r[k] for k in fields if k not in {"id","path"}}})
 print(f"PASS rows={len(by)}")
if __name__=="__main__":main()
