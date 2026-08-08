#!/usr/bin/env python3
"""M3-AUDIT forensics library (contract 2d9933d1; machinery reuse under the
M3 authorization mechanism, prereg commit 523f4aca — this work is part of
M3-AUDIT under 2d9933d1). FORENSICS ONLY (F-FIX): everything computed here
is diagnostic EVIDENCE for grading; nothing replaces a banked M3 number.

Frozen-estimator REUSE (no re-choosing): theta bins, window, weights,
split-averaged RR over 4 files, cap-combine union jackknife, LS, bump
machinery — all imported from v_bao unchanged.

Honest deviation note (documented in AUDIT_REPORT.md): the M3 checkpoints
persisted only region-SUMMED counts, so B2's drop-one-region refits require
bounded fresh recomputes of the region-blocked counts (piecewise, cached);
the same blocks serve B4 per-cap w(theta) (caps are block-diagonal in the
frozen cap-combine estimator — per-cap LS is a restriction, not a re-choice).
"""
import os
import sys
import json
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
M2_BUILD = os.path.join(REPO, "udt_xmax_scale_observational_M2_build_2026-08-07")
M3_RUNS = os.path.join(REPO, "udt_xmax_scale_observational_M3_runs_2026-08-07")
CKPT_DIR = os.path.join(M3_RUNS, "bao_checkpoints")
AUDIT_DATA = os.path.join(HERE, "audit_data")
BLOCKS_DIR = os.path.join(AUDIT_DATA, "blocks")
sys.path.insert(0, M2_BUILD)
import v_bao  # noqa: E402

M3_PREREG_COMMIT = "523f4aca"      # cited for authorize_m3 (as the M3 runners)
AUDIT_PREREG_COMMIT = "2d9933d1"   # this audit's contract
CAPS = ("NGC", "SGC")
N_RAN_FILES = 4
NREG = v_bao.N_JACKKNIFE           # 24 per cap (frozen)

# The nine frozen targets (contract SS2): (tracer, zlo, zhi, role)
TARGETS = [
    ("LRG", 0.95, 1.00, "outlier-8.8deg (named lead: LRG selection-edge thinning)"),
    ("LRG", 1.05, 1.10, "outlier-1.17deg"),
    ("QSO", 1.85, 2.00, "outlier-0.71deg"),
    ("LRG", 1.00, 1.05, "thread-control-2.44deg"),
    ("LRG", 0.70, 0.75, "thread-2.37deg"),
    ("LRG", 0.90, 0.95, "thread-2.34deg"),
    ("QSO", 0.95, 1.10, "thread-1.39deg"),
    ("QSO", 1.10, 1.25, "thread-2.05deg"),
    ("LRG", 0.75, 0.80, "fitter-level-70.7deg (B6)"),
]

LOG_BIN_FACTOR = (v_bao.THETA_MAX_DEG / v_bao.THETA_MIN_DEG) ** (1.0 / v_bao.N_THETA_BINS)


def authorize():
    v_bao.authorize_m3(M3_PREREG_COMMIT)


def dat_path(tracer, cap):
    return os.path.join(v_bao.DATA_DIR, f"{tracer}_{cap}_clustering.dat.fits")


def ran_path(tracer, cap, i):
    return os.path.join(v_bao.DATA_DIR, f"{tracer}_{cap}_{i}_clustering.ran.fits")


def variant_kwargs(variant):
    """Weight variants used by the audit. 'sys' = the M3 primary (all three
    weights on); 'nozfail' = B5 (WEIGHT_ZFAIL dropped, others on)."""
    if variant == "sys":
        return dict(use_sys=True, use_zfail=True, use_comp=True)
    if variant == "nozfail":
        return dict(use_sys=True, use_zfail=False, use_comp=True)
    raise ValueError(variant)


def unit_key(variant, tracer, zlo, zhi, cap):
    return f"{tracer}_{zlo:.3f}_{zhi:.3f}_{variant}_{cap}"


def load_cap(tracer, cap, zlo, zhi, variant):
    kw = variant_kwargs(variant)
    D = v_bao.load_catalog(dat_path(tracer, cap), zrange=(zlo, zhi), **kw)
    R_list = [v_bao.load_catalog(ran_path(tracer, cap, i), zrange=(zlo, zhi), **kw)
              for i in range(N_RAN_FILES)]
    return D, R_list


