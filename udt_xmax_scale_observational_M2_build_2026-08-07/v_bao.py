#!/usr/bin/env python3
"""V-BAO validator pipeline (M2 build, D3 agent, 2026-08-07).

Frozen per PREREGISTRATION.md section 4 and D1_FORMULAS.md 'FOR THE BUILDERS'.
BUILD-AND-VALIDATE-ON-SYNTHETIC ONLY at M2: real-data w(theta) is machine-guarded
(M2Guard) -- it raises unless the input is tagged synthetic, or smoke mode is used
(deliberately tiny subsample, quarantined output, DO-NOT-INTERPRET header).

F-IMPORT-LCDM wired: the loader is physically unable to return NX or WEIGHT_FKP
(column whitelist + blacklist assertion) or to open any `_rec` file (path check
BEFORE any I/O). No comoving distance, no fiducial cosmology, no r_d anywhere:
the only geometry used is theta = ell/r(z) with r(z) from the frozen native
profile menu (P1/P2/P3), parametrized in (X_eff, shape) per D1.

F-STEER: no default seeds n=1 or alpha=2; the bump search window is the FULL
theta range (no LCDM-predicted center anywhere).
"""
import os
import json
import numpy as np
from dataclasses import dataclass, field
from scipy.spatial import cKDTree
from scipy.optimize import minimize_scalar, minimize

# ----------------------------------------------------------------------------
# FROZEN CONSTANTS (prereg section 4; any change = new prereg)
# ----------------------------------------------------------------------------
DATA_DIR = "/media/udt-admin/ScratchDisk/Data/desi_dr1"

ALLOWED_COLUMNS = ("RA", "DEC", "Z", "WEIGHT_COMP", "WEIGHT_ZFAIL", "WEIGHT_SYS")
BLACKLIST_COLUMNS = ("NX", "WEIGHT_FKP")   # F-IMPORT-LCDM: fiducial-cosmology carriers
BLACKLIST_PATH_TOKEN = "_rec"              # reconstruction products forbidden

TRACER_ZRANGE = {"BGS_BRIGHT": (0.01, 0.50), "LRG": (0.40, 1.10),
                 "ELG_LOPnotqso": (0.80, 1.60), "QSO": (0.80, 3.50)}
SHELL_DZ = {"BGS_BRIGHT": 0.05, "LRG": 0.05, "ELG_LOPnotqso": 0.05, "QSO": 0.15}
SHELL_MIN_WEIGHTED = 5.0e4                 # weighted-galaxy floor per shell

THETA_MIN_DEG, THETA_MAX_DEG, N_THETA_BINS = 0.3, 12.0, 40   # log bins
N_JACKKNIFE = 24                           # angular jackknife regions (3 dec x 8 ra)

# M2 guard: real-data w(theta) forbidden. M3 flips this ONLY via its own prereg.
M3_REAL_RUN_AUTHORIZED = False
SMOKE_MAX = {"data": 20000, "randoms": 40000}   # frozen smoke subsample caps

SMOKE_HEADER = (
    "DO-NOT-INTERPRET: M2 I/O+correctness smoke output on a deliberately tiny "
    "subsample (<=2e4 gal / <=4e4 randoms). At this pair-count noise level no "
    "BAO-scale bump could be resolved; numbers here are NOT science and MUST NOT "
    "steer M3. F-PEEK ledger entry required for any use.")


class BlacklistViolation(Exception):
    """F-IMPORT-LCDM machine wire: forbidden column or _rec path requested."""


class M2GuardViolation(Exception):
    """F-PEEK machine wire: real-data correlation attempted at M2."""


@dataclass
class Catalog:
    ra: np.ndarray
    dec: np.ndarray
    z: np.ndarray
    w: np.ndarray
    tag: str          # 'real' | 'smoke' | 'synthetic'
    name: str = ""

    def __len__(self):
        return self.ra.size

    @property
    def w_total(self):
        return float(self.w.sum())


