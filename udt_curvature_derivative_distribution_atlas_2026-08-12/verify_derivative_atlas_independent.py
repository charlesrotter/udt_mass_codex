#!/usr/bin/env python3
"""Independent nested finite-difference replay of the curvature-derivative atlas."""

from __future__ import annotations

import csv
import importlib.util
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT_DIR = ROOT / "udt_curvature_principal_split_ownership_audit_2026-08-12"
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
INNER_H = 2e-4
OUTER_LADDER = (8e-3, 4e-3, 2e-3)
RANK_TOL = 1e-7
BLOCK_TOL = 2e-6
GAP_TOL = 2e-5


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


BASE = load_module("independent_curvature_base", PARENT_DIR / "verify_curvature_split_independent.py")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def levi_symbol() -> np.ndarray:
    out = np.zeros((4, 4, 4, 4))
    for p in itertools.permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
        out[p] = -1.0 if inversions % 2 else 1.0
    return out


EPS = levi_symbol()


def curvature_all(fun, x: np.ndarray) -> dict[str, np.ndarray | float]:
    g = fun(x); gi = np.linalg.inv(g); gamma = BASE.connection(fun, x, INNER_H)
    dgamma = np.array([BASE.fd1(lambda y: BASE.connection(fun, y, INNER_H), x, axis, INNER_H) for axis in range(4)])
    rup = np.zeros((4, 4, 4, 4))
    for a, b, c, d in itertools.product(range(4), repeat=4):
        rup[a, b, c, d] = dgamma[c, a, d, b] - dgamma[d, a, c, b] + sum(
            gamma[a, c, e] * gamma[e, d, b] - gamma[a, d, e] * gamma[e, c, b]
            for e in range(4)
        )
    riemann = np.einsum("ae,ebcd->abcd", g, rup)
    ricci = np.einsum("abad->bd", rup)
    scalar = np.einsum("ab,ab", gi, ricci)
    weyl = np.zeros_like(riemann)
    for a, b, c, d in itertools.product(range(4), repeat=4):
        weyl[a, b, c, d] = riemann[a, b, c, d] - 0.5 * (
            g[a, c] * ricci[d, b] - g[a, d] * ricci[c, b]
            - g[b, c] * ricci[d, a] + g[b, d] * ricci[c, a]
        ) + scalar / 6.0 * (g[a, c] * g[d, b] - g[a, d] * g[c, b])
    return {"g": g, "gi": gi, "gamma": gamma, "riemann": riemann, "ricci": ricci, "scalar": scalar, "weyl": weyl}


def invariants(raw: dict[str, np.ndarray | float]) -> np.ndarray:
    g = raw["g"]; gi = raw["gi"]; ricci = raw["ricci"]; weyl = raw["weyl"]
    mixed = gi @ ricci
    cop = np.einsum("abef,ec,fd->abcd", weyl, gi, gi)
    eps_cov = np.sqrt(abs(np.linalg.det(g))) * EPS
    eps_mixed = np.einsum("abmn,mc,nd->abcd", eps_cov, gi, gi)
    star_weyl = 0.5 * np.einsum("abef,efcd->abcd", eps_mixed, weyl)
    star_cop = np.einsum("abef,ec,fd->abcd", star_weyl, gi, gi)
    return np.array((
        raw["scalar"], np.trace(mixed @ mixed), np.trace(mixed @ mixed @ mixed),
        np.einsum("abcd,cdab", cop, cop), np.einsum("abcd,cdab", star_cop, cop),
        np.einsum("abcd,cdef,efab", cop, cop, cop),
        np.einsum("abcd,cdef,efab", star_cop, cop, cop),
    ))


def stencil(values: dict[tuple[int, int], dict[str, np.ndarray | float]], name: str, axis: int, h: float) -> np.ndarray:
    return (
        -np.asarray(values[(axis, 2)][name]) + 8 * np.asarray(values[(axis, 1)][name])
        - 8 * np.asarray(values[(axis, -1)][name]) + np.asarray(values[(axis, -2)][name])
    ) / (12 * h)


