"""tw_probe.py -- Task (c): the missing twin fundamental.
Part 1 (no shots): exact turning-band structure from Lemma 1+2 (CAS-verified identities):
  turning requires U(rho)<2 (Lemma 1);  on a falling arc G=Phi^2-2Z rho^2(2-U) obeys
  dG/dphi = 2G - 2Z rho rho_phi [2(2-U) - rho U']  (exact, CAS tw_cas A6)
  => turning confined to the band Bnd = {rho<1 : rho U' > 2(2-U)}.
Part 2 (shots, bounded): termination scan d' in [0.0052, 0.0074] (does the twin ladder reach N=1?)
  + large-d' escalation {0.016..0.09}.  <= 12 shots + optional short bisection.
"""
import sys
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, miss

M, Z = 3.0, 8.0

print("="*100)
print("PART 1 -- turning-band structure (exact family algebra, no shots)")
print("="*100)
def band(a_param):
    U, Up, _ = make_risefall_slice(a_param, m=M)
    # rho* : inner root of U=2 below 1 (hump exit); rho_crit = sqrt(m/2a) = hump top
    rho_crit = np.sqrt(M/(2*a_param))
    f2 = lambda rho: U(rho) - 2.0
    rho_star = brentq(f2, 1e-6, rho_crit, xtol=1e-14) if f2(1e-6) < 0 else np.nan
    # band bottom rho_t : rho U'(rho) = 2(2-U)
    fb = lambda rho: rho*Up(rho) - 2.0*(2.0 - U(rho))
    # fb>0 in band; find root below rho_star
    rho_t = brentq(fb, 1e-6, rho_star, xtol=1e-14) if fb(1e-6) < 0 and fb(rho_star) > 0 else np.nan
    # turning threshold T(rho) = 2Z rho^2 (2-U): max over band
    rg = np.linspace(rho_t, rho_star, 20001)
    T = 2.0*Z*rg**2*(2.0 - U(rg))
    return rho_star, rho_t, float(np.max(T)), rg[np.argmax(T)]

print(f"{'dprime':>9} {'a':>9} {'rho*':>8} {'rho_t':>8} {'T_max':>10} {'@rho':>7}")
for dp in (0.0039, 0.0065, 0.0124, 0.02, 0.04, 0.09, 0.2, 0.5):
    a_param = 1.5*(1.0 + dp)
    rs_, rt_, Tm, rTm = band(a_param)
    print(f"{dp:9.4f} {a_param:9.5f} {rs_:8.5f} {rt_:8.5f} {Tm:10.4f} {rTm:7.4f}")
print("\nBelow-side N=0 comparison (banked): seals at rho_s=2.2614 with q^2 = Phi_s^2 = 159.38")
a0 = 1.4813439655172531
U0, Up0, _ = make_risefall_slice(a0, m=M)
print(f"  U(rho_s)={U0(2.2614034898623525):.5f} (outer plateau, U~0: threshold T=2Z rho^2(2-U) "
      f"= {2*Z*2.2614**2*(2-U0(2.2614)):.2f} and GROWING in rho)")
print("  twin-image inner seal would sit at rho~1/2.2614=0.4422:")
a_tw = 1.5*(1.0 + 0.0124)
U1, Up1, _ = make_risefall_slice(a_tw, m=M)
print(f"  at a={a_tw:.5f}: U(0.4422)={U1(0.4422):.4f}, threshold T(0.4422)="
      f"{2*Z*0.4422**2*(2-U1(0.4422)):.3f}  << the flux the fall accumulates (see probes)")

print()
print("="*100)
print("PART 2 -- probe shots (bounded, single process)")
print("="*100)
SHOTS = 0
def probe(dp):
    global SHOTS
    a_param = 1.5*(1.0 + dp)
    U, Up, _ = make_risefall_slice(a_param, m=M)
    SHOTS += 1
    f, o = miss(Z, U, Up, 1.0)
    st = o["status"]
    extra = ""
    if st == "seal":
        extra = f" rho_s={o['rho_s']:.5f} q={o['q']:.4f} r_s={o['r_s']:.1f}"
    print(f"  d'={dp:.6f} a={a_param:.7f}  miss(rho'_s)={f if np.isfinite(f) else float('nan'):+.5e} [{st}]{extra}")
    return f, o

print("termination scan (does the above ladder reach the N=1/N=2 twins? below rungs: N=3@d=0.005552,")
print(" N=2@0.006226, N=1@0.006462; twin locations ~ +d^2):")
term = []
for dp in (0.0052, 0.0058, 0.0063, 0.00655, 0.0068, 0.0074):
    f, o = probe(dp)
    term.append((dp, f, o["status"]))

print("\nlarge-d' escalation (N=0-twin window and beyond; banked 13-pt probe found miss<0 monotone")
print(" on (0.0082, 0.014]):")
big = []
for dp in (0.016, 0.020, 0.028, 0.040, 0.060, 0.090):
    f, o = probe(dp)
    big.append((dp, f, o["status"]))

# sign-change hunt in the termination scan -> short bisection (bounded 8 steps) per bracket
print("\nbrackets in termination scan:")
brs = []
for (d1, f1, s1), (d2, f2, s2) in zip(term, term[1:]):
    if s1 == s2 == "seal" and np.isfinite(f1) and np.isfinite(f2) and f1*f2 < 0:
        brs.append((d1, d2, f1))
        print(f"  bracket ({d1}, {d2})")
if not brs:
    print("  NONE")
for (dlo, dhi, flo) in brs[:2]:
    a_, b_, fa = dlo, dhi, flo
    for _ in range(10):
        mid = 0.5*(a_ + b_)
        fm, om = probe(mid)
        if not np.isfinite(fm): break
        if fa*fm <= 0: b_ = mid
        else: a_, fa = mid, fm
    dstar = 0.5*(a_ + b_)
    fm, om = probe(dstar)
    if om["status"] == "seal":
        print(f"  ROOT d'*={dstar:.7f} a*={1.5*(1+dstar):.8f} rho_s={om['rho_s']:.6f} "
              f"q={om['q']:.5f} r_s={om['r_s']:.2f}")

print(f"\ntotal probe shots = {SHOTS}")
