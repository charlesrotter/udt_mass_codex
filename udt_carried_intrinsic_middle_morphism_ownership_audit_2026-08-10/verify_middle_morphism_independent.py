#!/usr/bin/env python3
"""Independent Fraction-based verifier; imports no production derivation code."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def eye() -> list[list[F]]:
    return [[F(int(i == j)) for j in range(4)] for i in range(4)]


def mm(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] - b[i][j] for j in range(4)] for i in range(4)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def diag(values: list[F]) -> list[list[F]]:
    return [[values[i] if i == j else F(0) for j in range(4)] for i in range(4)]


def zero(a: list[list[F]]) -> bool:
    return all(value == 0 for row in a for value in row)


def conjugate(a: list[list[F]], x: list[list[F]], ainv: list[list[F]]) -> list[list[F]]:
    return mm(mm(a, x), ainv)


def main() -> None:
    eta = diag([F(-1), F(1), F(1), F(1)])
    ident = eye()
    pu = diag([F(1), F(0), F(0), F(0)])
    pn = diag([F(0), F(1), F(0), F(0)])
    hs = diag([F(0), F(0), F(1), F(1)])

    b = eye()
    b[0][0] = b[1][1] = F(5, 4)
    b[0][1] = b[1][0] = F(3, 4)
    binv = eye()
    binv[0][0] = binv[1][1] = F(5, 4)
    binv[0][1] = binv[1][0] = F(-3, 4)
    r = eye()
    r[2][2] = r[3][3] = F(0)
    r[2][3] = F(-1)
    r[3][2] = F(1)
    m0 = binv
    m1 = mm(r, binv)

    b02 = eye()
    b02[0][0] = b02[2][2] = F(5, 4)
    b02[0][2] = b02[2][0] = F(3, 4)
    b02inv = eye()
    b02inv[0][0] = b02inv[2][2] = F(5, 4)
    b02inv[0][2] = b02inv[2][0] = F(-3, 4)

    assert zero(sub(mm(mm(transpose(b), eta), b), eta))
    assert zero(sub(mm(b, binv), ident))
    assert zero(sub(mm(mm(transpose(r), eta), r), eta))
    assert m0 != m1

    # Independent balanced-product control for three reduction torsors.
    r2 = mm(r, r)
    m12 = mm(b, r)
    m23 = mm(mm(b02, r2), binv)
    m13 = mm(m23, m12)
    h2 = mm(mm(b, r), binv)
    h2inv = mm(mm(b, transpose(r)), binv)
    assert mm(mm(m23, h2), mm(h2inv, m12)) == m13
    for projector in (pu, pn, hs):
        reduction3 = conjugate(b02, projector, b02inv)
        assert conjugate(m13, projector, mm(mm(transpose(r), transpose(r2)), b02inv)) == reduction3

    lambdas = [F(-2), F(-1), F(0), F(1, 2), F(1), F(2)]
    rows = []
    for lam in lambdas:
        x = diag([F(-1), F(1), lam, lam])
        xc = conjugate(b, x, binv)
        assert xc != x
        for m in (m0, m1):
            minv = b if m == m0 else mm(b, transpose(r))
            assert conjugate(m, xc, minv) == x
            for projector in (pu, pn, hs):
                carried = conjugate(b, projector, binv)
                assert conjugate(m, carried, minv) == projector

        # Independent analytic count: a Lorentz generator in plane ij commutes iff x_i=x_j.
        eig = [F(-1), F(1), lam, lam]
        generator_planes = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        grading_dim = sum(eig[i] == eig[j] for i, j in generator_planes)
        flag_labels = [0, 1, 2, 2]
        flag_dim = sum(flag_labels[i] == flag_labels[j] for i, j in generator_planes)
        assert grading_dim == (3 if lam in (F(-1), F(1)) else 1)
        assert flag_dim == 1
        rows.append((str(lam), grading_dim, flag_dim))

    with (HERE / "SOURCE_MANIFEST.tsv").open() as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    assert len(manifest) == 18
    for row in manifest:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
        blob = subprocess.check_output(["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True).strip()
        assert blob == row["git_blob"]

    with (ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOCAL_NABLA_X.tsv").open() as handle:
        local = list(csv.DictReader(handle, delimiter="\t"))
    with (ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOOP_HOLONOMY.tsv").open() as handle:
        loops = list(csv.DictReader(handle, delimiter="\t"))
    assert len(local) == 18 and all(float(row["clock_ruler"]) > 0 for row in local)
    assert len(loops) == 36 and all(float(row["nonidentity_max"]) > 1e-10 for row in loops)
    assert all(float(row["ordinary_closure_residual"]) > 1e-10 for row in loops)
    assert all(float(row["composition_residual"]) < 1e-10 for row in loops)

    result = {
        "verdict": "VERIFIED",
        "method": "independent pure-Python Fraction matrices plus analytic generator count",
        "lambda_rows": rows,
        "distinct_alignment_witnesses": 2,
        "source_hashes_verified": len(manifest),
        "local_nonparallel_rows": len(local),
        "loop_path_label_rows": len(loops),
        "balanced_bitorsor_composition_exact": True,
        "primary_landing_reproduced": "GAUGE_GROUPOID_ALREADY_SUFFICIENT_FOR_PROJECTOR_ALIGNMENT__CALIBRATION_DESCENT_OPEN",
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
