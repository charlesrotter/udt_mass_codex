"""BLIND VERIFIER C2 + C7: capacity law and demanded-amplitude kinetic density.

Independent derivation (convention-free core):
  Sphere-integrated C1 action: S = Int dy { (1/4)[ Int dOmega y^2 f_y^2 ] + Q[f]/4 },
  f = F(1+kappa cos th), a = Y10 coeff, kappa = c a / F, c = sqrt(3/4pi).
  Monopole EL (= dOmega-average of exact EL, = dS/dF):
      (y^2 F')' = P_F / (8 pi)               [P = sphere-integrated angular term]
  and independently, by direct angular average of the full f-equation:
      (y^2 F')' = -(1/8pi) Int dOmega |grad f|^2/f^2 .
  Collar on-shell: (y^2 F')' = sigma = -q(1-q) y^-q = -2 s y^-q  (per solid angle,
  same normalization as f0 = y^-q itself).

Adjudication targets:
  (a) closed form: -(1/4) P_F = pi (L-2k)/k   [the agent's 'capacity']  -- check
  (b) the DEMAND: is it capacity = s y^-q (agent) or capacity = 4 pi s y^-q (EL)?
  (c) numeric kappa0: agent 0.230329; EL-correct sqrt(6s) = sqrt(2/3) = 0.816497
      (leading order), exact solve of (L-2k)/(2k) = 2 s y^-q at y=1.
  (d) C7: per-solid-angle ell=1 radial kinetic density of the demanded amplitude
      = (eta/4) dln y at q=1/3?  Test BOTH conventions; test exactness vs
      leading-order under the full capacity law.
"""
import numpy as np
import sympy as sp
from scipy import integrate, optimize

c = np.sqrt(3/(4*np.pi))
q = sp.Rational(1, 3); s = q*(1-q)/2; eta = q/6
print(f"q=1/3, s={s}={float(s):.6f}, eta={eta}={float(eta):.6f}")

# ---------- (a) closed form of -(1/4)P_F ----------
k, F = sp.symbols('k F', positive=True)
L = sp.log((1+k)/(1-k))
P = 2*sp.pi*F*(2 + (k - 1/k)*L)        # verified in C1 script
a = sp.Symbol('a', positive=True)
csym = sp.sqrt(sp.Rational(3,4)/sp.pi)
P_F = sp.diff(P.subs(k, csym*a/F), F)  # at fixed a
cap = sp.simplify((-P_F/4).subs(a, k*F/csym))
claimed_cap = sp.pi*(L - 2*k)/k
print("\n(a) -(1/4)P_F closed form:")
print("   residual vs pi(L-2k)/k:", sp.simplify(cap - claimed_cap))

# small-k limit
print("   small-k series of capacity:", sp.series(claimed_cap, k, 0, 4))

# ---------- (b) the demand: independent monopole projection ----------
# direct angular average of exact EL: (y^2F')' = -(1/8pi) Int |grad f|^2/f^2 dOmega
def avg_source(kv):
    g = lambda x: (1-x*x)/(1+kv*x)**2
    val, _ = integrate.quad(g, -1, 1, epsabs=1e-13, epsrel=1e-13)
    return -(1/(8*np.pi))*2*np.pi*kv*kv*val     # dOmega = 2pi dx, |grad|^2/f^2 = k^2(1-x^2)/(1+kx)^2
def Lf(kv): return np.log((1+kv)/(1-kv))
print("\n(b) monopole supply per solid angle, three independent routes:")
for kv in [0.1, 0.4, 0.8]:
    r1 = avg_source(kv)                          # direct projection
    r2 = -(Lf(kv)-2*kv)/(2*kv)                   # closed form -(L-2k)/(2k)
    r3 = float((P_F/(8*sp.pi)).subs({a: kv*1.0/float(csym), F: 1.0}).evalf())  # EL route
    print(f"   k={kv}: proj={r1:.10f} closed={r2:.10f} EL={r3:.10f}")
print("   => (y^2F')' = -(L-2k)/(2k); collar needs (y^2F')' = -2s y^-q")
print("   => demand: (L-2k)/(2k) = 2 s y^-q  <=>  pi(L-2k)/k = 4 pi s y^-q")
print(f"   agent demand: pi(L-2k)/k = s y^-q  -> off by factor 4*pi = {4*np.pi:.6f}")

