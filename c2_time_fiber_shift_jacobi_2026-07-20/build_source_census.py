#!/usr/bin/env python3
"""Freeze the base-tree source census for the shift Jacobi audit."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"c2_variable_lapse_selector_2026-07-20/build_source_census.py"


def main() -> None:
    spec=importlib.util.spec_from_file_location("shift_census_base",SOURCE)
    if spec is None or spec.loader is None: raise RuntimeError("cannot load census base")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module.BASE="61f6bc01e5732b3bc59120d506bd6b2716646369"
    module.PACKAGE="c2_time_fiber_shift_jacobi_2026-07-20/"
    module.HERE=Path(__file__).resolve().parent
    module.LOAD_BEARING=set(module.LOAD_BEARING)|{
        "c2_variable_lapse_selector_2026-07-20/AUDIT_REPORT.md",
        "c2_variable_lapse_selector_2026-07-20/STATUS_LEDGER.tsv",
        "c2_variable_lapse_selector_2026-07-20/EQUATION_LEDGER.tsv",
        "c2_variable_lapse_selector_2026-07-20/DERIVATION_RESULT.json",
        "c2_variable_lapse_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md",
        "c2_variable_lapse_selector_2026-07-20/COMPLETENESS_SCOPE.tsv",
    }
    module.main()


if __name__=="__main__": main()
