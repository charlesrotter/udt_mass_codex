#!/usr/bin/env python3
from __future__ import annotations
import csv,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; HERE=Path(__file__).resolve().parent
source=ROOT/"c2_time_fiber_shift_jacobi_2026-07-20/build_source_adjudication.py"
# Load the variable-lapse adjudication base, then add both later parent layers explicitly.
base_source=ROOT/"c2_variable_lapse_selector_2026-07-20/build_source_adjudication.py"
spec=importlib.util.spec_from_file_location("zoom_adjudication_base",base_source)
if spec is None or spec.loader is None: raise RuntimeError("cannot load adjudication base")
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
additions={
"c2_variable_lapse_selector_2026-07-20/AUDIT_REPORT.md":("variable-lapse audit","CURRENT_EVIDENCE","diagonal lapse rigidity and CSN copy","bounded compact branch only","RIGIDITY_INPUT"),
"c2_variable_lapse_selector_2026-07-20/STATUS_LEDGER.tsv":("variable-lapse ledger","CURRENT_EVIDENCE","exact scoped labels","no UDT-wide promotion","STATUS_SCOPE"),
"c2_variable_lapse_selector_2026-07-20/EQUATION_LEDGER.tsv":("variable-lapse equations","CURRENT_EVIDENCE","conformal reduction","boundary/shift open","CONDITIONAL_ALGEBRA"),
"c2_variable_lapse_selector_2026-07-20/DERIVATION_RESULT.json":("variable-lapse output","CURRENT_EVIDENCE","exact curvature result","inherits premises","CONDITIONAL_ALGEBRA"),
"c2_variable_lapse_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md":("parent navigation","CURRENT_NAVIGATION","time/fiber seam","not outcome authority","QUESTION_HISTORY"),
"c2_variable_lapse_selector_2026-07-20/COMPLETENESS_SCOPE.tsv":("variable-lapse scope","CURRENT_EVIDENCE","omitted layers","omissions remain open","SCOPE_GATE"),
"c2_time_fiber_shift_jacobi_2026-07-20/AUDIT_REPORT.md":("immediate parent audit","CURRENT_EVIDENCE","shift Jacobi rigidity and mandatory zoom-out","linear compact branch only","RIGIDITY_INPUT"),
"c2_time_fiber_shift_jacobi_2026-07-20/STATUS_LEDGER.tsv":("shift status ledger","CURRENT_EVIDENCE","exact scoped labels","no nonlinear promotion","STATUS_SCOPE"),
"c2_time_fiber_shift_jacobi_2026-07-20/EQUATION_LEDGER.tsv":("shift equations","CURRENT_EVIDENCE","Weyl/Bach Jacobi operator","Jacobi order only","CONDITIONAL_ALGEBRA"),
"c2_time_fiber_shift_jacobi_2026-07-20/DERIVATION_RESULT.json":("shift exact output","CURRENT_EVIDENCE","kernel and Bach projection","inherits compact round premises","CONDITIONAL_ALGEBRA"),
"c2_time_fiber_shift_jacobi_2026-07-20/NEXT_SCIENTIFIC_DECISION.md":("authorized zoom-out seam","CURRENT_NAVIGATION","defines three-route comparison","not evidence for outcome","QUESTION_ONLY"),
"c2_time_fiber_shift_jacobi_2026-07-20/COMPLETENESS_SCOPE.tsv":("shift scope census","CURRENT_EVIDENCE","nonlinear/boundary/domain omissions","omissions remain open","SCOPE_GATE")}
adjudications={**module.ROWS,**additions}
with (HERE/"SOURCE_CENSUS.tsv").open(encoding="utf-8",newline="") as handle: census=list(csv.DictReader(handle,delimiter="\t"))
expected={row["path"] for row in census if row["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
if expected!=set(adjudications): raise AssertionError(f"mismatch missing={sorted(expected-set(adjudications))} extra={sorted(set(adjudications)-expected)}")
fields=["id","path","role","authority","affirmative_use","prohibition","audit_ruling"]
with (HERE/"SOURCE_ADJUDICATION.tsv").open("w",encoding="utf-8",newline="") as handle:
    writer=csv.DictWriter(handle,fieldnames=fields,delimiter="\t",lineterminator="\n"); writer.writeheader()
    for index,path in enumerate(sorted(adjudications),1):
        role,authority,use,prohibition,ruling=adjudications[path]
        writer.writerow({"id":f"R{index:02d}","path":path,"role":role,"authority":authority,
            "affirmative_use":use,"prohibition":prohibition,"audit_ruling":ruling})
print(f"PASS rows={len(adjudications)}")