def load_catalog(path, zrange=None, use_sys=True, use_zfail=True, use_comp=True):
    """Load a DESI LSS catalog. Whitelist-only; blacklist enforced BEFORE I/O.

    Returns Catalog(tag='real'). Weight = product of the enabled native
    completeness weights (WEIGHT_COMP x WEIGHT_ZFAIL x WEIGHT_SYS); the
    use_sys=False variant implements M1's over-correction caveat test.
    NX / WEIGHT_FKP are never read; `_rec` paths are refused outright.
    """
    wanted = ["RA", "DEC", "Z"]
    for flag, col in ((use_comp, "WEIGHT_COMP"), (use_zfail, "WEIGHT_ZFAIL"),
                      (use_sys, "WEIGHT_SYS")):
        if flag:
            wanted.append(col)
    cols = load_columns(path, wanted)
    z = cols["Z"]
    sel = np.ones(z.size, dtype=bool)
    if zrange is not None:
        sel = (z >= zrange[0]) & (z < zrange[1])
    w = np.ones(int(sel.sum()), dtype=np.float64)
    for c in wanted[3:]:
        w *= cols[c][sel]
    return Catalog(cols["RA"][sel], cols["DEC"][sel], z[sel], w,
                   tag="real", name=os.path.basename(str(path)))


def load_columns(path, columns):
    """The ONLY read path to catalog files. Enforces, BEFORE any I/O:
    (a) no `_rec` (reconstruction) file may be opened;
    (b) every requested column must be on ALLOWED_COLUMNS and not on
        BLACKLIST_COLUMNS (NX / WEIGHT_FKP are physically unreturnable)."""
    base = os.path.basename(str(path))
    if BLACKLIST_PATH_TOKEN in base.lower():
        raise BlacklistViolation(
            f"path '{base}' is a reconstruction product (_rec): forbidden")
    for c in columns:
        if str(c).upper() in BLACKLIST_COLUMNS:
            raise BlacklistViolation(
                f"column '{c}' is blacklisted (F-IMPORT-LCDM)")
        if str(c).upper() not in ALLOWED_COLUMNS:
            raise BlacklistViolation(
                f"column '{c}' is not on the whitelist")
    from astropy.io import fits
    out = {}
    with fits.open(path, memmap=True) as hdul:
        data = hdul[1].data
        for c in columns:
            out[c] = np.asarray(data[c], dtype=np.float64)
    return out

def make_smoke(cat, kind, seed=0):
    """Convert a real Catalog to smoke mode: enforced tiny subsample, tag='smoke'.

    kind in {'data','randoms'}; cap = SMOKE_MAX[kind] (frozen). The cap is what
    makes smoke mode science-free: at <=2e4/4e4 points a BAO-amplitude bump is
    far below the pair-count noise floor.
    """
    cap = SMOKE_MAX[kind]
    rng = np.random.default_rng(seed)
    n = len(cat)
    idx = rng.choice(n, size=min(n, cap), replace=False) if n > cap else np.arange(n)
    return Catalog(cat.ra[idx], cat.dec[idx], cat.z[idx], cat.w[idx],
                   tag="smoke", name=cat.name + "[smoke]")


def _check_guard(cat, kind):
    """kind in {'data','randoms'}: the smoke cap is enforced PER ROLE at its
    strictest applicable value (A7 amendment: a hand-tagged 'smoke' DATA
    catalog above the 2e4 data cap is now caught here, not only in
    make_smoke)."""
    if cat.tag == "real" and not M3_REAL_RUN_AUTHORIZED:
        raise M2GuardViolation(
            "w(theta)/pair counts on real data are forbidden at M2 "
            "(F-PEEK). Use make_smoke() for I/O smoke tests, or wait for "
            "the M3 prereg gate.")
    if cat.tag == "smoke" and len(cat) > SMOKE_MAX[kind]:
        raise M2GuardViolation(
            f"smoke catalog exceeds the frozen {kind} cap {SMOKE_MAX[kind]}")


