#!/usr/bin/env python3
"""BOSS DR12 loader adapter for the FROZEN M3b pipeline (Phase 3).

Prereg af9fa75d + freeze f9c5b436 (F-RETRO: ell + prediction frozen BEFORE any
BOSS contact). This adapter reuses the FROZEN M2/M3 machinery in v_bao UNCHANGED
(Landy-Szalay, bump search, look-elsewhere, GPU spot-check). It ONLY:
  (1) maps BOSS DR12v5 combined-LSS column names onto the v_bao Catalog;
  (2) extends the F-IMPORT-LCDM blacklist to BOSS fiducial-cosmology carriers
      (NZ / NBAR / WEIGHT_FKP / any comoving/DISTANCE column / any _rec file)
      and machine-tests that they are physically unreturnable;
  (3) applies a pre-declared Category-A random DOWNSAMPLE for compute
      tractability (anti-hang) -- estimator/bins/bump/thresholds all frozen.

BOSS completeness weight (standard, Reid et al. 2016 eq.):
      w = WEIGHT_SYSTOT * (WEIGHT_CP + WEIGHT_NOZ - 1)
It is a COMPLETENESS weight (fiber-collision + redshift-failure + imaging
systematics), NOT a fiducial-cosmology weight. WEIGHT_FKP (uses n(z) and a
fiducial P0) is fiducial -> BLACKLISTED. NZ/NBAR (n(z), fiducial cosmology) ->
BLACKLISTED. Randoms carry no CP/NOZ/SYSTOT -> random weight = 1 (they ARE the
selection function). The use_sys=False variant drops WEIGHT_SYSTOT (imaging-
systematics over-correction caveat), matching the DESI sys/nosys split.

NOTHING here touches ell (58.34 Mpc), r(z), the prediction table, the bin/shell/
threshold choices, or any frozen pipeline parameter.
"""
import os
import numpy as np

import v_bao  # frozen M2 pipeline (on sys.path via the runner)

BOSS_DIR = "/media/udt-admin/ScratchDisk/Data/boss_dr12"

# --- Column policy (F-IMPORT-LCDM, extended to BOSS names) ---
BOSS_ALLOWED = ("RA", "DEC", "Z", "WEIGHT_SYSTOT", "WEIGHT_CP", "WEIGHT_NOZ")
BOSS_BLACKLIST = ("NZ", "NBAR", "WEIGHT_FKP", "COMOVING", "DISTANCE",
                  "DC", "RADIAL_DISTANCE", "COMP")
BLACKLIST_PATH_TOKEN = "_rec"   # reconstruction products forbidden

# --- Category-A random downsample (compute/noise only; declared BEFORE any
#     w(theta) is seen; F-RETRO safe -- not tuned to results). RR/DR noise at
#     20x data is far below the 24-region jackknife sample variance. ---
RAN_FACTOR = 10
RAN_SEED = 20260808


class BossBlacklistViolation(Exception):
    """F-IMPORT-LCDM machine wire (BOSS): forbidden column or _rec path."""


def _load_boss_columns(path, columns):
    """The ONLY read path to BOSS files. Enforces BEFORE any I/O:
       (a) no `_rec` (reconstruction) file may be opened;
       (b) every requested column is on BOSS_ALLOWED and not on BOSS_BLACKLIST.
    A fiducial-cosmology / n(z) / comoving column is physically unreturnable."""
    base = os.path.basename(str(path))
    if BLACKLIST_PATH_TOKEN in base.lower():
        raise BossBlacklistViolation(
            f"path '{base}' is a reconstruction product (_rec): forbidden")
    for c in columns:
        cu = str(c).upper()
        if cu in BOSS_BLACKLIST:
            raise BossBlacklistViolation(
                f"column '{c}' is blacklisted (F-IMPORT-LCDM)")
        if cu not in BOSS_ALLOWED:
            raise BossBlacklistViolation(
                f"column '{c}' is not on the BOSS whitelist")
    from astropy.io import fits
    out = {}
    with fits.open(path, memmap=True) as hdul:
        data = hdul[1].data
        avail = {c.name.upper() for c in data.columns}
        for c in columns:
            if str(c).upper() not in avail:
                # missing (e.g. randoms have no CP/NOZ/SYSTOT) -> caller default
                out[c] = None
                continue
            out[c] = np.asarray(data[c], dtype=np.float64)
    return out


def load_boss(path, zrange=None, use_sys=True, is_random=False,
              ran_factor=RAN_FACTOR, seed=RAN_SEED):
    """Load a BOSS DR12 combined-LSS catalog as a v_bao.Catalog(tag='real').

    Galaxy weight = WEIGHT_SYSTOT^[use_sys] * (WEIGHT_CP + WEIGHT_NOZ - 1).
    Random weight = 1 (randoms carry no completeness columns; they are the
    selection function). Randoms are uniformly downsampled to <= ran_factor x
    the (pre-shell) galaxy-equivalent count -- Category-A, declared pre-freeze
    of results; caller passes n_data_ref for the factor, else no cap.
    """
    if is_random:
        cols = _load_boss_columns(path, ["RA", "DEC", "Z"])
        ra, dec, z = cols["RA"], cols["DEC"], cols["Z"]
        w = np.ones(ra.size, dtype=np.float64)
    else:
        want = ["RA", "DEC", "Z", "WEIGHT_CP", "WEIGHT_NOZ"]
        if use_sys:
            want.append("WEIGHT_SYSTOT")
        cols = _load_boss_columns(path, want)
        ra, dec, z = cols["RA"], cols["DEC"], cols["Z"]
        cp = cols["WEIGHT_CP"]
        noz = cols["WEIGHT_NOZ"]
        w = (cp + noz - 1.0)
        if use_sys and cols.get("WEIGHT_SYSTOT") is not None:
            w = w * cols["WEIGHT_SYSTOT"]
        w = w.astype(np.float64)
    if zrange is not None:
        sel = (z >= zrange[0]) & (z < zrange[1])
        ra, dec, z, w = ra[sel], dec[sel], z[sel], w[sel]
    return v_bao.Catalog(ra, dec, z, w, tag="real",
                         name=os.path.basename(str(path)))


def downsample(cat, n_target, seed=RAN_SEED):
    """Uniform random downsample of a Catalog to <= n_target rows (Category-A;
    preserves the angular selection function). Deterministic given seed."""
    n = len(cat)
    if n <= n_target:
        return cat
    rng = np.random.default_rng(seed)
    idx = rng.choice(n, size=int(n_target), replace=False)
    return v_bao.Catalog(cat.ra[idx], cat.dec[idx], cat.z[idx], cat.w[idx],
                         tag=cat.tag, name=cat.name + "[ds]")
