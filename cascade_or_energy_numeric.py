"""or_energy_numeric.py -- D-D spot check on the banked rung (cascade_stageB_rungs.json rung 0:
a* = 1.4813439655, risefall m=3, Z=8, rho_c=1). ONE IVP shot; all else quadrature on dense output.
Checks the derived bookkeeping:
  (1) E_can := -int L dr  (canonical t-energy per-4pi, c=1)  ==  int (2U-4) dr   [via H==0]
  (2) E_can  ==  [4 e^{-2phi} rho rho']_0^{r_s} - int rho U'(rho) dr             [C9 identity]
  (3) Delta m_MS = m(r_s)-m(0) = (rho_s - rho_c)/2  ==  int 4 pi rho^2 rho' eps dr  [C10/C12]
  (4) sign comparison E_can vs Delta m_MS vs m_MS(seal)  [D-C anchor]
"""
import json, sys
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, shoot

rung = json.load(open("/home/udt-admin/udt_mass_codex/cascade_stageB_rungs.json"))["rungs"][0]
a_star, Z, rho_c = rung["a_star"], 8.0, 1.0
U, Up, lab = make_risefall_slice(a_star, m=3.0, rho_c=rho_c)
o = shoot(Z, U, Up, rho_c)                       # IVP shot #1 (the only one)
assert o["status"] == "seal", o["status"]
r_s, rho_s, q = o["r_s"], o["rho_s"], o["q"]
print(f"slice={lab}  Z={Z:g}  status={o['status']}")
print(f"r_s={r_s:.10g}  rho_s={rho_s:.10g}  rho'_s={o['rhop_s']:.3e}  q={q:.10g}")
print(f"rung JSON:  r_s={rung['r_s']:.10g}  rho_s={rung['rho_s']:.10g}  q={rung['q']:.10g}")

rr = np.linspace(0.0, r_s, 200001)
phi, phip, rho, rhop = o["sol"].sol(rr)
e2p = np.exp(2.0 * phi)
Uv, Upv = U(rho), Up(rho)

# banked reduced Lagrangian and r-Hamiltonian
L = 0.5 * Z * rho**2 * phip**2 - 2.0 * rhop**2 / e2p + 2.0 - Uv
H = 0.5 * Z * rho**2 * phip**2 - 2.0 * rhop**2 / e2p - 2.0 + Uv
print(f"\nH_drift (max|H|)            = {np.max(np.abs(H)):.3e}   (background quality)")

I = lambda f: float(np.trapezoid(f, rr))
E_can   = -I(L)
E_can2  = I(2.0 * Uv - 4.0)
bdy     = 4.0 * rho / e2p * rhop
E_can3  = (bdy[-1] - bdy[0]) - I(rho * Upv)
print(f"\nE_can = -int L dr           = {E_can:+.10g}")
print(f"int (2U-4) dr               = {E_can2:+.10g}   rel.diff = {abs(E_can-E_can2)/abs(E_can):.2e}")
print(f"[4e^-2phi rho rho'] - int rho U' = {E_can3:+.10g}   rel.diff = {abs(E_can-E_can3)/abs(E_can):.2e}")
print(f"   (boundary piece [4e^-2phi rho rho']_0^rs = {bdy[-1]-bdy[0]:+.3e}, ~0 by fold pins)")

# Misner-Sharp route
m = 0.5 * rho * (1.0 - rhop**2 / e2p)
dm = m[-1] - m[0]
# eps on the EL equations (C12, no H used): 8 pi rho^2 eps = 1 - e^{-2phi}rho'^2 - 2 rho e^{-2phi}phi'rho' + (Z/2)rho^2 phi'^2 - (rho/2)U'
eps8 = 1.0 - rhop**2 / e2p - 2.0 * rho * phip * rhop / e2p + 0.5 * Z * rho**2 * phip**2 - 0.5 * rho * Upv
dm_int = I(4.0 * np.pi * rho**2 * rhop * eps8 / (8.0 * np.pi * rho**2))
print(f"\nm_MS(0) = {m[0]:+.10g}  (rho_c/2 = {rho_c/2:+.10g})")
print(f"m_MS(r_s) = {m[-1]:+.10g}  (rho_s/2 = {rho_s/2:+.10g});  2m/rho seal = {2*m[-1]/rho[-1]:.12f}")
print(f"Delta m_MS = {dm:+.10g}   vs (rho_s-rho_c)/2 = {(rho_s-rho_c)/2:+.10g}")
print(f"int 4 pi rho^2 rho' eps dr  = {dm_int:+.10g}   rel.diff = {abs(dm-dm_int)/abs(dm):.2e}")

print(f"\nD-C sign data:  sign(E_can) = {np.sign(E_can):+.0f};  sign(Delta m_MS) = {np.sign(dm):+.0f};  "
      f"m_MS(seal) = {m[-1]:+.6g} > 0")
print(f"ratios (NOT expected constant): E_can/Delta m = {E_can/dm:+.6g};  E_can/m_s = {E_can/m[-1]:+.6g}")
# where does eps change sign / where is -L density concentrated
negL = 2.0 * Uv - 4.0
print(f"\ndensity structure: min/max of -L density = {negL.min():+.4g}/{negL.max():+.4g}; "
      f"min/max of eps*8pi rho^2 = {eps8.min():+.4g}/{eps8.max():+.4g}")
frac_eps_neg = float(np.trapezoid((eps8 < 0).astype(float), rr) / r_s)
print(f"coordinate fraction with eps<0 = {frac_eps_neg:.4f}")