def derivative_data(fun, x: np.ndarray, h: float) -> dict[str, np.ndarray]:
    central = curvature_all(fun, x)
    values: dict[tuple[int, int], dict[str, np.ndarray | float]] = {}
    invariant_values: dict[tuple[int, int], np.ndarray] = {}
    for axis in range(4):
        direction = np.zeros(4); direction[axis] = h
        for multiple in (-2, -1, 1, 2):
            raw = curvature_all(fun, x + multiple * direction)
            values[(axis, multiple)] = raw
            invariant_values[(axis, multiple)] = invariants(raw)
    dr = np.stack([stencil(values, "riemann", axis, h) for axis in range(4)], axis=-1)
    dric = np.stack([stencil(values, "ricci", axis, h) for axis in range(4)], axis=-1)
    dc = np.stack([stencil(values, "weyl", axis, h) for axis in range(4)], axis=-1)
    gradients = np.stack([
        (-invariant_values[(axis, 2)] + 8 * invariant_values[(axis, 1)]
         - 8 * invariant_values[(axis, -1)] + invariant_values[(axis, -2)]) / (12 * h)
        for axis in range(4)
    ], axis=1)
    gamma = central["gamma"]; riemann = central["riemann"]; ricci = central["ricci"]; weyl = central["weyl"]
    nr = np.empty((4, 4, 4, 4, 4)); nc = np.empty_like(nr); nric = np.empty((4, 4, 4))
    for a, b, c in itertools.product(range(4), repeat=3):
        nric[a, b, c] = dric[b, c, a] - sum(
            gamma[f, a, b] * ricci[f, c] + gamma[f, a, c] * ricci[b, f]
            for f in range(4)
        )
        for d, e in itertools.product(range(4), repeat=2):
            nr[a, b, c, d, e] = dr[b, c, d, e, a] - sum(
                gamma[f, a, b] * riemann[f, c, d, e]
                + gamma[f, a, c] * riemann[b, f, d, e]
                + gamma[f, a, d] * riemann[b, c, f, e]
                + gamma[f, a, e] * riemann[b, c, d, f]
                for f in range(4)
            )
            nc[a, b, c, d, e] = dc[b, c, d, e, a] - sum(
                gamma[f, a, b] * weyl[f, c, d, e]
                + gamma[f, a, c] * weyl[b, f, d, e]
                + gamma[f, a, d] * weyl[b, c, f, e]
                + gamma[f, a, e] * weyl[b, c, d, f]
                for f in range(4)
            )
    gi = central["gi"]
    kr = np.einsum("acdef,bghij,cg,dh,ei,fj->ab", nr, nr, gi, gi, gi, gi)
    kric = np.einsum("acd,bef,ce,df->ab", nric, nric, gi, gi)
    kc = np.einsum("acdef,bghij,cg,dh,ei,fj->ab", nc, nc, gi, gi, gi, gi)
    return {"gradients": gradients, "k_riem": kr, "k_ric": kric, "k_weyl": kc, "nabla_riemann": nr, "nabla_ricci": nric, "nabla_weyl": nc, "metric": central["g"]}


