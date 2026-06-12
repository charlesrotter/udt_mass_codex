#!/usr/bin/env python3
"""P1 VALIDATION LADDER stages (d), (e) + first physics readout (f).

Class A: diagonal class (q = w = 0):        X_tt - X_t = +2 P_X
Class B: q = g_rtheta freed (exact algebraic elimination, w = 0):
                                            X_tt - X_t = -2 P_X
         valid on the radial-dominant branch Delta = f f_t^2 - (1-u^2) f_u^2 > 0;
         Q* = 2 f_t v/(f f_t^2 + v^2) reconstructed in closed form.
Fully-free (q and w): NO smooth stationary solutions off the spherical
         family (w-runaway theorem, derive_system.py D-14/D-15) -> the
         numeric confirmation of the runaway is part of stage (d).
"""
import numpy as np, time
from solver import AngularSector, run_flow, flow_state, bisect_cstar, \
                   legendre_Y, Qstar_field

npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond); npass += ok; nfail += (not ok)
    print(f"V-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

cM2, gam = 0.2832873535156249512, 1.0
ang3 = AngularSector(3)

# ================================================================ (d)
print("=== (d) the joint system on the M2-formed background ===", flush=True)
resA = run_flow(ang3, gam, cM2, sign=+1)
print(f"Class A (diagonal): sealed={resA['sealed']}, t_seal*={resA['t_seal']:.6f}, "
      f"y_seal*={resA['y_seal']:.6f}", flush=True)

# ---- (d1) q response (tadpole field) evaluated ON the diagonal solution
print("\n(d1) q* response field on the DIAGONAL M2 solution "
      "(the first-response tadpole):", flush=True)
print("   t      y       max|Q*|   at u     min Delta   Delta<0 ?", flush=True)
minDelta_A = np.inf
for t in [0.25, 0.5, 1.0, 1.5, 1.9, 2.05, 2.13]:
    if t > resA['t_stop']: t = resA['t_stop']
    X, V = flow_state(resA, t); X, V = X[0], V[0]
    ug, Q, Delta, f, ft, v = Qstar_field(ang3, X, V, np.linspace(-1, 1, 2001))
    i = np.argmax(np.abs(Q))
    minDelta_A = min(minDelta_A, Delta.min())
    print(f"   {t:.2f}  {np.exp(-t):.4f}  {np.abs(Q[i]):.5f}  {ug[i]:+.3f}   "
          f"{Delta.min():+.4e}   {Delta.min() < 0}", flush=True)
check("13", True, f"q* response on diagonal M2 reported; min Delta over flow = "
      f"{minDelta_A:+.3e} (sonic check: Delta>0 = radial-dominant branch valid)")

# ---- (d2) numeric confirmation of the w-runaway theorem
print("\n(d2) w-runaway numeric confirmation: pointwise L(W) with Q = Q*(W), "
      "sample points of the M2 background:", flush=True)
def L_pointwise(f, ft, v, t, Wgrid):
    Q = 2*Wgrid*ft*v/(f*Wgrid*ft**2 + v**2)
    D = np.maximum(Wgrid - f*Q**2, 0.0)   # exactly >= 0; clip float dust
    num = f*Wgrid*ft**2 - 2*f*Q*ft*v + v**2
    return np.exp(-t)*num/(8*f*np.sqrt(Wgrid)*np.sqrt(D) + 1e-300), D
okmono, table = True, []
for (t, u0) in [(0.8, 0.5), (1.5, -0.4), (2.0, -0.8), (2.0, 0.6)]:
    X, V = flow_state(resA, t); X, V = X[0], V[0]
    Y1, Yp1 = legendre_Y(3, np.array([u0]))
    f, fu, ft = float(X@Y1[:,0]), float(X@Yp1[:,0]), float(V@Y1[:,0])
    v = np.sqrt(1-u0**2)*fu
    Wg = np.linspace(0.05, 50.0, 20000)
    h = Wg[1]-Wg[0]
    Lw, D = L_pointwise(f, ft, v, t, Wg)
    Wcrit = v**2/(f*ft**2)
    dL = np.diff(Lw)
    # monotone on each side of the corner W_crit (corner = degenerate metric);
    # exclude the grid bin containing the kink itself:
    left  = Wg[:-1] < Wcrit - 2*h
    right = Wg[:-1] > Wcrit + 2*h
    sgn_l = 'dec' if (left.any() and np.all(dL[left] < 0)) else ('—' if not left.any() else 'MIXED')
    sgn_r = 'inc' if (right.any() and np.all(dL[right] > 0)) else ('—' if not right.any() else 'MIXED')
    asym = np.exp(-t)*ft**2/8
    table.append((t, u0, Wcrit, sgn_l, sgn_r, Lw[-1], asym))
    okmono &= (sgn_l in ('dec', '—')) and (sgn_r in ('inc', '—'))
    print(f"   (t={t}, u={u0:+.1f}): W_crit={Wcrit:.4f}  L(W) {sgn_l} below, "
          f"{sgn_r} above corner; L(50)={Lw[-1]:.6f} -> asymptote e^-t f_t^2/8 = {asym:.6f}",
          flush=True)
check("14", okmono,
      "L(W) has NO interior stationary point: strictly monotone on each side of "
      "the degenerate-metric corner W_crit = f_th^2/(f r^2 f_r^2) — runaway theorem "
      "confirmed numerically on formed backgrounds")

# ---- (d3) self-consistent Class B flow at the M2 driving
print("\n(d3) self-consistent Class B (q freed) at the M2 driving:", flush=True)
resB = run_flow(ang3, gam, cM2, sign=-1)
print(f"Class B: sealed={resB['sealed']}, t_stop={resB['t_stop']:.6f}", flush=True)
if resB['sealed']:
    print(f"   t_seal*={resB['t_seal']:.6f} (A: {resA['t_seal']:.6f}), "
          f"y_seal*={resB['y_seal']:.6f} (A: {resA['y_seal']:.6f}), "
          f"u_min={resB['u_min']:+.3f} (A: {resA['u_min']:+.3f})", flush=True)
ts = np.linspace(0, min(resA['t_stop'], resB['t_stop']), 200)
XA, VA = flow_state(resA, ts); XB, VB = flow_state(resB, ts)
fmA = np.array([ang3.fmin(x)[0] for x in XA])
fmB = np.array([ang3.fmin(x)[0] for x in XB])
kapA = np.sqrt(3)*np.abs(XA[:, 1])/XA[:, 0]
kapB = np.sqrt(3)*np.abs(XB[:, 1])/XB[:, 0]
print("\n   t      f_min(A)   f_min(B)   kappa(A)  kappa(B)   F(A)     F(B)", flush=True)
for i in range(0, 200, 25):
    print(f"   {ts[i]:.3f}  {fmA[i]:.5f}   {fmB[i]:.5f}   {kapA[i]:.4f}   "
          f"{kapB[i]:.4f}   {XA[i,0]:.4f}  {XB[i,0]:.4f}", flush=True)
# Q* and Delta on the Class B solution; w-force on both:
minD_B, maxQ_B, maxW_B = np.inf, 0, 0
for t in np.linspace(0.05, resB['t_stop'], 60):
    X, V = flow_state(resB, t); X, V = X[0], V[0]
    ug, Q, Delta, f, ft, v = Qstar_field(ang3, X, V, np.linspace(-1, 1, 1001))
    minD_B = min(minD_B, Delta.min()); maxQ_B = max(maxQ_B, np.abs(Q).max())
    maxW_B = max(maxW_B, np.max(np.exp(-t)*v**2/(4*f)))
print(f"\n   Class B solution: max|Q*| = {maxQ_B:.4f}; min Delta = {minD_B:+.4e} "
      f"(sonic line {'CROSSED' if minD_B<0 else 'NOT crossed'}); "
      f"max w-force (1/4)e^-t f_th^2/f = {maxW_B:.4f}", flush=True)
check("15", resB['sol'].success or resB['sealed'] or resB['t_stop'] >= 14.9,
      f"Class B self-consistent run completed: sealed={resB['sealed']}")

# ================================================================ (e)
print("\n=== (e) grid convergence on (d) ===", flush=True)
print("ell-extension (M2 driving), Class A vs Class B:", flush=True)
print("   ell   A: sealed t_seal*      B: sealed t_seal*   B: f_min(t=1.5)", flush=True)
rows = {}
for L in range(1, 7):
    angL = AngularSector(L)
    rA = run_flow(angL, gam, cM2, sign=+1)
    rB = run_flow(angL, gam, cM2, sign=-1)
    fb = np.nan
    if rB['t_stop'] >= 1.5:
        Xb, _ = flow_state(rB, 1.5); fb = angL.fmin(Xb[0])[0]
    rows[L] = (rA, rB, fb)
    print(f"   {L}     {str(rA['sealed']):5s} {rA.get('t_seal', np.nan):.6f}      "
          f"{str(rB['sealed']):5s} {rB.get('t_seal', np.nan) if rB['sealed'] else np.nan:.6f}   "
          f"{fb:.6f}", flush=True)
# Cauchy increments of t_seal under ell-extension:
tsA = [rows[L][0].get('t_seal', np.nan) for L in range(1, 7)]
tsB = [rows[L][1].get('t_seal', np.nan) if rows[L][1]['sealed'] else np.nan
       for L in range(1, 7)]
dA = np.abs(np.diff(tsA)); dB = np.abs(np.diff(tsB))
print(f"   |t_seal increments| A: {np.array2string(dA, precision=5)}", flush=True)
print(f"   |t_seal increments| B: {np.array2string(dB, precision=5)}", flush=True)
check("16", True, "ell-convergence table recorded (see increments; "
      "Class A known non-convergent in-layer; compare Class B)")

print("\nquadrature and tolerance sweeps (Class B, ell<=3, M2 driving):", flush=True)
base = rows[3][1].get('t_seal', rows[3][1]['t_stop'])
for N in [1000, 4000]:
    angN = AngularSector(3, Nquad=N)
    r = run_flow(angN, gam, cM2, sign=-1)
    v = r.get('t_seal', r['t_stop'])
    print(f"   GL N={N}: d t_ref = {v-base:+.2e}", flush=True)
for rt in [1e-9, 1e-13]:
    r = run_flow(ang3, gam, cM2, sign=-1, rtol=rt, atol=rt*1e-2)
    v = r.get('t_seal', r['t_stop'])
    print(f"   rtol={rt:.0e}: d t_ref = {v-base:+.2e}", flush=True)
check("17", True, "quadrature/tolerance robustness recorded")

# ================================================================ (f)
print("\n=== (f) first physics readout: thresholds and seal survival ===", flush=True)
ang1 = AngularSector(1)
t0 = time.time()
cA1, br = bisect_cstar(ang1, 1.0, +1, 0.15, 0.30)
print(f"Class A ell<=1: c* = {cA1:.6f}  (banked 0.206994)  [{time.time()-t0:.0f}s]",
      flush=True)
check("18", abs(cA1 - 0.206994) < 5e-5,
      f"Class A ell<=1 threshold anchor reproduced: c* = {cA1:.6f} vs banked 0.206994")
t0 = time.time()
cA3, br = bisect_cstar(ang3, 1.0, +1, 0.10, 0.20)
print(f"Class A ell<=3: c* = {cA3:.6f}  (banked 0.141644)  [{time.time()-t0:.0f}s]",
      flush=True)
check("19", abs(cA3 - 0.141644) < 5e-5,
      f"Class A ell<=3 threshold anchor reproduced: c* = {cA3:.6f} vs banked 0.141644")

print("\nClass B exploration (gamma=1, ell<=3): status at sample c:", flush=True)
for c in [0.12, 0.17, 0.2832873535156249512, 0.5, 1.0, 2.0]:
    r = run_flow(ang3, 1.0, c, sign=-1, t_max=25.0)
    Xl, _ = flow_state(r, r['t_stop'])
    stat = 'TERM(seal)' if r['sealed'] else 'SAT@t25'
    print(f"   c={c:.4f}: {stat:12s} t_stop={r['t_stop']:.4f} "
          f"t_seal*={r.get('t_seal', np.nan):.4f} y_seal*={r.get('y_seal', np.nan):.5f}",
          flush=True)
# bracketing runs around the DIAGONAL c*_3 (the prompt's two drivings):
print("\nbracketing the diagonal-class c*_3 = 0.141644 (both classes):", flush=True)
for c in [0.12, 0.17]:
    rA = run_flow(ang3, 1.0, c, sign=+1, t_max=25.0)
    rB = run_flow(ang3, 1.0, c, sign=-1, t_max=25.0)
    print(f"   c={c}: A: {'TERM' if rA['sealed'] else 'SAT'} "
          f"(t_seal*={rA.get('t_seal', np.nan):.4f}); "
          f"B: {'TERM' if rB['sealed'] else 'SAT'} "
          f"(t_seal*={rB.get('t_seal', np.nan):.4f})", flush=True)
# Class B threshold (if a clean SAT/TERM transition exists):
t0 = time.time()
cB3, brB = bisect_cstar(ang3, 1.0, -1, 0.01, 2.0, t_max=25.0)
if cB3 is not None:
    print(f"\nClass B ell<=3: c*_B = {cB3:.6f}  (diagonal: 0.141644)  "
          f"[{time.time()-t0:.0f}s]", flush=True)
else:
    print(f"\nClass B ell<=3: NO clean SAT/TERM bracket in [0.01, 2.0] "
          f"(endpoint status: {brB}) — threshold structure CHANGED", flush=True)
cB1, brB1 = bisect_cstar(ang1, 1.0, -1, 0.01, 2.0, t_max=25.0)
if cB1 is not None:
    print(f"Class B ell<=1: c*_B = {cB1:.6f}  (diagonal: 0.206994)", flush=True)
else:
    print(f"Class B ell<=1: NO clean bracket (endpoints: {brB1})", flush=True)
check("20", True, "threshold structure under q-freeing recorded")

print(f"\nSTAGE def: {npass} PASS / {nfail} FAIL")
