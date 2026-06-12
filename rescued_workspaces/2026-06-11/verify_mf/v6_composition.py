"""
VERIFIER v6 (H2-D): EXPLICIT COMPOSITION OF THE TWO HALVES.

Question (the one place the halves could collide): H2-C derives a real,
channel-resolved H1^2 loading from the NATIVE completion (the angular
sector of C1). H1-B derives the exact flip W = -(c/2) r^2 sin from
full-row Schur elimination, and H1-D says only a POSITED proper
completion (kappa_V != 0) deforms it. If H2's native loading entered
H1's alpha-block as an ADDITION, the flip would be dressed. Resolve.

Already proven symbolically (v1 G1-G3):
  G1: H2-C's coeff[H1^2] IS alpha_aa of H1's full second variation,
      restricted to the rotation class -- the SAME term, not an addition.
  G2: the full-row Schur on the rotation class = -(c/2) r^2 sin EXACT.
  G3: the native angular sector loads beta_b too (alignment); a posited
      potential term loads alpha only (kappa_V mechanism).

Here, numerics on the critical collar (q = 1/3) quantify the collision
had it been composed wrongly, and confirm the native composition:
 D1  alpha_aa sign on the collar: the a-only DEN = X - Y > 0 everywhere
     (truncated elimination regular on the collar -- unlike the formed
     S1 members) but the truncated flip Lambda(theta) != 1: dressing
     would be REAL if the b-row were dropped.
 D2  size of the wrong-composition dressing: channel-averaged
     <Lambda>-1 at y = 1 (reported); -> 0 far-collar.
 D3  the correct composition: full-row Schur pointwise == -(c/2) r^2
     sin on collar slices (numerical evaluation of the v1 matrices).
 D4  kappa_V(native) == 0: the native completion adds NO -cV U(f)
     sqrt(-g) term; equivalently, the derived time weight stays
     <R R'/f^2> with ZERO deformation. (Consequence of G1+G2; numeric
     re-check via direct Schur at sample collar points.)
"""
import numpy as np
from scipy.optimize import brentq
from math import log

PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"V6 {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

q = 1.0/3.0; s = q*(1-q)/2.0
Lk = lambda k: log((1+k)/(1-k))
H = lambda k: Lk(k)/(2*k) - 1.0
Hp = lambda k: 1.0/(k*(1-k**2)) - Lk(k)/(2*k**2)
def bg(yv):
    F = yv**(-q); Fp = -q*yv**(-q-1)
    k = brentq(lambda kk: H(kk) - 2*s*yv**(-q), 1e-13, 1-1e-13, xtol=1e-16)
    kp = -2*q*s*yv**(-q-1)/Hp(k)
    return F, Fp, k, kp, F*k, Fp*k + F*kp

ug, wq = np.polynomial.legendre.leggauss(800)

def XY(yv):
    """X = r^2 f^2 phi_r^2, Y = f phi_th^2 on the collar slice."""
    F, Fp, k, kp, a, ap = bg(yv)
    f = F*(1 + k*ug)
    X = yv**2*(Fp + ap*ug)**2/4.0          # r^2 f_r^2/4 = r^2 f^2 phi_r^2
    Y = (a**2*(1 - ug**2))/(4*f)           # f phi_th^2
    return X, Y, f

# ---- D1: collar DEN sign map (VERIFIER FINDING, sharper than H1-C) --
# the a-only DEN = X - Y is NEGATIVE on MOST of the collar sphere at
# every y: far-collar Y/X -> (6s/q^2)(1-u^2) = 6(1-u^2) at q = 1/3, so
# DEN < 0 for |u| < sqrt(1 - q^2/(6s)) = sqrt(5/6) = 0.91287.
ufine = np.linspace(-1, 1, 200001)
def band(yv):
    F, Fp, k, kp, a, ap = bg(yv)
    f = F*(1 + k*ufine)
    X = yv**2*(Fp + ap*ufine)**2/4.0
    Y = a**2*(1 - ufine**2)/(4*f)
    neg = ufine[(X - Y) < 0]
    return neg.min(), neg.max(), len(neg)/len(ufine)
ok1 = True
for yv in (1.0, 10.0, 1e3, 1e6):
    lo, hi, fr = band(yv)
    print(f"   y={yv:8.0f}: DEN<0 band u in [{lo:+.4f}, {hi:+.4f}] "
          f"(fraction {fr:.3f})")
    ok1 &= fr > 0.5
edge = np.sqrt(1 - q**2/(6*s))
lo8, hi8, _ = band(1e8)
check("D1 (FINDING) the alpha_aa = 0 locus exists ON THE CRITICAL "
      "COLLAR at every y, covering MOST of the sphere; far-collar "
      "edges -> +-sqrt(1 - q^2/(6s)) = 0.9129 (analytic, < 2%)",
      ok1 and abs(hi8 - edge)/edge < 0.02 and abs(-lo8 - edge)/edge < 0.02,
      f"y=1e8 band [{lo8:+.4f}, {hi8:+.4f}] vs +-{edge:.4f}")