def compute_cap_blocks(tracer, zlo, zhi, cap, variant, log=print):
    """One (target, cap, variant): region map from the concatenated randoms
    (frozen convention), then the six count pieces (DD, DR, RR0..RR3), each
    cached to its own npz (staged banking; resumable per piece)."""
    key = unit_key(variant, tracer, zlo, zhi, cap)
    done_fn = os.path.join(BLOCKS_DIR, key + "_META.json")
    if os.path.exists(done_fn):
        return json.load(open(done_fn))
    authorize()
    D, R_list = load_cap(tracer, cap, zlo, zhi, variant)
    Rcat = v_bao._concat_catalogs(R_list)
    rm = v_bao.make_region_map(Rcat.ra, Rcat.dec, Rcat.w, 3, NREG // 3)
    regD = v_bao.apply_region_map(rm, D.ra, D.dec)
    regC = v_bao.apply_region_map(rm, Rcat.ra, Rcat.dec)
    meta = {"key": key, "n_D": len(D), "n_R": [len(R) for R in R_list],
            "t_pieces_s": {}, "prereg": [M3_PREREG_COMMIT, AUDIT_PREREG_COMMIT]}
    WD, SD2 = v_bao._region_weight_sums(D.w, regD, NREG)
    WRcat, _ = v_bao._region_weight_sums(Rcat.w, regC, NREG)
    pieces = [("DD", lambda: v_bao.pair_count_blocks(D, D, regD, regD, NREG, True)),
              ("DR", lambda: v_bao.pair_count_blocks(D, Rcat, regD, regC, NREG, False))]
    for f in range(N_RAN_FILES):
        def _rr(f=f):
            regf = v_bao.apply_region_map(rm, R_list[f].ra, R_list[f].dec)
            return v_bao.pair_count_blocks(R_list[f], R_list[f], regf, regf, NREG, True)
        pieces.append((f"RR{f}", _rr))
    for name, fn in pieces:
        pf = os.path.join(BLOCKS_DIR, key + f"_{name}.npz")
        if os.path.exists(pf):
            continue
        t0 = time.time()
        Cw = fn()
        meta["t_pieces_s"][name] = round(time.time() - t0, 1)
        np.savez(pf, Cw=Cw)
        log(f"  piece {key} {name} done in {meta['t_pieces_s'][name]}s")
    wrf, sr2f = [], []
    for f in range(N_RAN_FILES):
        regf = v_bao.apply_region_map(rm, R_list[f].ra, R_list[f].dec)
        a, b = v_bao._region_weight_sums(R_list[f].w, regf, NREG)
        wrf.append(a.tolist()); sr2f.append(b.tolist())
    meta.update({"WD": WD.tolist(), "SD2": SD2.tolist(),
                 "WRcat": WRcat.tolist(), "WRf": wrf, "SR2f": sr2f})
    with open(done_fn, "w") as fh:
        json.dump(meta, fh)
    return meta


# ---------------------------------------------------------------------------
# Assembly from cached blocks (cheap once pieces exist)
# ---------------------------------------------------------------------------
def _load_blocks(tracer, zlo, zhi, cap, variant):
    key = unit_key(variant, tracer, zlo, zhi, cap)
    meta = json.load(open(os.path.join(BLOCKS_DIR, key + "_META.json")))
    arr = {}
    for name in ["DD", "DR"] + [f"RR{f}" for f in range(N_RAN_FILES)]:
        arr[name] = np.load(os.path.join(BLOCKS_DIR, key + f"_{name}.npz"))["Cw"]
    return meta, arr


def assemble_union(tracer, zlo, zhi, variant, caps=CAPS):
    """Rebuild the frozen cap-combine LS + union leave-one-out jackknife from
    cached blocks. caps can be a single-cap tuple (B4 restriction)."""
    K = len(caps)
    T = K * NREG
    NB = v_bao.N_THETA_BINS
    DD = np.zeros((T, T, NB)); DR = np.zeros((T, T, NB))
    RRf = [np.zeros((T, T, NB)) for _ in range(N_RAN_FILES)]
    WD = np.zeros(T); SD2 = np.zeros(T); WRcat = np.zeros(T)
    WRl = [np.zeros(T) for _ in range(N_RAN_FILES)]
    SRl = [np.zeros(T) for _ in range(N_RAN_FILES)]
    for c, cap in enumerate(caps):
        meta, arr = _load_blocks(tracer, zlo, zhi, cap, variant)
        s = slice(c * NREG, (c + 1) * NREG)
        DD[s, s] = arr["DD"]; DR[s, s] = arr["DR"]
        WD[s] = meta["WD"]; SD2[s] = meta["SD2"]; WRcat[s] = meta["WRcat"]
        for f in range(N_RAN_FILES):
            RRf[f][s, s] = arr[f"RR{f}"]
            WRl[f][s] = meta["WRf"][f]; SRl[f][s] = meta["SR2f"][f]
    w, w_jk, cov = v_bao._ls_from_blocks_general(DD, DR, WD, SD2, WRcat,
                                                 RRf, WRl, SRl)
    return {"theta": v_bao.theta_bin_centers(), "w": w, "w_jk": w_jk,
            "cov": cov, "sig": np.sqrt(np.diag(cov)), "T": T}


def bump(theta, w, sig):
    return v_bao.detect_bump(theta, w, sig, refine=True)


def b2_drop_one(tracer, zlo, zhi, variant="sys"):
    """B2: refit the bump on every leave-one-region-out jackknife curve using
    the full-sample sig (frozen bump machinery). Returns per-region theta_b,
    dchi2, A_b + the full-sample refit for reference."""
    res = assemble_union(tracer, zlo, zhi, variant)
    th, sig = res["theta"], res["sig"]
    full = bump(th, res["w"], sig)
    rows = []
    for k in range(res["T"]):
        f = bump(th, res["w_jk"][k], sig)
        rows.append({"region": k, "theta_b": f["theta_b"],
                     "dchi2": f["dchi2"], "A_b": f["A_b"]})
    return {"full": full, "regions": rows, "w": res["w"].tolist(),
            "sig": sig.tolist()}


def b4_per_cap(tracer, zlo, zhi, variant="sys"):
    """B4: per-cap LS (restriction of the frozen estimator to one cap's
    blocks; 24-region per-cap jackknife) + frozen bump fit per cap."""
    out = {}
    for cap in CAPS:
        r = assemble_union(tracer, zlo, zhi, variant, caps=(cap,))
        f = bump(r["theta"], r["w"], r["sig"])
        out[cap] = {"bump": f, "w": r["w"].tolist(), "sig": r["sig"].tolist()}
    return out


def full_shell_w(tracer, zlo, zhi, variant):
    """Combined-cap w + frozen bump fit from cached blocks (B5 / B3 halves /
    reproduction check vs the M3 checkpoint)."""
    r = assemble_union(tracer, zlo, zhi, variant)
    f = bump(r["theta"], r["w"], r["sig"])
    return {"bump": f, "w": r["w"].tolist(), "sig": r["sig"].tolist()}


def b6_constrained(tracer=None, zlo=0.75, zhi=0.80, variant="sys"):
    """B6 (LRG 0.75-0.80): frozen bump machinery but with the refine step's
    center CONSTRAINED to the frozen search window [theta_min, theta_max]
    (grid stage is already in-window; only the unbounded Nelder-Mead refine
    could leave it). Report-only (F-FIX: no banked number is replaced)."""
    z = np.load(os.path.join(CKPT_DIR, f"LRG_{zlo:.2f}_{zhi:.2f}_{variant}.npz"))
    th, w, sig = z["theta"], z["w"], z["sig"]
    x = np.log(th)
    good = np.isfinite(w) & np.isfinite(sig) & (sig > 0)
    xg, yg = x[good], w[good]
    ivar = 1.0 / sig[good] ** 2
    Xn = v_bao._null_design(x)[good]
    _, chi2_null = v_bao._gls_lin(Xn, yg, ivar)

    def chi2_alt(xc, sw):
        g = np.exp(-0.5 * ((xg - xc) / sw) ** 2)
        beta, c2 = v_bao._gls_lin(np.column_stack([Xn, g]), yg, ivar)
        return c2, beta[-1]

    best = (np.inf, None, None, None)
    for xc in x:
        for sw in v_bao.BUMP_WIDTH_GRID:
            c2, ab = chi2_alt(xc, sw)
            if c2 < best[0]:
                best = (c2, xc, sw, ab)
    c2b, xcb, swb, ab = best
    from scipy.optimize import minimize
    lo, hi = np.log(v_bao.THETA_MIN_DEG), np.log(v_bao.THETA_MAX_DEG)
    res = minimize(lambda p: chi2_alt(float(np.clip(p[0], lo, hi)),
                                      float(np.clip(np.exp(p[1]), 0.03, 1.5)))[0],
                   x0=[xcb, np.log(swb)], method="Nelder-Mead",
                   options={"xatol": 1e-4, "fatol": 1e-8, "maxiter": 200})
    xcb = float(np.clip(res.x[0], lo, hi))
    swb = float(np.clip(np.exp(res.x[1]), 0.03, 1.5))
    c2b, ab = chi2_alt(xcb, swb)
    return {"variant": variant, "grid_best_theta": float(np.exp(best[1])),
            "constrained": {"dchi2": chi2_null - c2b,
                            "theta_b": float(np.exp(xcb)), "sigma_b": swb,
                            "A_b": float(ab)},
            "unconstrained_checkpoint": json.load(open(os.path.join(
                CKPT_DIR, f"LRG_{zlo:.2f}_{zhi:.2f}_{variant}.json")))["bump"]}
