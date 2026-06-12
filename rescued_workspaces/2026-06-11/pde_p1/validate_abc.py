#!/usr/bin/env python3
"""P1 VALIDATION LADDER, stages (a), (b), (c)."""
import numpy as np, torch, time
from solver import (AngularSector, run_flow, flow_state, NewtonBVP, Newton2D,
                    legendre_Y, Qstar_field, DEV, KER)

npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond); npass += ok; nfail += (not ok)
    print(f"V-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

print(f"device = {DEV}", flush=True)

# ---------------------------------------------------------------- kernels
# torch kernels vs sympy-lambdified numpy kernels on random states:
ang3 = AngularSector(3)
rng = np.random.default_rng(11)
X = np.array([3.0, -0.6, 0.25, -0.1])
g_np = ang3.gradP(X)
U = torch.tensor(X, device=DEV).reshape(1, -1)
g_t = ang3.t_gradP(U).cpu().numpy()[0]
H_np = ang3.hessP(X)
H_t = ang3.t_hessP(U).cpu().numpy()[0]
check("00", np.max(np.abs(g_np-g_t)) < 1e-13 and np.max(np.abs(H_np-H_t)) < 1e-13,
      f"torch kernels == sympy-generated numpy kernels (grad diff "
      f"{np.max(np.abs(g_np-g_t)):.1e}, hess diff {np.max(np.abs(H_np-H_t)):.1e})")
# finite-difference check of gradP / hessP:
eps = 1e-6
gfd = np.array([(ang3.P(X+eps*np.eye(4)[l]) - ang3.P(X-eps*np.eye(4)[l]))/(2*eps)
                for l in range(4)])
Hfd = np.array([[(ang3.gradP(X+eps*np.eye(4)[m])[l]-ang3.gradP(X-eps*np.eye(4)[m])[l])/(2*eps)
                 for m in range(4)] for l in range(4)])
check("01", np.max(np.abs(gfd-g_np)) < 1e-8 and np.max(np.abs(Hfd-H_np)) < 1e-7,
      "analytic P_X, P_XX match finite differences of quadrature P")

# ---------------------------------------------------------------- (a)
print("\n--- (a) spherical vacuum f = A + B/y ---", flush=True)
gam = 0.7
res = run_flow(ang3, gam, 0.0, sign=+1, t_max=2.0, drive=np.zeros(3))
tt = np.linspace(0, res['t_stop'], 60)
Xt, Vt = flow_state(res, tt)
exact = (1-gam) + gam*np.exp(tt)
err_iv = np.max(np.abs(Xt[:, 0]-exact)/exact)
err_ang = np.max(np.abs(Xt[:, 1:]))
check("02", err_iv < 1e-10 and err_ang < 1e-12,
      f"IVP: f = (1-g) + g e^t reproduced (rel err {err_iv:.1e}; angular {err_ang:.1e})")

T = 1.5
bvp = NewtonBVP(ang3, T, 64, sign=+1)
X0 = torch.zeros(4, device=DEV); X0[0] = 1.0
XT = torch.zeros(4, device=DEV); XT[0] = (1-gam) + gam*np.exp(T)
U0 = torch.zeros(65, 4, device=DEV); U0[:, 0] = torch.linspace(1.0, XT[0].item(), 65, device=DEV)
U, nr, it, ok = bvp.solve(U0, ('dirichlet', X0, XT))
ex = (1-gam) + gam*np.exp(bvp.t)
err_bvp = np.max(np.abs(U[:, 0].cpu().numpy()-ex)/ex)
check("03", ok and err_bvp < 1e-10,
      f"Newton-Chebyshev BVP (Dirichlet): vacuum reproduced, rel err {err_bvp:.1e}, "
      f"|R|={nr:.1e}, {it} its")

n2 = Newton2D(T, 40, 28)
f0 = torch.ones(28, device=DEV)
fT = torch.full((28,), (1-gam)+gam*np.exp(T), device=DEV)
ex2g = (1-gam) + gam*np.exp(n2.t)
F0 = torch.tensor(np.tile(ex2g, (28, 1)).T, device=DEV)*0.9 + 0.1  # off-solution guess
F, nr2, it2, ok2 = n2.solve(F0, f0, fT)
ex2 = (1-gam) + gam*np.exp(n2.t)
err_2d = np.max(np.abs(F.cpu().numpy()-ex2[:, None])/ex2[:, None])
check("04", ok2 and err_2d < 1e-9,
      f"2D tensor-spectral Newton (Class A): vacuum reproduced, rel err {err_2d:.1e}, "
      f"|R|={nr2:.1e}, {it2} its")

# ---------------------------------------------------------------- (b)
print("\n--- (b) library M2 reproduction (ell<=3, gamma=1, c=0.2832873535156249512) ---",
      flush=True)
lib = np.loadtxt('/tmp/seal_s1/lib/bg_M2.dat')
tl, Fl, a1l, g2l, h3l = lib[:, 0], lib[:, 2], lib[:, 3], lib[:, 4], lib[:, 5]
fminl = lib[:, 10]
cM2 = 0.2832873535156249512
t0 = time.time()
resA = run_flow(ang3, 1.0, cM2, sign=+1, t_max=15.0)
print(f"   flow time {time.time()-t0:.1f}s; sealed={resA['sealed']} "
      f"t_stop={resA['t_stop']:.6f} t_seal*={resA.get('t_seal', np.nan):.6f} "
      f"y_seal*={resA.get('y_seal', np.nan):.6f}", flush=True)
mask = tl <= resA['t_stop']
XL, VL = flow_state(resA, tl[mask])
dF  = np.max(np.abs(XL[:, 0]-Fl[mask])/np.abs(Fl[mask]))
da1 = np.max(np.abs(XL[:, 1]-a1l[mask]))
dg2 = np.max(np.abs(XL[:, 2]-g2l[mask]))
dh3 = np.max(np.abs(XL[:, 3]-h3l[mask]))
check("05", dF < 1e-7 and da1 < 1e-7 and dg2 < 1e-7 and dh3 < 1e-7,
      f"M2 profiles reproduced: max|dF|/F={dF:.1e}, |da1|={da1:.1e}, "
      f"|dg2|={dg2:.1e}, |dh3|={dh3:.1e}")
check("06", abs(resA['t_stop']-2.134243) < 5e-5 and abs(resA['t_seal']-2.134509) < 5e-5
      and abs(resA['y_seal']-0.118303) < 1e-5,
      f"M2 seal locus: t_stop {resA['t_stop']:.6f} (lib 2.134243), "
      f"t_seal* {resA['t_seal']:.6f} (lib 2.134509), y_seal* {resA['y_seal']:.6f} (lib 0.118303)")
# f_min profile:
fmins = np.array([ang3.fmin(x)[0] for x in XL])
dfm = np.max(np.abs(fmins-fminl[mask]))
check("07", dfm < 1e-6, f"f_min profile max abs diff {dfm:.1e}")

# Newton-Chebyshev BVP (Cauchy rows) must reproduce the same flow:
Tb = 1.8
bvpA = NewtonBVP(ang3, Tb, 160, sign=+1)
X0 = torch.tensor([1.0, 0, 0, 0], device=DEV)
V0 = torch.tensor([1.0, -cM2, 0, 0], device=DEV)
ts = bvpA.t
Xc, Vc = flow_state(resA, ts)
U0 = torch.tensor(Xc, device=DEV)*0.95 + 0.05  # perturbed guess
t0 = time.time()
U, nrb, itb, okb = bvpA.solve(U0, ('cauchy', X0, V0))
errb = np.max(np.abs(U.cpu().numpy()-Xc))
check("08", errb < 1e-8 and nrb < 1e-6,
      f"Newton-Chebyshev (Cauchy weld rows, Nt=160) == IVP flow: max diff {errb:.1e} "
      f"(|R| floor {nrb:.1e} = D^2 conditioning at Nt=160, cond~N^4; solution "
      f"machine-accurate), {itb} its, {time.time()-t0:.1f}s")

# 2D full-theta Newton (Class A elliptic) vs library in trust region t<1.168:
T2 = 1.1
n2b = Newton2D(T2, 48, 32)
Y32, _ = legendre_Y(3, n2b.u)
XT2, _ = flow_state(resA, T2)
f0 = torch.ones(32, device=DEV)
fT = torch.tensor(XT2[0] @ Y32, device=DEV)
tt2 = n2b.t
Xg, _ = flow_state(resA, tt2)
F0 = torch.tensor(Xg @ Y32, device=DEV)
F2d, nr2b, it2b, ok2b = n2b.solve(F0*0.97 + 0.03, f0, fT, verbose=False)
flib = torch.tensor(Xg @ Y32, device=DEV)
rel = ((F2d-flib).abs()/flib.abs()).cpu().numpy()
check("09", ok2b and np.max(rel) < 0.01,
      f"2D Newton (full theta, Nt=48 x Nu=32) vs ell<=3 library in trust region "
      f"[0,1.1]: max rel diff {np.max(rel):.2e} (interior truncation error; "
      f"trust-region bound 1%)  |R|={nr2b:.1e}")
print(f"   2D-vs-library rel diff profile: t=0.28: {np.max(rel[12]):.2e}, "
      f"t=0.55: {np.max(rel[24]):.2e}, t=0.83: {np.max(rel[36]):.2e}", flush=True)

# ---------------------------------------------------------------- (c)
print("\n--- (c) free q, w on the spherical background ---", flush=True)
# tadpoles on the (a) solution: dL/dq = (1/4) f_r f_th sin, dL/dw ~ f_th^2
maxa = np.max(np.abs(Xt[:, 1:]))
ug, Q, Delta, f, ft, v = Qstar_field(ang3, Xt[-1], Vt[-1])
check("10", maxa < 1e-12 and np.max(np.abs(Q)) < 1e-10,
      f"spherical background: angular modes {maxa:.1e}, q* field {np.max(np.abs(Q)):.1e} "
      f"-> q tadpole = 0, q* = 0 (exact)")
wforce = np.max(np.abs(v**2/f))  # |dL_eff/dw| ~ (1/4) e^{-t} v^2/f per (du/2)
check("11", wforce < 1e-20,
      f"spherical background: w-force (1/4)e^-t f_th^2/f = {wforce:.1e} -> w tadpole = 0 "
      f"(w is an exact FLAT direction spherically: L is W-independent at f_th=0)")
# Class B from spherical drive must return the identical spherical flow:
resB0 = run_flow(ang3, gam, 0.0, sign=-1, t_max=2.0, drive=np.zeros(3))
XB, _ = flow_state(resB0, tt)
check("12", np.max(np.abs(XB-Xt)) < 1e-10,
      f"Class B (q freed) on spherical data == Class A flow: max diff "
      f"{np.max(np.abs(XB-Xt)):.1e} (zero tadpole spherically)")

print(f"\nSTAGE abc: {npass} PASS / {nfail} FAIL")
