"""
S3: EXACT static nonlocal Schur elimination of the responding amplitude,
numerically, on the demanded background. Decisive computation.

Q[u,b] = int dy [ pi y^2 u'^2 + (1/4) y^2 b'^2 + (1/2) P_aa (b - ktil u)^2 ]
P_aa = (3/8) H''(kappa) y^q ;  ktil = sqrt(4pi/3) kappa(y);
demand: kappa H' - H = 8 s y^-q  (verified S1, reproduces kappa(1)=0.683095).

Substitute b = ktil u + xi, minimize exactly over xi (P1 FEM):
Q_min[u] = pi*int y^2 u'^2 + (1/4)int y^2 ((ktil u)')^2  - (1/2) c^T A^{-1} c
with (1/2)xi^T A xi = int[(1/4) y^2 xi'^2 + (1/2)P_aa xi^2],
c_i = (1/2) int y^2 (ktil u)' phi_i' dy.

Probe in SL variables: u = w/sqrt(ptil), ptil = 1+kappa^2/3.
Effective mass functional:  Qt[w] = Q_min[u] - pi int y^2 w'^2 dy  ==  pi int mu_eff w^2 (local approx)
Compare mu_hat = Qt[w]/(pi int w^2) against candidates:
  (a) 2s = 2/9          [n=0, banked weld]
  (b) 0                 [n=1 exact]
  (c) mu_BO = 3 y^2 kappa'^2/(3+kappa^2)^2   [N1 kinetic lifting]
"""
import numpy as np
from scipy.optimize import brentq
from scipy.sparse import lil_matrix, csc_matrix
from scipy.sparse.linalg import spsolve

q = 1.0/3.0
s = q*(1-q)/2.0   # = 1/9
twos = 2*s

def H(k):
    L = np.log((1+k)/(1-k))
    return (2*k + (k**2-1)*L)/k
def Hp(k):
    # sympy-derived exact: H' = ((k^2+1)L - 2k)/k^2
    L = np.log((1+k)/(1-k))
    return ((k**2+1)*L - 2*k)/k**2
def Hpp(k):
    # sympy-derived exact: H'' = 2(2k - (1-k^2)L)/(k^3 (1-k^2))
    L = np.log((1+k)/(1-k))
    return 2*(2*k - (1-k**2)*L)/(k**3*(1-k**2))

# sanity vs FD (float-safe step sizes)
for kk in [0.3, 0.683095, 0.9]:
    h = 1e-6
    assert abs(Hp(kk) - (H(kk+h)-H(kk-h))/(2*h)) < 1e-6, (kk, 'Hp')
    h = 1e-4
    assert abs(Hpp(kk) - (H(kk+h)-2*H(kk)+H(kk-h))/h**2) < 1e-4, (kk, 'Hpp')
assert abs(Hpp(0.683095) - 5.5927943/ (5.5927943/Hpp(0.683095))) < 1e-6
print("H'/H'' analytic forms: PASS vs finite differences; H''(0.683095)=%.6f" % Hpp(0.683095))

def demand_k(y):
    rhs = 8*s*y**(-q)
    f = lambda k: k*Hp(k) - H(k) - rhs
    return brentq(f, 1e-8, 1-1e-12, xtol=1e-15)

def kappa_prime(y, k):
    # implicit: d/dk(kH'-H) = k H'' ; rhs' = -8 s q y^{-q-1}
    return -8*s*q*y**(-q-1)/(k*Hpp(k))

def build_background(ylo, yhi, N):
    yg = np.exp(np.linspace(np.log(ylo), np.log(yhi), N))
    kg = np.array([demand_k(t) for t in yg])
    kpg = np.array([kappa_prime(t, k) for t, k in zip(yg, kg)])
    return yg, kg, kpg

def mu_BO(yg, kg, kpg):
    return 3*yg**2*kpg**2/(3+kg**2)**2