# ---------- (c) numeric kappa(y) ----------
sv = float(s)
def kap_exact(rhs):   # solve (L-2k)/(2k) = rhs
    return optimize.brentq(lambda kk: (Lf(kk)-2*kk)/(2*kk) - rhs, 1e-12, 1-1e-15)
print("\n(c) demanded kappa at y=1:")
k_agent_lead = np.sqrt(3*sv/(2*np.pi))      # from (2pi/3)k^2 = s
k_el_lead    = np.sqrt(6*sv)                # from k^2/3 = 2s
print(f"   agent leading-order kappa0 = sqrt(3s/2pi) = {k_agent_lead:.6f} (claimed 0.230329)")
print(f"   EL-correct leading-order  = sqrt(6s)     = {k_el_lead:.6f}")
print(f"   EL-correct EXACT at y=1: solve (L-2k)/2k = 2s -> k = {kap_exact(2*sv):.6f}")
print(f"   agent-convention exact at y=1: (L-2k)/2k = s/(2pi) -> k = {kap_exact(sv/(2*np.pi)):.6f}")
# where does leading-order EL-correct kappa formally reach 1?
print(f"   EL-correct leading-order kappa(y)=sqrt(2/3) y^(-1/6) -> =1 at y={(2/3)**3:.6f}")
print(f"   (exact capacity diverges as k->1, so DEMANDED kappa never reaches 1 at y>0)")
for yv in [0.5, 0.1, 0.01, 1e-4]:
    print(f"     y={yv:g}: exact demanded kappa = {kap_exact(2*sv*yv**(-1/3)):.6f}")

# ---------- (d) C7 kinetic density ----------
print("\n(d) C7: per-solid-angle ell=1 radial kinetic density, leading-order kappa:")
# a(y) = kappa F / c, F=y^-q. kinetic per solid angle = (1/16pi) y^2 a'^2
y = sp.Symbol('y', positive=True)
for name, k0 in [("agent k0=sqrt(3s/2pi), SPHERE-integrated (1/4)y^2 a'^2", None),
                 ("EL k0=sqrt(6s), PER-SOLID-ANGLE (1/16pi) y^2 a'^2", None)]:
    pass
qv = sp.Rational(1,3)
for label, k0sq, measure in [
        ("agent  k0^2=3s/(2pi), sphere measure (1/4)y^2a'^2", 3*s/(2*sp.pi), sp.Rational(1,4)),
        ("agent  k0^2=3s/(2pi), perOmega (1/16pi)y^2a'^2", 3*s/(2*sp.pi), 1/(16*sp.pi)),
        ("ELcorr k0^2=6s,      sphere measure (1/4)y^2a'^2", 6*s, sp.Rational(1,4)),
        ("ELcorr k0^2=6s,      perOmega (1/16pi)y^2a'^2", 6*s, 1/(16*sp.pi))]:
    aofy = sp.sqrt(k0sq)*y**(-qv/2) * y**(-qv) / csym       # kappa(y) F(y)/c
    dens = sp.simplify(measure * y**2 * sp.diff(aofy, y)**2)
    dens_dlny = sp.simplify(dens*y)   # density wrt dln y
    print(f"   {label}: y^2-kinetic density = {sp.nsimplify(dens_dlny, [sp.pi])} dlny"
          f"  [eta/4 = {sp.nsimplify(eta/4)}]")

# exactness test: full capacity law (EL-correct), q=1/3 — is density exactly eta/4 dlny?
print("\n(d2) exactness under FULL capacity law (EL-correct demand):")
def kap_full(yv): return kap_exact(2*sv*yv**(-1/3.0))
ys = np.logspace(-4, 0, 200)
avals = np.array([kap_full(t)*t**(-1/3.0)/c for t in ys])
dady = np.gradient(avals, ys)
dens = (1/(16*np.pi))*ys**2*dady**2*ys   # per dlny
print("   y, perOmega kinetic density per dlny, ratio to eta/4:")
for i in [199, 150, 100, 50, 0]:
    print(f"   y={ys[i]:.2e}: {dens[i]:.6f}  ratio={dens[i]/(float(eta)/4):.4f}")
