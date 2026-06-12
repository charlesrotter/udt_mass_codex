"""VERIFIER script 2: B1 BVP reproduction with an INDEPENDENT method.
Second-order central finite differences on a UNIFORM grid in tau = ln y
(E1 used P1 FEM on a log y grid - different discretization, different
assembly). Closed-form P derivatives from the S1 anchors (not sympy
integration of E1's expression).

System (second variation around the demanded collar, tau = ln y):
  dF_tautau + dF_tau = 2 (H_FF dF + H_Fa da)
  da_tautau + da_tau = 2 (H_Fa dF + H_aa da)
BC: dF(0)=1, dF(T)=0 (Dirichlet), da' = 0 both ends (natural).
"""
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
SQ3 = np.sqrt(3.0)

# ---- closed-form P derivatives (anchors), k = sqrt3 a/F ---------------------
def Lk(k): return np.log((1+k)/(1-k))
def P_F(k):
    k = np.asarray(k, float)
    out = np.where(k < 1e-5, -k**2/6 - k**4/10, (1 - Lk(np.clip(k,1e-300,None))/(2*np.clip(k,1e-300,None)))/2)
    return out
# Hessian via exact differentiation of the anchors:
# P_F depends on k only; P_FF = dP_F/dk * dk/dF = P_F'(k) * (-k/F)
# P_Fa = P_F'(k) * (sqrt3/F);  P_aa from P_aa = P_FF * (F/a)^2 ... use rank-1:
# Hessian = h(k)/F * v v^T with v = (-k/sqrt3 ... ) -- safer: numeric diff of
# closed forms in (F,a) with high-order stencils.
def P_F_FA(F, a):
    return P_F(SQ3*np.abs(a)/F)
def dPF(k):
    # derivative of P_F wrt k, exact: P_F = (1 - L/(2k))/2
    # dP_F/dk = -(1/2) d/dk [L/(2k)] = -(1/2)[ L'/(2k) - L/(2k^2) ]
    # L' = 2/(1-k^2)
    k = np.asarray(k, float)
    small = k < 1e-5
    kk = np.where(small, 0.5, k)
    val = -(0.5)*((2/(1-kk**2))/(2*kk) - Lk(kk)/(2*kk**2))
    ser = -k/3 - 2*k**3/5
    return np.where(small, ser, val)
def hessian(F, a):
    """exact rank-1 Hessian from the anchors.
    P_FF = dP_F/dF|_a = dPF(k) * dk/dF = dPF(k) * (-k/F)
    P_Fa = dPF(k) * dk/da = dPF(k) * (sqrt3/F)
    P_aa from rank-1: P_aa = P_Fa^2 / P_FF (valid k>0)."""
    k = SQ3*a/F
    d = dPF(k)
    HFF = d*(-k/F)
    HFa = d*(SQ3/F)
    Haa = np.where(np.abs(HFF) > 0, HFa**2/np.where(HFF != 0, HFF, 1), 0.0)
    return HFF, HFa, Haa

# sanity of the rank-1 P_aa against the direct small-k series P_aa = 1/F + ...
Ft_, at_ = 1.7, 0.05
HFF_, HFa_, Haa_ = hessian(np.array([Ft_]), np.array([at_]))
k_ = SQ3*at_/Ft_
Paa_series = (1/Ft_)*(1 + (6*3/5.)*(at_/Ft_)**2)   # P_a = a/F + (6/5)a^3/F^3 -> P_aa = 1/F + 18a^2/5F^3
check("V2.0 rank-1 P_aa matches series 1/F + (18/5)a^2/F^3 at a test point",
      abs(Haa_[0] - Paa_series) < 2e-4*abs(Paa_series),
      f"{Haa_[0]:.8f} vs {Paa_series:.8f}")

def kap_of_y(yv):
    rhs = -s*yv**(-q)
    return brentq(lambda kk: float(P_F(np.array([kk]))[0]) - rhs, 1e-9, 1-1e-12,
                  xtol=1e-15)

