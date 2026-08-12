#!/usr/bin/env python3
"""First curvature-derivative intrinsic-distribution atlas.

This is a local metric-concomitant map over supplied off-shell metric witnesses.
It does not select a physical history, query, realization, split, or dynamics.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import platform
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch.func import jacfwd, jacrev


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT_DIR = ROOT / "udt_curvature_principal_split_ownership_audit_2026-08-12"
ETA_T = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0], dtype=torch.float64))
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
RANK_TOL = 1.0e-7
BLOCK_TOL = 2.0e-6
GAP_TOL = 2.0e-5


def load_parent():
    spec = importlib.util.spec_from_file_location("curvature_parent", PARENT_DIR / "derive_curvature_split_atlas.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load parent curvature implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PARENT = load_parent()


def levi_civita_symbol() -> torch.Tensor:
    out = torch.zeros((4, 4, 4, 4), dtype=torch.float64)
    import itertools
    for p in itertools.permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
        out[p] = -1.0 if inversions % 2 else 1.0
    return out


EPS_SYMBOL = levi_civita_symbol()


@dataclass(frozen=True)
class Jet:
    key: str
    scope: str
    identity: str
    point: str
    x: np.ndarray
    metric_fn: object
    coframe_fn: object
    parent_owner: str


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing empty output: {path}")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify_sources() -> int:
    rows = table(HERE / "SOURCE_MANIFEST.tsv")
    if len(rows) != 9 or len({row["path"] for row in rows}) != 9:
        raise RuntimeError("source manifest is not exactly nine unique sources")
    base=(HERE / "SOURCE_BASE_COMMIT.txt").read_text().strip()
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            raise RuntimeError(f"source hash mismatch: {path}")
        if row["path"]=="CURRENT_SCIENTIFIC_PREMISES.md":
            blob=subprocess.run(["git","show",f"{base}:{row['path']}"],cwd=ROOT,capture_output=True,check=True).stdout
            actual=hashlib.sha256(blob).hexdigest()
        else: actual=digest(path)
        if actual != row["sha256"]: raise RuntimeError(f"source hash mismatch: {path}")
    return len(rows)


def parent_owner_map() -> dict[str, str]:
    out = {}
    for row in table(PARENT_DIR / "CURVATURE_SPLIT_ATLAS.tsv"):
        out[f"{row['scope']}|{row['identity']}|{row['point']}"] = row["owner_class"]
    return out


def enumerate_jets() -> list[Jet]:
    owners = parent_owner_map()
    jets: list[Jet] = []
    for sample in PARENT.load_g63_samples():
        metric_fn = lambda x, sample=sample: PARENT.g63_metric(x, sample)
        coframe_fn = lambda x, sample=sample: PARENT.g63_coframe(x, sample)
        for point, x in PARENT.g63_points(sample).items():
            key = f"G63|{sample.sample_id}|{point}"
            jets.append(Jet(key, "G63", sample.sample_id, point, x, metric_fn, coframe_fn, owners[key]))

    profiles = PARENT.load_g85_profiles()
    controls = (("C0", 0.0, 0.0), ("CMINUS", -0.3, 0.4), ("CPLUS", 0.3, 0.4))
    for profile_id, coefficients in sorted(profiles.items()):
        for archetype in ("A03_RADIAL_SHIFT_TIMELIVE", "A04_LAPSE_LIFT_TIMELIVE"):
            for control, epsilon, tau in controls:
                witness = PARENT.G85Witness(profile_id, coefficients, archetype, control, epsilon, tau)
                metric_fn = lambda x, witness=witness: PARENT.g85_metric(x, witness)
                coframe_fn = lambda x, metric_fn=metric_fn: PARENT.coframe_from_metric(metric_fn(x))
                identity = f"{profile_id}:{archetype}"
                key = f"G85|{identity}|{control}"
                x = np.array([tau, math.pi / 2, 1.1, 0.37])
                jets.append(Jet(key, "G85", identity, control, x, metric_fn, coframe_fn, owners[key]))

    representative_id, representative_coefficients = sorted(profiles.items())[0]
    for control, epsilon, tau in controls:
        archetype = "A05_SHIFT_SUPPORTED_TAPER"
        witness = PARENT.G85Witness(representative_id, representative_coefficients, archetype, control, epsilon, tau)
        metric_fn = lambda x, witness=witness: PARENT.g85_metric(x, witness)
        coframe_fn = lambda x, metric_fn=metric_fn: PARENT.coframe_from_metric(metric_fn(x))
        parent_key = f"G85|{representative_id}:{archetype}|{control}"
        jets.append(Jet(
            f"G85|A05_UNIQUE|{control}", "G85", "A05_UNIQUE", control,
            np.array([tau, math.pi / 2, 1.1, 0.37]), metric_fn, coframe_fn, owners[parent_key]
        ))

    if len(jets) != 1221 or len({jet.key for jet in jets}) != 1221:
        raise RuntimeError(f"distinct-jet census failure: {len(jets)}")
    if Counter(jet.scope for jet in jets) != Counter({"G63": 42, "G85": 1179}):
        raise RuntimeError("scope census failure")
    return jets


def christoffel(metric_fn, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    g = metric_fn(x)
    gi = torch.linalg.inv(g)
    dg = jacrev(metric_fn)(x)
    terms = dg.permute(0, 2, 1) + dg - dg.permute(2, 0, 1)
    gamma = 0.5 * torch.einsum("ad,dbc->abc", gi, terms)
    return g, gi, dg, gamma


def curvature_raw(metric_fn, x: torch.Tensor) -> dict[str, torch.Tensor]:
    g, gi, _, gamma = christoffel(metric_fn, x)
    gamma_fn = lambda y: christoffel(metric_fn, y)[3]
    dgamma = jacrev(gamma_fn)(x)
    rup = (
        dgamma.permute(0, 2, 3, 1) - dgamma.permute(0, 2, 1, 3)
        + torch.einsum("ace,edb->abcd", gamma, gamma)
        - torch.einsum("ade,ecb->abcd", gamma, gamma)
    )
    rdown = torch.einsum("ae,ebcd->abcd", g, rup)
    ricci = torch.einsum("abad->bd", rup)
    scalar = torch.einsum("ab,ab->", gi, ricci)
    kulkarni = (
        torch.einsum("ac,db->abcd", g, ricci)
        - torch.einsum("ad,cb->abcd", g, ricci)
        - torch.einsum("bc,da->abcd", g, ricci)
        + torch.einsum("bd,ca->abcd", g, ricci)
    )
    scalar_term = torch.einsum("ac,db->abcd", g, g) - torch.einsum("ad,cb->abcd", g, g)
    weyl = rdown - 0.5 * kulkarni + scalar * scalar_term / 6.0
    return {"g": g, "gi": gi, "gamma": gamma, "riemann": rdown, "ricci": ricci, "scalar": scalar, "weyl": weyl}


def scalar_invariants(raw: dict[str, torch.Tensor]) -> torch.Tensor:
    g, gi, ricci, scalar, weyl = raw["g"], raw["gi"], raw["ricci"], raw["scalar"], raw["weyl"]
    mixed_ricci = gi @ ricci
    ric2 = torch.trace(mixed_ricci @ mixed_ricci)
    ric3 = torch.trace(mixed_ricci @ mixed_ricci @ mixed_ricci)
    cop = torch.einsum("abef,ec,fd->abcd", weyl, gi, gi)
    eps_cov = torch.sqrt(torch.abs(torch.linalg.det(g))) * EPS_SYMBOL.to(dtype=g.dtype)
    eps_mixed = torch.einsum("abmn,mc,nd->abcd", eps_cov, gi, gi)
    star_weyl = 0.5 * torch.einsum("abef,efcd->abcd", eps_mixed, weyl)
    star_cop = torch.einsum("abef,ec,fd->abcd", star_weyl, gi, gi)
    w2 = torch.einsum("abcd,cdab->", cop, cop)
    sw2 = torch.einsum("abcd,cdab->", star_cop, cop)
    w3 = torch.einsum("abcd,cdef,efab->", cop, cop, cop)
    sw3 = torch.einsum("abcd,cdef,efab->", star_cop, cop, cop)
    return torch.stack((scalar, ric2, ric3, w2, sw2, w3, sw3))


def curvature_vector(metric_fn, x: torch.Tensor) -> torch.Tensor:
    raw = curvature_raw(metric_fn, x)
    return torch.cat((raw["riemann"].reshape(-1), raw["ricci"].reshape(-1), raw["weyl"].reshape(-1), scalar_invariants(raw)))


def covariant_derivatives(metric_fn, x: torch.Tensor) -> dict[str, torch.Tensor]:
    raw = curvature_raw(metric_fn, x)
    derivative = jacfwd(lambda y: curvature_vector(metric_fn, y))(x)
    offset = 0
    driemann = derivative[offset:offset + 256].reshape(4, 4, 4, 4, 4); offset += 256
    dricci = derivative[offset:offset + 16].reshape(4, 4, 4); offset += 16
    dweyl = derivative[offset:offset + 256].reshape(4, 4, 4, 4, 4); offset += 256
    gradients = derivative[offset:offset + 7]
    gamma, riemann, ricci, weyl = raw["gamma"], raw["riemann"], raw["ricci"], raw["weyl"]

    nabla_r = torch.empty((4, 4, 4, 4, 4), dtype=x.dtype)
    nabla_c = torch.empty_like(nabla_r)
    nabla_ric = torch.empty((4, 4, 4), dtype=x.dtype)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                nabla_ric[a, b, c] = dricci[b, c, a] - sum(
                    gamma[f, a, b] * ricci[f, c] + gamma[f, a, c] * ricci[b, f]
                    for f in range(4)
                )
                for d in range(4):
                    for e in range(4):
                        correction_r = sum(
                            gamma[f, a, b] * riemann[f, c, d, e]
                            + gamma[f, a, c] * riemann[b, f, d, e]
                            + gamma[f, a, d] * riemann[b, c, f, e]
                            + gamma[f, a, e] * riemann[b, c, d, f]
                            for f in range(4)
                        )
                        correction_c = sum(
                            gamma[f, a, b] * weyl[f, c, d, e]
                            + gamma[f, a, c] * weyl[b, f, d, e]
                            + gamma[f, a, d] * weyl[b, c, f, e]
                            + gamma[f, a, e] * weyl[b, c, d, f]
                            for f in range(4)
                        )
                        nabla_r[a, b, c, d, e] = driemann[b, c, d, e, a] - correction_r
                        nabla_c[a, b, c, d, e] = dweyl[b, c, d, e, a] - correction_c
    return {**raw, "nabla_riemann": nabla_r, "nabla_ricci": nabla_ric, "nabla_weyl": nabla_c, "gradients": gradients}


def derivative_grams(data: dict[str, torch.Tensor]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    gi = data["gi"]
    nr, nric, nc = data["nabla_riemann"], data["nabla_ricci"], data["nabla_weyl"]
    kr = torch.einsum("acdef,bghij,cg,dh,ei,fj->ab", nr, nr, gi, gi, gi, gi)
    kric = torch.einsum("acd,bef,ce,df->ab", nric, nric, gi, gi)
    kc = torch.einsum("acdef,bghij,cg,dh,ei,fj->ab", nc, nc, gi, gi, gi, gi)
    return kr, kric, kc


def frame_covariant(tensor: np.ndarray, coframe: np.ndarray) -> np.ndarray:
    frame = np.linalg.inv(coframe)
    return frame.T @ tensor @ frame


def spi_distribution(gradients: np.ndarray, metric: np.ndarray, coframe: np.ndarray) -> dict[str, object]:
    vectors_coordinate = gradients @ np.linalg.inv(metric)
    vectors_frame = vectors_coordinate @ coframe.T
    _, singular, vh = np.linalg.svd(vectors_frame, full_matrices=False)
    denominator = max(1.0, float(singular[0]) if len(singular) else 0.0)
    ratios = singular / denominator
    unresolved = any(RANK_TOL / 5.0 < value < 5.0 * RANK_TOL for value in ratios)
    rank = int(np.sum(ratios > RANK_TOL))
    result: dict[str, object] = {
        "rank": rank,
        "singular": singular,
        "ratios": ratios,
        "pair_defect": math.nan,
        "screen_defect": math.nan,
        "negative_directions": -1,
    }
    if unresolved:
        result["class"] = "SPI_DEGENERATE_OR_NUMERICALLY_UNRESOLVED"
        return result
    if rank <= 1:
        result["class"] = "SPI_RANK0_OR_1_UNDERDETERMINED"
        return result
    if rank >= 3:
        result["class"] = "SPI_RANK3_OR_4_NO_INTRINSIC_2PLANE"
        return result
    basis = vh[:2]
    restricted = basis @ ETA @ basis.T
    negative = int(np.sum(np.linalg.eigvalsh(restricted) < -1e-8))
    projector = basis.T @ basis
    pair = np.diag([1.0, 1.0, 0.0, 0.0])
    screen = np.diag([0.0, 0.0, 1.0, 1.0])
    pair_defect = float(np.linalg.norm(projector - pair))
    screen_defect = float(np.linalg.norm(projector - screen))
    result.update({"pair_defect": pair_defect, "screen_defect": screen_defect, "negative_directions": negative})
    if pair_defect <= 2e-3 and negative == 1:
        result["class"] = "SPI_RANK2_REGISTERED_PAIR"
    elif screen_defect <= 2e-3 and negative == 0:
        result["class"] = "SPI_RANK2_REGISTERED_SCREEN"
    else:
        result["class"] = "SPI_RANK2_ALTERNATIVE_PLANE"
    return result


def gram_diagnostic(k_frame: np.ndarray) -> dict[str, object]:
    endomorphism = ETA @ k_frame
    scale = max(1.0, float(np.linalg.norm(endomorphism)))
    off = np.block([
        [np.zeros((2, 2)), endomorphism[:2, 2:]],
        [endomorphism[2:, :2], np.zeros((2, 2))],
    ])
    residual = float(np.linalg.norm(off)) / scale
    pair_eig = np.linalg.eigvals(endomorphism[:2, :2])
    screen_eig = np.linalg.eigvals(endomorphism[2:, 2:])
    gap = float(min(abs(a - b) for a in pair_eig for b in screen_eig)) / scale
    norm = float(np.linalg.norm(endomorphism))
    if norm <= 1e-10:
        cls = "DERIVATIVE_GRAM_DEGENERATE"
    elif BLOCK_TOL / 5.0 < residual < 5.0 * BLOCK_TOL or GAP_TOL / 5.0 < gap < 5.0 * GAP_TOL:
        cls = "NUMERICALLY_UNRESOLVED"
    elif residual <= BLOCK_TOL / 5.0 and gap >= 5.0 * GAP_TOL:
        cls = "DERIVATIVE_GRAM_OWNS_REGISTERED_SPLIT"
    elif residual <= BLOCK_TOL / 5.0 and gap <= GAP_TOL / 5.0:
        cls = "DERIVATIVE_GRAM_PRESERVES_WITHOUT_GAP"
    else:
        cls = "DERIVATIVE_GRAM_DEFINES_ALTERNATIVE_SPECTRAL_STRUCTURE"
    return {"class": cls, "block_residual": residual, "spectral_gap": gap, "endomorphism": endomorphism}


def algebra_dimension(endomorphisms: list[np.ndarray]) -> int:
    normalized = []
    for matrix in endomorphisms:
        norm = np.linalg.norm(matrix)
        normalized.append(matrix / norm if norm > 1e-14 else matrix)
    basis: list[np.ndarray] = [np.eye(4)]
    queue = [np.eye(4)]
    while queue and len(basis) < 16:
        word = queue.pop(0)
        for generator in normalized:
            candidate = generator @ word
            norm = np.linalg.norm(candidate)
            if norm > 1e-14:
                candidate = candidate / norm
            old = np.stack([x.reshape(-1) for x in basis])
            new = np.vstack((old, candidate.reshape(1, -1)))
            if np.linalg.matrix_rank(new, tol=1e-8) > len(basis):
                basis.append(candidate)
                queue.append(candidate)
                if len(basis) == 16:
                    break
    return len(basis)


def classify_jet(jet: Jet) -> tuple[dict[str, object], dict[str, np.ndarray]]:
    x = torch.tensor(jet.x, dtype=torch.float64)
    data = covariant_derivatives(jet.metric_fn, x)
    grams = derivative_grams(data)
    metric = data["g"].detach().numpy()
    coframe = jet.coframe_fn(x).detach().numpy()
    gradients = data["gradients"].detach().numpy()
    spi = spi_distribution(gradients, metric, coframe)
    gram_frames = [frame_covariant(tensor.detach().numpy(), coframe) for tensor in grams]
    gram_results = [gram_diagnostic(tensor) for tensor in gram_frames]
    endomorphisms = [result["endomorphism"] for result in gram_results]
    owner_count = sum(result["class"] == "DERIVATIVE_GRAM_OWNS_REGISTERED_SPLIT" for result in gram_results)
    derivative_owner = owner_count > 0 or spi["class"] in {"SPI_RANK2_REGISTERED_PAIR", "SPI_RANK2_REGISTERED_SCREEN"}
    row = {
        "scope": jet.scope,
        "identity": jet.identity,
        "point": jet.point,
        "parent_owner_class": jet.parent_owner,
        "spi_class": spi["class"],
        "spi_rank": spi["rank"],
        "spi_singular_1": f"{spi['singular'][0]:.17g}",
        "spi_singular_2": f"{spi['singular'][1]:.17g}",
        "spi_singular_3": f"{spi['singular'][2]:.17g}",
        "spi_singular_4": f"{spi['singular'][3]:.17g}",
        "spi_pair_defect": f"{spi['pair_defect']:.17g}",
        "spi_screen_defect": f"{spi['screen_defect']:.17g}",
        "spi_negative_directions": spi["negative_directions"],
        "k_riem_class": gram_results[0]["class"],
        "k_riem_block_residual": f"{gram_results[0]['block_residual']:.17g}",
        "k_riem_spectral_gap": f"{gram_results[0]['spectral_gap']:.17g}",
        "k_ric_class": gram_results[1]["class"],
        "k_ric_block_residual": f"{gram_results[1]['block_residual']:.17g}",
        "k_ric_spectral_gap": f"{gram_results[1]['spectral_gap']:.17g}",
        "k_weyl_class": gram_results[2]["class"],
        "k_weyl_block_residual": f"{gram_results[2]['block_residual']:.17g}",
        "k_weyl_spectral_gap": f"{gram_results[2]['spectral_gap']:.17g}",
        "joint_registered_preservation": str(all(result["block_residual"] <= BLOCK_TOL / 5.0 for result in gram_results)).upper(),
        "generated_algebra_dimension": algebra_dimension(endomorphisms),
        "tested_derivative_owner": str(derivative_owner).upper(),
    }
    arrays = {
        "gradients": gradients,
        "k_riem": grams[0].detach().numpy(),
        "k_ric": grams[1].detach().numpy(),
        "k_weyl": grams[2].detach().numpy(),
        "nabla_riemann": data["nabla_riemann"].detach().numpy(),
        "nabla_ricci": data["nabla_ricci"].detach().numpy(),
        "nabla_weyl": data["nabla_weyl"].detach().numpy(),
    }
    return row, arrays


def landing(rows: list[dict[str, object]]) -> str:
    if any("UNRESOLVED" in str(value) for row in rows for value in row.values()):
        return "FIRST_DERIVATIVE_ATLAS_NUMERICALLY_OR_JET_UNRESOLVED"
    prior_misaligned = [row for row in rows if row["parent_owner_class"] == "SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS"]
    recovered = [row for row in prior_misaligned if row["tested_derivative_owner"] == "TRUE"]
    alternatives = [row for row in rows if row["spi_class"] == "SPI_RANK2_ALTERNATIVE_PLANE"]
    if prior_misaligned and len(recovered) == len(prior_misaligned):
        return "FIRST_DERIVATIVE_CONCOMITANTS_OWN_REGISTERED_SPLIT_ON_ALL_PRIOR_MISALIGNED_JETS"
    if recovered:
        return "FIRST_DERIVATIVE_CONCOMITANTS_OWN_REGISTERED_SPLIT_ON_A_PROPER_SUBSET"
    if alternatives:
        return "FIRST_DERIVATIVE_CONCOMITANTS_SUPPLY_ALTERNATIVE_INTRINSIC_DISTRIBUTIONS"
    return "NO_TESTED_FIRST_DERIVATIVE_CONCOMITANT_RECOVERS_REGISTERED_SPLIT"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="implementation smoke test only; nonbankable")
    parser.add_argument("--output-suffix", default="")
    args = parser.parse_args()
    source_count = verify_sources()
    jets = enumerate_jets()
    if args.limit:
        jets = jets[:args.limit]
    rows = []
    keys = []
    saved: dict[str, list[np.ndarray]] = {name: [] for name in ("gradients", "k_riem", "k_ric", "k_weyl", "nabla_riemann", "nabla_ricci", "nabla_weyl")}
    for index, jet in enumerate(jets, 1):
        row, arrays = classify_jet(jet)
        rows.append(row); keys.append(jet.key)
        for name, value in arrays.items():
            saved[name].append(value)
        if index % 25 == 0 or index == len(jets):
            print(f"completed {index}/{len(jets)}", flush=True)
    suffix = args.output_suffix
    if args.limit and not suffix:
        suffix = "_SMOKE"
    write_tsv(HERE / f"DERIVATIVE_DISTRIBUTION_ATLAS{suffix}.tsv", rows)
    np.savez_compressed(HERE / f"PRODUCTION_DERIVATIVE_TENSORS{suffix}.npz", keys=np.asarray(keys), **{name: np.asarray(values) for name, values in saved.items()})
    result = {
        "schema": "udt-first-curvature-derivative-distribution-v1",
        "status": "SMOKE_NONBANKABLE" if args.limit else "PRODUCTION_COMPLETE",
        "primary_landing": "SMOKE_NONBANKABLE" if args.limit else landing(rows),
        "counts": {"rows": len(rows), "G63": sum(row["scope"] == "G63" for row in rows), "G85": sum(row["scope"] == "G85" for row in rows)},
        "source_manifest_rows": source_count,
        "spi_counts": dict(sorted(Counter(str(row["spi_class"]) for row in rows).items())),
        "k_riem_counts": dict(sorted(Counter(str(row["k_riem_class"]) for row in rows).items())),
        "k_ric_counts": dict(sorted(Counter(str(row["k_ric_class"]) for row in rows).items())),
        "k_weyl_counts": dict(sorted(Counter(str(row["k_weyl_class"]) for row in rows).items())),
        "derivative_owner_count": sum(row["tested_derivative_owner"] == "TRUE" for row in rows),
        "no_physical_selection": True,
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "torch": torch.__version__},
    }
    (HERE / f"DERIVATION_RESULT{suffix}.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
