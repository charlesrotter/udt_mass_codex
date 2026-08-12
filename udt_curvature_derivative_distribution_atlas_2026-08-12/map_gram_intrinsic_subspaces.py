#!/usr/bin/env python3
"""Production map of full Gram spectra, Jordan/rank data, and spectral subspaces."""

from __future__ import annotations

import csv
import importlib.util
import itertools
import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
RANK_TOL = 1e-8
IMAG_TOL = 1e-8
CLUSTER_TOL = 1e-7


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


DERIVE = load_module("derivative_atlas_for_spectral_map", HERE / "derive_derivative_atlas.py")


def write_tsv(path: Path, output: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(output)


def null_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    _, singular, vh = np.linalg.svd(matrix)
    rank = int(np.sum(singular > tolerance))
    return vh[rank:].conj().T


def orthonormal_real(columns: np.ndarray, tolerance: float) -> np.ndarray:
    if columns.size == 0:
        return np.zeros((4, 0))
    real = np.column_stack(tuple(np.real(columns[:, i]) for i in range(columns.shape[1])) + tuple(np.imag(columns[:, i]) for i in range(columns.shape[1])))
    u, singular, _ = np.linalg.svd(real, full_matrices=False)
    return u[:, singular > tolerance]


def signature(basis: np.ndarray) -> str:
    if basis.shape[1] == 0:
        return "0,0,0"
    values = np.linalg.eigvalsh(basis.T @ ETA @ basis)
    neg = int(np.sum(values < -1e-8)); zero = int(np.sum(abs(values) <= 1e-8)); pos = int(np.sum(values > 1e-8))
    return f"{neg},{zero},{pos}"


def projector_record(basis: np.ndarray) -> dict[str, object]:
    projector = basis @ basis.T
    pair = np.diag([1.0, 1.0, 0.0, 0.0]); screen = np.diag([0.0, 0.0, 1.0, 1.0])
    return {
        "dimension": int(basis.shape[1]),
        "signature": signature(basis),
        "pair_defect": float(np.linalg.norm(projector - pair)),
        "screen_defect": float(np.linalg.norm(projector - screen)),
        "projector": [float(x) for x in projector.reshape(-1)],
    }


def spectral_map(operator: np.ndarray) -> dict[str, object]:
    scale = max(1.0, float(np.linalg.norm(operator)))
    rank_step = RANK_TOL * scale; imag_step = IMAG_TOL * scale; cluster_step = CLUSTER_TOL * scale
    singular = np.linalg.svd(operator, compute_uv=False)
    ratios = singular / scale
    unresolved = any(RANK_TOL / 5 < value < 5 * RANK_TOL for value in ratios)
    rank = int(np.sum(singular > rank_step))
    values, vectors = np.linalg.eig(operator)
    if any(IMAG_TOL / 5 * scale < abs(value.imag) < 5 * IMAG_TOL * scale for value in values):
        unresolved = True
    for a, b in itertools.combinations(values, 2):
        gap = abs(a - b)
        if CLUSTER_TOL / 5 * scale < gap < 5 * CLUSTER_TOL * scale:
            unresolved = True

    order = sorted(range(4), key=lambda i: (round(values[i].real / cluster_step), round(values[i].imag / cluster_step), values[i].real, values[i].imag))
    values = values[order]; vectors = vectors[:, order]
    used: set[int] = set(); blocks = []
    jordan_defect = 0
    for i, value in enumerate(values):
        if i in used:
            continue
        if abs(value.imag) <= imag_step:
            members = [j for j, other in enumerate(values) if j not in used and abs(other.imag) <= imag_step and abs(other.real - value.real) <= cluster_step]
            used.update(members); center = float(np.mean([values[j].real for j in members])); alg = len(members)
            geom_complex = null_basis(operator - center * np.eye(4), rank_step); geom = geom_complex.shape[1]
            generalized = null_basis(np.linalg.matrix_power(operator - center * np.eye(4), alg), rank_step)
            basis = orthonormal_real(generalized, rank_step)
            jordan_defect += max(0, alg - geom)
            kind = "REAL"
            label = f"{center:.17g}"
        elif value.imag > imag_step:
            positive = [j for j, other in enumerate(values) if j not in used and other.imag > imag_step and abs(other - value) <= cluster_step]
            negative = []
            for j in positive:
                candidates = [k for k, other in enumerate(values) if k not in used and other.imag < -imag_step and abs(other - values[j].conjugate()) <= cluster_step]
                if not candidates:
                    unresolved = True
                else:
                    negative.append(candidates[0])
            members = positive + negative; used.update(members)
            center = sum(values[j] for j in positive) / max(1, len(positive)); alg_complex = len(positive)
            geom_complex = null_basis(operator.astype(complex) - center * np.eye(4), rank_step); geom_complex_dim = geom_complex.shape[1]
            generalized = null_basis(np.linalg.matrix_power(operator.astype(complex) - center * np.eye(4), max(1, alg_complex)), rank_step)
            basis = orthonormal_real(generalized, rank_step)
            alg = 2 * alg_complex; geom = 2 * geom_complex_dim
            jordan_defect += max(0, alg - geom)
            kind = "COMPLEX_PAIR"
            label = f"{center.real:.17g}{center.imag:+.17g}i"
        else:
            # Negative members are consumed by their positive conjugate.
            unresolved = True; used.add(i); continue
        if basis.shape[1] != alg:
            unresolved = True
        record = projector_record(basis)
        record.update({"kind": kind, "eigenvalue": label, "algebraic_multiplicity": alg, "geometric_multiplicity": geom})
        blocks.append({"basis": basis, "record": record})

    blocks.sort(key=lambda item: (item["record"]["dimension"], item["record"]["kind"], item["record"]["eigenvalue"]))
    planes = []
    for count in range(1, len(blocks) + 1):
        for subset in itertools.combinations(range(len(blocks)), count):
            if sum(blocks[i]["basis"].shape[1] for i in subset) != 2:
                continue
            basis = np.column_stack([blocks[i]["basis"] for i in subset])
            basis, _, _ = np.linalg.svd(basis, full_matrices=False)
            item = projector_record(basis[:, :2]); item["blocks"] = list(subset)
            if not any(np.linalg.norm(np.array(item["projector"]) - np.array(old["projector"])) <= 1e-8 for old in planes):
                planes.append(item)

    real_count = int(sum(abs(value.imag) <= imag_step for value in values))
    complex_pairs = (4 - real_count) // 2
    if unresolved:
        structure = "SPECTRALLY_UNRESOLVED"
    elif jordan_defect:
        structure = "DEFECTIVE"
    elif complex_pairs == 0 and len(blocks) == 4:
        structure = "FOUR_REAL_SIMPLE_LINES"
    elif complex_pairs == 0:
        structure = "REAL_REPEATED_DIAGONALIZABLE"
    elif complex_pairs == 1:
        structure = "ONE_COMPLEX_PLANE_PLUS_REAL_STRUCTURE"
    else:
        structure = "TWO_COMPLEX_PLANES"
    values_sorted = sorted(values, key=lambda z: (z.real, z.imag))
    return {
        "status": "SPECTRALLY_UNRESOLVED" if unresolved else "RESOLVED",
        "structure": structure,
        "operator_rank": rank,
        "real_eigenvalue_count": real_count,
        "complex_pair_count": complex_pairs,
        "jordan_defect": jordan_defect,
        "eigenvalues": values_sorted,
        "blocks": [item["record"] for item in blocks],
        "planes": planes,
    }


def row_for(key: str, tensor_name: str, operator: np.ndarray) -> dict[str, object]:
    result = spectral_map(operator)
    row: dict[str, object] = {
        "key": key,
        "tensor": tensor_name,
        "status": result["status"],
        "structure": result["structure"],
        "operator_rank": result["operator_rank"],
        "real_eigenvalue_count": result["real_eigenvalue_count"],
        "complex_pair_count": result["complex_pair_count"],
        "jordan_defect": result["jordan_defect"],
        "spectral_block_count": len(result["blocks"]),
        "candidate_2plane_count": len(result["planes"]),
    }
    for i, value in enumerate(result["eigenvalues"], 1):
        row[f"eigen_{i}_real"] = f"{value.real:.17g}"; row[f"eigen_{i}_imag"] = f"{value.imag:.17g}"
    row["spectral_blocks_json"] = json.dumps(result["blocks"], separators=(",", ":"), sort_keys=True)
    row["candidate_2planes_json"] = json.dumps(result["planes"], separators=(",", ":"), sort_keys=True)
    return row


def main() -> None:
    saved = np.load(HERE / "PRODUCTION_DERIVATIVE_TENSORS.npz")
    jets = DERIVE.enumerate_jets()
    if list(saved["keys"]) != [jet.key for jet in jets]:
        raise RuntimeError("production tensor/jet order mismatch")
    output = []
    for index, jet in enumerate(jets):
        x = DERIVE.torch.tensor(jet.x, dtype=DERIVE.torch.float64)
        coframe = jet.coframe_fn(x).detach().numpy(); frame = np.linalg.inv(coframe)
        for tensor_name in ("k_riem", "k_ric", "k_weyl"):
            k_frame = frame.T @ saved[tensor_name][index] @ frame
            output.append(row_for(jet.key, tensor_name, ETA @ k_frame))
    write_tsv(HERE / "GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv", output)
    summary = {
        "schema": "udt-Gram-intrinsic-subspaces-production-v1",
        "status": "COMPLETE",
        "rows": len(output),
        "structure_counts": dict(sorted(__import__("collections").Counter(row["structure"] for row in output).items())),
        "rank_counts": dict(sorted(__import__("collections").Counter(str(row["operator_rank"]) for row in output).items())),
        "candidate_2plane_counts": dict(sorted(__import__("collections").Counter(str(row["candidate_2plane_count"]) for row in output).items())),
    }
    (HERE / "GRAM_INTRINSIC_SUBSPACE_RESULT.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