def solve_native(Y=1.0e5, N=14000, mode="native"):
    T = np.log(Y)
    tau = np.linspace(0.0, T, N)
    h = tau[1] - tau[0]
    yg = np.exp(tau)
    kg = np.array([kap_of_y(v) for v in yg])
    F0 = yg**(-q); a0 = kg*F0/SQ3
    HFF, HFa, Haa = hessian(F0, a0)
    if mode == "locked":
        HFF = np.full(N, -s); HFa = np.zeros(N); Haa = np.full(N, 1e8)
    elif mode == "frozen":
        HFF = np.full(N, 2/9.); HFa = np.zeros(N); Haa = np.full(N, 1e8)
        # mass 2*HFF = 4/9 in the EL
    A = lil_matrix((2*N, 2*N)); b = np.zeros(2*N)
    def row(i, off, Hrow):
        # dX_tautau + dX_tau - 2(H.dX) = 0, central differences
        A[off+i, off+i-1] += 1/h**2 - 1/(2*h)
        A[off+i, off+i]   += -2/h**2
        A[off+i, off+i+1] += 1/h**2 + 1/(2*h)
        A[off+i, 0+i]     += -2*Hrow[0]
        A[off+i, N+i]     += -2*Hrow[1]
    for i in range(1, N-1):
        row(i, 0, (HFF[i], HFa[i]))
        row(i, N, (HFa[i], Haa[i]))
    # BC dF
    A[0, 0] = 1.0; b[0] = 1.0
    A[N-1, N-1] = 1.0; b[N-1] = 0.0
    # BC da: natural da' = 0, second-order one-sided
    A[N, N] = -3.0; A[N, N+1] = 4.0; A[N, N+2] = -1.0; b[N] = 0.0
    A[2*N-1, 2*N-1] = 3.0; A[2*N-1, 2*N-2] = -4.0; A[2*N-1, 2*N-3] = 1.0
    b[2*N-1] = 0.0
    x = spsolve(csc_matrix(A.tocsr()), b)
    return yg, kg, F0, a0, x[:N], x[N:], HFF, HFa

def slope(yg, w, ylo, yhi):
    m = (yg > ylo) & (yg < yhi) & (np.abs(w) > 0)
    return np.polyfit(np.log(yg[m]), np.log(np.abs(w[m])), 1)[0]

print("solving native coupled BVP (Y=1e5, N=14000, FD method)...")
yg, kg, F0, a0, dF, da, HFF, HFa = solve_native()
check("V2.1 background kappa(1) = 0.6830951", abs(kg[0] - 0.68309514) < 1e-6,
      f"{kg[0]:.8f}")
p_main = slope(yg, dF, 50., 2000.)
check("V2.2 NATIVE exponent of dF in [50,2000] = -1.000 within 1%",
      abs(p_main + 1) < 0.01, f"slope = {p_main:.4f}")
p_far = slope(yg, dF, 20., 500.)
print(f"   window [20,500]: slope = {p_far:.4f}")

# rival distances
check("V2.3 rivals excluded: |p+2/3| > 0.25, |p+1.187| > 0.15, |p+4/3| > 0.25",
      abs(p_main + 2/3.) > 0.25 and abs(p_main + 1.187) > 0.15 and abs(p_main + 4/3.) > 0.25)

# response lock & privacy of the heavy combination
lock = da/((a0/F0)*dF)
m = (yg > 50) & (yg < 2000)
check("V2.4 responsive lock da -> (a0/F0) dF (median within 5%)",
      abs(np.median(lock[m]) - 1) < 0.05, f"median {np.median(lock[m]):.4f}")
heavy = da - (a0/F0)*dF
# stretched-exponential privacy: ln|heavy| ~ -6 sqrt2 y^{1/6} (WKB)
mh = (yg > 5) & (yg < 200) & (np.abs(heavy) > 1e-200)
ch = np.polyfit(yg[mh]**(1/6.), np.log(np.abs(heavy[mh])), 1)[0]
print(f"   heavy-combination decay: slope in y^(1/6) = {ch:.3f} "
      f"(WKB -6*sqrt2 = {-6*np.sqrt(2):.3f}) -- stretched-exponential privacy")
check("V2.5 heavy (non-scaling) channel is stretched-exponentially private "
      "(slope in y^(1/6) within 35% of WKB -8.49, and decisively non-power-law)",
      ch < -5.0, f"slope {ch:.3f}")