# ----------------------------------------------------------------------------
# Shell binner (frozen dz, weighted floor; dropped shells reported)
# ----------------------------------------------------------------------------
def shell_edges(tracer):
    zlo, zhi = TRACER_ZRANGE[tracer]
    dz = SHELL_DZ[tracer]
    n = int(round((zhi - zlo) / dz))
    return zlo + dz * np.arange(n + 1)


def bin_shells(cat, tracer, min_weighted=SHELL_MIN_WEIGHTED):
    """Assign catalog rows to frozen z-shells. Returns (kept, dropped) lists of
    dicts {zlo, zhi, mask, w_sum}; a shell is kept iff weighted count >= floor."""
    edges = shell_edges(tracer)
    kept, dropped = [], []
    for zlo, zhi in zip(edges[:-1], edges[1:]):
        mask = (cat.z >= zlo) & (cat.z < zhi)
        w_sum = float(cat.w[mask].sum())
        rec = {"zlo": float(zlo), "zhi": float(zhi), "mask": mask, "w_sum": w_sum}
        (kept if w_sum >= min_weighted else dropped).append(rec)
    return kept, dropped


# ----------------------------------------------------------------------------
# Angular jackknife regions (frozen: 3 weighted-dec bands x 8 ra slices = 24),
# boundaries defined on the RANDOMS and applied to both catalogs.
# ----------------------------------------------------------------------------
def _weighted_quantiles(x, w, qs):
    o = np.argsort(x)
    cw = np.cumsum(w[o])
    cw = (cw - 0.5 * w[o]) / cw[-1]
    return np.interp(qs, cw, x[o])


def _ra_origin(ra):
    """Deterministic RA unwrap origin: start of the largest empty 1-deg gap."""
    hist, _ = np.histogram(ra % 360.0, bins=360, range=(0.0, 360.0))
    occ = np.flatnonzero(hist > 0)
    if occ.size == 0 or occ.size == 360:
        return 0.0
    ext = np.concatenate([occ, occ[:1] + 360])
    gaps = np.diff(ext)
    k = int(np.argmax(gaps))
    return float((occ[k] + 1) % 360)


def make_region_map(ra, dec, w=None, n_dec=3, n_ra=8):
    if w is None:
        w = np.ones(ra.size)
    ra0 = _ra_origin(ra)
    ru = (ra - ra0) % 360.0
    dec_edges = _weighted_quantiles(dec, w, np.arange(1, n_dec) / n_dec)
    band = np.clip(np.searchsorted(dec_edges, dec), 0, n_dec - 1)
    ra_edges = []
    for b in range(n_dec):
        m = band == b
        ra_edges.append(_weighted_quantiles(ru[m], w[m], np.arange(1, n_ra) / n_ra))
    return {"ra0": ra0, "dec_edges": dec_edges, "ra_edges": ra_edges,
            "n_dec": n_dec, "n_ra": n_ra}


def apply_region_map(rm, ra, dec):
    ru = (ra - rm["ra0"]) % 360.0
    band = np.clip(np.searchsorted(rm["dec_edges"], dec), 0, rm["n_dec"] - 1)
    reg = np.empty(ra.size, dtype=np.int64)
    for b in range(rm["n_dec"]):
        m = band == b
        s = np.clip(np.searchsorted(rm["ra_edges"][b], ru[m]), 0, rm["n_ra"] - 1)
        reg[m] = b * rm["n_ra"] + s
    return reg

# ----------------------------------------------------------------------------
# Pair counting: exact weighted dual-tree counts on unit-sphere 3-vectors,
# region-blocked so the 24 leave-one-out jackknife samples cost ~nothing extra.
# ----------------------------------------------------------------------------
def theta_bin_edges():
    return np.geomspace(THETA_MIN_DEG, THETA_MAX_DEG, N_THETA_BINS + 1)


