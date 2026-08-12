#!/usr/bin/env python3
"""Metric-led curvature-principal split ownership atlas.

This script classifies supplied metric witnesses.  It does not select a physical
history, observer query, pair realization, action, source, or boundary.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp
import torch
from torch.func import jacrev


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G63 = ROOT / "udt_solved_geometry_relation_family_survivor_atlas_2026-08-11"
G85 = ROOT / "udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12"
ETA_T = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0], dtype=torch.float64))
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
ALG_TOL = 1.0e-9
EIG_TOL = 2.0e-7
ALIGN_TOL = 2.0e-7
RICCI_GAP_TOL = 2.0e-6


@dataclass(frozen=True)
class G63Sample:
    sample_id: str
    geometry: str
    lam: float = 0.0
    eps: float = 0.0
    twist: float = 0.4


@dataclass(frozen=True)
class G85Witness:
    profile_id: str
    q_coefficients: tuple[float, ...]
    archetype: str
    control: str
    epsilon: float
    tau: float


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
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
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    if len(rows) != 12 or len({row["path"] for row in rows}) != 12:
        raise RuntimeError("source manifest is not the reviewed 12-source universe")
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"]:
            raise RuntimeError(f"source hash failure: {path}")
    return len(rows)


def load_g63_samples() -> list[G63Sample]:
    out: list[G63Sample] = []
    for row in read_tsv(G63 / "NUMERICAL_SAMPLE_UNIVERSE.tsv"):
        pars = {
            x.split("=", 1)[0]: x.split("=", 1)[1]
            for x in (row["parameter_1"], row["parameter_2"])
            if "=" in x
        }
        out.append(G63Sample(row["sample_id"], row["geometry"], float(pars.get("lambda", 0)), float(pars.get("epsilon", 0))))
    if len(out) != 14 or len({sample.sample_id for sample in out}) != 14:
        raise RuntimeError("G63 universe is not exactly 14 unique samples")
    return out


def load_g85_profiles() -> dict[str, tuple[float, ...]]:
    s = sp.symbols("s", real=True)
    rows = read_tsv(G85 / "PROFILE_ARCHETYPE_ATLAS.tsv")
    profiles: dict[str, tuple[float, ...]] = {}
    for row in rows:
        pid = row["profile_id"]
        poly = sp.Poly(sp.sympify(row["q_of_s"], locals={"s": s}), s)
        coeff = tuple(float(poly.nth(i)) for i in range(poly.degree() + 1))
        if pid in profiles and profiles[pid] != coeff:
            raise RuntimeError(f"profile polynomial changed across archetypes: {pid}")
        profiles[pid] = coeff
    if len(profiles) != 196:
        raise RuntimeError(f"expected 196 G85 profiles, got {len(profiles)}")
    return profiles


def g63_r17_phi(x: torch.Tensor, eps: float) -> torch.Tensor:
    _, th, va, ps = x.unbind()
    x1 = torch.cos(th / 2) * torch.cos((ps + va) / 2)
    x2 = torch.cos(th / 2) * torch.sin((ps + va) / 2)
    x3 = torch.sin(th / 2) * torch.cos((ps - va) / 2)
    x4 = torch.sin(th / 2) * torch.sin((ps - va) / 2)
    return 0.12 * x1 + 0.08 * x2 * x3 - 0.05 * (x4 * x4 - x3 * x3) + eps * (0.11 * x4 + 0.07 * x1 * x2)


def g63_r17_coframe(x: torch.Tensor, sample: G63Sample) -> torch.Tensor:
    _, th, _, ps = x.unbind()
    phi = g63_r17_phi(x, sample.eps)
    u, v = torch.exp(phi), torch.exp(sample.lam * phi)
    zero = torch.zeros((), dtype=x.dtype)
    one = torch.ones((), dtype=x.dtype)
    s1 = 0.5 * torch.stack((zero, torch.cos(ps), torch.sin(ps) * torch.sin(th), zero))
    s2 = 0.5 * torch.stack((zero, -torch.sin(ps), torch.cos(ps) * torch.sin(th), zero))
    s3 = 0.5 * torch.stack((zero, zero, torch.cos(th), one))
    dt = torch.stack((one, zero, zero, zero))
    return torch.stack(((dt + sample.twist * s3) / u, u * s3, v * s1, v * s2))


def g63_timelive_coframe(x: torch.Tensor, sample: G63Sample) -> torch.Tensor:
    t, xx, y, z = x.unbind(); e = sample.eps
    kap = .035*torch.sin(t+.3*y)+.018*torch.cos(xx-z)+e*.025*torch.sin(t+xx+y)
    phi = .11*torch.cos(xx-.2*t)+.025*torch.sin(y+z)+e*.08*torch.cos(t-z+.4*xx)
    beta = .12*torch.sin(t+xx)+.04*torch.cos(y-z)+e*.05*torch.sin(t+y)
    gam = .16*torch.sin(t-y+.2*z)+e*.04*torch.cos(xx+z)
    q1 = .045*torch.cos(t+y)+e*.03*torch.sin(xx-z)
    q2 = -.035*torch.sin(xx+z)+e*.025*torch.cos(t-y)
    shear = .07*torch.sin(t+xx+y+z)+e*.025*torch.cos(xx-y)
    S = torch.stack((
        torch.stack((.055*torch.cos(t+y)+e*.02*torch.sin(z), .045*torch.sin(xx-z)+e*.015*torch.cos(t+y))),
        torch.stack((-.04*torch.cos(t-xx+y)+e*.02*torch.sin(xx+z), .05*torch.sin(t+z)+e*.018*torch.cos(xx-y))),
    ))
    T, L = torch.exp(kap-phi), torch.exp(kap+phi)
    zero = torch.zeros((), dtype=x.dtype)
    B = torch.stack((torch.stack((T, T*beta)), torch.stack((zero, L))))
    R = torch.stack((torch.stack((torch.cos(gam),-torch.sin(gam))), torch.stack((torch.sin(gam),torch.cos(gam)))))
    U = torch.stack((torch.stack((torch.exp(q1),shear)), torch.stack((zero,torch.exp(q2)))))
    Q = R @ U
    top = torch.cat((B, torch.zeros((2,2), dtype=x.dtype)), dim=1)
    bottom = torch.cat((Q @ S, Q), dim=1)
    return torch.cat((top, bottom), dim=0)


def g63_coframe(x: torch.Tensor, sample: G63Sample) -> torch.Tensor:
    return g63_r17_coframe(x, sample) if sample.geometry == "R17_GLOBAL" else g63_timelive_coframe(x, sample)


def g63_metric(x: torch.Tensor, sample: G63Sample) -> torch.Tensor:
    E = g63_coframe(x, sample)
    return E.T @ ETA_T @ E


def polynomial(x: torch.Tensor, coefficients: tuple[float, ...]) -> torch.Tensor:
    value = torch.zeros((), dtype=x.dtype)
    for coefficient in reversed(coefficients):
        value = value * x + coefficient
    return value


def g85_metric(x: torch.Tensor, witness: G85Witness) -> torch.Tensor:
    tau, chi, theta, _ = x.unbind()
    A = torch.cos(chi) ** 2
    D = 4.0 * torch.sin(chi) ** 2
    C = D * torch.sin(theta) ** 2
    time_factor = 1.0 + witness.epsilon * torch.sin(1.1 * tau)
    if witness.archetype == "A03_RADIAL_SHIFT_TIMELIVE":
        u, b = -A, 0.6 * time_factor
        h = D * polynomial(D, witness.q_coefficients)
    elif witness.archetype == "A04_LAPSE_LIFT_TIMELIVE":
        u, b = -A - 0.45 * time_factor, torch.zeros((), dtype=x.dtype)
        h = D * polynomial(D, witness.q_coefficients)
    elif witness.archetype == "A05_SHIFT_SUPPORTED_TAPER":
        u, b = -A, 0.6 * time_factor
        h = torch.zeros((), dtype=x.dtype)
    else:
        raise ValueError(witness.archetype)
    H = h * torch.sin(theta) ** 2
    zero = torch.zeros((), dtype=x.dtype)
    return torch.stack((
        torch.stack((u, b, zero, H)),
        torch.stack((b, torch.as_tensor(4.0, dtype=x.dtype), zero, zero)),
        torch.stack((zero, zero, D, zero)),
        torch.stack((H, zero, zero, C)),
    ))


def coframe_from_metric(g: torch.Tensor) -> torch.Tensor:
    """Return a pair-adapted orthonormal coframe for a regular 2+2 block metric."""
    screen = g[2:, 2:]
    cross = g[:2, 2:]
    S = torch.linalg.solve(screen, cross.T)
    base = g[:2, :2] - cross @ torch.linalg.solve(screen, cross.T)
    vals, vecs = torch.linalg.eigh(base)
    neg = int(torch.argmin(vals).item())
    pos = 1 - neg
    if not (vals[neg] < 0 and vals[pos] > 0):
        raise RuntimeError("base block is not Lorentzian")
    # Rows are normalized covectors after diagonalizing the covariant metric.
    B = torch.stack((vecs[:, neg] * torch.sqrt(-vals[neg]), vecs[:, pos] * torch.sqrt(vals[pos])))
    Q = torch.linalg.cholesky(screen).T
    E = torch.zeros((4, 4), dtype=g.dtype)
    E[:2, :2] = B
    E[2:, :2] = Q @ S
    E[2:, 2:] = Q
    defect = torch.linalg.norm(E.T @ ETA_T @ E - g)
    if float(defect) > 5e-10:
        raise RuntimeError(f"coframe reconstruction defect {float(defect)}")
    return E


def g63_points(sample: G63Sample) -> dict[str, np.ndarray]:
    if sample.geometry == "R17_GLOBAL":
        p = np.array([0.07, 1.08, 0.31, 0.44])
        q = p + np.array([0.08, 0.035, -0.04, 0.06])
        r = p + np.array([0.13, -0.025, 0.07, 0.11])
    else:
        p = np.array([0.12, -0.18, 0.23, -0.14])
        q = p + np.array([0.07, -0.05, 0.04, 0.03])
        r = p + np.array([0.14, 0.025, -0.06, 0.08])
    return {"p": p, "q": q, "r": r}


def christoffel(metric_fn, x: torch.Tensor) -> torch.Tensor:
    g = metric_fn(x)
    gi = torch.linalg.inv(g)
    dg = jacrev(metric_fn)(x)  # dg[a,b,k]
    G = torch.zeros((4, 4, 4), dtype=x.dtype)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                G[a, b, c] = 0.5 * sum(
                    gi[a, d] * (dg[d, c, b] + dg[d, b, c] - dg[b, c, d])
                    for d in range(4)
                )
    return G


def curvature(metric_fn, coframe_fn, x_np: np.ndarray) -> dict[str, np.ndarray | float]:
    x = torch.tensor(x_np, dtype=torch.float64)
    g = metric_fn(x)
    G_fn = lambda y: christoffel(metric_fn, y)
    G = G_fn(x)
    dG = jacrev(G_fn)(x)  # dG[a,b,c,k]
    Rup = torch.zeros((4,4,4,4), dtype=x.dtype)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    Rup[a,b,c,d] = (
                        dG[a,d,b,c] - dG[a,c,b,d]
                        + sum(G[a,c,e]*G[e,d,b] - G[a,d,e]*G[e,c,b] for e in range(4))
                    )
    Rdown = torch.einsum("ae,ebcd->abcd", g, Rup)
    Ric = torch.einsum("abad->bd", Rup)
    gi = torch.linalg.inv(g)
    scalar = torch.einsum("ab,ab->", gi, Ric)
    Weyl = torch.zeros_like(Rdown)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    Weyl[a,b,c,d] = Rdown[a,b,c,d] - 0.5*(
                        g[a,c]*Ric[d,b] - g[a,d]*Ric[c,b]
                        - g[b,c]*Ric[d,a] + g[b,d]*Ric[c,a]
                    ) + scalar/6.0*(g[a,c]*g[d,b]-g[a,d]*g[c,b])
    E = coframe_fn(x)
    frame = torch.linalg.inv(E)
    Wf = torch.einsum("ma,nb,pc,qd,mnpq->abcd", frame, frame, frame, frame, Weyl)
    Rf = torch.einsum("ma,nb,mn->ab", frame, frame, Ric)
    result = {
        "metric": g.detach().numpy(),
        "coframe": E.detach().numpy(),
        "weyl_coordinate": Weyl.detach().numpy(),
        "ricci_coordinate": Ric.detach().numpy(),
        "riemann_frame": torch.einsum("ma,nb,pc,qd,mnpq->abcd", frame, frame, frame, frame, Rdown).detach().numpy(),
        "weyl_frame": Wf.detach().numpy(),
        "ricci_frame": Rf.detach().numpy(),
        "scalar": float(scalar),
    }
    return result


def self_dual_weyl(weyl_frame: np.ndarray) -> tuple[np.ndarray, float, float]:
    electric = np.empty((3,3), dtype=float)
    magnetic = np.zeros((3,3), dtype=float)
    eps = np.zeros((3,3,3), dtype=float)
    eps[0,1,2] = eps[1,2,0] = eps[2,0,1] = 1.0
    eps[0,2,1] = eps[2,1,0] = eps[1,0,2] = -1.0
    for i in range(3):
        for j in range(3):
            electric[i,j] = weyl_frame[0,i+1,0,j+1]
            magnetic[i,j] = 0.5 * sum(
                eps[i,k,l] * weyl_frame[k+1,l+1,0,j+1]
                for k in range(3) for l in range(3)
            )
    Q = electric + 1j * magnetic
    trace_defect = float(abs(np.trace(Q)))
    symmetry_defect = float(np.linalg.norm(Q-Q.T))
    return Q, trace_defect, symmetry_defect


def matrix_rank(a: np.ndarray, scale: float) -> int:
    singular = np.linalg.svd(a, compute_uv=False)
    return int(np.sum(singular > ALG_TOL * max(1.0, scale)))


def petrov_class(Q: np.ndarray) -> tuple[str, dict[str, object]]:
    norm = float(np.linalg.norm(Q))
    scale = max(1.0, norm)
    Q2, Q3 = Q @ Q, Q @ Q @ Q
    eig = np.linalg.eigvals(Q)
    I = 0.5 * np.trace(Q2)
    Jdet = np.linalg.det(Q)
    discriminant = 4.0 * I**3 - 27.0 * Jdet**2
    near_alg = lambda value: ALG_TOL/5.0 < value/scale < 5.0*ALG_TOL
    if near_alg(norm) or near_alg(float(np.linalg.norm(Q2))) or near_alg(float(np.linalg.norm(Q3))):
        ptype = "NUMERICALLY_UNRESOLVED"
    elif norm <= ALG_TOL:
        ptype = "O"
    elif np.linalg.norm(Q2) <= ALG_TOL * scale:
        ptype = "N"
    elif np.linalg.norm(Q3) <= ALG_TOL * scale:
        ptype = "III"
    else:
        distances = [abs(eig[i]-eig[j])/scale for i in range(3) for j in range(i+1,3)]
        minimum_distance = min(distances)
        if EIG_TOL/5.0 < minimum_distance < 5.0*EIG_TOL:
            ptype = "NUMERICALLY_UNRESOLVED"
        elif minimum_distance > EIG_TOL:
            ptype = "I"
        else:
            pair = min(((i,j) for i in range(3) for j in range(i+1,3)), key=lambda ij: abs(eig[ij[0]]-eig[ij[1]]))
            repeated = 0.5 * (eig[pair[0]] + eig[pair[1]])
            rank = matrix_rank(Q-repeated*np.eye(3), scale)
            ptype = "D" if rank <= 1 else "II"
    diagnostics = {
        "norm": norm,
        "I_real": float(I.real), "I_imag": float(I.imag),
        "Jdet_real": float(Jdet.real), "Jdet_imag": float(Jdet.imag),
        "discriminant_abs": float(abs(discriminant)),
        "eig": eig,
        "q2_norm": float(np.linalg.norm(Q2)),
        "q3_norm": float(np.linalg.norm(Q3)),
    }
    return ptype, diagnostics


def weyl_split_diagnostics(Q: np.ndarray, ptype: str) -> dict[str, object]:
    scale = max(1.0, float(np.linalg.norm(Q)))
    registered_residual = float(np.linalg.norm(Q[1:,0])) / scale
    eigvals, eigvecs = np.linalg.eig(Q)
    best = int(np.argmax(np.abs(eigvecs[0,:]) / np.linalg.norm(eigvecs, axis=0)))
    v = eigvecs[:,best] / np.linalg.norm(eigvecs[:,best])
    target = np.zeros((3,3), dtype=complex); target[0,0] = 1.0
    projector_defect = float(np.linalg.norm(np.outer(v, v.conj()) - target))
    gap = float(min(abs(eigvals[best]-eigvals[j]) for j in range(3) if j != best)) / scale
    aligned = registered_residual <= ALIGN_TOL and projector_defect <= 5.0*ALIGN_TOL
    unique = ptype == "D" and aligned and gap > EIG_TOL
    finite = ptype == "I" and aligned
    return {
        "registered_residual": registered_residual,
        "projector_defect": projector_defect,
        "principal_gap": gap,
        "aligned": aligned,
        "unique": unique,
        "finite": finite,
    }


def ricci_split_diagnostics(ricci_frame: np.ndarray) -> dict[str, object]:
    operator = ETA @ ricci_frame
    scale = max(1.0, float(np.linalg.norm(operator)))
    off = np.block([[np.zeros((2,2)), operator[:2,2:]], [operator[2:,:2], np.zeros((2,2))]])
    residual = float(np.linalg.norm(off)) / scale
    pair_eig = np.linalg.eigvals(operator[:2,:2])
    screen_eig = np.linalg.eigvals(operator[2:,2:])
    gap = float(min(abs(a-b) for a in pair_eig for b in screen_eig))
    preserve = residual <= ALIGN_TOL
    owns = preserve and gap >= RICCI_GAP_TOL * scale
    return {
        "operator": operator,
        "block_residual": residual,
        "spectral_gap": gap / scale,
        "preserves": preserve,
        "owns": owns,
    }


def owner_class(ptype: str, w: dict[str, object], r: dict[str, object]) -> str:
    if ptype == "NUMERICALLY_UNRESOLVED":
        return "NUMERICALLY_UNRESOLVED"
    if bool(w["unique"]) and bool(r["owns"]):
        return "WEYL_AND_RICCI_AGREE_ON_SPLIT"
    if bool(w["unique"]):
        return "UNIQUE_WEYL_DERIVED_SPLIT"
    if bool(w["finite"]) and bool(r["owns"]):
        return "RICCI_DERIVED_WITH_WEYL_ALIGNMENT"
    if bool(w["finite"]):
        return "FINITE_WEYL_PRINCIPAL_CANDIDATES__REGISTERED_ONE_ALIGNED"
    if ptype == "O" and bool(r["owns"]):
        return "RICCI_DERIVED_WHEN_WEYL_DEGENERATE"
    if bool(r["preserves"]) or bool(w["aligned"]):
        return "CURVATURE_ALIGNED_BUT_NOT_UNIQUE"
    if ptype in {"I", "D", "II"}:
        return "SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS"
    return "NO_TESTED_POINTWISE_CURVATURE_OWNER"


def classify(curv: dict[str, np.ndarray | float]) -> dict[str, object]:
    Q, trace_defect, symmetry_defect = self_dual_weyl(curv["weyl_frame"])
    ptype, pdiag = petrov_class(Q)
    wdiag = weyl_split_diagnostics(Q, ptype)
    rdiag = ricci_split_diagnostics(curv["ricci_frame"])
    return {
        "petrov": ptype,
        "Q": Q,
        "trace_defect": trace_defect,
        "symmetry_defect": symmetry_defect,
        "petrov_diag": pdiag,
        "weyl_split": wdiag,
        "ricci_split": rdiag,
        "owner_class": owner_class(ptype, wdiag, rdiag),
    }


def invariant_eigenvalue_defect(a: np.ndarray, b: np.ndarray) -> float:
    import itertools
    scale = max(1.0, float(np.linalg.norm(a)), float(np.linalg.norm(b)))
    return min(max(abs(a[i]-b[p[i]]) for i in range(3)) for p in itertools.permutations(range(3))) / scale


def split_preserving_frame_test(curv: dict[str, np.ndarray | float], base: dict[str, object]) -> tuple[float, bool]:
    rapidity, angle = 0.23, 0.31
    L = np.eye(4)
    L[:2,:2] = [[math.cosh(rapidity), math.sinh(rapidity)], [math.sinh(rapidity), math.cosh(rapidity)]]
    L[2:,2:] = [[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]]
    A = np.linalg.inv(L)
    W2 = np.einsum("ma,nb,pc,qd,mnpq->abcd", A,A,A,A,curv["weyl_frame"])
    R2 = np.einsum("ma,nb,mn->ab", A,A,curv["ricci_frame"])
    other = classify({"weyl_frame":W2,"ricci_frame":R2})
    defect = invariant_eigenvalue_defect(np.linalg.eigvals(base["Q"]), np.linalg.eigvals(other["Q"]))
    same = base["petrov"] == other["petrov"] and base["owner_class"] == other["owner_class"]
    return defect, same


def result_row(scope: str, identity: str, point: str, curv: dict[str, object], result: dict[str, object]) -> dict[str, object]:
    pdiag = result["petrov_diag"]
    wdiag = result["weyl_split"]
    rdiag = result["ricci_split"]
    frame_defect, frame_same = split_preserving_frame_test(curv, result)
    signature = np.linalg.eigvalsh(curv["metric"])
    riemann = curv["riemann_frame"]
    return {
        "scope": scope,
        "identity": identity,
        "point": point,
        "petrov": result["petrov"],
        "owner_class": result["owner_class"],
        "metric_negative_eigenvalues": int(np.sum(signature < 0)),
        "scalar_curvature": f"{curv['scalar']:.17g}",
        "weyl_norm": f"{pdiag['norm']:.17g}",
        "weyl_I": f"{pdiag['I_real']:.17g}{pdiag['I_imag']:+.17g}j",
        "weyl_det": f"{pdiag['Jdet_real']:.17g}{pdiag['Jdet_imag']:+.17g}j",
        "discriminant_abs": f"{pdiag['discriminant_abs']:.17g}",
        "weyl_trace_defect": f"{result['trace_defect']:.17g}",
        "weyl_symmetry_defect": f"{result['symmetry_defect']:.17g}",
        "registered_weyl_residual": f"{wdiag['registered_residual']:.17g}",
        "registered_projector_defect": f"{wdiag['projector_defect']:.17g}",
        "weyl_principal_gap": f"{wdiag['principal_gap']:.17g}",
        "ricci_block_residual": f"{rdiag['block_residual']:.17g}",
        "ricci_spectral_gap": f"{rdiag['spectral_gap']:.17g}",
        "riemann_pair_antisym_defect": f"{np.linalg.norm(riemann+riemann.swapaxes(0,1)):.17g}",
        "riemann_last_pair_antisym_defect": f"{np.linalg.norm(riemann+riemann.swapaxes(2,3)):.17g}",
        "frame_eigenvalue_defect": f"{frame_defect:.17g}",
        "frame_classification_same": str(frame_same).upper(),
    }


def package_landing(rows: list[dict[str, object]]) -> str:
    classes = {str(row["owner_class"]) for row in rows}
    recovered = {
        "UNIQUE_WEYL_DERIVED_SPLIT", "RICCI_DERIVED_WHEN_WEYL_DEGENERATE",
        "WEYL_AND_RICCI_AGREE_ON_SPLIT", "RICCI_DERIVED_WITH_WEYL_ALIGNMENT",
    }
    finite = "FINITE_WEYL_PRINCIPAL_CANDIDATES__REGISTERED_ONE_ALIGNED"
    unresolved = {"NUMERICALLY_UNRESOLVED", "INSUFFICIENT_OWNED_JET"}
    if classes & unresolved:
        return "BOUNDED_EVIDENCE_NUMERICALLY_OR_JET_UNRESOLVED"
    if classes <= recovered:
        return "CURVATURE_OWNS_REGISTERED_SPLIT_ON_ALL_TESTED_NONDEGENERATE_STRATA"
    if classes <= recovered | {finite} and finite in classes:
        return "CURVATURE_REDUCES_SPLIT_TO_FINITE_CANDIDATES_WITHOUT_UNIQUE_GLOBAL_OWNER"
    if classes & (recovered | {finite}):
        return "CURVATURE_OWNS_REGISTERED_SPLIT_ONLY_ON_A_PROPER_SUBSET_OF_TESTED_STRATA"
    return "REGISTERED_SPLIT_IS_NOT_RECOVERED_BY_TESTED_POINTWISE_CURVATURE_OPERATORS"


def main() -> None:
    source_count = verify_sources()
    g63_rows: list[dict[str, object]] = []
    tensor_keys: list[str] = []
    weyl_tensors: list[np.ndarray] = []
    ricci_tensors: list[np.ndarray] = []
    for sample in load_g63_samples():
        metric_fn = lambda x, sample=sample: g63_metric(x, sample)
        coframe_fn = lambda x, sample=sample: g63_coframe(x, sample)
        for point_name, x in g63_points(sample).items():
            curv = curvature(metric_fn, coframe_fn, x)
            result = classify(curv)
            g63_rows.append(result_row("G63", sample.sample_id, point_name, curv, result))
            tensor_keys.append(f"G63|{sample.sample_id}|{point_name}")
            weyl_tensors.append(curv["weyl_coordinate"])
            ricci_tensors.append(curv["ricci_coordinate"])

    profiles = load_g85_profiles()
    controls = (("C0",0.0,0.0),("CMINUS",-0.3,0.4),("CPLUS",0.3,0.4))
    archetypes = ("A03_RADIAL_SHIFT_TIMELIVE", "A04_LAPSE_LIFT_TIMELIVE", "A05_SHIFT_SUPPORTED_TAPER")
    g85_rows: list[dict[str, object]] = []
    cache: dict[tuple[object,...], tuple[dict[str,object],dict[str,object]]] = {}
    for profile_id, coefficients in sorted(profiles.items()):
        for archetype in archetypes:
            for control, epsilon, tau in controls:
                witness = G85Witness(profile_id, coefficients, archetype, control, epsilon, tau)
                key = (archetype, control) if archetype == "A05_SHIFT_SUPPORTED_TAPER" else (profile_id,archetype,control)
                if key not in cache:
                    x = np.array([tau, math.pi/2, 1.1, 0.37])
                    metric_fn = lambda y, witness=witness: g85_metric(y, witness)
                    coframe_fn = lambda y, metric_fn=metric_fn: coframe_from_metric(metric_fn(y))
                    curv = curvature(metric_fn, coframe_fn, x)
                    cache[key] = (curv, classify(curv))
                curv, result = cache[key]
                g85_rows.append(result_row("G85", f"{profile_id}:{archetype}", control, curv, result))
                tensor_keys.append(f"G85|{profile_id}:{archetype}|{control}")
                weyl_tensors.append(curv["weyl_coordinate"])
                ricci_tensors.append(curv["ricci_coordinate"])

    if len(g63_rows) != 42 or len(g85_rows) != 196*3*3:
        raise RuntimeError(f"row census failure: G63={len(g63_rows)} G85={len(g85_rows)}")
    all_rows = g63_rows + g85_rows
    write_tsv(HERE / "CURVATURE_SPLIT_ATLAS.tsv", all_rows)
    np.savez_compressed(
        HERE / "PRODUCTION_CURVATURE_TENSORS.npz",
        keys=np.asarray(tensor_keys),
        weyl=np.asarray(weyl_tensors),
        ricci=np.asarray(ricci_tensors),
    )
    from collections import Counter
    result = {
        "schema": "udt-curvature-principal-split-ownership-v1",
        "status": "PRODUCTION_COMPLETE",
        "primary_landing": package_landing(all_rows),
        "source_manifest_rows": source_count,
        "counts": {
            "g63_samples": 14, "g63_points": len(g63_rows),
            "g85_profiles": len(profiles), "g85_archetypes": 3,
            "g85_controls": 3, "g85_rows": len(g85_rows),
            "g85_unique_metric_jets": len(cache),
            "total_rows": len(all_rows), "total_unique_metric_jets": len(g63_rows)+len(cache),
        },
        "petrov_counts": dict(sorted(Counter(str(row["petrov"]) for row in all_rows).items())),
        "owner_counts": dict(sorted(Counter(str(row["owner_class"]) for row in all_rows).items())),
        "unique_metric_jet_owner_counts": dict(sorted(Counter(
            [str(row["owner_class"]) for row in g63_rows]
            + [str(classification["owner_class"]) for _, classification in cache.values()]
        ).items())),
        "scope_owner_counts": {
            scope: dict(sorted(Counter(str(row["owner_class"]) for row in all_rows if row["scope"] == scope).items()))
            for scope in ("G63","G85")
        },
        "all_metric_signatures_lorentzian": all(int(row["metric_negative_eigenvalues"]) == 1 for row in all_rows),
        "all_split_preserving_frame_classifications_covariant": all(row["frame_classification_same"] == "TRUE" for row in all_rows),
        "maximum_conclusion": "bounded_pointwise_curvature_ownership_of_registered_split_only",
        "no_physical_history_selected": True,
        "no_query_or_realization_selected": True,
        "versions": {"python":platform.python_version(),"numpy":np.__version__,"sympy":sp.__version__,"torch":torch.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
