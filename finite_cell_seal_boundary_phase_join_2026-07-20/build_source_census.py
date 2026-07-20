#!/usr/bin/env python3
"""Freeze the base-tree source census for the seal-to-boundary join audit."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/"c2_variable_lapse_selector_2026-07-20/build_source_census.py"
def main():
 spec=importlib.util.spec_from_file_location("seal_join_census_base",SOURCE)
 if spec is None or spec.loader is None:raise RuntimeError("cannot load census base")
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.BASE="55a2c53daade7282526581f20360f57aecfec12d";m.PACKAGE="finite_cell_seal_boundary_phase_join_2026-07-20/";m.HERE=Path(__file__).resolve().parent
 m.LOAD_BEARING=set(m.LOAD_BEARING)|{
  "c2_variable_lapse_selector_2026-07-20/AUDIT_REPORT.md","c2_variable_lapse_selector_2026-07-20/STATUS_LEDGER.tsv","c2_variable_lapse_selector_2026-07-20/EQUATION_LEDGER.tsv","c2_variable_lapse_selector_2026-07-20/DERIVATION_RESULT.json","c2_variable_lapse_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md","c2_variable_lapse_selector_2026-07-20/COMPLETENESS_SCOPE.tsv",
  "c2_time_fiber_shift_jacobi_2026-07-20/AUDIT_REPORT.md","c2_time_fiber_shift_jacobi_2026-07-20/STATUS_LEDGER.tsv","c2_time_fiber_shift_jacobi_2026-07-20/EQUATION_LEDGER.tsv","c2_time_fiber_shift_jacobi_2026-07-20/DERIVATION_RESULT.json","c2_time_fiber_shift_jacobi_2026-07-20/NEXT_SCIENTIFIC_DECISION.md","c2_time_fiber_shift_jacobi_2026-07-20/COMPLETENESS_SCOPE.tsv",
  "c2_rigidity_three_route_zoomout_2026-07-20/AUDIT_REPORT.md","c2_rigidity_three_route_zoomout_2026-07-20/STATUS_LEDGER.tsv","c2_rigidity_three_route_zoomout_2026-07-20/ROUTE_COMPARISON.tsv","c2_rigidity_three_route_zoomout_2026-07-20/DERIVATION_RESULT.json","c2_rigidity_three_route_zoomout_2026-07-20/NEXT_SCIENTIFIC_DECISION.md","c2_rigidity_three_route_zoomout_2026-07-20/COMPLETENESS_SCOPE.tsv",
  "c2_finite_cell_boundary_variation_2026-07-20/AUDIT_REPORT.md","c2_finite_cell_boundary_variation_2026-07-20/STATUS_LEDGER.tsv","c2_finite_cell_boundary_variation_2026-07-20/EQUATION_LEDGER.tsv","c2_finite_cell_boundary_variation_2026-07-20/BOUNDARY_CLASS_LEDGER.tsv","c2_finite_cell_boundary_variation_2026-07-20/CONVENTION_LEDGER.tsv","c2_finite_cell_boundary_variation_2026-07-20/DERIVATION_RESULT.json","c2_finite_cell_boundary_variation_2026-07-20/NEXT_SCIENTIFIC_DECISION.md","c2_finite_cell_boundary_variation_2026-07-20/COMPLETENESS_SCOPE.tsv",
  "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md","udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
  "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md","copresence_causal_accessibility_selector_2026-07-19/STATUS_LEDGER.tsv",
  "copresence_gr_constraint_regrade_2026-07-19/DERIVATION_REPORT.md","copresence_gr_constraint_regrade_2026-07-19/RECLASSIFICATION_TABLE.tsv",
  "native_action_final_adjudication_2026-07-18/MECHANICAL_AGREEMENT_DISAGREEMENT.tsv"}
 m.main()
if __name__=="__main__":main()
