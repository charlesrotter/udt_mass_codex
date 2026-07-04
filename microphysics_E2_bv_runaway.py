"""microphysics_E2_bv_runaway.py -- BLIND VERIFIER attack 4: recompute (own code, CPU) the
runaway characterization claims from the saved .pt states:
  (a) self-similarity / dilation exponents: -1.31 (A1Z8), -0.99 (A1Z1), -1.00 (A3Z8),
      non-self-similar decelerating (A3Z1, max|F| exponent ~ -1.40)
  (b) H_cell O(1) on end states (>= 4 states across brackets) -- the false-floor logic
  (c) shell-width preservation numbers
  (d) bracket-4 preserved-vs-tuned arithmetic: seed height 1.0037706012 vs station
      1.0036152090; end-state rho_p at seed height to 1.5e-7..3.2e-5; U(rho_p) < 2
  (e) bracket-2 retro-check: "locked" rho_p = seed value 1.0036886, station root = 1.003829
NOT committed. Single process, CPU only (residual evaluations, no solves).
"""
import os, math, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import cell_solver_f2d as F2D

def load_state(fn):
    d = torch.load(fn, map_location="cpu", weights_only=False)
    return d

def c1c_rows(Nr, Nth):
    off = 2*(Nr-2) + (Nr-2)*Nth + 2 + Nth
    return off, off+Nth

def eval_state(fn, lab):
    d = load_state(fn)
    br = C.load_bracket(lab)
    ctx = C.make_ctx_comp(d["Nr"], d["Nth"], d["Na"], kmap=d["kmap"], device="cpu")
    w = d["w"].to(torch.float64)
    prm = tuple(d["prm"])
    F = C.residual_comp(w, ctx, prm, br)
    a, b = c1c_rows(d["Nr"], d["Nth"])
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(w, ctx)
    return dict(d=d, br=br, ctx=ctx, w=w, prm=prm, F=F.detach(),
                C1c=F[a:b].detach().numpy(), maxF=float(F.abs().max()),
                r_p=float(r_p), r_sU=float(r_sU),
                rho_p=float(rho_a[0]), phi_core=float(phi_c[0]))

print("="*100)
print("(a) DILATION EXPONENTS (own recomputation, CPU residuals from saved .pt)")
print("="*100)
pairs = [
    ("A1 m=3 Z=8", "E2b_A1Z8_P2_W6_plateau.pt",  "E2b_A1Z8_P2b_wideguard_W6_plateau.pt",  -1.31),
    ("A1 m=3 Z=1", "E2b_A1Z1_P2_W4_wall.pt",     "E2b_A1Z1_P2b_wideguard_W4_wall.pt",     -0.99),
    ("A3 Z=8",     "E2b_A3Z8_P2_W3_wall.pt",     "E2b_A3Z8_P2b_wideguard_W3_wall.pt",     -1.00),
    ("A3 Z=1",     "E2b_A3Z1_P2_W4_wall.pt",     "E2b_A3Z1_P2b_wideguard_CONT_W4_wall.pt", None),
]
for lab, f1, f2, claimed in pairs:
    s1 = eval_state(f1, lab); s2 = eval_state(f2, lab)
    dil = s2["r_p"] / s1["r_p"]
    r1, r2 = s1["C1c"], s2["C1c"]
    ratio = r1 / r2                     # parent/wide: >1 if residual decays with dilation
    same_sign = np.all(np.sign(r1) == np.sign(r2))
    with np.errstate(all="ignore"):
        per_node = np.log(np.abs(r2/r1)) / np.log(dil)
    expF = math.log(s2["maxF"]/s1["maxF"]) / math.log(dil)
    print(f"\n{lab}: parent r_p={s1['r_p']:.1f} maxF={s1['maxF']:.3e} | wide r_p={s2['r_p']:.1f} "
          f"maxF={s2['maxF']:.3e} | dilation x{dil:.4f}")
    print(f"  C1c parent: {np.array2string(r1, precision=2)}")
    print(f"  C1c wide  : {np.array2string(r2, precision=2)}")
    print(f"  same sign pattern: {same_sign}")
    print(f"  per-node exponents: {np.array2string(per_node, precision=3)}")
    print(f"  per-node mean+/-sd: {np.nanmean(per_node):+.3f} +/- {np.nanstd(per_node):.3f}"
          f"   ratio scatter: {np.nanmean(np.abs(r1/r2)):.4f} +/- {np.nanstd(np.abs(r1/r2)):.4f}")
    print(f"  max|F| exponent: {expF:+.4f}   (claimed: {claimed})")

print("\n" + "="*100)
print("(b) H_cell FREE GATE on end states (own recompute via F2D.H_of_r, CPU)")
print("="*100)
hstates = [
    ("A1 m=3 Z=8", "E2b_A1Z8_P2_W1_wall.pt"),
    ("A1 m=3 Z=8", "E2b_A1Z8_P2b_wideguard_W6_plateau.pt"),
    ("A1 m=3 Z=1", "E2b_A1Z1_P2c_extended_W5_wall.pt"),
    ("A3 Z=8",     "E2b_A3Z8_P2c_extended_W5_wall.pt"),
    ("A3 Z=1",     "E2b_A3Z1_P2_W5_wall.pt"),
    ("A3 Z=1",     "E2b_A3Z1_P2b_wideguard_CONT_W4_wall.pt"),
]
for lab, fn in hstates:
    s = eval_state(fn, lab)
    d = s["d"]
    ctx = s["ctx"]
    Q, v_cell = C.cell_fields(s["w"], ctx, s["prm"])
    Hc = F2D.H_of_r(v_cell, ctx["cell"], s["prm"])
    print(f"{fn:48s} maxF={s['maxF']:.3e}  H_cell_max={float(Hc.abs().max()):.3e}  "
          f"H_cell(seal)={float(Hc[-1]):+.3e}")

