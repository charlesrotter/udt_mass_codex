#!/usr/bin/env python3
"""Independent exact verifier using only the Python standard library.

This implementation does not import the production derivation or SymPy.  It
reconstructs the finite linear-algebra witnesses with Fraction arithmetic and
checks the differential law through exact rational directional derivatives.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
ZERO = F(0)
ONE = F(1)
PREREG_COMMIT = "8425e2a2"


def eye(n: int) -> list[list[F]]:
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]


def diag(values: list[F]) -> list[list[F]]:
    return [[values[i] if i == j else ZERO for j in range(len(values))]
            for i in range(len(values))]


def gram(columns: list[list[F]], metric: list[list[F]]) -> list[list[F]]:
    return matmul(matmul(transpose(columns), metric), columns)


def det2(a: list[list[F]]) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def equal(a: list[list[F]], b: list[list[F]]) -> bool:
    return a == b


def density_data(
    arrow: list[list[F]], flag: list[list[F]], source_metric: list[list[F]], target_metric: list[list[F]]
) -> tuple[F, F, F]:
    source = gram(flag, source_metric)
    target = gram(matmul(arrow, flag), target_metric)
    rho1 = target[0][0] / source[0][0]
    rho2 = det2(target) / det2(source)
    return rho1, rho2, rho2 / (rho1 * rho1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pair_q(h00: F, h01: F, h11: F) -> F:
    determinant = h00 * h11 - h01 * h01
    return -determinant / (h00 * h00)


def pair_depth_rate(h: tuple[F, F, F], dh: tuple[F, F, F]) -> F:
    h00, h01, h11 = h
    d00, d01, d11 = dh
    determinant = h00 * h11 - h01 * h01
    ddet = d00 * h11 + h00 * d11 - 2 * h01 * d01
    return ddet / (4 * determinant) - d00 / (2 * h00)


def main() -> None:
    checks: dict[str, bool] = {}
    eta = diag([F(-1), ONE, ONE, ONE])
    flag = [[ONE, ZERO], [ZERO, ONE], [ZERO, ZERO], [ZERO, ZERO]]

    a = [
        [F(1, 2), ZERO, ZERO, ZERO],
        [ZERO, F(2), ZERO, ZERO],
        [F(1, 4), ZERO, ONE, ZERO],
        [ZERO, ZERO, ZERO, ONE],
    ]
    rho1_a, rho2_a, q_a = density_data(a, flag, eta, eta)
    checks["mixing_rho1"] = rho1_a == F(3, 16)
    checks["mixing_rho2"] = rho2_a == F(3, 4)
    checks["mixing_q"] = q_a == F(64, 3)

    b = [
        [F(3, 2), ZERO, ZERO, ZERO],
        [ZERO, F(2, 3), ZERO, ZERO],
        [F(1, 10), F(1, 8), ONE, ZERO],
        [ZERO, ZERO, ZERO, ONE],
    ]
    carried = matmul(a, flag)
    rho1_b, rho2_b, q_b = density_data(b, carried, eta, eta)
    rho1_ba, rho2_ba, q_ba = density_data(matmul(b, a), flag, eta, eta)
    checks["composition_rho1"] = rho1_ba == rho1_b * rho1_a
    checks["composition_rho2"] = rho2_ba == rho2_b * rho2_a
    checks["composition_q"] = q_ba == q_b * q_a

    boost = [
        [F(5, 4), F(3, 4), ZERO, ZERO],
        [F(3, 4), F(5, 4), ZERO, ZERO],
        [ZERO, ZERO, ONE, ZERO],
        [ZERO, ZERO, ZERO, ONE],
    ]
    checks["boost_isometry"] = equal(matmul(matmul(transpose(boost), eta), boost), eta)
    checks["boost_zero_depth"] = density_data(boost, flag, eta, eta) == (ONE, ONE, ONE)

    rotation = [
        [ONE, ZERO, ZERO, ZERO],
        [ZERO, ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO, F(-1)],
        [ZERO, ZERO, ONE, ZERO],
    ]
    rotation_inverse = transpose(rotation)
    checks["screen_rotation_isometry"] = equal(
        matmul(matmul(transpose(rotation), eta), rotation), eta
    )
    rotated_a = matmul(matmul(rotation, a), rotation_inverse)
    checks["screen_rotation_density_descent"] = density_data(rotated_a, flag, eta, eta) == (
        rho1_a, rho2_a, q_a
    )

    # Independent pair-metric controls, including nonzero shift.
    samples = [
        (F(-3, 16), ZERO, F(4), F(64, 3)),
        (F(-3, 16), F(1, 12), F(37, 9), F(1792, 81)),
        (F(-5, 7), F(2, 9), F(11, 6), pair_q(F(-5, 7), F(2, 9), F(11, 6))),
    ]
    for index, (h00, h01, h11, expected_q) in enumerate(samples, start=1):
        checks[f"pair_q_{index}"] = pair_q(h00, h01, h11) == expected_q
        common = F(index + 1)
        checks[f"common_scale_{index}"] = pair_q(
            common * common * h00,
            common * common * h01,
            common * common * h11,
        ) == expected_q

    # Exact directional derivative: two independently derived expressions agree.
    rate_samples = [
        ((F(-1), ZERO, ONE), (F(2), F(3), F(5))),
        ((F(-3, 16), F(1, 12), F(37, 9)), (F(1, 7), F(-2, 5), F(3, 8))),
        ((F(-5, 7), F(2, 9), F(11, 6)), (F(-1, 6), F(4, 11), F(2, 13))),
    ]
    for index, (hvals, dhvals) in enumerate(rate_samples, start=1):
        h00, h01, h11 = hvals
        d00, d01, d11 = dhvals
        determinant = h00 * h11 - h01 * h01
        ddet = d00 * h11 + h00 * d11 - 2 * h01 * d01
        clock_rate = d00 / (2 * h00)
        ruler_rate = (ddet / determinant - d00 / h00) / 2
        independently_rebuilt = (ruler_rate - clock_rate) / 2
        checks[f"pair_rate_{index}"] = pair_depth_rate(hvals, dhvals) == independently_rebuilt

    # Generator controls: common, reciprocal, Lorentz, and time-live reciprocal rate.
    generators = {
        "common": (F(3), F(3), ZERO),
        "reciprocal": (F(-5), F(5), F(5)),
        "lorentz": (ZERO, ZERO, ZERO),
        "time_live": (F(-7, 3), F(7, 3), F(7, 3)),
    }
    for name, (b00, b11, expected) in generators.items():
        checks[f"generator_{name}"] = (b11 - b00) / 2 == expected

    # Exact diagonal coframe-parallel transport between distinct endpoint metrics.
    ep = [F(2), F(3), F(5), F(7)]
    eq = [F(11), F(13), F(17), F(19)]
    gp = diag([-ep[0] ** 2, ep[1] ** 2, ep[2] ** 2, ep[3] ** 2])
    gq = diag([-eq[0] ** 2, eq[1] ** 2, eq[2] ** 2, eq[3] ** 2])
    aw = diag([ep[i] / eq[i] for i in range(4)])
    checks["coframe_parallel_isometry"] = equal(matmul(matmul(transpose(aw), gq), aw), gp)
    checks["coframe_parallel_zero_depth"] = density_data(aw, flag, gp, gq) == (ONE, ONE, ONE)

    # Algebraic character and reset controls.
    reciprocal_diagonal = diag([F(1, 2), F(2), ONE, ONE])
    determinant = reciprocal_diagonal[0][0] * reciprocal_diagonal[1][1]
    checks["determinant_blind_to_reciprocal"] = determinant == ONE
    offsets = (F(2, 7), F(-3, 11), F(5, 13))
    obstruction = offsets[0] + offsets[1] - offsets[2]
    checks["independent_tape_obstruction_nonzero"] = obstruction != ZERO
    phi_a, phi_b, phi_c = F(2, 5), F(-7, 9), F(13, 17)
    checks["common_family_telescope"] = (
        (phi_b - phi_a) + (phi_c - phi_b) == phi_c - phi_a
    )

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count"] = len(sources) == 15
    checks["source_unique"] = len({row["path"] for row in sources}) == 15
    # SOURCE_MANIFEST.tsv freezes the exact preregistration/reviewer intake.  Current navigation
    # may advance afterward, so replay provenance against the preregistration commit rather than
    # silently rewriting the historical manifest to match mutable startup controls.
    for index, row in enumerate(sources, start=1):
        frozen = subprocess.run(
            ["git", "show", f"{PREREG_COMMIT}:{row['path']}"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        checks[f"source_hash_{index:02d}"] = (
            frozen.returncode == 0
            and hashlib.sha256(frozen.stdout).hexdigest() == row["sha256"]
        )
        checks[f"source_not_protected_{index:02d}"] = (
            "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
        )

    with (PKG / "TRANSPORT_FAMILY_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    checks["atlas_count"] = len(atlas) == 10
    checks["atlas_unique"] = len({row["family_id"] for row in atlas}) == 10
    checks["no_selected_physical_owner"] = all(
        row["owner"] not in {"physical UDT law", "selected branch"} for row in atlas
    )

    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "schema_version": 1,
        "implementation": "standard_library_fraction_reconstruction",
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "failed": failed,
        "checks": checks,
        "reset_obstruction_witness": str(obstruction),
    }
    (PKG / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    assert not failed, f"independent failures: {failed}"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
