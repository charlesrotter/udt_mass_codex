#!/usr/bin/env python3
"""Sampled independent smoke test with Fraction arithmetic and no SymPy import.

This is deliberately not a universal proof of the symbolic identities or local classification.
The exact derivation plus the cold semantic review carry that theorem-level burden.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "86380447"


def det2(m: list[list[F]]) -> F:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def main() -> None:
    checks: dict[str, bool] = {}

    T, L, beta = F(3), F(5), F(2, 7)
    h = [
        [-T * T, -T * T * beta],
        [-T * T * beta, L * L - T * T * beta * beta],
    ]
    checks["determinant"] = det2(h) == -T * T * L * L
    r_plus, r_minus = -beta + L / T, -beta - L / T
    q = lambda r: h[0][0] * r * r + 2 * h[0][1] * r + h[1][1]
    checks["null_plus"] = q(r_plus) == 0
    checks["null_minus"] = q(r_minus) == 0
    checks["center"] = (r_plus + r_minus) / 2 == -beta
    checks["half_width"] = (r_plus - r_minus) / 2 == L / T
    w_plus, w_minus = 1 / r_plus, 1 / r_minus
    checks["balanced_inverse_speed"] = (1 / w_plus - 1 / w_minus) / 2 == L / T
    checks["ceff_ratio"] = T / L == F(3, 5)
    checks["one_way_shifted"] = w_plus != -w_minus

    scale = F(11, 4)
    hs = [[scale * scale * value for value in row] for row in h]
    checks["common_scale_beta"] = hs[0][1] / hs[0][0] == beta
    checks["common_scale_width"] = (scale * L) / (scale * T) == L / T

    K = [[F(0), F(-1)], [F(-1), F(0)]]
    D = [[F(2), F(0)], [F(0), F(3)]]
    A = [[F(0), F(2)], [F(3), F(0)]]
    checks["diagonal_causal"] = matmul(matmul(transpose(D), K), D) == [[F(0), F(-6)], [F(-6), F(0)]]
    checks["anti_diagonal_causal"] = matmul(matmul(transpose(A), K), A) == [[F(0), F(-6)], [F(-6), F(0)]]
    D2 = [[F(5), F(0)], [F(0), F(7)]]
    checks["composition"] = matmul(D2, D) == [[F(10), F(0)], [F(0), F(21)]]
    checks["inverse"] = matmul(D, [[F(1, 2), F(0)], [F(0), F(1, 3)]]) == [[F(1), F(0)], [F(0), F(1)]]

    # f_e(u)=u+e*u^3 fixes value and first derivative at the calibration anchor.
    eps, u = F(2, 5), F(3, 7)
    f_value = u + eps * u**3
    f_derivative = 1 + 3 * eps * u**2
    checks["nonlinear_anchor_value"] = F(0) + eps * F(0) ** 3 == 0
    checks["nonlinear_anchor_derivative"] = 1 + 3 * eps * F(0) ** 2 == 1
    checks["nonlinear_positive"] = f_derivative > 0
    checks["nonlinear_nonidentity"] = f_value != u

    # Time-live screen-graph witness z=q*t*s.
    graph_q, t, s = F(1, 3), F(1, 4), F(1, 5)
    hg = [
        [-1 + graph_q**2 * s**2, graph_q**2 * t * s],
        [graph_q**2 * t * s, 1 + graph_q**2 * t**2],
    ]
    expected_det = -1 - graph_q**2 * t**2 + graph_q**2 * s**2
    checks["graph_determinant"] = det2(hg) == expected_det
    checks["graph_regular_clock"] = hg[0][0] < 0
    checks["graph_regular_lorentzian"] = expected_det < 0
    checks["graph_has_shift"] = hg[0][1] != 0
    phi_argument = (-expected_det) / (hg[0][0] ** 2)
    checks["graph_phi_positive_argument"] = phi_argument > 0

    # Infinite asymptotic-profile deformation has the same center/endpoints.
    profile_deformation = lambda z: z * (1 - z * z)
    checks["profile_center"] = profile_deformation(F(0)) == 0
    checks["profile_endpoints"] = profile_deformation(F(1)) == profile_deformation(F(-1)) == 0
    checks["profile_nontrivial"] = profile_deformation(F(1, 2)) != 0

    pa, pb, pc = F(2, 5), F(-7, 9), F(13, 17)
    checks["common_family_telescope"] = (pb - pa) + (pc - pb) == pc - pa
    oa, ob, oc = F(2, 7), F(-3, 11), F(5, 13)
    checks["independent_offset"] = oa + ob - oc != 0

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    checks["source_count"] = len(sources) == 14
    checks["source_unique"] = len({row["path"] for row in sources}) == 14
    for index, row in enumerate(sources, start=1):
        frozen = subprocess.run(
            ["git", "show", f"{PREREG_COMMIT}:{row['path']}"], cwd=ROOT,
            capture_output=True, check=False,
        )
        checks[f"source_hash_{index:02d}"] = (
            frozen.returncode == 0
            and hashlib.sha256(frozen.stdout).hexdigest() == row["sha256"]
        )
        checks[f"source_scope_{index:02d}"] = (
            "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
            and "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]
        )

    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "schema_version": 1,
        "implementation": "sampled_independent_standard_library_fraction_smoke_test",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "failed": failed,
        "checks": checks,
        "witnesses": {
            "r_plus": str(r_plus),
            "r_minus": str(r_minus),
            "time_live_phi_argument": str(phi_argument),
            "offset_obstruction": str(oa + ob - oc),
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    assert not failed, failed
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
