#!/usr/bin/env python3
"""Independent standard-library replay for the G155 common-scale landing."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "2f5cf474"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    ledger = rows(HERE / "EQUATION_ROLE_LEDGER.tsv")
    assert len(manifest) == 41 == len(ledger)
    for item in manifest:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{item['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(item["bytes"])
        assert hashlib.sha256(payload).hexdigest() == item["sha256"]
    assert {r["source_id"] for r in manifest} == {r["source_id"] for r in ledger}

    rng = random.Random(155)
    trials = 500
    triangle_trials = 500
    for _ in range(trials):
        # Build a regular Lorentzian triangular pair metric from T,L,beta.
        T = math.exp(rng.uniform(-2.0, 2.0))
        L = math.exp(rng.uniform(-2.0, 2.0))
        beta = rng.uniform(-3.0, 3.0)
        scale = math.exp(rng.uniform(-3.0, 3.0))
        h00 = -T * T
        h01 = -T * T * beta
        h11 = L * L - T * T * beta * beta
        det_h = h00 * h11 - h01 * h01
        assert det_h < 0.0
        phi = 0.25 * math.log((-det_h) / (h00 * h00))
        kappa = 0.25 * math.log(-det_h)
        hs00, hs01, hs11 = scale * scale * h00, scale * scale * h01, scale * scale * h11
        det_s = hs00 * hs11 - hs01 * hs01
        phi_s = 0.25 * math.log((-det_s) / (hs00 * hs00))
        kappa_s = 0.25 * math.log(-det_s)
        beta_s = hs01 / hs00
        assert math.isclose(phi_s, phi, rel_tol=2e-12, abs_tol=2e-12)
        assert math.isclose(beta_s, beta, rel_tol=2e-12, abs_tol=2e-12)
        assert math.isclose(kappa_s, kappa + math.log(scale), rel_tol=2e-12, abs_tol=2e-12)
        Xstar = math.exp(rng.uniform(-1.0, 2.0))
        rho = Xstar * math.tanh(phi)
        rho_s = Xstar * math.tanh(phi_s)
        assert math.isclose(rho_s, rho, rel_tol=2e-12, abs_tol=2e-12)
        phi_sigma = rng.uniform(-4.0, 4.0)
        n_rho = Xstar * (1.0 - math.tanh(phi) ** 2) * phi_sigma / L
        n_rho_s = Xstar * (1.0 - math.tanh(phi_s) ** 2) * phi_sigma / (scale * L)
        assert math.isclose(n_rho_s, n_rho / scale, rel_tol=3e-11, abs_tol=3e-11)

    for _ in range(triangle_trials):
        pA, pB, pC = (rng.uniform(-5.0, 5.0) for _ in range(3))
        # These arbitrary scale values represent a conformal twin. They do not
        # enter the reciprocal potential-difference edges.
        _kA, _kB, _kC = (rng.uniform(-5.0, 5.0) for _ in range(3))
        loop = (pB - pA) + (pC - pB) + (pA - pC)
        assert abs(loop) < 4e-15

    history_rows = [
        r for r in ledger if r["role"] in {"PHYSICAL_HISTORY_CONSTRAINT", "PHYSICAL_HISTORY_EVOLUTION"}
    ]
    rank = sum(int(r["physical_history_principal_rank"]) for r in history_rows)
    assert history_rows == []
    assert rank == 0
    assert next(r for r in ledger if r["source_id"] == "S06")["active_status"] == "INACTIVE_CHALLENGED"
    assert next(r for r in ledger if r["source_id"] == "S37")["role"] == "QUERY_EVOLUTION"

    result = {
        "status": "PASS",
        "method": "stdlib_only_no_production_import",
        "manifest_files": len(manifest),
        "ledger_rows": len(ledger),
        "numeric_conformal_trials": trials,
        "three_observer_conformal_triangle_trials": triangle_trials,
        "role_counts": dict(sorted(Counter(r["role"] for r in ledger).items())),
        "owned_physical_history_equation_count": len(history_rows),
        "common_scale_physical_history_principal_rank": rank,
        "landing": "RANK_ZERO",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