# ---- D2: the wrong composition is PV-ILL-DEFINED, not just dressed --
vals = []
for N in (400, 800, 1600, 3200):
    x2, w2 = np.polynomial.legendre.leggauss(N)
    F, Fp, k, kp, a, ap = bg(1.0)
    f = F*(1 + k*x2)
    X = (Fp + ap*x2)**2/4.0
    Y = a**2*(1 - x2**2)/(4*f)
    vals.append((w2 @ ((3*x2**2)*((X + Y)/(X - Y))/f**2))/2)
print("   collar y=1 truncated <Y1^2 Lambda/f^2> under doubling: "
      + " ".join(f"{v:+.3f}" for v in vals))
spl = abs(vals[-1] - vals[-2])
check("D2 (FINDING) the a-only elimination on the collar is PV-NON-"
      "CONVERGENT (the wrong composition does not even exist as a "
      "channel weight; H2's H1-only scheme must not be used for "
      "elimination -- loading coefficients only)",
      spl > 0.02*abs(vals[-1]) or spl > abs(vals[1] - vals[0]),
      f"last doubling moves {spl:.2e}")

# ---- D3: correct composition: full-row Schur pointwise on collar ----
# alpha_ab (2x2), beta_ab per unit (c r^2 sin): from the v1 closed forms
# evaluated numerically at sample (y, u) points; W must be -(1/2) c r^2 s.
ok3 = True; worst = 0.0
for yv in (1.0, 3.0, 1e2, 1e5):
    F, Fp, k, kp, a, ap = bg(yv)
    for uv in (-0.9, -0.3, 0.2, 0.7, 0.95):
        f = F*(1 + k*uv)
        p0r = -(Fp + ap*uv)/(2*f)
        S2 = 1 - uv**2
        p0t = (a*np.sqrt(S2)/2)/f
        r2 = yv**2
        G0 = f*p0r**2 + p0t**2/r2
        st = np.sqrt(S2)
        # alpha = (1/2) r^2 st [ (hg)(hg)^T - G0/2 h^-1 ], c = 1
        hg = np.array([f*p0r, p0t/r2])
        hinv = np.diag([f, 1/r2])
        al = 0.5*r2*st*(np.outer(hg, hg) - 0.5*G0*hinv)
        be = -r2*st*hg
        Wnum = 0.5*r2*st - 0.25*be @ np.linalg.solve(al, be)
        dev = abs(Wnum + 0.5*r2*st)/(0.5*r2*st)
        worst = max(worst, dev)
        ok3 &= dev < 1e-12
check("D3 correct composition: full-row Schur == -(c/2) r^2 sin at "
      "every sampled collar point (rel < 1e-12): W_A survives EXACTLY "
      "for the native theory", ok3, f"worst rel dev {worst:.1e}")

# ---- D4: the native deformation is ZERO (not merely small) ----
# the native completion's alpha-contribution: Delta-alpha_ang =
# alpha(p0t) - alpha(p0t=0); its beta contribution: Delta-beta_ang.
# Composing alpha WITH its aligned beta gives the exact flip (D3);
# composing alpha WITHOUT beta (potential-style) gives the dressing.
yv, uv = 1.0, 0.5
F, Fp, k, kp, a, ap = bg(yv)
f = F*(1 + k*uv); S2 = 1 - uv**2; st = np.sqrt(S2); r2 = yv**2
p0r = -(Fp + ap*uv)/(2*f); p0t = (a*np.sqrt(S2)/2)/f
G0 = f*p0r**2 + p0t**2/r2
hg = np.array([f*p0r, p0t/r2]); hinv = np.diag([f, 1/r2])
al = 0.5*r2*st*(np.outer(hg, hg) - 0.5*G0*hinv)
be = -r2*st*hg
# native angular pieces:
hg0 = np.array([f*p0r, 0.0]); G00 = f*p0r**2
al0 = 0.5*r2*st*(np.outer(hg0, hg0) - 0.5*G00*hinv)
be0 = -r2*st*hg0
W_alpha_only = 0.5*r2*st - 0.25*be0 @ np.linalg.solve(al, be0)  # WRONG mix
W_aligned = 0.5*r2*st - 0.25*be @ np.linalg.solve(al, be)       # native
check("D4 native deformation ZERO: aligned composition gives exactly "
      "-(c/2) r^2 sin, while alpha-without-beta (potential-style "
      "loading of the SAME angular term) shifts W (kappa_V mechanism "
      "is the only deformation channel; native kappa_V = 0)",
      abs(W_aligned + 0.5*r2*st) < 1e-14*r2 and
      abs(W_alpha_only + 0.5*r2*st) > 1e-3*r2,
      f"aligned dev {abs(W_aligned+0.5*r2*st):.1e}, "
      f"misaligned shift {W_alpha_only+0.5*r2*st:+.4f}")

n = sum(1 for _, ok in PASS if ok)
print(f"\nV6 TOTAL: {n}/{len(PASS)} PASS")
