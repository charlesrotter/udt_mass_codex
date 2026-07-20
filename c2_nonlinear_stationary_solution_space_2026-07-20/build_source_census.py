#!/usr/bin/env python3
"""Freeze the base-tree source census for the nonlinear stationary solution-space tile."""
from __future__ import annotations
import csv,importlib.util,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
BASE="786d00a05a4475fcd8495645d39ee2897f5185b3";PACKAGE="c2_nonlinear_stationary_solution_space_2026-07-20/"
PARENT="complete_coframe_seal_involution_2026-07-20/SOURCE_ADJUDICATION.tsv"
ADDITIONS={
 "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md",
 "complete_coframe_seal_involution_2026-07-20/STATUS_LEDGER.tsv",
 "complete_coframe_seal_involution_2026-07-20/NEXT_SCIENTIFIC_DECISION.md",
 "complete_coframe_seal_involution_2026-07-20/BLOCK_REALIZATION_LEDGER.tsv",
 "complete_coframe_seal_involution_2026-07-20/EXTENSION_FAMILY_LEDGER.tsv",
 "complete_coframe_seal_involution_2026-07-20/COMPLETE_EXTENSION_WITNESSES.tsv",
 "complete_coframe_seal_involution_2026-07-20/REQUIREMENT_MATRIX.tsv",
 "complete_coframe_seal_involution_2026-07-20/DERIVATION_RESULT.json",
}
def main():
 raw=subprocess.check_output(["git","show",f"{BASE}:{PARENT}"],cwd=ROOT,text=True);inherited={r["path"] for r in csv.DictReader(raw.splitlines(),delimiter="\t")}
 source=ROOT/"c2_variable_lapse_selector_2026-07-20/build_source_census.py";spec=importlib.util.spec_from_file_location("stationary_census_base",source)
 if spec is None or spec.loader is None:raise RuntimeError("cannot load census base")
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.BASE=BASE;m.PACKAGE=PACKAGE;m.HERE=HERE;m.LOAD_BEARING=inherited|ADDITIONS;m.main()
if __name__=="__main__":main()
