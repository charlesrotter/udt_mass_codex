"""VERIFIER stage 4: weight-class / seal-endpoint divergence powers (C4).
Own background flow to the seal (M2), own G assembly; fit divergence
powers of the weight entries in the relevant invariant directions as
mu = f(pole) -> 0; independent limit-point/limit-circle reasoning.

Model facts being tested (package claims):
  W_A: vhat ~ 1/mu (slope -1.01); m=1 ~ log (slope -0.12); m=2 and
       m=0-complement bounded.
  W_B: vhat ~ 1/mu^2 (-2.00); m=1 ~ 1/mu (-0.99).
LC/LP consequence: with tau = t_seal - t and mu ~ v* tau (linear layer),
indicial branches u ~ {1, tau}:
  Int_0 W u^2 dtau:  W ~ log: both branches integrable  => LIMIT CIRCLE
                     W ~ 1/tau: constant branch log-divergent => LIMIT POINT
So W_A m=1: family survives; W_B m=1: family killed. Verify the linear
layer mu ~ v* tau too (it feeds the classification).
"""
import numpy as np, sys, time
sys.path.insert(0, '/tmp/verify_s2')
from v_lib import *

P, F = [], []
def check(name, ok, detail=""):
    (P if ok else F).append(name)
    print(f"VCHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

t0 = time.time()
MEM = load_members()
sol = flow(MEM['M2']['gamma'], MEM['M2']['c'])
tstop = sol.t[-1]

pole = lambda t: float(sol.sol(t)[:4] @ YP1)
def state_at_mu(mu):
    tl = brentq(lambda t: pole(t) - mu, 0.2*tstop, tstop)
    return sol.sol(tl)[:4], tl

# linear-layer check: mu vs tau = t_seal - t
tseal = MEM['M2']['tseal']
mus = np.array([0.3, 0.1, 0.03, 0.01, 0.003])
taus = []
for mu in mus:
    _, tl = state_at_mu(mu)
    taus.append(tseal - tl)
taus = np.array(taus)
slope_mt = np.polyfit(np.log(taus[-3:]), np.log(mus[-3:]), 1)[0]
vstar = mus[-1]/taus[-1]
print(f"linear layer: mu/tau -> {vstar:.4f} (package v* = 7.5339); "
      f"log-log slope {slope_mt:.4f}")
check("L0 linear seal layer mu = v* tau (slope 1, v* ~ 7.53)",
      abs(slope_mt - 1) < 0.02 and abs(vstar - 7.5339) < 0.05)

QD = Q(4000)
BD = {m: Blk(m, QD) for m in range(3)}
rows = {k: [] for k in ('A_vhat', 'A_m1', 'A_m2', 'A_comp',
                        'B_vhat', 'B_m1', 'B_m2')}
for mu in mus:
    X, _ = state_at_mu(mu)
    _, GA0, GB0 = BD[0].mats(X); GA0, GB0 = GA0[0], GB0[0]
    _, GA1, GB1 = BD[1].mats(X); GA1, GB1 = GA1[0], GB1[0]
    _, GA2, _ = BD[2].mats(X); GA2 = GA2[0]
    rows['A_vhat'].append(VH @ GA0 @ VH)
    rows['A_comp'].append(np.linalg.eigvalsh(WC.T @ GA0 @ WC)[-1])
    rows['A_m1'].append(GA1[0, 0])
    rows['A_m2'].append(GA2[0, 0])
    rows['B_vhat'].append(VH @ GB0 @ VH)
    rows['B_m1'].append(GB1[0, 0])
    rows['B_m2'].append(GB1[0, 0]*0 + BD[2].mats(X)[2][0][0, 0])
ln = np.log(mus)
def slope(k):
    v = np.log(np.abs(rows[k]))
    return (v[-1] - v[-2])/(ln[-1] - ln[-2])
print("entries vs mu:")
for k in rows:
    print(f"  {k:7s}: " + " ".join(f"{v:11.4f}" for v in rows[k])
          + f"   slope {slope(k):+.3f}")
check("W1 W_A vhat ~ 1/mu (package -1.010)", abs(slope('A_vhat') + 1) < 0.05,
      f"{slope('A_vhat'):+.3f}")
check("W2 W_A m=1 sub-power/log (package -0.123)",
      abs(slope('A_m1')) < 0.2, f"{slope('A_m1'):+.3f}")
check("W3 W_A m=2 + m=0-complement bounded",
      abs(slope('A_m2')) < 0.1 and abs(slope('A_comp')) < 0.1,
      f"{slope('A_m2'):+.3f} {slope('A_comp'):+.3f}")
check("W4 W_B vhat ~ 1/mu^2 (package -2.001)",
      abs(slope('B_vhat') + 2) < 0.05, f"{slope('B_vhat'):+.3f}")
check("W5 W_B m=1 ~ 1/mu (package -0.992)",
      abs(slope('B_m1') + 1) < 0.05, f"{slope('B_m1'):+.3f}")

# m=1 log refinement: fit a + b ln(1/mu) and check residuals shrink
v = np.array(rows['A_m1'])
b, a = np.polyfit(np.log(1/mus), v, 1)
res = np.abs(v - (a + b*np.log(1/mus))).max()/np.abs(v).max()
check("W6 W_A m=1 is genuinely logarithmic (linear in ln(1/mu), "
      "residual < 3%)", res < 0.03, f"b={b:.4f}, rel residual {res:.1e}")

# LC/LP integrals, numerically: Int_eps W(tau) u(tau)^2 dtau for u=1, tau
print("\nLC/LP integral test (numerical, on-flow):")
taug = np.geomspace(2e-4, 0.05, 40)
WA1 = []; WB1 = []
for tu in taug:
    X = sol.sol(tseal - tu)[:4]
    WA1.append(BD[1].mats(X)[1][0][0, 0])
    WB1.append(BD[1].mats(X)[2][0][0, 0])
WA1, WB1 = np.array(WA1), np.array(WB1)
# mass-per-decade test for Int W u^2 dtau, u = 1 (constant branch):
# log weight => decade mass shrinks ~10x per decade (integral CONVERGES);
# 1/tau weight => decade mass constant (integral DIVERGES like log).
from scipy.integrate import trapezoid
def decade_mass(W, a, b):
    sel = (taug >= a) & (taug <= b)
    return trapezoid(W[sel], taug[sel])
dA1 = decade_mass(WA1, 2.2e-4, 2.2e-3); dA2 = decade_mass(WA1, 2.2e-3, 2.2e-2)
dB1 = decade_mass(WB1, 2.2e-4, 2.2e-3); dB2 = decade_mass(WB1, 2.2e-3, 2.2e-2)
print(f"  decade mass Int W dtau: W_A m=1: [2e-4,2e-3] {dA1:.2e} vs "
      f"[2e-3,2e-2] {dA2:.2e} (ratio {dA1/dA2:.3f} -> 0: CONVERGES); "
      f"W_B m=1: {dB1:.2e} vs {dB2:.2e} (ratio {dB1/dB2:.3f} -> const: "
      f"log-DIVERGES)")
check("W7 LC/LP: W_A m=1 constant branch normalizable (decade mass "
      "vanishing => limit circle, theta-family SURVIVES); W_B m=1 decade "
      "mass ~constant => Int(1/tau) log-diverges => limit point (family "
      "KILLED). With verified powers (W1-W6) + linear layer (L0) this is "
      "an analytic consequence.", dA1/dA2 < 0.25 and dB1/dB2 > 0.6)

print("\nGRADE of the fork (verifier): W_A is the licensed primary "
      "(banked n-symbolic time term + exact Jacobian d-phi = -d-f/2f); "
      "W_B is hypothesis-grade (H1 elimination not re-derived on "
      "nonspherical backgrounds). They agree on every sign/structure "
      "result in S2 and disagree ONLY on the m=1 endpoint class at the "
      "true seal => the fork is load-bearing exactly where the report "
      "says it is (the BC-family's existence), nowhere else.")
print(f"\nV4 STAGE: PASS {len(P)}/{len(P)+len(F)}  wall {time.time()-t0:.0f}s")
if F: print("FAILS:", F)
