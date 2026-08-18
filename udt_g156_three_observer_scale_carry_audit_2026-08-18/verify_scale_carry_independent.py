#!/usr/bin/env python3
"""Independent exact-rational replay for G156; imports no production code."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "b42c771d"
QUALIFIED_LANDING = (
    "PAIR_METRIC_CANONICALLY_SUPPLIES_POSITIVE_HALF_DENSITY_SECTION__"
    "ANY_SUPPLIED_TYPED_CARRY_INDUCES_GAUGE_INVARIANT_LOG_DETERMINANT_CHARACTER__"
    "FULL_CLOSURE_IMPLIES_BUT_IS_NOT_IMPLIED_BY_SCALE_CLOSURE__"
    "OWNED_CHART_OVERLAP_AND_LEVI_CIVITA_CARRIES_ARE_SCALE_FLAT__"
    "ARBITRARY_SUPPLIED_NONISOMETRIC_CARRIES_NEED_NOT_BE_FLAT__"
    "NO_METRIC_OWNED_CROSS_QUERY_CARRY_OR_KAPPA_HISTORY"
)


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a):
    d = det(a)
    assert d != 0
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def tri(a, n, d):
    return [[F(a), F(n)], [F(0), F(d)]]


def eq(a, b):
    return all(a[i][j] == b[i][j] for i in range(2) for j in range(2))


def manifest_rows():
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest(rows):
    assert len(rows) == 19
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"])
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]


def main():
    rows = manifest_rows()
    verify_manifest(rows)
    rng = random.Random(156)
    trials = 500

    for _ in range(trials):
        RA = tri(rng.randint(1, 9), rng.randint(-5, 5), rng.randint(1, 9))
        RB = tri(rng.randint(1, 9), rng.randint(-5, 5), rng.randint(1, 9))
        RC = tri(rng.randint(1, 9), rng.randint(-5, 5), rng.randint(1, 9))
        MBA = tri(rng.randint(1, 9), rng.randint(-5, 5), rng.randint(1, 9))
        MCB = tri(rng.randint(1, 9), rng.randint(-5, 5), rng.randint(1, 9))
        MCA = mm(MCB, MBA)

        CBA = mm(mm(RB, MBA), inv(RA))
        CCB = mm(mm(RC, MCB), inv(RB))
        CCA = mm(mm(RC, MCA), inv(RA))
        assert eq(mm(CCB, CBA), CCA)
        assert det(CCB) * det(CBA) == det(CCA)

        # Endpoint gauge covariance.
        PA = tri(rng.randint(1, 9), rng.randint(-5, 5), rng.randint(1, 9))
        PB = tri(rng.randint(1, 9), rng.randint(-5, 5), rng.randint(1, 9))
        RAp = mm(RA, PA)
        RBp = mm(RB, PB)
        MBAp = mm(mm(inv(PB), MBA), PA)
        CBAp = mm(mm(RBp, MBAp), inv(RAp))
        assert eq(CBAp, CBA)

        # Squared half-density scale factor equals det(total comparison).
        expected_det = det(RB) * det(MBA) / det(RA)
        assert det(CBA) == expected_det

    # Scale closure is strictly weaker than matrix closure.
    I = tri(1, 0, 1)
    shear = tri(1, 1, 1)
    assert det(I) * det(I) == det(shear)
    assert not eq(mm(I, I), shear)

    # A deliberately inconsistent direct carry has nonzero scalar defect.
    dilation = tri(2, 0, 1)
    assert det(I) * det(I) / det(dilation) == F(1, 2)

    # Chart Jacobian carries telescope exactly.
    JA, JB, JC = tri(2, 1, 3), tri(5, 2, 7), tri(11, 3, 13)
    chart_BA = mm(JB, inv(JA))
    chart_CB = mm(JC, inv(JB))
    chart_CA = mm(JC, inv(JA))
    assert eq(mm(chart_CB, chart_BA), chart_CA)

    result = {
        "status": "PASS",
        "method": "stdlib_fraction_exact_no_production_import",
        "source_count": len(rows),
        "randomized_exact_trials": trials,
        "gauge_trials": trials,
        "composition_trials": trials,
        "half_density_determinant_trials": trials,
        "sl2_kernel_counterexample": True,
        "nonzero_scale_defect_witness": "1/2",
        "landing": QUALIFIED_LANDING,
        "registered_outcome_class": "CONDITIONAL_FLAT_SCALE_CARRY",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