def enumerate_jets():
    out = []
    for sample in BASE.samples():
        p = np.array([.07, 1.08, .31, .44]) if sample.geometry == "R17_GLOBAL" else np.array([.12, -.18, .23, -.14])
        offsets = [np.zeros(4), np.array([.08, .035, -.04, .06]), np.array([.13, -.025, .07, .11])] if sample.geometry == "R17_GLOBAL" else [np.zeros(4), np.array([.07, -.05, .04, .03]), np.array([.14, .025, -.06, .08])]
        for point, offset in zip(("p", "q", "r"), offsets):
            fun = lambda x, sample=sample: BASE.g63_metric(x, sample)
            coframe = lambda x, sample=sample: BASE.r17_E(x, sample) if sample.geometry == "R17_GLOBAL" else BASE.live_E(x, sample)
            out.append((f"G63|{sample.name}|{point}", fun, coframe, p + offset))
    profiles = BASE.profiles(); controls = (("C0", 0., 0.), ("CMINUS", -.3, .4), ("CPLUS", .3, .4))
    for pid, coeff in sorted(profiles.items()):
        for arch in ("A03_RADIAL_SHIFT_TIMELIVE", "A04_LAPSE_LIFT_TIMELIVE"):
            for point, eps, tau in controls:
                fun = lambda x, coeff=coeff, arch=arch, eps=eps: BASE.g85_metric(x, coeff, arch, eps)
                coframe = lambda x, fun=fun: BASE.metric_coframe(fun(x))
                out.append((f"G85|{pid}:{arch}|{point}", fun, coframe, np.array([tau, np.pi/2, 1.1, .37])))
    _, coeff = sorted(profiles.items())[0]
    for point, eps, tau in controls:
        fun = lambda x, coeff=coeff, eps=eps: BASE.g85_metric(x, coeff, "A05_SHIFT_SUPPORTED_TAPER", eps)
        coframe = lambda x, fun=fun: BASE.metric_coframe(fun(x))
        out.append((f"G85|A05_UNIQUE|{point}", fun, coframe, np.array([tau, np.pi/2, 1.1, .37])))
    assert len(out) == len({x[0] for x in out}) == 1221
    return out


def relative(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(1., np.linalg.norm(a), np.linalg.norm(b)))


def spi_class(gradients: np.ndarray, metric: np.ndarray, coframe: np.ndarray) -> tuple[str, int, np.ndarray]:
    vectors = gradients @ np.linalg.inv(metric) @ coframe.T
    _, singular, vh = np.linalg.svd(vectors, full_matrices=False)
    ratios = singular / max(1., singular[0])
    if any(RANK_TOL/5 < value < 5*RANK_TOL for value in ratios):
        return "SPI_DEGENERATE_OR_NUMERICALLY_UNRESOLVED", -1, np.zeros((4, 4))
    rank = int(np.sum(ratios > RANK_TOL))
    if rank <= 1: return "SPI_RANK0_OR_1_UNDERDETERMINED", rank, np.zeros((4, 4))
    if rank >= 3: return "SPI_RANK3_OR_4_NO_INTRINSIC_2PLANE", rank, np.eye(4)
    basis = vh[:2]; projector = basis.T @ basis; negative = np.sum(np.linalg.eigvalsh(basis @ ETA @ basis.T) < -1e-8)
    if np.linalg.norm(projector - np.diag([1,1,0,0])) <= 2e-3 and negative == 1: cls = "SPI_RANK2_REGISTERED_PAIR"
    elif np.linalg.norm(projector - np.diag([0,0,1,1])) <= 2e-3 and negative == 0: cls = "SPI_RANK2_REGISTERED_SCREEN"
    else: cls = "SPI_RANK2_ALTERNATIVE_PLANE"
    return cls, rank, projector


def gram_class(k: np.ndarray, coframe: np.ndarray) -> str:
    frame = np.linalg.inv(coframe); kf = frame.T @ k @ frame; op = ETA @ kf; scale = max(1., np.linalg.norm(op))
    off = np.block([[np.zeros((2,2)),op[:2,2:]],[op[2:,:2],np.zeros((2,2))]])
    residual = np.linalg.norm(off)/scale
    gap = min(abs(a-b) for a in np.linalg.eigvals(op[:2,:2]) for b in np.linalg.eigvals(op[2:,2:]))/scale
    if np.linalg.norm(op) <= 1e-10: return "DERIVATIVE_GRAM_DEGENERATE"
    if BLOCK_TOL/5 < residual < 5*BLOCK_TOL or GAP_TOL/5 < gap < 5*GAP_TOL: return "NUMERICALLY_UNRESOLVED"
    if residual <= BLOCK_TOL/5 and gap >= 5*GAP_TOL: return "DERIVATIVE_GRAM_OWNS_REGISTERED_SPLIT"
    if residual <= BLOCK_TOL/5 and gap <= GAP_TOL/5: return "DERIVATIVE_GRAM_PRESERVES_WITHOUT_GAP"
    return "DERIVATIVE_GRAM_DEFINES_ALTERNATIVE_SPECTRAL_STRUCTURE"