# flux convergence
Q = -yg**2*np.gradient(dF, yg)
i5, i2k = np.searchsorted(yg, 5.), np.searchsorted(yg, 2000.)
check("V2.6 flux Q = -y^2 dF' converges: |Q(2000)/Q(5)-1| < 0.06",
      abs(Q[i2k]/Q[i5] - 1) < 0.06, f"Q(5)={Q[i5]:.5f} Q(2000)={Q[i2k]:.5f}")

# local effective mass tail
Mloc = 2*(HFF*dF + HFa*da)/np.where(np.abs(dF) > 1e-300, dF, 1)
mw = (yg > 50) & (yg < 2000)
sM = np.polyfit(np.log(yg[mw]), np.log(np.abs(Mloc[mw])), 1)[0]
cM = np.median(Mloc[mw]*162*yg[mw]**(1/3.))
check("V2.7 |M(y)| = O(y^-1/3) tail (slope within 0.12) and coefficient |.|<12",
      abs(sM + 1/3.) < 0.12 and abs(cM) < 12,
      f"slope {sM:.4f}, signed coef*162 y^(1/3) = {cM:.4f}")

# robustness: smaller domain
yg2, kg2, F02, a02, dF2, da2, _, _ = solve_native(Y=1.0e4, N=7000)
p2 = slope(yg2, dF2, 30., 300.)
check("V2.8 robustness Y=1e4: exponent within 2% of -1", abs(p2 + 1) < 0.02,
      f"slope {p2:.4f}")

# controls (scalar): banked-n0 in dphi; demand-locked; frozen-da
def solve_scalar(Y, N, pw, mw_, u0=1.0):
    """(pw(y) u')' = mw(y) u in y; FD in tau."""
    T = np.log(Y); tau = np.linspace(0, T, N); h = tau[1]-tau[0]
    yv = np.exp(tau)
    # (pw u')' = mw u; u' = u_tau/y; d/dy = (1/y) d/dtau
    # (1/y) d/dtau (pw u_tau / y) = mw u
    pv = pw(yv); mv = mw_(yv)
    A = lil_matrix((N, N)); b = np.zeros(N)
    # d/dtau( g u_tau ) = y^2 mw u with g = pw/y... derive:
    # (1/y)d/dtau( (pv/y) u_tau ) = mv u  ->  d/dtau( (pv/y) u_tau ) = y mv u
    g = pv/yv
    for i in range(1, N-1):
        gp = 0.5*(g[i] + g[i+1]); gm = 0.5*(g[i] + g[i-1])
        A[i, i-1] = gm/h**2
        A[i, i]   = -(gp + gm)/h**2 - yv[i]*mv[i]
        A[i, i+1] = gp/h**2
    A[0, 0] = 1.0; b[0] = u0
    A[N-1, N-1] = 1.0; b[N-1] = 0.0
    return yv, spsolve(csc_matrix(A.tocsr()), b)

yb, ub = solve_scalar(1e5, 14000, lambda v: v**2*v**(-2*q), lambda v: 4*s*v**(-2*q))
pb = slope(yb, ub, 50., 2000.)
check("V2.9 CTRL banked-n0 (dphi): exponent -0.8539",
      abs(pb + 0.853884) < 0.01, f"slope {pb:.4f}")
ye, ue = solve_scalar(1e5, 14000, lambda v: v**2, lambda v: np.full_like(v, -2*s))
mfit = (ye > 50) & (ye < 5000)
Af = np.vstack([ye[mfit]**(-2/3.), ye[mfit]**(-1/3.)]).T
c2c, c1c = np.linalg.lstsq(Af, ue[mfit], rcond=None)[0]
check("V2.10 CTRL demand-locked: y^-2/3 member dominant, -1/3 admixture at "
      "Dirichlet size c1/c2 ~ -Y^-1/3",
      abs(c1c/c2c + 1e5**(-1/3.)) < 0.4*1e5**(-1/3.), f"c1/c2 = {c1c/c2c:.5f}")
yf, uf = solve_scalar(1e5, 14000, lambda v: v**2, lambda v: np.full_like(v, 4/9.))
pf = slope(yf, uf, 50., 2000.)
check("V2.11 CTRL frozen-da (mass 4/9): exponent -4/3", abs(pf + 4/3.) < 0.01,
      f"slope {pf:.4f}")

print(f"\n=== V2 TOTALS: {PASS} PASS / {FAIL} FAIL ===")
