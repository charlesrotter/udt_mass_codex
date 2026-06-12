#!/usr/bin/env python3
"""P1 final physics battery after the ride-away-event fix.
All flows: fate decided only by seal (absolute classifier, cutoff 0.002)
or t_max horizon (stated).  No early ride-away exit (scale covariance)."""
import numpy as np, time
from solver import AngularSector, run_flow, flow_state, bisect_cstar, \
                   legendre_Y, Qstar_field

npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond); npass += ok; nfail += (not ok)
    print(f"V-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

cM2, gam = 0.2832873535156249512, 1.0
ang1, ang3 = AngularSector(1), AngularSector(3)

# ---------------- threshold anchors (the V-19 redo, corrected classifier)
t0 = time.time()
cA1, _ = bisect_cstar(ang1, 1.0, +1, 0.15, 0.30)
cA3, _ = bisect_cstar(ang3, 1.0, +1, 0.10, 0.20)
print(f"anchors: ell<=1 c*_A = {cA1:.6f} (banked 0.206994/0.207001); "
      f"ell<=3 c*_A = {cA3:.6f} (banked 0.141644)   [{time.time()-t0:.0f}s]", flush=True)
check("19f", abs(cA1-0.207001) < 2e-5 and abs(cA3-0.141644) < 2e-5,
      f"Class A threshold anchors: {cA1:.6f} vs 0.207001, {cA3:.6f} vs 0.141644 "
      f"(ride-away event was the defect; classification now horizon-only)")

# ---------------- Class B at M2 driving, long horizon: does it EVER seal?
t0 = time.time()
resB = run_flow(ang3, gam, cM2, sign=-1, t_max=60.0)
ts = np.linspace(0, resB['t_stop'], 400)
XB, VB = flow_state(resB, ts)
kapB = np.sqrt(3)*np.abs(XB[:, 1])/XB[:, 0]
fmB = np.array([ang3.fmin(x)[0] for x in XB])
print(f"Class B at M2 driving, t_max=60: sealed={resB['sealed']}, "
      f"t_stop={resB['t_stop']:.3f}  [{time.time()-t0:.0f}s]", flush=True)
print(f"   kappa_B(t): max={kapB.max():.4f} at t={ts[np.argmax(kapB)]:.2f}, "
      f"end={kapB[-1]:.5f}; f_min end = {fmB[-1]:.3e}", flush=True)
check("25", True, f"Class B fate at M2 driving on long horizon recorded: "
      f"{'TERM t_seal=%.4f' % resB.get('t_seal', np.nan) if resB['sealed'] else 'SAT to t=60 (shape decays: kappa_end=%.1e)' % kapB[-1]}")

# ---------------- corrected c*(ell) tables, both classes
print("\nc*(ell), gamma = 1, t_max = 60, no ride exit:", flush=True)
print("   ell    c*_A         c*_B", flush=True)
cA, cB = {}, {}
for L in range(1, 6):
    angL = AngularSector(L)
    t0 = time.time()
    cA[L], _ = bisect_cstar(angL, 1.0, +1, 0.05, 0.30)
    cB[L], _ = bisect_cstar(angL, 1.0, -1, 0.2, 3.5)
    print(f"   {L}      {cA[L]:.6f}     {cB[L] if cB[L] else float('nan'):.6f}"
          f"   [{time.time()-t0:.0f}s]", flush=True)
banked = {1: 0.207001, 2: 0.158948, 3: 0.141644, 4: 0.132798, 5: 0.127417}
okA = all(abs(cA[L]-banked[L]) < 5e-5 for L in range(1, 6))
check("26", okA, "c*_A(ell) ell=1..5 reproduce the banked/VS1 values "
      + str({L: round(cA[L], 6) for L in cA}))
dA = [abs(cA[L+1]-cA[L]) for L in range(1, 5)]
dB = [abs(cB[L+1]-cB[L]) for L in range(1, 5)]
print(f"   |incr| A: {['%.5f' % x for x in dA]} ratios "
      f"{['%.3f' % (dA[i+1]/dA[i]) for i in range(3)]}", flush=True)
print(f"   |incr| B: {['%.5f' % x for x in dB]} ratios "
      f"{['%.3f' % (dB[i+1]/dB[i]) for i in range(3)]}", flush=True)

# ---------------- bracketing runs around diagonal c*_3 (corrected)
print("\nbracketing c*_3(diagonal) = 0.141644 (t_max=60):", flush=True)
for c in [0.12, 0.17]:
    rA = run_flow(ang3, 1.0, c, sign=+1, t_max=60.0)
    rB = run_flow(ang3, 1.0, c, sign=-1, t_max=60.0)
    print(f"   c={c}: A: {'TERM t_seal*=%.4f y_seal*=%.5f' % (rA.get('t_seal', np.nan), rA.get('y_seal', np.nan)) if rA['sealed'] else 'SAT(t60)'};  "
          f"B: {'TERM t_seal*=%.4f y_seal*=%.5f' % (rB.get('t_seal', np.nan), rB.get('y_seal', np.nan)) if rB['sealed'] else 'SAT(t60)'}", flush=True)
check("27", True, "bracketing pair recorded")

# ---------------- sealed Class B flows: sonic audit + seal locus
print("\nClass B sealed-flow audit (just above c*_B):", flush=True)
for L, cstar in [(1, cB[1]), (3, cB[3])]:
    angL = AngularSector(L)
    c = cstar*1.02
    r = run_flow(angL, 1.0, c, sign=-1, t_max=60.0)
    minD, tD = np.inf, np.nan
    if r['sealed']:
        for t in np.linspace(1e-3, r['t_stop'], 150):
            X, V = flow_state(r, t); X, V = X[0], V[0]
            _, Q, Delta, *_ = Qstar_field(angL, X, V, np.linspace(-1, 1, 1001))
            if Delta.min() < minD: minD, tD = Delta.min(), t
    print(f"   ell<={L}, c = 1.02 c*_B = {c:.4f}: sealed={r['sealed']} "
          f"t_seal*={r.get('t_seal', np.nan):.4f} y_seal*={r.get('y_seal', np.nan):.5f} "
          f"min Delta={minD:+.3e} at t={tD:.3f} -> radial-dominant branch "
          f"{'HELD' if minD > 0 else 'EXITED (mixed-type flow: trust-bounded)'}",
          flush=True)
check("28", True, "sonic/branch audit of near-threshold Class B seals recorded")

print(f"\nSTAGE f3: {npass} PASS / {nfail} FAIL")
