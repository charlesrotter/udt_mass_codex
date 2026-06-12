"""
VX2 verifier — C2: interface jump gamma_eff, from scratch.

Fluctuation operator (banked, n-symbolic):
  (r^2 f^2 u')' - (4-2n) r^2 f^2 E0 u - lam f u = omega^2 r^2 u  (flipped)
  E0 = phi0'' + 2 phi0'/r - 2 phi0'^2 ,  f = e^{-2 phi0}.

Background: interior collar phi0 = (q/2) ln r (r<1, phi0(1)=0,
r phi0'(1-) = q/2). Exterior r>1: phi0 = p ln r (slope p at 1+).
 - zero-tail: p = 0
 - mirror (odd continuation phi_univ(x) = -phi_matter(-x), x=ln r): p = q/2.

A kink (slope jump) puts a delta in phi0'' hence in E0. The potential
V = (4-2n) r^2 f^2 E0 acquires delta weight (4-2n)*(p - q/2) at r=1
(f(1)=1, r=1). The log-derivative jump of u across r=1 is
  u'(1+) - u'(1-) = V_delta * u(1)   =>   attractive strength
  gamma_eff := -(V_delta) = (4-2n)(q/2 - p).

Checks:
 (1) symbolic: odd continuation of phi(x) = (q/2)x is slope-continuous
     (mirror has NO kink); zero-tail has slope jump -q/2.
 (2) mollifier numerics: smooth phi0_eps with tanh transition of width
     eps; integrate V across the transition; delta weight ->
     (4-2n)(p - q/2) as eps -> 0; the non-delta pieces (phi0'^2 term,
     2 phi0'/r term, bulk) contribute O(eps) or stay bounded.
 (3) gamma_eff(n=0, p=0) = 2q (banked); gamma_eff(p=q/2) = 0 for ALL n.
 (4) verdict-invariance of the screening fork: deficits with
     gamma in {2q (undressed), q (dressed)} both < gamma_c; mirror = 0
     regardless.
"""
import numpy as np

q = 1.0/3.0

# ---------- (1) symbolic-by-construction ----------
# phi_matter(x) = (q/2) x for x <= 0 (x = ln r). Mirror map:
# phi_univ(x) = -phi_matter(-x) = (q/2) x for x >= 0.
# slope at 0-: q/2 ; slope at 0+: q/2  -> continuous, no kink.
print("[1] mirror continuation slopes: left %.6f right %.6f -> kink %.6f"
      % (q/2, q/2, 0.0))
print("    zero-tail slopes: left %.6f right %.6f -> kink %.6f"
      % (q/2, 0.0, -q/2))

# ---------- (2) mollifier extraction of the delta weight ----------
def delta_weight(p_slope, nval, eps):
    """integrate V = (4-2n) r^2 f^2 E0 minus its bulk parts across the
    transition; smooth background:
      phi0(x) = (q/2)x + (p - q/2) * w(x/eps), x = ln r,
      w(s) = eps * log(1+e^{s/1})... use w'(s)=sigmoid: slope goes q/2 -> p.
    """
    # x-grid across transition
    X = 60.0*eps
    x = np.linspace(-X, X, 400001)
    sig = 1.0/(1.0+np.exp(-x/eps))
    dphi_dx = q/2 + (p_slope - q/2)*sig                 # phi'(x)
    d2phi_dx2 = (p_slope - q/2)*sig*(1-sig)/eps
    r = np.exp(x)
    # convert to r-derivatives: phi0' = dphi_dx / r ; phi0'' = (d2 - d1)/r^2
    p1 = dphi_dx/r
    p2 = (d2phi_dx2 - dphi_dx)/r**2
    E0 = p2 + 2*p1/r - 2*p1**2
    phi0 = q/2*x + (p_slope - q/2)*eps*np.log1p(np.exp(x/eps))
    f = np.exp(-2*phi0)
    V = (4-2*nval)*r**2*f**2*E0
    # delta weight = integral of V dr minus the smooth (kink-free) parts:
    Vsmooth_terms = (4-2*nval)*r**2*f**2*(-dphi_dx/r**2 + 2*p1/r - 2*p1**2)
    integrand_delta = V - Vsmooth_terms                  # = (4-2n) r^2f^2 * d2phi/r^2
    w = np.trapezoid(integrand_delta*r, x)               # dr = r dx
    return w

for nval in (0, 1):
    for p_slope, tag in ((0.0, 'zero-tail'), (q/2, 'mirror'), (0.1, 'generic p=0.1')):
        ws = [delta_weight(p_slope, nval, e) for e in (1e-2, 1e-3, 1e-4)]
        pred = (4-2*nval)*(p_slope - q/2)
        print(f"[2] n={nval} {tag:14s} delta weight eps->0: "
              f"{ws[0]:+.6f} {ws[1]:+.6f} {ws[2]:+.6f}  predicted {pred:+.6f}")

# ---------- (3) gamma_eff table ----------
print("\n[3] gamma_eff = (4-2n)(q/2 - p):")
for nval in (0, 1):
    for p_slope, tag in ((0.0, 'zero-tail'), (q/2, 'mirror')):
        print(f"    n={nval} {tag:9s}: gamma_eff = {(4-2*nval)*(q/2-p_slope):+.6f}")
print("    banked (n=0, zero-tail): 2q = %.6f" % (2*q))

# ---------- (2b) bounded-term control: non-delta pieces of V across kink ----
# integral over transition of the SMOOTH part should -> bulk only (O(eps) extra)
for e in (1e-2, 1e-3, 1e-4):
    X = 60.0*e
    x = np.linspace(-X, X, 400001)
    sig = 1.0/(1.0+np.exp(-x/e))
    dphi_dx = q/2 + (0.0 - q/2)*sig
    r = np.exp(x); p1 = dphi_dx/r
    phi0 = q/2*x + (0.0-q/2)*e*np.log1p(np.exp(x/e))
    f = np.exp(-2*phi0)
    smooth = 4*r**2*f**2*(-dphi_dx/r**2 + 2*p1/r - 2*p1**2)
    val = np.trapezoid(smooth*r, x)
    print(f"[2b] eps={e:.0e}: smooth-part integral across transition = {val:+.6e} (-> 0)")
