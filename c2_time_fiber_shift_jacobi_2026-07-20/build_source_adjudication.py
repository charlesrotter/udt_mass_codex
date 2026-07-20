#!/usr/bin/env python3
"""Build explicit one-row-per-load-bearing-source adjudication."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/"c2_variable_lapse_selector_2026-07-20/build_source_adjudication.py"


def main() -> None:
    spec=importlib.util.spec_from_file_location("shift_adjudication_base",SOURCE)
    if spec is None or spec.loader is None: raise RuntimeError("cannot load adjudication base")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    additions={
        "c2_variable_lapse_selector_2026-07-20/AUDIT_REPORT.md":("immediate parent audit","CURRENT_EVIDENCE","positive lapse/CSN classification","static diagonal and compact caveats remain","PARENT_RESULT"),
        "c2_variable_lapse_selector_2026-07-20/STATUS_LEDGER.tsv":("parent status ledger","CURRENT_EVIDENCE","conditional lapse labels","no nonlinear shift or matter promotion","STATUS_SCOPE"),
        "c2_variable_lapse_selector_2026-07-20/EQUATION_LEDGER.tsv":("parent equations","CURRENT_EVIDENCE","conformal reduction and orbit matching","no time/fiber shift equation","PARENT_ALGEBRA"),
        "c2_variable_lapse_selector_2026-07-20/DERIVATION_RESULT.json":("parent exact output","CURRENT_EVIDENCE","lapse curvature checks","inherits fixed-basis compact premises","PARENT_ALGEBRA"),
        "c2_variable_lapse_selector_2026-07-20/NEXT_SCIENTIFIC_DECISION.md":("authorized seam","CURRENT_NAVIGATION","defines time/fiber connection question","not evidence for outcome","QUESTION_ONLY"),
        "c2_variable_lapse_selector_2026-07-20/COMPLETENESS_SCOPE.tsv":("parent scope census","CURRENT_EVIDENCE","shift/time-live omission","omissions remain open","SCOPE_GATE"),
    }
    adjudications={**module.ROWS,**additions}
    with (HERE/"SOURCE_CENSUS.tsv").open(encoding="utf-8",newline="") as handle:
        census=list(csv.DictReader(handle,delimiter="\t"))
    expected={row["path"] for row in census if row["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
    if expected!=set(adjudications):
        raise AssertionError(f"mismatch missing={sorted(expected-set(adjudications))} extra={sorted(set(adjudications)-expected)}")
    fields=["id","path","role","authority","affirmative_use","prohibition","audit_ruling"]
    with (HERE/"SOURCE_ADJUDICATION.tsv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=fields,delimiter="\t",lineterminator="\n"); writer.writeheader()
        for index,path in enumerate(sorted(adjudications),1):
            role,authority,use,prohibition,ruling=adjudications[path]
            writer.writerow({"id":f"R{index:02d}","path":path,"role":role,"authority":authority,
                "affirmative_use":use,"prohibition":prohibition,"audit_ruling":ruling})
    print(f"PASS rows={len(adjudications)}")


if __name__=="__main__": main()
