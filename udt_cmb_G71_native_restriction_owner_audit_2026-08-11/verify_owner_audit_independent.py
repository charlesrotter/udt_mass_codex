#!/usr/bin/env python3
"""Independent numeric and semantic replay of G71 without importing its production builder."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import logm


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    targets = table(HERE / "OWNER_TARGET_LEDGER.tsv")
    atlas = table(HERE / "SOURCE_TARGET_ATLAS.tsv")
    graph = table(HERE / "DEPENDENCY_GRAPH.tsv")
    assert len(manifest) == len(atlas) == 21
    assert all(digest(ROOT / row["path"]) == row["sha256"] for row in manifest)
    assert {row["path"] for row in manifest} == {row["source_path"] for row in atlas}
    for row in targets:
        text = (ROOT / row["source_path"]).read_text(encoding="utf-8", errors="replace")
        assert row["evidence_token"] in text, (row["target"], row["evidence_token"])

    rng = np.random.default_rng(7102026)
    max_congruence = 0.0
    max_shape_shift = 0.0
    minimum_source_eigenvalue = float("inf")
    for _ in range(200):
        dmat = rng.normal(size=(2, 2))
        while abs(np.linalg.det(dmat)) < 0.15:
            dmat = rng.normal(size=(2, 2))
        q = rng.normal(size=(2, 2))
        observed = q @ q.T + 0.5 * np.eye(2)
        di = np.linalg.inv(dmat)
        source = di @ observed @ di.T
        replay = dmat @ source @ dmat.T
        max_congruence = max(max_congruence, float(np.linalg.norm(replay - observed) / np.linalg.norm(observed)))
        minimum_source_eigenvalue = min(minimum_source_eigenvalue, float(np.linalg.eigvalsh(source)[0]))

        base = dmat @ observed @ dmat.T
        base_log = np.real_if_close(logm(base), tol=1000).astype(float)
        base_shape = np.array([0.5 * (base_log[0, 0] - base_log[1, 1]), base_log[0, 1]])
        alpha = float(np.exp(rng.uniform(-3.0, 3.0)))
        scaled_log = np.real_if_close(logm(alpha * base), tol=1000).astype(float)
        scaled_shape = np.array([0.5 * (scaled_log[0, 0] - scaled_log[1, 1]), scaled_log[0, 1]])
        max_shape_shift = max(max_shape_shift, float(np.linalg.norm(scaled_shape - base_shape)))

    assert max_congruence <= 2.0e-12
    assert max_shape_shift <= 2.0e-11
    assert minimum_source_eigenvalue > 0.0
    assert not any(row["status"] == "OWNED_NATIVE" for row in targets)
    assert sum(row["status"] == "DERIVED_CONDITIONAL_ON_QUERY" for row in targets) == 1
    assert any(row["edge"] == "observation_projection" and row["status"] == "TYPE_MISMATCH" for row in graph)

    result = {
        "schema": "udt-cmb-g71-independent-v1",
        "status": "PASS",
        "imports_production_builder": False,
        "source_rows": len(manifest),
        "target_rows": len(targets),
        "atlas_rows": len(atlas),
        "graph_edges": len(graph),
        "numeric_trials": 200,
        "maximum_congruence_relative": max_congruence,
        "maximum_shape_coordinate_shift_under_amplitude": max_shape_shift,
        "minimum_constructed_source_eigenvalue": minimum_source_eigenvalue,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