def theta_bin_centers():
    e = theta_bin_edges()
    return np.sqrt(e[:-1] * e[1:])


def _chord(theta_deg):
    return 2.0 * np.sin(np.radians(theta_deg) / 2.0)


def _unit_vectors(ra, dec):
    ra_r, dec_r = np.radians(ra), np.radians(dec)
    cd = np.cos(dec_r)
    return np.column_stack([cd * np.cos(ra_r), cd * np.sin(ra_r), np.sin(dec_r)])


def pair_count_blocks(catA, catB, regA, regB, nreg=N_JACKKNIFE, auto=False):
    """Weighted ordered-pair counts per (regionA, regionB, theta bin).

    Exact (cKDTree.count_neighbors, dual-tree, chord metric). Self-pairs land
    at chord 0 < edge[0] and cancel in the cumulative diff. For auto=True,
    catB must be catA and the symmetric blocks are mirrored.
    Full counts = Cw.sum((0,1)); jackknife-k counts = Cw with row+col k removed.
    """
    edges = _chord(theta_bin_edges())
    xyzA, xyzB = _unit_vectors(catA.ra, catA.dec), None
    idxA = [np.flatnonzero(regA == i) for i in range(nreg)]
    treesA = [cKDTree(xyzA[ix]) if ix.size else None for ix in idxA]
    if auto:
        idxB, treesB, wB = idxA, treesA, catA.w
    else:
        xyzB = _unit_vectors(catB.ra, catB.dec)
        idxB = [np.flatnonzero(regB == i) for i in range(nreg)]
        treesB = [cKDTree(xyzB[ix]) if ix.size else None for ix in idxB]
        wB = catB.w
    Cw = np.zeros((nreg, nreg, N_THETA_BINS))
    for i in range(nreg):
        if treesA[i] is None:
            continue
        wi = catA.w[idxA[i]]
        jstart = i if auto else 0
        for j in range(jstart, nreg):
            if treesB[j] is None:
                continue
            cum = treesA[i].count_neighbors(treesB[j], edges,
                                            weights=(wi, wB[idxB[j]]),
                                            cumulative=True)
            Cw[i, j, :] = np.diff(cum)
            if auto and j > i:
                Cw[j, i, :] = Cw[i, j, :]
    return Cw


def _region_weight_sums(w, reg, nreg):
    W = np.zeros(nreg)
    S2 = np.zeros(nreg)
    np.add.at(W, reg, w)
    np.add.at(S2, reg, w * w)
    return W, S2


