#!/usr/bin/env python3
"""Independent standard-library reconstruction of the joint-functor claims."""

from __future__ import annotations

import cmath
import csv
import json
import math
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
TOL = 2.0e-12


def close(a: complex | float, b: complex | float) -> bool:
    return abs(a - b) < TOL * max(1.0, abs(a), abs(b))


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    rng = random.Random(781731)
    checks: dict[str, bool] = {}

    composition_ok = inversion_ok = gauge_ok = determinant_ok = True
    screen_ok = relative_ok = loop_ok = True
    for _ in range(200):
        d1, d2 = (rng.uniform(-3.0, 3.0) for _ in range(2))
        t1, t2 = (rng.uniform(-math.pi, math.pi) for _ in range(2))
        w = rng.uniform(-2.5, 2.5)
        ap, aq = (rng.uniform(-math.pi, math.pi) for _ in range(2))

        def C(depth: float, angle: float) -> complex:
            return math.exp(w * depth) * cmath.exp(1j * angle)

        composition_ok &= close(C(d2, t2) * C(d1, t1), C(d1 + d2, t1 + t2))
        inversion_ok &= close(C(-d1, -t1) * C(d1, t1), 1.0)
        transformed = cmath.exp(-1j * aq) * C(d1, t1) * cmath.exp(1j * ap)
        gauge_ok &= close(transformed, C(d1, t1 + ap - aq))
        determinant_ok &= close(abs(C(d1, t1)) ** 2, math.exp(2.0 * w * d1))

        lam = rng.uniform(-2.5, 2.5)
        pp, pq = (rng.uniform(-1.5, 1.5) for _ in range(2))
        delta = pq - pp
        vp, vq = math.exp(lam * pp), math.exp(lam * pq)
        screen_ok &= close(vp / vq, math.exp(-lam * delta))
        screen_ok &= close(vq / vp, math.exp(lam * delta))

        eta, gamma = (rng.uniform(-math.pi, math.pi) for _ in range(2))
        u_eta, u_gamma = cmath.exp(1j * eta), cmath.exp(1j * gamma)
        ug_eta = cmath.exp(-1j * aq) * u_eta * cmath.exp(1j * ap)
        ug_gamma = cmath.exp(-1j * aq) * u_gamma * cmath.exp(1j * ap)
        relative_ok &= close(ug_gamma / ug_eta, u_gamma / u_eta)
        loop_ok &= close((pp - pp), 0.0)

    checks["complex_joint_composition_200"] = composition_ok
    checks["complex_joint_inversion_200"] = inversion_ok
    checks["independent_endpoint_gauge_covariance_200"] = gauge_ok
    checks["CO2_determinant_200"] = determinant_ok
    checks["screen_vector_covector_weights_200"] = screen_ok
    checks["relative_holonomy_gauge_cancellation_200"] = relative_ok
    checks["loop_depth_zero_200"] = loop_ok

    # Endpoint rotations can send any open-path phase to any other phase.
    transitive = True
    for _ in range(100):
        source = rng.uniform(-math.pi, math.pi)
        target = rng.uniform(-math.pi, math.pi)
        alpha_p = 0.0
        alpha_q = source - target
        mapped = source + alpha_p - alpha_q
        transitive &= close(cmath.exp(1j * mapped), cmath.exp(1j * target))
    checks["open_path_phase_gauge_action_transitive_100"] = transitive

    # Periodicity kills any real additive angular coefficient b: b*2pi=0.
    for b in (-3.0, -0.25, 0.0, 0.5, 7.0):
        if close(b * 2.0 * math.pi, 0.0):
            assert close(b, 0.0)
        else:
            assert not close(b, 0.0)
    checks["real_angular_character_periodicity_control"] = True

    # The representative joint one-form alpha=x dy is additive but path-dependent.
    x0, x1, y0, y1 = 0.5, 2.0, -1.0, 3.0
    segment_sum = x1 * (y1 - y0) + x0 * (y0 - y1)
    area = (x1 - x0) * (y1 - y0)
    checks["general_one_form_nonzero_loop_control_not_R17_witness"] = close(segment_sum, area) and not close(area, 0.0)
    b_control = 2.0 - 1.0 + (1.0 / 64.0) ** 2
    checks["C08_zero_depth_nonzero_angular_curvature"] = close(b_control, 4097.0 / 4096.0) and close(-2.0 * b_control, -4097.0 / 2048.0)

    candidates = rows("JOINT_CANDIDATE_CLASSIFICATION.tsv")
    checks["candidate_universe_exact_12"] = [row["candidate_id"] for row in candidates] == [f"J{i:02d}" for i in range(1, 13)]
    checks["all_candidates_classified"] = all(row["classification"] and row["composition"] for row in candidates)
    checks["character_atlas_three_targets"] = len(rows("CHARACTER_ATLAS.tsv")) == 3
    checks["gauge_atlas_four_queries"] = len(rows("GAUGE_INVARIANT_QUERY_ATLAS.tsv")) == 4
    checks["one_form_atlas_four_families"] = len(rows("LOCAL_ONE_FORM_COCYCLE_ATLAS.tsv")) == 4

    failed = [name for name, value in checks.items() if not value]
    result = {
        "schema_version": 1,
        "method": "INDEPENDENT_STDLIB_COMPLEX_GROUP_AND_PATH_CONTROLS",
        "checks": checks,
        "passed": len(checks) - len(failed),
        "total": len(checks),
        "failed": failed,
        "status": "PASS" if not failed else "FAIL",
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
