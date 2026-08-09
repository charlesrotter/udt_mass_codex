#!/usr/bin/env python3
"""M3d LEG A mock generator (prereg 962bd0c6, SS1 frozen design).

Synthetic universes with ONE true scale, built on the REAL survey skeletons:
  * footprint/selection = the real DESI DR1 / BOSS DR12 randoms (per shell);
  * per-shell weighted densities = the real per-shell weighted data counts;
  * redshifts resampled from the real per-shell weighted dN/dz;
  * feature = pair-splitting: a fraction F_PAIR of points are companions
    placed at theta_t(z) = ell_t / r_truth(z) from a parent (random azimuth);
    companions falling OUTSIDE the footprint are dropped and replaced by an
    unpaired skeleton point (matching the real selection: a partner outside
    the survey is simply not observed).  Density is preserved exactly.

FAIRNESS (F-FAIR-MOCK): amplitude is calibrated so the mock fitted bump
amplitude matches the REAL banked LRG driver-shell A_b (run_legA phase 'cal').
Mock data/randoms carry tag='synthetic' -- the M2 guard stays honest: no real
DATA position is ever pair-counted here; real catalogs contribute ONLY the
randoms skeleton, per-shell counts and the z-histogram (selection facts).

Truth variants (both preregistered):
  i  : ell_t = 58.34 Mpc with the UDT P1-fitted r(z) (rerun_m3c.rz);
  ii : published-shape gentle-fall drift curve (attributed instrument-test
       input): theta_ii(z) = theta_i(0.9) * (z/0.9)**(-0.774) deg.
       Exact form derivation: the mainstream angular-BAO scale drifts as
       theta ~ 1/D_C(z); a power-law fit of that shape over 0.70<=z<=1.10
       gives exponent -0.774; amplitude anchored to variant i at z=0.9 so
       both truths cover the same theta range (prereg: "matched to
       variant-i's range").
"""
import os
import sys
import zlib

import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
M2 = os.path.join(ROOT, "udt_xmax_scale_observational_M2_build_2026-08-07")
M3B = os.path.join(ROOT, "udt_xmax_scale_observational_M3b_BOSS_2026-08-08")
M3C = os.path.join(ROOT, "udt_xmax_scale_observational_M3c_matched_rigor_2026-08-08")
for p in (M2, M3B, M3C):
    if p not in sys.path:
        sys.path.insert(0, p)

import v_bao                      # noqa: E402  frozen pipeline
import rerun_m3c as m3c           # noqa: E402  frozen M3c machinery (rz, forms)

ASSET_DIR = os.path.join(HERE, "legA_checkpoints", "assets")
RR_DIR = os.path.join(HERE, "legA_checkpoints", "rr_cache")
os.makedirs(ASSET_DIR, exist_ok=True)
os.makedirs(RR_DIR, exist_ok=True)

RAN_FACTOR = 10          # LS randoms = 10 x data (M3b's declared Category-A value)
BASE_SEED = 20260808     # asset partition seed base (frozen)
POOL_MIN_FACTOR = 1.5    # pool must hold >= 1.5 x N_target points

# Shell sets (frozen, prereg SS1): the M3 LRG driver set + the QSO split shells,
# and the M3b CMASS shells for the BOSS-density arm.
DESI_SHELLS = ([("LRG", round(z, 2), round(z + 0.05, 2))
                for z in np.arange(0.70, 1.10 - 1e-9, 0.05)]
               + [("QSO", 0.95, 1.10), ("QSO", 1.10, 1.25)])
BOSS_SHELLS = [("CMASS", round(z, 2), round(z + 0.05, 2))
               for z in np.arange(0.43, 0.68 - 1e-9, 0.05)]
DESI_CAPS = ("NGC", "SGC")
BOSS_CAPS = ("North", "South")

# LRG driver shells used for the amplitude calibration (real banked nosys A_b)
CAL_TARGETS = {  # key -> real fitted A_b (M3 checkpoints, nosys, 40-bin diag)
    ("LRG", 0.70, 0.75): 0.006876,
    ("LRG", 0.90, 0.95): 0.008741,
    ("LRG", 1.00, 1.05): 0.015251,
}


# ---------------------------------------------------------------------------
# Truth curves
# ---------------------------------------------------------------------------
def theta_i_deg(z):
    """Variant i: ell=58.34 Mpc over the UDT P1-fitted r(z) (frozen M3b ruler)."""
    return m3c.theta_pred_deg(np.asarray(z, dtype=np.float64))


_PUBSHAPE_EXP = -0.774           # power-law approx of the published theta~1/D_C
_THETA_II_ANCHOR = None


def theta_ii_deg(z):
    """Variant ii: published-shape gentle fall, anchored to variant i at z=0.9."""
    global _THETA_II_ANCHOR
    if _THETA_II_ANCHOR is None:
        _THETA_II_ANCHOR = float(theta_i_deg(0.9))
    return _THETA_II_ANCHOR * (np.asarray(z, dtype=np.float64) / 0.9) ** _PUBSHAPE_EXP


