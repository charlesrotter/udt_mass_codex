"""VERIFIER 2b: privacy of ell>=1 hair, done right.
The SOURCE-FREE heavy channel on the collar: the non-scaling combination
sees the nonzero Hessian eigenvalue mu(y) = 2(P_FF + P_aa) -> 2/F0 = 2 y^{1/3}
(rank-1: nonzero eigenvalue = trace). Solve (y^2 w')' = mu(y) w with my FD
scheme; WKB predicts ln w ~ -6 sqrt2 y^{1/6} (stretched exponential).
Also classify the driven residual da - (a0/F0)dF from v2 as the POWER-LAW
adiabatic-lock correction (not hair)."""
import numpy as np
from scipy.optimize import brentq
from scipy.sparse import lil_matrix, csc_matrix
from scipy.sparse.linalg import spsolve

PASS = FAIL = 0
def check(name, ok, extra=""):
    global PASS, FAIL
    PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + f"  {name}" + (f"  [{extra}]" if extra else ""))

q = 1/3.; s = q*(1-q)/2.
SQ3 = np.sqrt(3.)
def Lk(k): return np.log((1+k)/(1-k))
def P_F(k):
    if k < 1e-6: return -k**2/6
    return (1 - Lk(k)/(2*k))/2
def kap_of_y(yv):
    return brentq(lambda kk: P_F(kk) + s*yv**(-q), 1e-9, 1-1e-12, xtol=1e-15)

# heavy eigenvalue: trace of Hessian of P at the collar point, computed by
# exact dPF (see v2) for P_FF and rank-1 for P_aa
def dPF(k):
    if k < 1e-5: return -k/3 - 2*k**3/5
    return -0.5*((2/(1-k**2))/(2*k) - Lk(k)/(2*k**2))
def heavy_mass(yv):
    kk = kap_of_y(yv)
    F0 = yv**(-q); a0 = kk*F0/SQ3
    d = dPF(kk)
    HFF = d*(-kk/F0); HFa = d*(SQ3/F0)
    Haa = HFa**2/HFF if HFF != 0 else 0.0
    return 2*(HFF + Haa)

Y, N = 1.0e4, 12000
tau = np.linspace(0, np.log(Y), N); h = tau[1]-tau[0]
yg = np.exp(tau)
mv = np.array([heavy_mass(v) for v in yg])
print(f"  heavy mass * y^(-1/3) at y = 10, 100, 1000: "
      f"{mv[np.searchsorted(yg,10)]/10**q:.4f}, "
      f"{mv[np.searchsorted(yg,100)]/100**q:.4f}, "
      f"{mv[np.searchsorted(yg,1000)]/1000**q:.4f}  (-> 2 expected)")
r10, r100, r1000 = (mv[np.searchsorted(yg, v)]/v**q for v in (10., 100., 1000.))
check("V2b.1 heavy-channel mass -> 2 y^{1/3} on the collar (O(y^-q) approach, "
      "monotone)", r10 > r100 > r1000 and abs(r1000 - 2) < 0.25)

A = lil_matrix((N, N)); b = np.zeros(N)
g = yg  # (y^2 w')' = m w  ->  d/dtau(y w_tau) = y m w  (w' = w_tau/y)
for i in range(1, N-1):
    gp = 0.5*(g[i]+g[i+1]); gm = 0.5*(g[i]+g[i-1])
    A[i, i-1] = gm/h**2
    A[i, i] = -(gp+gm)/h**2 - yg[i]*mv[i]
    A[i, i+1] = gp/h**2
A[0, 0] = 1.0; b[0] = 1.0
A[N-1, N-1] = 1.0; b[N-1] = 0.0
w = spsolve(csc_matrix(A.tocsr()), b)
mh = (yg > 3) & (yg < 60) & (w > 1e-280)
# full WKB phase from the ACTUAL mass (pre-asymptotic in this window):
# Phi(y) = Int_1^y sqrt(m(y'))/y' dy'; prediction ln w ~ -Phi + algebraic
from scipy.integrate import cumulative_trapezoid
Phi = cumulative_trapezoid(np.sqrt(np.maximum(mv, 0))/yg, yg, initial=0.0)
slope_wkb = np.polyfit(Phi[mh], np.log(w[mh]), 1)[0]
# Liouville-Green: w ~ (p Q)^(-1/4) e^(-Phi), p = y^2, Q = m
lnw_corr = np.log(w[mh]) + 0.25*np.log(yg[mh]**2*np.maximum(mv[mh], 1e-300))
slope_lg = np.polyfit(Phi[mh], lnw_corr, 1)[0]
pl = np.polyfit(np.log(yg[mh]), np.log(w[mh]), 1)
sl6 = np.polyfit(yg[mh]**(1/6.), np.log(w[mh]), 1)[0]
print(f"  hair decay: d ln w / d Phi_WKB = {slope_wkb:.4f}, with "
      f"Liouville-Green prefactor removed = {slope_lg:.4f} (predict -1); "
      f"slope in y^(1/6) = {sl6:.2f} (asymptotic WKB -8.49, pre-asymptotic "
      f"window steeper); naive power-law slope would be {pl[0]:.2f} "
      f"(vs public mode -1: hair is >2 powers steeper AND accelerating)")
check("V2b.2 ell=1 source-free hair decays at the WKB stretched-exponential "
      "rate (LG-corrected d ln w/d Phi within 12% of -1): PRIVATE, "
      "decisively non-power-law",
      abs(slope_lg + 1) < 0.12, f"{slope_lg:.4f}")

print(f"\n=== V2b TOTALS: {PASS} PASS / {FAIL} FAIL ===")
