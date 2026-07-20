#!/usr/bin/env python3
"""Fail-closed primary summary of the preregistered raw stationary-space census."""
from __future__ import annotations
import csv,json
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(name,condition,checks):
 if not bool(condition):raise AssertionError(name)
 checks[name]="PASS"
def main():
 raw=json.loads((HERE/"RAW_ATTEMPTS.json").read_text());checks={};attempts=raw["attempts"]
 need("raw_schema",raw["schema"]=="udt-c2-nonlinear-stationary-galerkin-census-1.0",checks)
 need("complete_budget",raw["result"]=="COMPLETE_WITHIN_BUDGET" and raw["coverage"]=={"attempted":198,"planned":198,"stopped_by_global_budget":False},checks)
 controls=raw["controls"];need("frozen_orders",controls["orders"]==[2,4],checks);need("frozen_sectors",controls["sectors"]==["GENERAL","SEAL_EVEN","SEAL_ODD_W"],checks)
 need("frozen_grids",controls["nodes"]==48 and controls["validation_nodes"]==96,checks);need("frozen_tolerances",controls["solve_tolerance"]==1e-9 and controls["validation_tolerance"]==1e-7,checks)
 statuses=Counter(a["status"] for a in attempts);need("status_counts",statuses=={"SOLVE_RESIDUAL_PASS":147,"NO_RESIDUAL_DECREASING_NEWTON_STEP":51},checks)
 by=defaultdict(list)
 for a in attempts:by[(a["order"],a["sector"])].append(a)
 need("six_strata",len(by)==6 and all(len(v)==33 for v in by.values()),checks)
 for key,items in by.items():
  seed_ids=[a["seed_id"] for a in items];need(f"unique_seeds_{key}",len(seed_ids)==len(set(seed_ids))==33,checks)
 passed=[a for a in attempts if a["status"]=="SOLVE_RESIDUAL_PASS"];failed=[a for a in attempts if a["status"]!="SOLVE_RESIDUAL_PASS"]
 need("all_raw_passes_below_gate",max(a["raw_residual_inf"] for a in passed)<=1e-9,checks)
 need("all_raw_passes_validated",all(a["validation"]["result"]=="PASS" for a in passed),checks)
 need("all_higher_projections_below_gate",max(a["validation"]["raw_projected_residual_inf"] for a in passed)<=1e-7,checks)
 max_norm=max(a["coefficient_norm"] for a in passed);need("all_certified_roots_round",max_norm<=1e-6,checks)
 need("unresolved_not_mislabeled",len(failed)==51 and min(a["raw_residual_inf"] for a in failed)>1e-3,checks)
 clusters=raw["clusters"];need("one_cluster_per_stratum",len(clusters)==6 and {(c["order"],c["sector"]) for c in clusters}==set(by),checks)
 need("all_clusters_round",all(c["classification"]=="ROUND_GAUGE_FIXED_ORBIT" and c["coefficient_norm"]==0 for c in clusters),checks)
 need("cluster_seed_total",sum(len(c["seed_ids"]) for c in clusters)==147,checks)
 fields=["order","sector","attempts","raw_passes","validation_passes","unresolved","max_pass_residual","max_validation_residual","min_unresolved_residual"]
 with (HERE/"ATTEMPT_CENSUS.tsv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for (order,sector),items in sorted(by.items()):
   ok=[a for a in items if a["status"]=="SOLVE_RESIDUAL_PASS"];bad=[a for a in items if a["status"]!="SOLVE_RESIDUAL_PASS"]
   w.writerow({"order":order,"sector":sector,"attempts":len(items),"raw_passes":len(ok),"validation_passes":sum(a["validation"]["result"]=="PASS" for a in ok),"unresolved":len(bad),"max_pass_residual":max(a["raw_residual_inf"] for a in ok),"max_validation_residual":max(a["validation"]["raw_projected_residual_inf"] for a in ok),"min_unresolved_residual":min((a["raw_residual_inf"] for a in bad),default="-")})
 with (HERE/"CLUSTER_LEDGER.tsv").open("w",encoding="utf-8",newline="") as h:
  fields=["cluster_id","order","sector","classification","coefficient_norm","seed_count","representative_coefficients"]
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for c in clusters:w.writerow({"cluster_id":c["cluster_id"],"order":c["order"],"sector":c["sector"],"classification":c["classification"],"coefficient_norm":c["coefficient_norm"],"seed_count":len(c["seed_ids"]),"representative_coefficients":json.dumps(c["representative_coefficients"],separators=(",",":"))})
 with (HERE/"UNRESOLVED_BASIN_LEDGER.tsv").open("w",encoding="utf-8",newline="") as h:
  fields=["id","order","sector","seed_id","status","initial_norm","final_norm","raw_residual_inf","iterations","elapsed_seconds"]
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for i,a in enumerate(failed,1):w.writerow({"id":f"U{i:02d}","order":a["order"],"sector":a["sector"],"seed_id":a["seed_id"],"status":a["status"],"initial_norm":sum(x*x for x in a["initial_coefficients"])**.5,"final_norm":a["coefficient_norm"],"raw_residual_inf":a["raw_residual_inf"],"iterations":a["iterations"],"elapsed_seconds":a["elapsed_seconds"]})
 result={"schema":"udt-c2-nonlinear-stationary-solution-space-summary-1.0","result":"PASS","checks":checks,"raw_counts":{"attempts":198,"certified_reduced_roots":147,"unresolved_attempt_basins":51,"strata":6,"clusters":6},"residuals":{"max_solve_pass":max(a["raw_residual_inf"] for a in passed),"max_higher_mode_validation":max(a["validation"]["raw_projected_residual_inf"] for a in passed),"min_unresolved":min(a["raw_residual_inf"] for a in failed)},"certified_root_max_coefficient_norm":max_norm,"primary_observation":"ONLY_ROUND_COORDINATE_CSN_ORBIT_OBSERVED_AMONG_147_CERTIFIED_ROOTS_IN_BOUNDED_SEARCH","solver_caveat":"51_PREREGISTERED_ATTEMPT_BASINS_UNRESOLVED; NO_BRANCH_EXCLUSION","coframe_ruling":"METRIC_ONLY_C2_CANNOT_DISTINGUISH_COFRAME_LIFTS_WITH_IDENTICAL_METRIC_PULLBACK","maximum_conclusion":"BROAD_ROUND_BASIN_OBSERVED_IN_CONDITIONAL_SMOOTH_CAP_TORIC_STATIONARY_C2_GALERKIN_TILE; DISCONNECTED_LARGE_AMPLITUDE_PHYSICAL_BOUNDARY_NONTORIC_TIME_LIVE_ACTION_AND_UDT_COMPLETION_OPEN","compute":{"cpu_only":True,"gpu_used":False}}
 (HERE/"SUMMARY_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");print(json.dumps({"result":"PASS","checks":len(checks),"attempts":198,"certified":147,"unresolved":51,"observation":result["primary_observation"]},sort_keys=True))
if __name__=="__main__":main()