print("\n" + "="*100)
print("(c) SHELL WIDTHS (r_sU - r_p) vs seed width 0.05*r_s")
print("="*100)
for lab, fn in [("A1 m=3 Z=8","E2b_A1Z8_P2_W1_wall.pt"),
                ("A1 m=3 Z=1","E2b_A1Z1_P2c_extended_W5_wall.pt"),
                ("A3 Z=8","E2b_A3Z8_P2c_extended_W5_wall.pt"),
                ("A3 Z=1","E2b_A3Z1_P2b_wideguard_CONT_W4_wall.pt")]:
    s = eval_state(fn, lab)
    seedw = 0.05 * s["br"]["r_s"]
    print(f"{fn:48s} width={s['r_sU']-s['r_p']:.4f}  seed width={seedw:.4f}  "
          f"rel dev={abs(s['r_sU']-s['r_p']-seedw)/seedw:.2e}")

print("\n" + "="*100)
print("(d) BRACKET 4 preserved-vs-tuned arithmetic (A3 Z=1)")
print("="*100)
br4 = C.load_bracket("A3 Z=1")
b = br4["a_star"]
station = b ** (-0.5)
seed_h = float(np.interp(0.95 * br4["r_s"], br4["prof_r"], br4["prof_rho"]))
U4, _ = C.make_slice(br4["family"], b, np)
print(f"a*=b={b!r}  station b^-1/2 = {station:.10f}  (claimed 1.0036152090)")
print(f"seed height rho(0.95 r_s) = {seed_h:.10f}  (claimed 1.0037706012)")
print(f"U(seed height) = {float(U4(np.longdouble(seed_h))):.7f} (claimed 1.9999977 < 2)")
print(f"U(station)     = {float(U4(np.longdouble(station))):.10f} (should be 2 exactly)")
print(f"separation seed-station = {seed_h-station:+.4e} (claimed +1.554e-4)")
print(f"r* = 0.94801*r_s = {0.94801*br4['r_s']:.2f}; 0.95*r_s = {0.95*br4['r_s']:.2f}")
devs = []
import glob
for fn in sorted(glob.glob("E2b_A3Z1_P2*wall*.pt")) + sorted(glob.glob("E2b_A3Z1_P2b*.pt")):
    s = eval_state(fn, "A3 Z=1")
    dv_seed = s["rho_p"] - seed_h; dv_stn = s["rho_p"] - station
    devs.append(abs(dv_seed))
    print(f"  {os.path.basename(fn):44s} rho_p={s['rho_p']:.7f} dev(seed)={dv_seed:+.2e} "
          f"dev(stn)={dv_stn:+.2e}  U(rho_p)={float(U4(np.longdouble(s['rho_p']))):.7f}")
print(f"  => max |dev(seed)| over wall states: {max(devs):.2e} vs |seed-station| = {abs(seed_h-station):.2e}")

print("\n" + "="*100)
print("(e) BRACKET 2 retro-check (A1 Z=1): seed height vs station root")
print("="*100)
br2 = C.load_bracket("A1 m=3 Z=1")
a2 = br2["a_star"]
seed_h2 = float(np.interp(0.95 * br2["r_s"], br2["prof_r"], br2["prof_rho"]))
# station root of U(rho)=2 for A1 m=3: rho^3 e^{-a(rho^2-1)} = 1, root > 1
from scipy.optimize import brentq
g = lambda rho: 3*math.log(rho) - a2*(rho*rho - 1.0)
root = brentq(g, 1.0005, 1.2)
U2, _ = C.make_slice(br2["family"], a2, np)
print(f"a* = {a2!r}")
print(f"seed height rho(0.95 r_s) = {seed_h2:.10f} (claimed 1.0036886)   U = {float(U2(np.longdouble(seed_h2))):.7f}")
print(f"station root (U=2, >1)    = {root:.10f} (claimed 1.003829)")
prof_station = float(np.interp(0.95172*br2["r_s"], br2["prof_r"], br2["prof_rho"]))
print(f"profile at r*=0.95172 r_s = {prof_station:.7f}")
for fn in ["E2b_A1Z1_P2_W5_wall.pt", "E2b_A1Z1_P2c_extended_W5_wall.pt", "E2b_A1Z1_P2_W6_wall.pt"]:
    s = eval_state(fn, "A1 m=3 Z=1")
    print(f"  {fn:40s} rho_p={s['rho_p']:.7f}  dev(seed)={s['rho_p']-seed_h2:+.2e} "
          f"dev(root)={s['rho_p']-root:+.2e}")

print("\nDONE (bv_runaway)")
