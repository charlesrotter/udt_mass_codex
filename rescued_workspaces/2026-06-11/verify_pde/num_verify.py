#!/usr/bin/env python3
"""BLIND ADVERSARIAL VERIFIER — numeric checks (V3 numeric, V4, V5, V6)."""
import numpy as np, time
from flowlib import Ang, legY, flow, state, bisect_cstar, fv_classB

npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond); npass += ok; nfail += (not ok)
    print(f"VN-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

cM2 = 0.2832873535156249512
ang1, ang3 = Ang(1), Ang(3)

# ================= V6: M2 library reproduction ===========================
lib = np.loadtxt('/tmp/seal_s1/lib/bg_M2.dat')
tl = lib[:, 0]
t0 = time.time()
rA = flow(ang3, 1.0, cM2, +1, t_max=15.0)
mask = tl <= rA['t_stop']
XL, VL = state(rA, tl[mask])
dF = np.max(np.abs(XL[:, 0] - lib[mask, 2])/np.abs(lib[mask, 2]))
dmodes = max(np.max(np.abs(XL[:, j] - lib[mask, 2 + j])) for j in (1, 2, 3))
check("6-lib", dF < 1e-10 and dmodes < 1e-10,
      f"M2 library reproduced by MY integrator (N=3000, own code): max|dF|/F={dF:.1e}, "
      f"max mode diff={dmodes:.1e}; seal t_stop={rA['t_stop']:.6f} (lib 2.134243), "
      f"t_seal*={rA['t_seal']:.6f} (lib 2.134509), y_seal*={rA['y_seal']:.6f} (lib 0.118303) "
      f"[{time.time()-t0:.1f}s]")
check("6-seal", abs(rA['t_stop'] - 2.134243) < 2e-5 and
      abs(rA['t_seal'] - 2.134509) < 2e-5 and abs(rA['y_seal'] - 0.118303) < 5e-6,
      "M2 seal locus matches library numbers")

# ================= V5: sonic crossing of the diagonal M2 =================
# Delta = f f_t^2 - (1-u^2) f_u^2 on a dense u grid; first t with min_u Delta < 0.
ud = np.linspace(-1, 1, 4001)
Y4, _ = legY(3, ud), None
# derivative matrix on dense grid via recursion:
P = Y4/np.sqrt(2*np.arange(4) + 1)[:, None]
Pp = np.zeros_like(P)
for l in range(1, 4):
    Pp[l] = l*(P[l-1] - ud*P[l])/np.where(np.abs(1 - ud**2) > 1e-14, 1 - ud**2, 1)
Pp[:, 0] = 0; Pp[:, -1] = 0   # v = sqrt(1-u^2) f_u -> 0 at poles anyway
Yp4 = np.sqrt(2*np.arange(4) + 1)[:, None]*Pp

def minDelta(t, res):
    X, V = state(res, t); X, V = X[0], V[0]
    f, fu, ft = X @ Y4, X @ Yp4, V @ Y4
    v2 = (1 - ud**2)*fu**2
    return np.min(f*ft**2 - v2)

ts = np.linspace(0.01, rA['t_stop'], 800)
md = np.array([minDelta(t, rA) for t in ts])
icross = np.argmax(md < 0)
# refine by bisection:
lo, hi = ts[icross - 1], ts[icross]
for _ in range(60):
    mid = 0.5*(lo + hi)
    if minDelta(mid, rA) < 0: hi = mid
    else: lo = mid
t_sonic = 0.5*(lo + hi)
check("5-sonic", abs(t_sonic - 1.256) < 2e-3,
      f"diagonal M2 crosses the joint-system sonic line (min_u Delta = 0) at "
      f"t = {t_sonic:.4f} (P1: 1.2558 / claim 1.256), BEFORE its seal at "
      f"{rA['t_seal']:.4f} (claim 2.135)")
# same readout directly from the LIBRARY file columns (background-data route):
Fb, a1b, g2b, h3b = lib[:, 2], lib[:, 3], lib[:, 4], lib[:, 5]
Ftb, a1tb, g2tb, h3tb = lib[:, 6], lib[:, 7], lib[:, 8], lib[:, 9]
Xb = lib[:, 2:6]; Vb = lib[:, 6:10]
mdlib = np.array([np.min((X @ Y4)*(V @ Y4)**2 - (1 - ud**2)*(X @ Yp4)**2)
                  for X, V in zip(Xb, Vb)])
i2 = np.argmax(mdlib < 0)
t_sonic_lib = np.interp(0.0, [-mdlib[i2 - 1], -mdlib[i2]], [tl[i2 - 1], tl[i2]])
check("5-sonic-lib", abs(t_sonic_lib - t_sonic) < 5e-3,
      f"same crossing from the library FILE alone: t = {t_sonic_lib:.4f}")

# ================= V3 numeric: L(W) scan on the formed background ========
# L_2D(W; Q=Q*(W)) ~ e^{-t} [f W f_t^2 - 2 f Q f_t v + v^2]/(8 f sqrt(W) sqrt(W - f Q^2))
def LW_scan(t, u0):
    X, V = state(rA, t); X, V = X[0], V[0]
    Yl = legY(3, np.array([u0]))
    Pl = Yl/np.sqrt(2*np.arange(4) + 1)[:, None]
    Ppl = np.zeros_like(Pl)
    for l in range(1, 4):
        Ppl[l] = l*(Pl[l-1] - u0*Pl[l])/(1 - u0**2)
    Ypl = np.sqrt(2*np.arange(4) + 1)[:, None]*Ppl
    f, fu, ft = float(X @ Yl[:, 0]), float(X @ Ypl[:, 0]), float(V @ Yl[:, 0])
    v = np.sqrt(1 - u0**2)*fu
    W = np.geomspace(1e-3, 1e3, 200001)
    Q = 2*W*ft*v/(f*W*ft**2 + v**2)
    D = np.maximum(W - f*Q**2, 0.0)
    num = f*W*ft**2 - 2*f*Q*ft*v + v**2
    L = np.exp(-t)*num/(8*f*np.sqrt(W)*np.sqrt(D) + 1e-300)
    Wcrit = v**2/(f*ft**2)
    # eliminated closed form for cross-check:
    Lcf = np.exp(-t)*np.abs(f*ft**2 - v**2/W)/(8*f)
    return W, L, Lcf, Wcrit, f, ft, v

okm, okcf = True, True
for (t, u0) in [(0.8, 0.5), (1.5, -0.4), (2.0, -0.8), (2.0, 0.6), (0.3, 0.9), (1.0, -0.95)]:
    W, L, Lcf, Wcrit, f, ft, v = LW_scan(t, u0)
    okcf &= np.max(np.abs(L - Lcf))/np.max(np.abs(Lcf)) < 1e-9   # scale-relative
    # (pointwise-relative is meaningless AT the corner where L -> 0 exactly)
    dL = np.diff(L)
    below = W[:-1] < Wcrit*0.999
    above = W[:-1] > Wcrit*1.001
    okm &= np.all(dL[below] < 0) and np.all(dL[above] > 0)
    print(f"   (t={t}, u={u0:+.2f}): W_crit={Wcrit:.5f}; L dec on (0,Wc), inc on (Wc,oo): "
          f"{np.all(dL[below]<0)}/{np.all(dL[above]>0)}; L(corner)={np.interp(Wcrit,W,L):.2e} "
          f"(=0); asymptote={np.exp(-t)*ft**2/8:.6f}, L(W=1e3)={L[-1]:.6f}", flush=True)
check("3-mono", okm and okcf,
      "L(W) with Q=Q*(W) on the FORMED M2 background: strictly monotone each side of "
      "the degenerate corner W_crit at all 6 sample points (incl. near-pole u=-0.95); "
      "matches eliminated closed form |Delta|/(8f) e^{-t} to 1e-8: NO stationary point")

# ================= V4: Class B at M2 driving =============================
t0 = time.time()
rB = flow(ang3, 1.0, cM2, -1, t_max=60.0)
tt = np.linspace(0, min(rB['t_stop'], 60.0), 2401)
XB, VB = state(rB, tt)
kap = np.sqrt(3)*np.abs(XB[:, 1])/XB[:, 0]
imax = np.argmax(kap)
fmin_end = rB['ang'].fmin(XB[-1])[0]
kap135 = np.interp(1.35, tt, kap)
check("4-B-M2", (not rB['sealed']) and abs(kap[imax] - 0.258) < 2e-3
      and 1.25 < tt[imax] < 1.45 and abs(kap135 - 0.2577) < 5e-4,
      f"Class B at M2 driving: NO SEAL to t=60 (f_min(60)={fmin_end:.2e}); "
      f"kappa peaks at {kap[imax]:.4f} at t={tt[imax]:.3f} (true argmax 1.304; "
      f"kappa(1.35)={kap135:.4f} = P1's quoted 0.2577 — flat peak, claim 'peaks "
      f"~0.258 near t~1.35' correct at stated precision), kappa(60)={kap[-1]:.4f} "
      f"(P1 0.1359)  [{time.time()-t0:.1f}s]")

# finite-volume cross-check (NO Galerkin, full PDE):
t0 = time.time()
solfv, mom = fv_classB(1.0, cM2, M=400, t_max=4.0)
tsf = np.linspace(0, 4, 401)
kfv = np.array([np.sqrt(3)*abs(mom(t)[1])/mom(t)[0] for t in tsf])
ifv = np.argmax(kfv)
# same diagnostic from the Galerkin flow:
kg = np.interp(tsf, tt, kap)
check("4-B-fv", abs(kfv[ifv] - kap[imax]) < 5e-3 and abs(tsf[ifv] - tt[imax]) < 0.06
      and np.max(np.abs(kfv - kg)) < 0.01,
      f"INDEPENDENT discretization (finite-volume MOL, M=400, no Galerkin): "
      f"kappa peak {kfv[ifv]:.4f} at t={tsf[ifv]:.2f}; max|kappa_fv - kappa_gal| "
      f"= {np.max(np.abs(kfv-kg)):.1e} on [0,4]  [{time.time()-t0:.1f}s]")

# ell-robustness of B no-seal:
ang5 = Ang(5)
rB5 = flow(ang5, 1.0, cM2, -1, t_max=60.0)
X5, _ = state(rB5, 60.0)
k5 = np.sqrt(3)*abs(X5[0][1])/X5[0][0]
check("4-B-ell", not rB5['sealed'] and abs(k5 - 0.1359) < 2e-3,
      f"ell<=5: Class B at M2 driving still NO SEAL to t=60, kappa_end={k5:.4f} (P1 0.1359)")

# ================= V6/V4: thresholds =====================================
t0 = time.time()
cA1, _ = bisect_cstar(ang1, 1.0, +1, 0.15, 0.30)
cA3, _ = bisect_cstar(ang3, 1.0, +1, 0.10, 0.20)
print(f"   c*_A(1) = {cA1:.6f} (banked 0.207001, P1 0.206995); "
      f"c*_A(3) = {cA3:.6f} (banked 0.141644, P1 0.141653)  [{time.time()-t0:.0f}s]", flush=True)
check("6-cA", abs(cA1 - 0.207001) < 1e-4 and abs(cA3 - 0.141644) < 1e-4,
      f"c*_A anchors reproduced within 1e-4: {cA1:.6f}, {cA3:.6f}")

t0 = time.time()
cB3, _ = bisect_cstar(ang3, 1.0, -1, 1.0, 2.5, tol=2e-5)
cB1, _ = bisect_cstar(ang1, 1.0, -1, 1.0, 2.5, tol=2e-5)
check("4-cB", abs(cB3 - 1.849) < 5e-3 and abs(cB1 - 1.3517) < 5e-3,
      f"c*_B(ell<=3, gamma=1) = {cB3:.6f} (P1 1.849203); c*_B(ell<=1) = {cB1:.6f} "
      f"(P1 1.351749)  [{time.time()-t0:.0f}s]")

# gamma scaling (ell<=1):
t0 = time.time()
out = {}
for gam, brA, brB in [(0.5, (0.03, 0.12), (0.5, 1.6)), (2.0, (0.3, 0.9), (1.2, 3.0))]:
    a, _ = bisect_cstar(ang1, gam, +1, *brA, tol=2e-5)
    b, _ = bisect_cstar(ang1, gam, -1, *brB, tol=2e-5)
    out[gam] = (a, b)
out[1.0] = (cA1, cB1)
print("   gamma:  c*_A        c*_A/g^2    c*_B       c*_B/g", flush=True)
for g in (0.5, 1.0, 2.0):
    a, b = out[g]
    print(f"   {g:.1f}    {a:.6f}   {a/g**2:.4f}     {b:.6f}   {b/g:.4f}", flush=True)
check("4-gam", abs(out[0.5][1] - 0.9965) < 5e-3 and abs(out[2.0][1] - 2.0192) < 5e-3
      and abs(out[0.5][0] - 0.069156) < 5e-4 and abs(out[2.0][0] - 0.568247) < 5e-4,
      f"gamma sweep reproduces P1: c*_B = {out[0.5][1]:.4f}/{out[1.0][1]:.4f}/"
      f"{out[2.0][1]:.4f} at gamma=0.5/1/2 (claim ~1.0/1.35/2.0)  [{time.time()-t0:.0f}s]")
rat = (out[0.5][0]/0.25, out[1.0][0], out[2.0][0]/4)
print(f"   ASSESS 'gamma^2 law' for A: c*_A/gamma^2 = {rat[0]:.4f}, {rat[1]:.4f}, "
      f"{rat[2]:.4f} -> NOT constant (varies ~2x over 4x gamma); A is steep "
      f"(~gamma^1.5-1.7), B is flat (c*_B/gamma falls 2.0 -> 1.0): the CONTRAST is "
      f"real, the literal 'gamma^2 law' label is loose", flush=True)

# ================= V5: cosmic point gamma = q = 1/3 ======================
t0 = time.time()
g3 = 1.0/3.0
cA_c, _ = bisect_cstar(ang3, g3, +1, 0.005, 0.08, tol=2e-6)
cB_c, _ = bisect_cstar(ang3, g3, -1, 0.5, 2.5, tol=2e-5)
check("5-cosmic", abs(cA_c - 0.0226) < 5e-4 and abs(cB_c - 1.339) < 8e-3,
      f"cosmic point (gamma=1/3, ell<=3): c*_A = {cA_c:.6f} (claim 0.0226), "
      f"c*_B = {cB_c:.6f} (claim 1.339); gap = {cB_c/cA_c:.1f}x (claim 59x)  "
      f"[{time.time()-t0:.0f}s]")

# ================= V5: near-threshold Class B seal geometry ==============
t0 = time.time()
rBn = flow(ang1, 1.0, 1.0005*cB1, -1, t_max=60.0)
# sonic audit on the sealed near-threshold flow:
ts2 = np.linspace(0.01, rBn['t_stop'], 400)
Y1d = legY(1, ud)
P1d = Y1d/np.sqrt(2*np.arange(2) + 1)[:, None]
Pp1 = np.zeros_like(P1d); Pp1[1] = (P1d[0] - ud*P1d[1])/np.where(np.abs(1-ud**2) > 1e-14, 1-ud**2, 1)
Pp1[:, 0] = 0; Pp1[:, -1] = 0
Yp1d = np.sqrt(2*np.arange(2) + 1)[:, None]*Pp1
mdB = []
for t in ts2:
    X, V = state(rBn, t); X, V = X[0], V[0]
    f, fu, ft = X @ Y1d, X @ Yp1d, V @ Y1d
    mdB.append(np.min(f*ft**2 - (1 - ud**2)*fu**2))
mdB = np.array(mdB)
check("5-shallow", rBn['sealed'] and abs(rBn['y_seal'] - 0.4588) < 0.01,
      f"near-threshold Class B (c=1.0005 c*_B, ell<=1): sealed, t_seal*={rBn['t_seal']:.4f}, "
      f"y_seal*={rBn['y_seal']:.5f} (P1 0.45875: SHALLOW, no depth divergence)")
check("5-exit", np.min(mdB) < 0 and ts2[np.argmax(mdB < 0)] < rBn['t_stop'],
      f"the near-threshold B seal EXITS the radial-dominant branch before sealing: "
      f"min Delta = {np.min(mdB):.3e} (first crossing t={ts2[np.argmax(mdB<0)]:.3f} "
      f"< t_seal {rBn['t_seal']:.3f})")
# Class A depth contrast:
rAn = flow(ang1, 1.0, 1.0005*cA1, +1, t_max=60.0)
check("5-deep", rAn['sealed'] and rAn['y_seal'] < 1e-3,
      f"contrast Class A at 1.0005 c*_A: y_seal* = {rAn['y_seal']:.2e} "
      f"(P1 1.3e-05: deep-cell divergence is diagonal-class)  [{time.time()-t0:.0f}s]")

# ================= V6: scale covariance (numeric) ========================
X = np.array([3.0, -0.6, 0.25, -0.1])
g1 = ang3.gradP(X); g2 = ang3.gradP(7.3*X)
P1v, P2v = ang3.P(X), ang3.P(7.3*X)
check("6-scale", np.max(np.abs(g1 - g2)) < 1e-14 and abs(P2v - 7.3*P1v) < 1e-12,
      f"P(lam X) = lam P(X) (deg-1) and P_X(lam X) = P_X(X) (deg-0) to machine "
      f"precision: amplitude exactly quotiented IN THE FORCE (diff {np.max(np.abs(g1-g2)):.1e})")

print(f"\nNUMERIC: {npass} PASS / {nfail} FAIL")