TRUTH_FNS = {"vi": theta_i_deg, "vii": theta_ii_deg}


def shell_key(survey, tracer, zlo, zhi):
    return f"{survey}_{tracer}_{zlo:.2f}_{zhi:.2f}"


def _det_seed(*parts):
    s = "|".join(str(p) for p in parts)
    return BASE_SEED + zlib.crc32(s.encode()) % 10_000_000


def _foot_deg2(ra, dec):
    ij = (np.floor(ra).astype(np.int64) % 360) * 181 + \
         (np.floor(dec).astype(np.int64) + 90)
    return float(np.unique(ij).size)

# ---------------------------------------------------------------------------
# Asset builder: per (survey, cap, shell) -- the skeleton facts of the real
# survey needed for a FAIR mock: footprint (randoms), weighted density (count),
# dN/dz (weighted z histogram).  Real data POSITIONS are never used.
# ---------------------------------------------------------------------------
def _asset_path(key, cap):
    return os.path.join(ASSET_DIR, f"{key}__{cap}.npz")


def build_asset_desi(tracer, cap, zlo, zhi):
    key = shell_key("DESI", tracer, zlo, zhi)
    fn = _asset_path(key, cap)
    if os.path.exists(fn):
        return fn
    dat = os.path.join(v_bao.DATA_DIR, f"{tracer}_{cap}_clustering.dat.fits")
    D = v_bao.load_catalog(dat, zrange=(zlo, zhi), use_sys=True)
    n_target = int(round(D.w_total))
    z_vals, z_w = D.z.copy(), D.w.copy()
    rans = [v_bao.load_catalog(
        os.path.join(v_bao.DATA_DIR, f"{tracer}_{cap}_{i}_clustering.ran.fits"),
        zrange=(zlo, zhi)) for i in range(4)]
    ra = np.concatenate([r.ra for r in rans])
    dec = np.concatenate([r.dec for r in rans])
    del rans, D
    _write_asset(fn, key, cap, ra, dec, n_target, z_vals, z_w)
    return fn


def build_asset_boss(tracer, cap, zlo, zhi):
    import boss_loader as bl
    key = shell_key("BOSS", tracer, zlo, zhi)
    fn = _asset_path(key, cap)
    if os.path.exists(fn):
        return fn
    D = bl.load_boss(os.path.join(bl.BOSS_DIR,
                                  f"galaxy_DR12v5_{tracer}_{cap}.fits.gz"),
                     zrange=(zlo, zhi), use_sys=True)
    n_target = int(round(D.w_total))
    z_vals, z_w = D.z.copy(), D.w.copy()
    R = bl.load_boss(os.path.join(bl.BOSS_DIR,
                                  f"random0_DR12v5_{tracer}_{cap}.fits.gz"),
                     zrange=(zlo, zhi), is_random=True)
    ra, dec = R.ra, R.dec
    del D
    _write_asset(fn, key, cap, ra, dec, n_target, z_vals, z_w)
    return fn


def _write_asset(fn, key, cap, ra, dec, n_target, z_vals, z_w):
    """Partition the real randoms deterministically: LS randoms (RAN_FACTOR x
    N_target) for the estimator, the REMAINDER = the skeleton pool that mock
    'galaxies' are drawn from (disjoint, so mock data never coincides with an
    LS random point)."""
    n_ran = ra.size
    n_ls = RAN_FACTOR * n_target
    if n_ran < n_ls + int(POOL_MIN_FACTOR * n_target):
        # reduce LS factor to preserve the pool (record actual factor)
        n_ls = max(n_ran - int(POOL_MIN_FACTOR * n_target), 4 * n_target)
    rng = np.random.default_rng(_det_seed("partition", key, cap))
    perm = rng.permutation(n_ran)
    ls, pool = perm[:n_ls], perm[n_ls:]
    foot = _foot_deg2(ra, dec)
    np.savez_compressed(
        fn, ls_ra=ra[ls], ls_dec=dec[ls], pool_ra=ra[pool],
        pool_dec=dec[pool], n_target=n_target, z_vals=z_vals, z_w=z_w,
        foot_deg2=foot, ls_factor=n_ls / max(n_target, 1))


# ---------------------------------------------------------------------------
# Mock generation on a cap
# ---------------------------------------------------------------------------
def _place_companions(p_xyz, theta_rad, rng):
    """Companion unit vectors at angular distance theta from parents p_xyz,
    random azimuth (pole-safe basis; same construction as synth_bao)."""
    a = np.zeros_like(p_xyz)
    polar = np.abs(p_xyz[:, 2]) > 0.9
    a[~polar, 2] = 1.0
    a[polar, 0] = 1.0
    e1 = np.cross(a, p_xyz)
    e1 /= np.linalg.norm(e1, axis=1)[:, None]
    e2 = np.cross(p_xyz, e1)
    psi = rng.uniform(0, 2 * np.pi, p_xyz.shape[0])
    th = theta_rad[:, None]
    return (np.cos(th) * p_xyz +
            np.sin(th) * (np.cos(psi)[:, None] * e1 +
                          np.sin(psi)[:, None] * e2))