def exact_schur_muhat(yg, kg, kpg, w, wp, xi_bc='natural'):
    """Return (Qt, int_w2, kinetic check pieces). w, wp given on nodes."""
    N = len(yg)
    ktil = np.sqrt(4*np.pi/3)*kg
    ktilp = np.sqrt(4*np.pi/3)*kpg
    Paa = (3.0/8.0)*np.array([Hpp(k) for k in kg])*yg**q
    ptil = 1+kg**2/3
    u = w/np.sqrt(ptil)
    # u' = w'/sqrt(ptil) - w * (kappa kappa'/3) / ptil^{3/2}
    up = wp/np.sqrt(ptil) - w*(kg*kpg/3)/ptil**1.5
    v = ktil*u                      # response profile (rigid part)
    vp = ktilp*u + ktil*up
    # element midpoint quadrature
    ym = 0.5*(yg[1:]+yg[:-1]); hy = np.diff(yg)
    def mid(f): return 0.5*(f[1:]+f[:-1])
    # FEM matrices for xi: (1/2)xi^T A xi = int[(1/4)y^2 xi'^2 + (1/2)Paa xi^2]
    # element stiffness coeff: (1/2) y^2 evaluated at midpoint -> A_kin elem = (ym^2/2)/h * [[1,-1],[-1,1]]
    A = lil_matrix((N, N))
    Pm = mid(Paa)
    for e in range(N-1):
        h = hy[e]; kcoef = (ym[e]**2/2.0)/h
        A[e, e] += kcoef; A[e+1, e+1] += kcoef
        A[e, e+1] -= kcoef; A[e+1, e] -= kcoef
        # mass: int Paa xi^2 over elem, consistent P1 mass matrix with midpoint coeff
        mcoef = Pm[e]*h
        A[e, e] += mcoef/3.0; A[e+1, e+1] += mcoef/3.0
        A[e, e+1] += mcoef/6.0; A[e+1, e] += mcoef/6.0
    # linear term: c_i = (1/2) int y^2 v' phi_i' dy  (phi_i' = +-1/h on elems)
    c = np.zeros(N)
    vpm = mid(vp)
    for e in range(N-1):
        h = hy[e]
        val = 0.5*ym[e]**2*vpm[e]   # (1/2) y^2 v' at midpoint
        c[e] += -val               # phi_e' = -1/h, times h
        c[e+1] += val
    if xi_bc == 'dirichlet':
        idx = np.arange(1, N-1)
        Ar = csc_matrix(A.tocsr()[np.ix_(idx, idx)])
        xi = np.zeros(N)
        xi[idx] = spsolve(Ar, -c[idx])
    else:
        xi = spsolve(csc_matrix(A.tocsr()), -c)
    Jmin = 0.5*xi@(A@xi) + c@xi    # = -(1/2) c A^-1 c
    # energies (midpoint quadrature)
    E_kin_u = np.sum(np.pi*ym**2*mid(up)**2*hy)
    E_v = np.sum(0.25*ym**2*mid(vp)**2*hy)
    E_w = np.sum(np.pi*ym**2*mid(wp)**2*hy)
    Qt = E_kin_u + E_v + Jmin - E_w
    int_w2 = np.sum(mid(w**2)*hy)
    return Qt, int_w2, Jmin, E_v

def report(ylo, yhi, N=6000):
    yg, kg, kpg = build_background(ylo, yhi, N)
    muBO = mu_BO(yg, kg, kpg)
    print(f"\n--- domain y in [{ylo}, {yhi}], N={N} ---")
    print(f"kappa range: [{kg.min():.6f}, {kg.max():.6f}]")
    # probe set: wide gaussian bumps (SL variable w), and w=1
    probes = []
    # w == 1 (pure mass probe; w'=0 so NO kinetic subtraction error)
    probes.append(('w=1 natural', np.ones(len(yg)), np.zeros(len(yg)), 'natural'))
    for (c0, rel) in [(0.3,0.25),(0.6,0.3),(1.0,0.4),(2.0,0.4)]:
        if c0 < ylo*1.5 or c0 > yhi/1.5: continue
        wdt = rel*c0
        w = np.exp(-((yg-c0)/wdt)**2)
        wp = -2*(yg-c0)/wdt**2*w
        probes.append((f'bump@{c0} (width {wdt:.2f})', w, wp, 'natural'))
    for name, w, wp, bc in probes:
        Qt, iw2, Jmin, Ev = exact_schur_muhat(yg, kg, kpg, w, wp, bc)
        mu_hat = Qt/(np.pi*iw2)
        # candidate averages weighted by w^2
        ym = 0.5*(yg[1:]+yg[:-1]); hy = np.diff(yg)
        wm2 = (0.5*(w[1:]+w[:-1]))**2
        mu_bo_avg = np.sum(0.5*(muBO[1:]+muBO[:-1])*wm2*hy)/np.sum(wm2*hy)
        print(f"  {name:26s} mu_hat = {mu_hat:+.6e} | BO avg = {mu_bo_avg:.6e} | 2s = {twos:.6e} | ratio mu/BO = {mu_hat/mu_bo_avg:+.4f} | n_eff = {1-mu_hat/twos:.6f}")
    # BC robustness on one bump
    for name, w, wp, bc in probes[1:2]:
        Qt, iw2, _, _ = exact_schur_muhat(yg, kg, kpg, w, wp, 'dirichlet')
        print(f"  [BC check] {name} dirichlet-xi: mu_hat = {Qt/(np.pi*iw2):+.6e}")

report(0.05, 5.0)
report(0.5, 50.0)
# convergence check
for N in (1500, 3000, 6000, 12000):
    yg, kg, kpg = build_background(0.05, 5.0, N)
    w = np.exp(-((yg-0.6)/0.18)**2); wp = -2*(yg-0.6)/0.18**2*w
    Qt, iw2, _, _ = exact_schur_muhat(yg, kg, kpg, w, wp)
    print(f"N={N}: bump@0.6 mu_hat = {Qt/(np.pi*iw2):+.8e}")
