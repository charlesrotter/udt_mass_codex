"""or_energy_rung1_and_alignment.py -- record of the 3rd/4th bounded IVP shots (rung 1 check +
pointwise sign-alignment stats on rungs 0,1). Outputs recorded in the D-D section of the report.

Shot 2 (rung 1, a*=1.4903071093405713, risefall m=3, Z=8):
  H_drift=1.08e-09
  E_can=-int L = -3.2237002;  int(2U-4)=-3.2237002;  int rho U'=+3.2237441
  Dm=-0.1786993 = (rho_s-1)/2;  int 4pi rho^2 rho' eps = -0.17869916   (rel 4e-6)
  signs: E_can -1, Dm -1, m_s=+0.321301 (>0)

Shots 3,4 (alignment stats, coordinate measure):
  rung 0: eps>0 on 0.9717 of cell; -L>0 on 0.954 (tiny values, max +4.7e-4) but
          int(-L)= -9.77 over m'>0 region, -1.84 over m'<0: MAGNITUDE-weighted, -L is negative
          where the MS reading is positive.
  rung 1: eps>0 on 1.0000; int(-L) = -0.713 (m'>0 region) + (-2.514) (m'<0 region) = -3.22.
"""
import json, sys
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, shoot

rungs = json.load(open("/home/udt-admin/udt_mass_codex/cascade_stageB_rungs.json"))["rungs"]
for i in (0, 1):
    U, Up, lab = make_risefall_slice(rungs[i]["a_star"], m=3.0, rho_c=1.0)
    o = shoot(8.0, U, Up, 1.0)
    rr = np.linspace(0.0, o["r_s"], 200001)
    phi, phip, rho, rhop = o["sol"].sol(rr)
    e2p = np.exp(2.0 * phi); Uv, Upv = U(rho), Up(rho)
    negL = 2.0 * Uv - 4.0                              # -L on-shell (banked-orientation energy density)
    eps8 = (1.0 - rhop**2 / e2p - 2.0 * rho * phip * rhop / e2p
            + 0.5 * 8.0 * rho**2 * phip**2 - 0.5 * rho * Upv)   # 8 pi rho^2 eps, on-shell (C12 pre-H form)
    mp = rhop * eps8 / 2.0                             # m' = 4 pi rho^2 rho' eps
    w = np.gradient(rr)
    I = lambda f, msk=None: float(np.sum((f * w)[msk]) if msk is not None else np.trapezoid(f, rr))
    m = 0.5 * rho * (1.0 - rhop**2 / e2p)
    print(f"rung {i}: E_can={-I(-negL):+.8g}"  # note: -int L = int(-L) = int negL on-shell
          f"  Dm={m[-1]-m[0]:+.8g}  m_s={m[-1]:+.8g}"
          f"  int(-L)|m'>0={I(negL, mp > 0):+.6g}  int(-L)|m'<0={I(negL, mp < 0):+.6g}"
          f"  frac(eps>0)={w[eps8 > 0].sum() / w.sum():.4f}")