class ShellAssets:
    """Loaded asset bundle + lazily-built membership tree for one cap-shell."""

    def __init__(self, survey, tracer, zlo, zhi, cap):
        key = shell_key(survey, tracer, zlo, zhi)
        d = np.load(_asset_path(key, cap))
        self.key, self.cap = key, cap
        self.ls_ra, self.ls_dec = d["ls_ra"], d["ls_dec"]
        self.pool_ra, self.pool_dec = d["pool_ra"], d["pool_dec"]
        self.n_target = int(d["n_target"])
        self.z_vals, zw = d["z_vals"], d["z_w"]
        self.z_p = zw / zw.sum()
        self.foot_deg2 = float(d["foot_deg2"])
        self.ls_factor = float(d["ls_factor"])
        lam = self.ls_ra.size / max(self.foot_deg2, 1.0)   # LS pts per deg^2
        self.r_memb_deg = float(np.sqrt(6.0 / (np.pi * lam)))
        self._tree = None

    @property
    def memb_tree(self):
        if self._tree is None:
            self._tree = cKDTree(v_bao._unit_vectors(self.ls_ra, self.ls_dec))
        return self._tree


def gen_mock_cap(assets, f_pair, truth_fn, rng):
    """One synthetic cap-shell catalog (tag='synthetic'), at the real weighted
    density, real footprint, real dN/dz, with the pair-split feature.

    F_PAIR definition (frozen): a fraction f_pair of the FINAL catalog points
    are companions; each companion sits at theta_t(z_parent) from its parent
    (random azimuth).  Companions outside the footprint (no LS random within
    r_memb_deg) are dropped and replaced by unpaired pool points, so the
    catalog size is exactly n_target and the density skeleton is preserved.
    Returns (Catalog, stats)."""
    N = assets.n_target
    n_c = int(round(f_pair * N))
    n_seed = N - n_c
    perm = rng.permutation(assets.pool_ra.size)
    if perm.size < N:
        raise RuntimeError(f"pool too small on {assets.key} {assets.cap}")
    seed_idx = perm[:n_seed]
    spare = perm[n_seed:]
    ra_s, dec_s = assets.pool_ra[seed_idx], assets.pool_dec[seed_idx]
    z_s = rng.choice(assets.z_vals, size=n_seed, replace=True, p=assets.z_p)
    # parents = the first n_c seeds (order already random)
    zp = z_s[:n_c]
    th_deg = np.asarray(truth_fn(zp), dtype=np.float64)
    p_xyz = v_bao._unit_vectors(ra_s[:n_c], dec_s[:n_c])
    q = _place_companions(p_xyz, np.radians(th_deg), rng)
    # footprint membership: nearest LS random within r_memb_deg
    dchord, _ = assets.memb_tree.query(q, k=1, workers=-1)
    accept = dchord <= v_bao._chord(assets.r_memb_deg)
    n_acc = int(accept.sum())
    ra_c = np.degrees(np.arctan2(q[accept, 1], q[accept, 0])) % 360.0
    dec_c = np.degrees(np.arcsin(np.clip(q[accept, 2], -1, 1)))
    z_c = zp[accept]
    n_rep = n_c - n_acc                      # replacements keep N exact
    rep_idx = spare[:n_rep]
    ra_r, dec_r = assets.pool_ra[rep_idx], assets.pool_dec[rep_idx]
    z_r = rng.choice(assets.z_vals, size=n_rep, replace=True, p=assets.z_p)
    ra = np.concatenate([ra_s, ra_c, ra_r])
    dec = np.concatenate([dec_s, dec_c, dec_r])
    zz = np.concatenate([z_s, z_c, z_r])
    w = np.ones(ra.size, dtype=np.float64)
    cat = v_bao.Catalog(ra, dec, zz, w, "synthetic",
                        f"mock-{assets.key}-{assets.cap}")
    stats = {"n_target": N, "n_pairs_planned": n_c, "n_pairs_placed": n_acc,
             "edge_loss_frac": (n_rep / max(n_c, 1)),
             "theta_t_mean_deg": float(th_deg.mean()),
             "theta_t_sd_deg": float(th_deg.std()),
             "r_memb_deg": assets.r_memb_deg}
    return cat, stats


def ls_catalog(assets, zc):
    """The fixed LS randoms catalog for a cap-shell (tag='synthetic': it is a
    frozen deterministic subsample of the real randoms, used as the mock's
    selection function; carries no real-data clustering)."""
    n = assets.ls_ra.size
    return v_bao.Catalog(assets.ls_ra, assets.ls_dec,
                         np.full(n, zc), np.ones(n),
                         "synthetic", f"lsran-{assets.key}-{assets.cap}")
