#!/usr/bin/env python3
"""Freeze the base-tree source census for the complete-coframe involution audit."""
from __future__ import annotations
import csv,importlib.util,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
BASE="5b1b57297bcceb5f8806b1ee238ac2ed2ccfcee3";PACKAGE="complete_coframe_seal_involution_2026-07-20/"
PARENT="finite_cell_seal_boundary_phase_join_2026-07-20/SOURCE_ADJUDICATION.tsv"
ADDITIONS={
 "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md",
 "finite_cell_seal_boundary_phase_join_2026-07-20/STATUS_LEDGER.tsv",
 "finite_cell_seal_boundary_phase_join_2026-07-20/DERIVATION_RESULT.json",
 "finite_cell_seal_boundary_phase_join_2026-07-20/NEXT_SCIENTIFIC_DECISION.md",
 "finite_cell_seal_boundary_phase_join_2026-07-20/SLOT_COVERAGE.tsv",
 "finite_cell_seal_boundary_phase_join_2026-07-20/STRONGEST_JOIN_CHALLENGES.tsv",
 "finite_cell_seal_boundary_phase_join_2026-07-20/CLAUSE_TO_BOUNDARY_SLOT.tsv",
 "finite_cell_seal_boundary_phase_join_2026-07-20/OUTCOME_BRANCH_LEDGER.tsv",
 "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md",
 "transverse_reciprocal_realization_selector_2026-07-19/STATUS_LEDGER.tsv",
 "transverse_reciprocal_realization_selector_2026-07-19/DERIVATION_RESULT.json",
 "transverse_reciprocal_realization_selector_2026-07-19/CANDIDATE_FAMILY.tsv",
}
def main():
 raw=subprocess.check_output(["git","show",f"{BASE}:{PARENT}"],cwd=ROOT,text=True)
 inherited={r["path"] for r in csv.DictReader(raw.splitlines(),delimiter="\t")}
 source=ROOT/"c2_variable_lapse_selector_2026-07-20/build_source_census.py"
 spec=importlib.util.spec_from_file_location("coframe_census_base",source)
 if spec is None or spec.loader is None:raise RuntimeError("cannot load census base")
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.BASE=BASE;m.PACKAGE=PACKAGE;m.HERE=HERE;m.LOAD_BEARING=inherited|ADDITIONS;m.main()
if __name__=="__main__":main()
