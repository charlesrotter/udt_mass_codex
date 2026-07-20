#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Load the stable implementation and add both later parent layers explicitly.
parent_source=ROOT/"c2_variable_lapse_selector_2026-07-20/build_source_census.py"
pspec=importlib.util.spec_from_file_location("zoom_parent_census",parent_source)
if pspec is None or pspec.loader is None: raise RuntimeError("cannot load parent census")
parent=importlib.util.module_from_spec(pspec); pspec.loader.exec_module(parent)
parent.BASE="f68c51aa79d65805da23fc5845576f87ef310d4f"; parent.PACKAGE="c2_rigidity_three_route_zoomout_2026-07-20/"
parent.HERE=Path(__file__).resolve().parent
parent.LOAD_BEARING=set(parent.LOAD_BEARING)|{
"c2_variable_lapse_selector_2026-07-20/AUDIT_REPORT.md","c2_variable_lapse_selector_2026-07-20/STATUS_LEDGER.tsv",
"c2_variable_lapse_selector_2026-07-20/EQUATION_LEDGER.tsv","c2_variable_lapse_selector_2026-07-20/DERIVATION_RESULT.json",
"c2_variable_lapse_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md","c2_variable_lapse_selector_2026-07-20/COMPLETENESS_SCOPE.tsv",
"c2_time_fiber_shift_jacobi_2026-07-20/AUDIT_REPORT.md","c2_time_fiber_shift_jacobi_2026-07-20/STATUS_LEDGER.tsv",
"c2_time_fiber_shift_jacobi_2026-07-20/EQUATION_LEDGER.tsv","c2_time_fiber_shift_jacobi_2026-07-20/DERIVATION_RESULT.json",
"c2_time_fiber_shift_jacobi_2026-07-20/NEXT_SCIENTIFIC_DECISION.md","c2_time_fiber_shift_jacobi_2026-07-20/COMPLETENESS_SCOPE.tsv"}
parent.main()
