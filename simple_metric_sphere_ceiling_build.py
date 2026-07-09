#!/usr/bin/env python3
"""
Build/characterize sphere-ceiling A=1-r/X under full light.
SNe: demo residual only (not law selection). LCDM = reference scaffold.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve

from simple_metric_sphere_ceiling import (
    M_sun_from_X_Mpc,
    dL_over_X_hyp_J1,
    dL_over_X_linear,
    m_of_r_linear,
    r_of_z_linear,
    rho_of_r_linear,
)

ROOT = Path(__file__).resolve().parent


def main():
    from simple_metric_sphere_ceiling import _self_check

    _self_check()

    d = np.genfromtxt(ROOT / "Data" / "Pantheon+SH0ES.dat", names=True, dtype=None, encoding=None)
    mask = (d["IS_CALIBRATOR"].astype(int) == 0) & (d["zHD"] > 0.01)
    idx = np.where(mask)[0]
    z = np.asarray(d["zHD"][mask], float)
    m = np.asarray(d["m_b_corr"][mask], float)
    with open(ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov") as f:
        N = int(f.readline())
    C = np.loadtxt(ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov", skiprows=1).reshape(N, N)
    C = 0.5 * (C + C.T)
    C = C[np.ix_(idx, idx)]
    cf = cho_factor(C, lower=True, check_finite=False)

    def score(f, label):
        mu = 5 * np.log10(np.maximum(f, 1e-30))
        dv = m - mu
        ones = np.ones_like(dv)
        O = float((ones @ cho_solve(cf, dv)) / (ones @ cho_solve(cf, ones)))
        res = dv - O
        chi2 = float(res @ cho_solve(cf, res))
        dof = len(z) - 1
        rms = float(np.sqrt(np.mean(res**2)))
        hi = z >= 0.6
        print(
            f"  [{label:40s}] chi2/dof={chi2/dof:.4f} RMS={rms:.4f} "
            f"〈res〉z>0.6={np.mean(res[hi]):+.4f}  O={O:.4f}"
        )
        return {
            "label": label,
            "chi2_dof": chi2 / dof,
            "rms": rms,
            "mean_res_hi": float(np.mean(res[hi])),
            "offset_O": O,
        }

    print("=" * 70)
    print("Sphere ceiling build — characterize (not law-picking)")
    print(f"N={len(z)}")
    print("=" * 70)

    s_lin = score(dL_over_X_linear(z), "A=1-r/X full light")
    s_hyp = score(dL_over_X_hyp_J1(z), "hyp tanh J1 full light")

    def lcdm(zz, Om=0.3):
        out = np.empty_like(zz)
        for i, zi in enumerate(zz):
            g = np.linspace(0, zi, 1024)
            E = np.sqrt(Om * (1 + g) ** 3 + (1 - Om))
            out[i] = (1 + zi) * np.trapezoid(1 / E, g)
        return out

    s_L = score(lcdm(z), "LCDM Om=0.3 REF only")

    # calibration X at M_B=-19.25
    MB = -19.25
    X = 10 ** ((s_lin["offset_O"] - MB - 25.0) / 5.0)
    print(f"\n  calib M_B={MB} => X={X:.2f} Mpc  M_tot={M_sun_from_X_Mpc(X):.3e} Msun")

    # density/mass sample at X=1 geometric units note
    print("\n  geometric (X=1 units): z, r/X, d_L/X, m/(c²X/2G), X*r*rho factor")
    for zz in [0.1, 0.5, 1.0, 2.0]:
        r = float(np.asarray(r_of_z_linear(zz, 1.0)).reshape(-1)[0])
        dL = float(np.asarray(dL_over_X_linear(zz)).reshape(-1)[0])
        # compactness 2Gm/(c²r) = r/X for this profile
        print(f"    z={zz:.1f}  r/X={r:.4f}  dL/X={dL:.4f}  compactness=r/X={r:.4f}")

    out = {
        "linear_ceiling": s_lin,
        "hyp_tanh": s_hyp,
        "lcdm_ref": s_L,
        "X_Mpc_MB_m19p25": float(X),
        "M_tot_Msun": float(M_sun_from_X_Mpc(X)),
        "provenance": {
            "A": "1-r/X",
            "vacuum": False,
            "rho": "c^2/(4 pi G X r)",
            "M_tot": "c^2 X/(2G)",
            "not": "tanh composition; half light; free D_A fit",
        },
    }
    path = ROOT / "simple_metric_sphere_ceiling_build_out.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
