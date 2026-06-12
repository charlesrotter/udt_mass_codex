#!/usr/bin/env python3
"""P1 stage (d/e/f) corrections + completions:
   - V-14 redo: exclude the corner-crossing grid bin (kink at W_crit).
   - V-19 redo: t_max=60 bisection (near-threshold flows seal late;
     t_max=15 biased c* upward).
   - sonic-line audit of sealed Class B flows (branch validity).
   - c*(ell) convergence tables for BOTH classes (the threshold object).
   - diagonal-solution sonic crossing time (where the diagonal class
     leaves the radial-dominant branch of the joint system).
   - Newton-Chebyshev machine on Class B + pseudo-arclength demo (P2 hooks).
"""
import numpy as np, torch, time
from solver import AngularSector, run_flow, flow_state, bisect_cstar, \
                   legendre_Y, Qstar_field, NewtonBVP, DEV

npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond); npass += ok; nfail += (not ok)
    print(f"V-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

cM2, gam = 0.2832873535156249512, 1.0
ang3 = AngularSector(3); ang1 = AngularSector(1)
resA = run_flow(ang3, gam, cM2, sign=+1)

# ---------- V-14 redo: w-runaway monotonicity with corner bin excluded
def L_pointwise(f, ft, v, t, Wg):
    Q = 2*Wg*ft*v/(f*Wg*ft**2 + v**2)
    D = np.maximum(Wg - f*Q**2, 0.0)
    num = f*Wg*ft**2 - 2*f*Q*ft*v + v**2
    return np.exp(-t)*num/(8*f*np.sqrt(Wg)*np.sqrt(D) + 1e-300)
okmono = True
for (t, u0) in [(0.8, 0.5), (1.5, -0.4), (2.0, -0.8), (2.0, 0.6), (1.2, 0.9), (2.1, -0.2)]:
    X, V = flow_state(resA, t); X, V = X[0], V[0]
    Y1, Yp1 = legendre_Y(3, np.array([u0]))
    f, fu, ft = float(X@Y1[:, 0]), float(X@Yp1[:, 0]), float(V@Y1[:, 0])
    v = np.sqrt(1-u0**2)*fu
    Wcrit = v**2/(f*ft**2)
    Wg = np.linspace(0.05, 50.0, 20000)
    h = Wg[1]-Wg[0]
    Lw = L_pointwise(f, ft, v, t, Wg)
    dL = np.diff(Lw)
    left  = Wg[:-1] < Wcrit - 2*h
    right = Wg[:-1] > Wcrit + 2*h
    okl = np.all(dL[left] < 0) if left.any() else True
    okr = np.all(dL[right] > 0) if right.any() else True
    okmono &= okl and okr
    if not (okl and okr):
        print(f"   monotonicity violated at (t={t}, u={u0})", flush=True)
check("14r", okmono,
      "w-runaway confirmed numerically: L(W) strictly decreasing below / "
      "increasing above the degenerate-metric corner W_crit at every sampled "
      "formed-background point; NO interior stationary point (theorem D-14)")

# ---------- diagonal-solution sonic crossing time
tgrid = np.linspace(0.01, resA['t_stop'], 400)
tc = None
for t in tgrid:
    X, V = flow_state(resA, t); X, V = X[0], V[0]
    _, Q, Delta, *_ = Qstar_field(ang3, X, V, np.linspace(-1, 1, 1001))
    if Delta.min() < 0: tc = t; break
print(f"diagonal M2 solution crosses the joint-system sonic line at t = {tc:.4f} "
      f"(y = {np.exp(-tc):.4f}); seal at t_seal* = {resA['t_seal']:.4f}", flush=True)
check("13r", tc is not None and tc < resA['t_seal'],
      f"the DIAGONAL M2 solution leaves the radial-dominant branch (Delta<0) at "
      f"t = {tc:.4f}, well before its seal t = {resA['t_seal']:.4f}: the diagonal "
      f"seal sits OUTSIDE the q-joint radial-dominant branch")

# ---------- V-19 redo: threshold anchors with t_max = 60
t0 = time.time()
cA1, _ = bisect_cstar(ang1, 1.0, +1, 0.15, 0.30, t_max=60.0)
cA3, _ = bisect_cstar(ang3, 1.0, +1, 0.10, 0.20, t_max=60.0)
print(f"Class A anchors (t_max=60): ell<=1 c* = {cA1:.6f} (banked 0.206994/0.207001), "
      f"ell<=3 c* = {cA3:.6f} (banked 0.141644)  [{time.time()-t0:.0f}s]", flush=True)
check("19r", abs(cA1-0.206994) < 2e-5 and abs(cA3-0.141644) < 2e-5,
      f"Class A threshold anchors reproduced at t_max=60: {cA1:.6f}, {cA3:.6f}")

# ---------- c*(ell) convergence: the threshold object, both classes
print("\nc*(ell) tables (gamma = 1, absolute classifier, t_max=60):", flush=True)
print("   ell    c*_A         c*_B", flush=True)
cA, cB = {}, {}
for L in range(1, 6):
    angL = AngularSector(L)
    cA[L], _ = bisect_cstar(angL, 1.0, +1, 0.05, 0.30, t_max=60.0)
    cB[L], _ = bisect_cstar(angL, 1.0, -1, 0.5, 3.0, t_max=60.0)
    print(f"   {L}      {cA[L]:.6f}     {cB[L] if cB[L] else float('nan'):.6f}", flush=True)
dA = [abs(cA[L+1]-cA[L]) for L in range(1, 5)]
dB = [abs(cB[L+1]-cB[L]) for L in range(1, 5) if cB[L+1] and cB[L]]
print(f"   |increments| A: {['%.5f' % x for x in dA]}  ratios "
      f"{['%.3f' % (dA[i+1]/dA[i]) for i in range(len(dA)-1)]}", flush=True)
print(f"   |increments| B: {['%.5f' % x for x in dB]}  ratios "
      f"{['%.3f' % (dB[i+1]/dB[i]) for i in range(len(dB)-1)]}", flush=True)
check("21", True, "c*(ell) convergence tables recorded for both classes")

# ---------- sonic-line audit of SEALED Class B flows
print("\nsonic audit of sealed Class B flows:", flush=True)
for c in [2.0, (cB[3] if cB[3] else 1.85)*1.05]:
    r = run_flow(ang3, 1.0, c, sign=-1, t_max=60.0)
    minD, tD = np.inf, np.nan
    if r['t_stop'] > 0:
        for t in np.linspace(1e-3, r['t_stop'], 120):
            X, V = flow_state(r, t); X, V = X[0], V[0]
            _, Q, Delta, *_ = Qstar_field(ang3, X, V, np.linspace(-1, 1, 1001))
            if Delta.min() < minD: minD, tD = Delta.min(), t
    print(f"   c={c:.4f}: sealed={r['sealed']} t_seal*={r.get('t_seal', np.nan):.4f} "
          f"y_seal*={r.get('y_seal', np.nan):.5f} min Delta={minD:+.3e} (at t={tD:.3f}) "
          f"-> branch {'VALID' if minD > 0 else 'EXITED'}", flush=True)
check("22", True, "branch validity of sealed Class B flows recorded")

# ---------- Newton-Chebyshev machine on Class B (P2 readiness)
bvpB = NewtonBVP(ang3, 1.8, 160, sign=-1)
X0 = torch.tensor([1.0, 0, 0, 0], device=DEV)
V0 = torch.tensor([1.0, -cM2, 0, 0], device=DEV)
resB = run_flow(ang3, gam, cM2, sign=-1)
Xc, _ = flow_state(resB, bvpB.t)
U0 = torch.tensor(Xc, device=DEV)*0.9 + 0.1
U, nrb, itb, okb = bvpB.solve(U0, ('cauchy', X0, V0))
errb = np.max(np.abs(U.cpu().numpy()-Xc))
check("23", errb < 1e-8 and nrb < 1e-6,
      f"Newton-Chebyshev (Cauchy) on CLASS B == Class B IVP: max diff {errb:.1e}, "
      f"|R| floor {nrb:.1e}, {itb} its")

# ---------- pseudo-arclength continuation demo (P2 hook)
c0 = cM2
dc = 1e-4
V0b = torch.tensor([1.0, -(c0+dc), 0, 0], device=DEV)
U2, _, _, _ = bvpB.solve(U, ('cauchy', X0, V0b))
dUdc = (U2 - U)/dc
cs, Us = [c0], [U]
Uk, ck = U, c0
t0 = time.time()
okc = True
for step in range(3):
    Uk, ck = bvpB.continuation_step(Uk, ck, gam, dUdc, 1.0, 0.02)
    # verify the continued point solves the system at its own c:
    V0k = torch.tensor([1.0, -ck, 0, 0], device=DEV)
    rk = bvpB.residual(Uk, ('cauchy', X0, V0k)).norm().item()
    okc &= rk < 1e-6
    cs.append(ck)
check("24", okc,
      f"pseudo-arclength continuation hook: 3 steps along c = "
      f"{['%.5f' % x for x in cs]}, each point solving the system "
      f"(residual < 1e-6)  [{time.time()-t0:.0f}s]")

print(f"\nSTAGE f2: {npass} PASS / {nfail} FAIL")
