#!/usr/bin/env python3
"""Independent Fraction verifier; imports no production derivation code."""

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


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(row) for row in zip(*a)]


def diag(values):
    return [[values[i] if i == j else F(0) for j in range(4)] for i in range(4)]


def gram(flag):
    eta = diag([F(-1), F(1), F(1), F(1)])
    return mm(mm(tr(flag), eta), flag)


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def density_arguments(arrow, flag):
    source = gram(flag)
    target = gram(mm(arrow, flag))
    line = abs(target[0][0]) / abs(source[0][0])
    area = abs(det2(target)) / abs(det2(source))
    return line, area, area / line**2


def rational_rotation(t: F):
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    out = eye()
    out[2][2] = out[3][3] = c
    out[2][3] = -s
    out[3][2] = s
    return out


def inv_rotation(r):
    return tr(r)


def main() -> None:
    flag = [[F(1), F(0)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    arrow = [
        [F(1, 2), F(0), F(0), F(0)],
        [F(0), F(2), F(0), F(0)],
        [F(1, 4), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    base = density_arguments(arrow, flag)
    assert base == (F(3, 16), F(3, 4), F(64, 3))
    pair_metric = gram(mm(arrow, flag))
    assert -det2(pair_metric) / pair_metric[0][0] ** 2 == F(64, 3)

    unnormalized_flag = mm(flag, [[F(2), F(0)], [F(0), F(3)]])
    unnormalized_source = gram(unnormalized_flag)
    unnormalized_target = gram(mm(arrow, unnormalized_flag))
    unnormalized_q = density_arguments(arrow, unnormalized_flag)[2]
    source_factor = abs(det2(unnormalized_source)) / abs(unnormalized_source[0][0]) ** 2
    terminal_bracket = -det2(unnormalized_target) / unnormalized_target[0][0] ** 2
    assert source_factor == F(9, 4)
    assert terminal_bracket != unnormalized_q
    assert terminal_bracket == unnormalized_q * source_factor

    rotations_checked = 0
    parameters = (F(0), F(1, 3), F(1, 2), F(1), F(2), F(3))
    for source_t in parameters:
        source_rotation = rational_rotation(source_t)
        assert mm(tr(source_rotation), mm(diag([F(-1), F(1), F(1), F(1)]), source_rotation)) == diag([F(-1), F(1), F(1), F(1)])
        for target_t in parameters:
            target_rotation = rational_rotation(target_t)
            assert mm(tr(target_rotation), mm(diag([F(-1), F(1), F(1), F(1)]), target_rotation)) == diag([F(-1), F(1), F(1), F(1)])
            transformed = mm(mm(target_rotation, arrow), inv_rotation(source_rotation))
            assert density_arguments(transformed, flag) == base
            assert gram(mm(transformed, flag)) == pair_metric
            rotations_checked += 1

    b01 = eye()
    b01[0][0] = b01[1][1] = F(5, 4)
    b01[0][1] = b01[1][0] = F(3, 4)
    b01inv = eye()
    b01inv[0][0] = b01inv[1][1] = F(5, 4)
    b01inv[0][1] = b01inv[1][0] = F(-3, 4)
    carried_flag = mm(b01, flag)
    assert density_arguments(b01inv, carried_flag) == (F(1), F(1), F(1))

    b02 = eye()
    b02[0][0] = b02[2][2] = F(5, 4)
    b02[0][2] = b02[2][0] = F(3, 4)
    dilation = diag([F(2, 3), F(3, 2), F(1), F(1)])
    a12 = arrow
    a23 = mm(b02, dilation)
    flag2 = mm(a12, flag)
    total = mm(a23, a12)
    d12 = density_arguments(a12, flag)
    d23 = density_arguments(a23, flag2)
    d13 = density_arguments(total, flag)
    assert tuple(d12[i] * d23[i] for i in range(3)) == d13

    middle = rational_rotation(F(1))
    a12g = mm(middle, a12)
    a23g = mm(a23, inv_rotation(middle))
    assert mm(a23g, a12g) == total
    assert density_arguments(a12g, flag) == d12
    assert density_arguments(a23g, mm(a12g, flag)) == d23

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        manifest = list(csv.DictReader(stream, delimiter="\t"))
    assert len(manifest) == 16
    for row in manifest:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
        blob = subprocess.check_output(["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True).strip()
        assert blob == row["git_blob"]

    with (ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOOP_HOLONOMY.tsv").open() as stream:
        loops = list(csv.DictReader(stream, delimiter="\t"))
    assert len(loops) == 36 and all(float(row["ordinary_closure_residual"]) > 1e-10 for row in loops)

    result = {
        "verdict": "VERIFIED",
        "method": "pure-Python Fraction matrices and determinant-line ratios; no production import",
        "rational_screen_rotations_checked": rotations_checked,
        "mixed_arrow_density_arguments": [str(value) for value in base],
        "terminal_argument_matches": True,
        "terminal_argument_normalization_factor_verified": str(source_factor),
        "isometric_alignment_density_arguments": ["1", "1", "1"],
        "balanced_composition_and_telescoping": True,
        "source_hashes_verified": len(manifest),
        "path_loop_rows_retained": len(loops),
        "primary_landing_reproduced": "RECIPROCAL_READOUT_DESCENT_DERIVED__CALIBRATION_MAGNITUDE_NOT_GENERATED",
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