def ls_w_theta(D, R, nreg=N_JACKKNIFE, region_map=None):
    """Landy-Szalay w(theta) with native weights + angular jackknife errors.

    Estimator (ordered weighted counts, self-pairs excluded by theta_min>0):
      w = (DD/nDD - 2 DR/nDR + RR/nRR) / (RR/nRR),
      nDD = W_D^2 - sum(w_D^2), nRR analogous, nDR = W_D W_R.
    Jackknife: leave-one-region-out via the region blocks (exact re-count).
    M2Guard enforced here.
    """
    _check_guard(D, "data")
    _check_guard(R, "randoms")
    if region_map is None:
        region_map = make_region_map(R.ra, R.dec, R.w, 3, nreg // 3)
    regD = apply_region_map(region_map, D.ra, D.dec)
    regR = apply_region_map(region_map, R.ra, R.dec)
    DD = pair_count_blocks(D, D, regD, regD, nreg, auto=True)
    RR = pair_count_blocks(R, R, regR, regR, nreg, auto=True)
    DR = pair_count_blocks(D, R, regD, regR, nreg, auto=False)
    WD, SD2 = _region_weight_sums(D.w, regD, nreg)
    WR, SR2 = _region_weight_sums(R.w, regR, nreg)

    def _ls(keep):
        wd, wr = WD[keep].sum(), WR[keep].sum()
        sd2, sr2 = SD2[keep].sum(), SR2[keep].sum()
        sub = np.ix_(keep, keep)
        dd = DD[sub].sum(axis=(0, 1)) / (wd * wd - sd2)
        rr = RR[sub].sum(axis=(0, 1)) / (wr * wr - sr2)
        dr = DR[sub].sum(axis=(0, 1)) / (wd * wr)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(rr > 0, (dd - 2 * dr + rr) / rr, np.nan)

    allk = np.ones(nreg, dtype=bool)
    w_full = _ls(allk)
    w_jk = np.empty((nreg, N_THETA_BINS))
    for k in range(nreg):
        keep = allk.copy()
        keep[k] = False
        w_jk[k] = _ls(keep)
    wbar = np.nanmean(w_jk, axis=0)
    dev = w_jk - wbar
    cov = (nreg - 1) / nreg * np.einsum("ki,kj->ij", np.nan_to_num(dev),
                                        np.nan_to_num(dev))
    return {"theta": theta_bin_centers(), "w": w_full, "w_jk": w_jk,
            "sig": np.sqrt(np.diag(cov)), "cov_jk": cov,
            "counts": {"DD": DD.sum((0, 1)), "DR": DR.sum((0, 1)),
                       "RR": RR.sum((0, 1))},
            "meta": {"nreg": nreg, "W_D": float(WD.sum()),
                     "W_R": float(WR.sum()), "tags": [D.tag, R.tag]}}

# ----------------------------------------------------------------------------
# Bump machinery (frozen): null = cubic in ln(theta); alt = null + Gaussian in
# ln(theta) (center theta_b, width sigma_b in ln-theta, amplitude A_b free).
# chi^2 uses DIAGONAL jackknife variances (conditioning choice, stated: the
# 24-region jackknife covariance of 40 bins is rank<=23, not invertible; the
# null-mock trials calibration uses the SAME diagonal, so the significance is
# self-consistent). Search window = FULL theta range (F-STEER: no seeded center).
# ----------------------------------------------------------------------------
BUMP_WIDTH_GRID = (0.10, 0.20, 0.35, 0.60)   # sigma_b grid in ln-theta, frozen


def _gls_lin(X, y, ivar):
    """Weighted linear least squares (rank-robust); returns (coeffs, chi2)."""
    sw = np.sqrt(ivar)
    beta, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    r = y - X @ beta
    return beta, float(np.sum(r * r * ivar))


def _null_design(x):
    return np.vander(x - x.mean(), 4, increasing=True)


def fit_null(theta, w, sig):
    x = np.log(theta)
    good = np.isfinite(w) & np.isfinite(sig) & (sig > 0)
    ivar = np.zeros_like(sig)
    ivar[good] = 1.0 / sig[good] ** 2
    beta, chi2 = _gls_lin(_null_design(x)[good], w[good], ivar[good])
    return {"beta": beta, "chi2": chi2, "ndof": int(good.sum()) - 4}


def detect_bump(theta, w, sig, refine=True):
    """Grid (all 40 centers x width grid) + optional local refine.
    Returns dchi2 = chi2_null - chi2_alt maximized over the FULL window."""
    x = np.log(theta)
    good = np.isfinite(w) & np.isfinite(sig) & (sig > 0)
    xg, yg = x[good], w[good]
    ivar = 1.0 / sig[good] ** 2
    Xn = _null_design(x)[good]
    _, chi2_null = _gls_lin(Xn, yg, ivar)

    def chi2_alt(xc, sw):
        g = np.exp(-0.5 * ((xg - xc) / sw) ** 2)
        beta, c2 = _gls_lin(np.column_stack([Xn, g]), yg, ivar)
        return c2, beta[-1]

    best = (np.inf, None, None, None)
    for xc in x:
        for sw in BUMP_WIDTH_GRID:
            c2, ab = chi2_alt(xc, sw)
            if c2 < best[0]:
                best = (c2, xc, sw, ab)
    c2b, xcb, swb, ab = best
    if refine:
        res = minimize(lambda p: chi2_alt(p[0], float(np.clip(
                           np.exp(p[1]), 0.03, 1.5)))[0],
                       x0=[xcb, np.log(swb)], method="Nelder-Mead",
                       options={"xatol": 1e-4, "fatol": 1e-8, "maxiter": 200})
        xcb = res.x[0]
        swb = float(np.clip(np.exp(res.x[1]), 0.03, 1.5))
        c2b, ab = chi2_alt(xcb, swb)
    return {"dchi2": chi2_null - c2b, "theta_b": float(np.exp(xcb)),
            "sigma_b": float(swb), "A_b": float(ab),
            "chi2_null": chi2_null, "chi2_alt": c2b}


def calibrate_max_dchi2(sig, n_mocks=400, seed=101, theta=None):
    """Trials (look-elsewhere) accounting, frozen method: null-mock calibration.
    Draw n_mocks realizations y ~ N(0, diag(sig^2)) (pure null), run the SAME
    grid search over the FULL window; return the sorted max-dchi2 distribution.
    Vectorized via projection quadratic forms (identical to the refine=False
    grid in detect_bump: chi2 = y'Wy - y'B_k y with B_k the GLS hat form)."""
    if theta is None:
        theta = theta_bin_centers()
    x = np.log(theta)
    good = np.isfinite(sig) & (sig > 0)
    xg = x[good]
    Wd = 1.0 / sig[good] ** 2
    Xn = _null_design(x)[good]

    def _B(X):
        WX = X * Wd[:, None]
        return WX @ np.linalg.solve(X.T @ WX, WX.T)

    B_null = _B(Xn)
    B_alt = [_B(np.column_stack([Xn, np.exp(-0.5 * ((xg - xc) / sw) ** 2)]))
             for xc in x for sw in BUMP_WIDTH_GRID]
    rng = np.random.default_rng(seed)
    Y = rng.normal(0.0, sig[good], size=(n_mocks, xg.size))
    q_null = np.einsum("mi,ij,mj->m", Y, B_null, Y)
    q_best = np.full(n_mocks, -np.inf)
    for B in B_alt:
        np.maximum(q_best, np.einsum("mi,ij,mj->m", Y, B, Y), out=q_best)
    return np.sort(q_best - q_null)


def bump_pvalue(dchi2_obs, null_dist):
    """Trials-corrected p-value: fraction of null mocks with max dchi2 >= obs."""
    return float(np.mean(null_dist >= dchi2_obs))

# ----------------------------------------------------------------------------
# UDT joint shape fit across shells: theta_BAO(z) = ell / r(z; profile) with
# ell a free nuisance (P-STATIC-RULER tag). D1 (X_eff, shape) coordinates:
#   r(z) = X_eff * g(shape, L),  L = ln(1+z), so theta = s / g with
#   s = ell / X_eff  (the identified combination; ell and X_eff separately
#   are degenerate in theta_BAO alone -- reported as s, honest).
# g: P1 (shape=1/n): (-expm1(-2*shape*L))/shape ; P2: 2L ;
#    P3 (shape=1/alpha): expm1(2*shape*L)/shape.  shape->0 limit = P2 (exact).
# F-STEER: SHAPE_GRID is a 24-point geometric grid on [0.05, 5] that contains
# neither 1/n=1 (n=1) nor 1/alpha=0.5 (alpha=2); no privileged defaults.
# ----------------------------------------------------------------------------
PROFILES = ("P1", "P2", "P3")
SHAPE_GRID = np.geomspace(0.05, 5.0, 24)


def shape_g(profile, L, shape=None):
    L = np.asarray(L, dtype=np.float64)
    if profile == "P2":
        return 2.0 * L
    if shape is None or shape <= 0:
        raise ValueError("P1/P3 need shape > 0 (1/n or 1/alpha)")
    if shape < 1e-8:                       # exact P2 limit, numerically safe
        return 2.0 * L
    if profile == "P1":
        return -np.expm1(-2.0 * shape * L) / shape
    if profile == "P3":
        return np.expm1(2.0 * shape * L) / shape
    raise ValueError(profile)


def theta_bao_pred(z, profile, s, shape=None):
    """theta_BAO(z) in radians-equivalent units of s (s = ell/X_eff)."""
    return s / shape_g(profile, np.log1p(z), shape)


def _best_s(g, th, iv):
    """theta = s/g is linear in s: closed-form weighted best s and chi2."""
    a = np.sum(iv / g ** 2)
    b = np.sum(th * iv / g)
    s = b / a
    chi2 = float(np.sum(iv * (th - s / g) ** 2))
    return s, chi2


def joint_shape_fit(z, theta_b, sigma_theta, profile):
    """Fit (s, shape) to per-shell bump centers. Returns best fit + a
    profile-likelihood interval on s (dchi2<=1, shape re-optimized)."""
    z = np.asarray(z, float)
    th = np.asarray(theta_b, float)
    iv = 1.0 / np.asarray(sigma_theta, float) ** 2
    L = np.log1p(z)

    def chi2_of_shape(shape):
        return _best_s(shape_g(profile, L, shape), th, iv)

    if profile == "P2":
        s_best, chi2_best, shape_best = *_best_s(2.0 * L, th, iv), None
    else:
        grid = [(chi2_of_shape(sh)[1], sh) for sh in SHAPE_GRID]
        c0, sh0 = min(grid)
        res = minimize_scalar(lambda t: chi2_of_shape(np.exp(t))[1],
                              bracket=None, bounds=(np.log(sh0) - 1.3,
                                                    np.log(sh0) + 1.3),
                              method="bounded", options={"xatol": 1e-5})
        shape_best = float(np.exp(res.x))
        s_best, chi2_best = chi2_of_shape(shape_best)

    def prof_chi2(s):
        if profile == "P2":
            return float(np.sum(iv * (th - s / (2.0 * L)) ** 2))
        f = lambda t: float(np.sum(iv * (th - s / shape_g(
            profile, L, np.exp(t))) ** 2))
        r = minimize_scalar(f, bounds=(np.log(SHAPE_GRID[0]) - 0.7,
                                       np.log(SHAPE_GRID[-1]) + 0.7),
                            method="bounded", options={"xatol": 1e-5})
        return float(r.fun)

    span = np.geomspace(0.5, 2.0, 61) * s_best
    pc = np.array([prof_chi2(s) for s in span])

    def _interval(dc):
        inside = span[pc <= chi2_best + dc]
        return ((float(inside.min()), float(inside.max())) if inside.size
                else (np.nan, np.nan))

    return {"profile": profile, "s_best": float(s_best),
            "shape_best": shape_best, "chi2": float(chi2_best),
            "ndof": int(z.size - (2 if profile != "P2" else 1)),
            "s_interval_dchi2_1": _interval(1.0),
            "s_interval_dchi2_4": _interval(4.0)}

# ----------------------------------------------------------------------------
# Smoke mode (quarantined) + M3 full-run cost estimation
# ----------------------------------------------------------------------------
def run_smoke_shell(tracer, cap, zlo, zhi, out_dir=None, seed=7):
    """I/O + correctness smoke test on ONE real shell at the frozen tiny
    subsample. Output goes ONLY to smoke_outputs/ with the DO-NOT-INTERPRET
    header. Bump machinery is deliberately NOT run here."""
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = out_dir or os.path.join(here, "smoke_outputs")
    os.makedirs(out_dir, exist_ok=True)
    import time as _t
    t0 = _t.time()
    D = load_catalog(os.path.join(DATA_DIR, f"{tracer}_{cap}_clustering.dat.fits"),
                     zrange=(zlo, zhi))
    R = load_catalog(os.path.join(DATA_DIR, f"{tracer}_{cap}_0_clustering.ran.fits"),
                     zrange=(zlo, zhi))
    t_io = _t.time() - t0
    n_shell = (len(D), len(R))
    Ds, Rs = make_smoke(D, "data", seed), make_smoke(R, "randoms", seed + 1)
    t1 = _t.time()
    res = ls_w_theta(Ds, Rs)
    t_ls = _t.time() - t1
    # A3 amendment: w(theta)/sigma values are computed transiently for the
    # feasibility check but are NEVER persisted (prereg: smoke tests "produce
    # NO science numbers"). Only I/O feasibility facts are stored.
    payload = {"HEADER": SMOKE_HEADER,
               "shell": {"tracer": tracer, "cap": cap, "z": [zlo, zhi]},
               "n_full_shell": n_shell, "n_smoke": (len(Ds), len(Rs)),
               "t_io_s": round(t_io, 2), "t_ls_s": round(t_ls, 2),
               "ls_completed": True,
               "n_finite_bins": int(np.isfinite(res["w"]).sum()),
               "n_theta_bins": N_THETA_BINS,
               "REDACTION_POLICY": ("w(theta)/sigma vectors computed "
                                    "transiently, never persisted (A3)")}
    fn = os.path.join(out_dir, f"smoke_{tracer}_{cap}_{zlo:.2f}_{zhi:.2f}.json")
    with open(fn, "w") as f:
        json.dump(payload, f, indent=1)
    return {"file": fn, "n_full_shell": n_shell, "t_io_s": t_io, "t_ls_s": t_ls}


def estimate_full_cost(pairs_per_sec, ran_factor=4.0):
    """M3 cost estimate from dN/dz (schema-level, F-PEEK legal) + measured
    pair throughput. Counts pairs within THETA_MAX for DD/DR/RR per kept
    shell: N^2 * (cap solid angle / footprint solid angle) scaling."""
    from astropy.io import fits
    cap_sr = 2 * np.pi * (1 - np.cos(np.radians(THETA_MAX_DEG)))
    total_s = 0.0
    rows = []
    for tracer, (zlo, zhi) in TRACER_ZRANGE.items():
        for cap in ("NGC", "SGC"):
            fpath = os.path.join(DATA_DIR, f"{tracer}_{cap}_clustering.dat.fits")
            with fits.open(fpath, memmap=True) as h:
                d = h[1].data
                z = np.asarray(d["Z"], float)
                ra = np.asarray(d["RA"], float)
                dec = np.asarray(d["DEC"], float)
            # footprint solid angle estimate: 1-deg^2 cells occupied
            ij = (np.floor(ra).astype(int) % 360) * 181 + \
                 (np.floor(dec).astype(int) + 90)
            foot_sr = np.unique(ij).size * (np.pi / 180.0) ** 2
            edges = shell_edges(tracer)
            for a, b in zip(edges[:-1], edges[1:]):
                n = int(((z >= a) & (z < b)).sum())
                if n < SHELL_MIN_WEIGHTED:     # unweighted proxy for estimate
                    continue
                frac = min(cap_sr / foot_sr, 1.0)
                nr = n * ran_factor
                pairs = (n * n + 2 * n * nr + nr * nr) * frac
                t = pairs / pairs_per_sec
                total_s += t
                rows.append({"tracer": tracer, "cap": cap, "z": [a, b],
                             "N": n, "foot_deg2": foot_sr * (180 / np.pi) ** 2,
                             "pairs": pairs, "t_s": t})
    return {"rows": rows, "total_cpu_hr": total_s / 3600.0,
            "assumes": {"pairs_per_sec": pairs_per_sec,
                        "ran_factor": ran_factor}}


if __name__ == "__main__":
    print(__doc__)

