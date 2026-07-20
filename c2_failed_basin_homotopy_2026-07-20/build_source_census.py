#!/usr/bin/env python3
from __future__ import annotations
import csv,importlib.util,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;BASE="33eaed961d4601019ee59df5ee8aa59fdc105353";PACKAGE="c2_failed_basin_homotopy_2026-07-20/";PARENT="c2_nonlinear_stationary_solution_space_2026-07-20/SOURCE_ADJUDICATION.tsv"
ADDITIONS={f"c2_nonlinear_stationary_solution_space_2026-07-20/{x}" for x in ["PREREGISTRATION.md","AUDIT_REPORT.md","STATUS_LEDGER.tsv","NEXT_SCIENTIFIC_DECISION.md","RAW_ATTEMPTS.json","SUMMARY_RESULT.json","ATTEMPT_CENSUS.tsv","UNRESOLVED_BASIN_LEDGER.tsv","COMPLETENESS_MAP.tsv","stationary_c2_engine.py","explore_stationary_space.py","VERIFICATION_RESULT.json"]}
def main():
 raw=subprocess.check_output(["git","show",f"{BASE}:{PARENT}"],cwd=ROOT,text=True);inherited={r["path"] for r in csv.DictReader(raw.splitlines(),delimiter="\t")};source=ROOT/"c2_variable_lapse_selector_2026-07-20/build_source_census.py";spec=importlib.util.spec_from_file_location("homotopy_census_base",source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.BASE=BASE;m.PACKAGE=PACKAGE;m.HERE=HERE;m.LOAD_BEARING=inherited|ADDITIONS;m.main()
if __name__=="__main__":main()
