"""
S6: (a) Independent numerical validation of the symbolic Hessian entries
(2nd finite differences of P itself, 2D sphere quadrature, finite kappa).
(b) Scan of mu_BO(y) and n_eff(y) over the collar (N1's [0.993,1) claim).
(c) m+-1 dressed mu_full: numerical far-collar extrapolation as a cross-check
    of the symbolic -1/45.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq

q = 1/3; s = q*(1-q)/2

# ---------- (a) numerical Hessian of P at kappa=0.3, F=1 ----------
NC, NP = 120, 64
xc, wc = leggauss(NC)
phg = np.linspace(0, 2*np.pi, NP, endpoint=False); wph = 2*np.pi/NP

def Yfuncs(c, ph):
    sq = np.sqrt
    om = 1-c**2
    return {
      'u':  np.ones_like(c),
      'a0': sq(3/(4*np.pi))*c,
      'a1': sq(3/(4*np.pi))*sq(om)*np.cos(ph),
      'g0': sq(5/(16*np.pi))*(3*c**2-1),
      'g1': sq(15/(4*np.pi))*c*sq(om)*np.cos(ph),
      'g2': sq(15/(16*np.pi))*om*np.cos(2*ph),
      'h2': sq(105/(16*np.pi))*c*om*np.cos(2*ph),
    }

C, PH = np.meshgrid(xc, phg, indexing='ij')
WW = wc[:,None]*wph
YY = Yfuncs(C, PH)
kap0, F0v = 0.3, 1.0

def Pfunc(eps):  # eps dict
    f = F0v*(1+kap0*C) + sum(eps.get(k,0.0)*YY[k] for k in YY)
    # gradients: need df/dc and df/dph of the SUM analytically -> use FD in c,ph?
    # simpler: build f on grid and differentiate spectrally in ph, FD in c is noisy.
    # Instead compute gradient analytically per term:
    dfc = F0v*kap0*np.ones_like(C)
    dfp = np.zeros_like(C)
    sq = np.sqrt; om = 1-C**2
    dYc = {
      'u': 0, 'a0': sq(3/(4*np.pi))*np.ones_like(C),
      'a1': sq(3/(4*np.pi))*(-C/sq(om))*np.cos(PH),
      'g0': sq(5/(16*np.pi))*6*C,
      'g1': sq(15/(4*np.pi))*np.cos(PH)*(sq(om) + C*(-C/sq(om))),
      'g2': sq(15/(16*np.pi))*(-2*C)*np.cos(2*PH),
      'h2': sq(105/(16*np.pi))*np.cos(2*PH)*(om + C*(-2*C)),
    }
    dYp = {
      'u': 0, 'a0': 0,
      'a1': sq(3/(4*np.pi))*sq(om)*(-np.sin(PH)),
      'g0': 0,
      'g1': sq(15/(4*np.pi))*C*sq(om)*(-np.sin(PH)),
      'g2': sq(15/(16*np.pi))*om*(-2*np.sin(2*PH)),
      'h2': sq(105/(16*np.pi))*C*om*(-2*np.sin(2*PH)),
    }
    for k, v in eps.items():
        dfc = dfc + v*dYc[k]
        dfp = dfp + v*dYp[k]
    grad2 = om*dfc**2 + dfp**2/om
    return 0.25*np.sum(WW*grad2/f)

dE = 1e-4
def hess(ki, kj):
    if ki == kj:
        return (Pfunc({ki: dE}) - 2*Pfunc({}) + Pfunc({ki: -dE}))/dE**2
    return (Pfunc({ki: dE, kj: dE}) - Pfunc({ki: dE, kj: -dE})
            - Pfunc({ki: -dE, kj: dE}) + Pfunc({ki: -dE, kj: -dE}))/(4*dE**2)

import sympy as sp
kapS, FS = sp.symbols('kappa F', positive=True)
sym = {  # from s5/s5b output (O(kappa^2) series) -- compare at kappa=0.3 with exact numeric
 ('a0','a0'): (6*kapS**2+5)/(5*FS), ('a1','a1'): (2*kapS**2+5)/(5*FS),
 ('a1','g1'): -sp.sqrt(5)*kapS/(2*FS), ('a0','g0'): -sp.sqrt(15)*kapS/(3*FS),
 ('g0','g0'): (44*kapS**2+63)/(21*FS), ('g1','g1'): 3*(4*kapS**2+7)/(7*FS),
 ('g2','g2'): (4*kapS**2+21)/(7*FS), ('g2','h2'): -5*sp.sqrt(7)*kapS/(7*FS),
 ('h2','h2'): (7*kapS**2+18)/(3*FS),
 ('u','u'): 4*sp.pi*kapS**2/(3*FS), ('u','a0'): -2*sp.sqrt(3)*sp.sqrt(sp.pi)*kapS/(3*FS),
}
print("Hessian validation at kappa=0.3, F=1 (numeric 2nd-diff vs symbolic O(k^2) series):")
ok = 0; tot = 0
for (ki,kj), expr in sym.items():
    vnum = hess(ki,kj)
    vsym = float(expr.subs([(kapS,0.3),(FS,1.0)]))
    rel = abs(vnum-vsym)/max(abs(vsym),1e-12)
    tot += 1
    tag = "PASS" if rel < 2e-2 else "  ?? (O(k^4) terms or error)"
    if rel < 2e-2: ok += 1
    print(f"  V_{ki}{kj}: num={vnum:+.6f} symO2={vsym:+.6f} rel={rel:.2e} {tag}")
print(f"  {ok}/{tot} within 2% (residual = O(kappa^4) truncation at k=0.3)")

# ---------- (b) mu_BO and n_eff over the collar ----------
def H(k):
    L = np.log((1+k)/(1-k)); return (2*k+(k**2-1)*L)/k
def Hp(k):
    L = np.log((1+k)/(1-k)); return ((k**2+1)*L-2*k)/k**2
def Hpp(k):
    L = np.log((1+k)/(1-k)); return 2*(2*k-(1-k**2)*L)/(k**3*(1-k**2))
yy = np.exp(np.linspace(np.log(1e-3), np.log(1e3), 400))
kk = np.array([brentq(lambda k: k*Hp(k)-H(k)-8*s*t**(-q), 1e-10, 1-1e-13, xtol=1e-15) for t in yy])
kp = np.array([-8*s*q*t**(-q-1)/(k*Hpp(k)) for t,k in zip(yy,kk)])
muBO = 3*yy**2*kp**2/(3+kk**2)**2
neff = 1-muBO/(2*s)
imax = np.argmax(muBO)
print(f"\nmu_BO over y in [1e-3,1e3]: max = {muBO[imax]:.6e} at y = {yy[imax]:.4f} (kappa={kk[imax]:.4f})")
print(f"n_eff^BO range: [{neff.min():.6f}, {neff[-1]:.8f}) ; N1 claim: [0.993, 1)")
print(f"mu_BO(y=1) = {np.interp(1.0, yy, muBO):.6e};  2s = {2*s:.4e}; ratio max(mu_BO)/2s = {muBO[imax]/(2*s):.4f}")