def main() -> None:
    production_rows = rows(HERE / "DERIVATIVE_DISTRIBUTION_ATLAS.tsv")
    production_npz = np.load(HERE / "PRODUCTION_DERIVATIVE_TENSORS.npz")
    production = {key: (row, index) for index, (key, row) in enumerate(zip(production_npz["keys"], production_rows))}
    comparisons = []; saved = {name: [] for name in ("gradients", "k_riem", "k_ric", "k_weyl", "nabla_riemann", "nabla_ricci", "nabla_weyl")}; saved_keys=[]
    for number, (key, fun, coframe_fn, x) in enumerate(enumerate_jets(), 1):
        ladder = [derivative_data(fun, x, h) for h in OUTER_LADDER]
        data = ladder[1]; row, index = production[key]; coframe = coframe_fn(x)
        spi, rank, projector = spi_class(data["gradients"], data["metric"], coframe)
        gram_classes = [gram_class(data[name], coframe) for name in ("k_riem", "k_ric", "k_weyl")]
        errors = {name: relative(data[name], production_npz[name][index]) for name in saved}
        convergence = max(relative(ladder[0][name], ladder[2][name]) for name in saved)
        pspi, prank, pprojector = spi_class(production_npz["gradients"][index], data["metric"], coframe)
        projector_defect = relative(projector, pprojector) if rank == prank == 2 else (0.0 if rank == prank else math.inf)
        same = spi == row["spi_class"] and gram_classes == [row["k_riem_class"], row["k_ric_class"], row["k_weyl_class"]]
        passed = max(errors.values()) <= 5e-3 and projector_defect <= 2e-3 and same
        comparisons.append({"key":key,"max_tensor_relative_error":f"{max(errors.values()):.17g}","gradient_relative_error":f"{errors['gradients']:.17g}","spi_projector_defect":f"{projector_defect:.17g}","outer_ladder_max_difference":f"{convergence:.17g}","production_spi":row["spi_class"],"independent_spi":spi,"production_gram_classes":"|".join((row["k_riem_class"],row["k_ric_class"],row["k_weyl_class"])),"independent_gram_classes":"|".join(gram_classes),"pass":str(passed).upper()})
        saved_keys.append(key)
        for name in saved: saved[name].append(data[name])
        if number % 10 == 0 or number == 1221: print(f"independent {number}/1221",flush=True)
    with (HERE/"INDEPENDENT_COMPARISON.tsv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(comparisons[0]),delimiter="\t",lineterminator="\n");writer.writeheader();writer.writerows(comparisons)
    np.savez_compressed(HERE/"INDEPENDENT_DERIVATIVE_TENSORS.npz",keys=np.asarray(saved_keys),**{name:np.asarray(values) for name,values in saved.items()})
    projector_values=[float(x["spi_projector_defect"]) for x in comparisons]
    result={"schema":"udt-first-curvature-derivative-independent-v1","status":"PASS" if all(x["pass"]=="TRUE" for x in comparisons) else "FAIL","checks":len(comparisons),"pass_count":sum(x["pass"]=="TRUE" for x in comparisons),"max_tensor_relative_error":max(float(x["max_tensor_relative_error"]) for x in comparisons),"max_gradient_relative_error":max(float(x["gradient_relative_error"]) for x in comparisons),"max_finite_spi_projector_defect":max((x for x in projector_values if math.isfinite(x)),default=0.0),"spi_projector_unmatched_count":sum(not math.isfinite(x) for x in projector_values),"max_outer_ladder_difference":max(float(x["outer_ladder_max_difference"]) for x in comparisons),"spi_counts":dict(sorted(Counter(x["independent_spi"] for x in comparisons).items()))}
    (HERE/"INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    if result["status"] != "PASS": raise RuntimeError("independent verification failed")


if __name__ == "__main__":
    main()
