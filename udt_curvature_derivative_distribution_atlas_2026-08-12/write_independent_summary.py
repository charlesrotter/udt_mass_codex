#!/usr/bin/env python3
"""Rebuild the independent summary from the saved replay table as strict JSON."""

import csv, json, math
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
with (HERE/"INDEPENDENT_COMPARISON.tsv").open(newline="",encoding="utf-8") as stream:
    rows=list(csv.DictReader(stream,delimiter="\t"))
projectors=[float(row["spi_projector_defect"]) for row in rows]
result={
    "schema":"udt-first-curvature-derivative-independent-v1",
    "status":"PASS" if all(row["pass"]=="TRUE" for row in rows) else "FAIL",
    "checks":len(rows),
    "pass_count":sum(row["pass"]=="TRUE" for row in rows),
    "max_tensor_relative_error":max(float(row["max_tensor_relative_error"]) for row in rows),
    "max_gradient_relative_error":max(float(row["gradient_relative_error"]) for row in rows),
    "max_finite_spi_projector_defect":max((x for x in projectors if math.isfinite(x)),default=0.0),
    "spi_projector_unmatched_count":sum(not math.isfinite(x) for x in projectors),
    "max_outer_ladder_difference":max(float(row["outer_ladder_max_difference"]) for row in rows),
    "spi_counts":dict(sorted(Counter(row["independent_spi"] for row in rows).items())),
}
(HERE/"INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
