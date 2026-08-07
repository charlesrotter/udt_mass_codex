#!/usr/bin/env python3
"""M1 spot-verify (F-PEEK-legal: schema, row counts, z-range, dN/dz only).

Verifies the M1 recon's load-bearing claims against the actual DESI DR1 files:
  - column names present (RA/DEC/Z, WEIGHT_COMP, WEIGHT_ZFAIL, WEIGHT_SYS)
  - NX / WEIGHT_FKP present-but-avoidable (i.e. they exist as columns we must blacklist)
  - no `_rec` products in the directory
  - row counts ~ as reported; z ranges as reported
  - dN/dz histograms (schema-level; saved as text)
NO correlation function, NO clustering statistic is computed here.
"""
import glob
import json
import os

import numpy as np
from astropy.io import fits

DATA_DIR = "/media/udt-admin/ScratchDisk/Data/desi_dr1"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vbao_outputs")
os.makedirs(OUT, exist_ok=True)

M1_CLAIMS = {  # tracer -> (N_ngc, N_sgc, zlo, zhi)
    "BGS_BRIGHT": (2909876, 1047989, 0.010, 0.500),
    "LRG": (1476135, 662492, 0.400, 1.100),
    "ELG_LOPnotqso": (1821322, 610750, 0.800, 1.600),
    "QSO": (793219, 430172, 0.800, 3.500),
}
NEEDED = ["RA", "DEC", "Z", "WEIGHT_COMP", "WEIGHT_ZFAIL", "WEIGHT_SYS"]
BLACKLISTED_PRESENT = ["NX", "WEIGHT_FKP"]

report = {"rec_files": [], "tracers": {}}

# 1. no _rec products anywhere in the directory
all_files = sorted(os.listdir(DATA_DIR))
report["rec_files"] = [f for f in all_files if "_rec" in f.lower()]
report["n_files"] = len(all_files)

for tracer, (n_ngc_claim, n_sgc_claim, zlo_c, zhi_c) in M1_CLAIMS.items():
    tinfo = {}
    for cap in ("NGC", "SGC"):
        dat = os.path.join(DATA_DIR, f"{tracer}_{cap}_clustering.dat.fits")
        with fits.open(dat, memmap=True) as hdul:
            hdu = hdul[1]
            cols = [c.name for c in hdu.columns]
            nrows = hdu.header["NAXIS2"]
            z = np.asarray(hdu.data["Z"], dtype=np.float64)
        hist, edges = np.histogram(z, bins=50, range=(zlo_c, zhi_c))
        tinfo[cap] = {
            "nrows": int(nrows),
            "claimed": n_ngc_claim if cap == "NGC" else n_sgc_claim,
            "cols_needed_present": [c for c in NEEDED if c in cols],
            "cols_needed_missing": [c for c in NEEDED if c not in cols],
            "blacklisted_present": [c for c in BLACKLISTED_PRESENT if c in cols],
            "z_min": float(z.min()),
            "z_max": float(z.max()),
            "claimed_z": [zlo_c, zhi_c],
            "dNdz_hist": hist.tolist(),
            "dNdz_edges": [float(edges[0]), float(edges[-1])],
        }
        del z
    # randoms: schema + rowcount of ran_0 only (I/O feasibility)
    ran = os.path.join(DATA_DIR, f"{tracer}_NGC_0_clustering.ran.fits")
    with fits.open(ran, memmap=True) as hdul:
        rcols = [c.name for c in hdul[1].columns]
        rrows = hdul[1].header["NAXIS2"]
    tinfo["ran0_NGC"] = {
        "nrows": int(rrows),
        "cols_needed_present": [c for c in NEEDED if c in rcols],
        "cols_needed_missing": [c for c in NEEDED if c not in rcols],
        "blacklisted_present": [c for c in BLACKLISTED_PRESENT if c in rcols],
    }
    report["tracers"][tracer] = tinfo

with open(os.path.join(OUT, "m1_spot_verify.json"), "w") as f:
    json.dump(report, f, indent=1)

# concise console summary
print("_rec files in dir:", report["rec_files"] or "NONE")
for t, ti in report["tracers"].items():
    for cap in ("NGC", "SGC"):
        d = ti[cap]
        ok_n = d["nrows"] == d["claimed"]
        print(f"{t} {cap}: rows={d['nrows']} (claim {d['claimed']} {'OK' if ok_n else 'MISMATCH'}) "
              f"z=[{d['z_min']:.4f},{d['z_max']:.4f}] claim {d['claimed_z']} "
              f"missing={d['cols_needed_missing']} blk_present={d['blacklisted_present']}")
    r = ti["ran0_NGC"]
    print(f"{t} ran0 NGC: rows={r['nrows']} missing={r['cols_needed_missing']} "
          f"blk_present={r['blacklisted_present']}")
