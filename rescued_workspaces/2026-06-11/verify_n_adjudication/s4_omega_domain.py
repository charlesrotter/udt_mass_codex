"""
S4: Frequency domain. (a) exact pointwise elimination at frequency omega;
reproduce N3's kernel bookkeeping; (b) radial-inclusive dynamical Schur at
small omega -> continuity to the static nonlocal Schur; order of limits.

Pointwise (radial terms of the responder DROPPED), probe u at fixed y:
  response: (P_aa - m_a w^2) b = P_aa ktil u  =>  b = ktil u/(1-W), W = m_a w^2/P_aa
  back-reaction kernel on u: K_back = -P_FF/(1-W)        [rank-1: P_Fa^2 = P_FF P_aa]
  TOTAL potential seen by u: K_tot = P_FF + K_back = -P_FF W/(1-W)
  N3's printed kernel: K_N3 = -P_FF^(small-kappa) W^2/(1-W)
  Identity: K_tot + P_FF*W = -P_FF W^2/(1-W)   (i.e. N3 = total minus its O(W) part)

Radial-inclusive: eliminate b from
  int[(1/4)y^2 b'^2 + (1/2)P_aa(b-ktil u)^2 - (1/2)w^2 m_a b^2],  m_a = (1/2)y^2
(time-kinetic convention (1/4) y^2 (da/dt)^2; the w->0 limit is insensitive).
"""
import numpy as np, sympy as sp
from scipy.optimize import brentq
from scipy.sparse import lil_matrix, csc_matrix
from scipy.sparse.linalg import spsolve

# ---------- (a) symbolic bookkeeping identity ----------
PFF, W = sp.symbols('P_FF W', positive=True)
K_tot = -PFF*W/(1-W)
K_N3_struct = -PFF*W**2/(1-W)
print("identity: K_tot + P_FF*W - (-P_FF W^2/(1-W)) =", sp.simplify(K_tot + PFF*W - K_N3_struct))
print("=> N3's W^2/(1-W) kernel == (total pointwise potential) - (its O(W) inertia part).")
print("   total pointwise potential at omega->0: K_tot -> 0  LINEARLY in W (not W^2).")
print("   K_tot(0) = 0 means: bare fixed-amplitude jet P_FF is EXACTLY cancelled by the")
print("   static response (rank-1 screening). The probe sees ZERO total potential, i.e.")
print("   the mu=0 / n=1 family value -- NOT an unchanged n=0 bare operator.")

# coefficient check at the demanded amplitude
q = 1.0/3.0; s = q*(1-q)/2.0
def H(k):
    L = np.log((1+k)/(1-k)); return (2*k+(k**2-1)*L)/k
def Hp(k):
    L = np.log((1+k)/(1-k)); return ((k**2+1)*L-2*k)/k**2
def Hpp(k):
    L = np.log((1+k)/(1-k)); return 2*(2*k-(1-k**2)*L)/(k**3*(1-k**2))
k1 = brentq(lambda k: k*Hp(k)-H(k)-8*s, 1e-8, 1-1e-12)
print(f"\nP_FF exact = (pi/2) kappa^2 H'' y^q ; N3 coefficient (4pi/3) kappa^2 y^q (small-kappa)")
print(f"at demanded kappa(1) = {k1:.6f}: exact/N3 = (3/8)H'' = {0.375*Hpp(k1):.4f}")
print("=> N3's kernel coefficient understates the exact one by ~2.1x at the demanded amplitude")
print("   (small-kappa Hessian used at non-small kappa); the W^2/(1-W) STRUCTURE itself is")
print("   exact at every amplitude (rank-1), with P_FF the exact entry.")

# ---------- (b) radial-inclusive dynamical Schur, w -> 0 ----------
def demand_k(y): return brentq(lambda k: k*Hp(k)-H(k)-8*s*y**(-q), 1e-8, 1-1e-12, xtol=1e-15)
def kappa_prime(y, k): return -8*s*q*y**(-q-1)/(k*Hpp(k))

ylo, yhi, N = 0.05, 5.0, 6000
yg = np.exp(np.linspace(np.log(ylo), np.log(yhi), N))
kg = np.array([demand_k(t) for t in yg])
kpg = np.array([kappa_prime(t,k) for t,k in zip(yg,kg)])
ktil = np.sqrt(4*np.pi/3)*kg
Paa = (3/8)*np.array([Hpp(k) for k in kg])*yg**q
ptil = 1+kg**2/3
w = np.ones(N); wp = np.zeros(N)         # SL probe w=1
u = w/np.sqrt(ptil)
up = -u*(kg*kpg/3)/ptil

ym = 0.5*(yg[1:]+yg[:-1]); hy = np.diff(yg)
def mid(f): return 0.5*(f[1:]+f[:-1])
m_a = 0.5*yg**2

def E_pointwise(om2):
    Wf = om2*m_a/Paa
    integ = 0.5*Paa*ktil**2*u**2*(-Wf/(1-Wf))   # total potential energy for probe
    return np.sum(mid(integ)*hy)

def E_radial(om2):
    A = lil_matrix((N,N)); Pm = mid(Paa); Mm = mid(m_a)
    for e in range(N-1):
        h = hy[e]; kc = (ym[e]**2/2.0)/h
        A[e,e]+=kc; A[e+1,e+1]+=kc; A[e,e+1]-=kc; A[e+1,e]-=kc
        mc = (Pm[e]-om2*Mm[e])*h
        A[e,e]+=mc/3; A[e+1,e+1]+=mc/3; A[e,e+1]+=mc/6; A[e+1,e]+=mc/6
    # linear term from -(P_aa ktil u) b : c_i = -int Paa ktil u phi_i
    src = Paa*ktil*u; srcm = mid(src)
    cvec = np.zeros(N)
    for e in range(N-1):
        cvec[e]   += -srcm[e]*hy[e]/2
        cvec[e+1] += -srcm[e]*hy[e]/2
    b = spsolve(csc_matrix(A.tocsr()), -cvec)
    quad = 0.5*b@(A@b) + cvec@b
    const = np.sum(mid(0.5*Paa*ktil**2*u**2)*hy)
    return quad + const

int_w2 = np.sum(mid(w**2)*hy)
print("\nradial-INCLUSIVE vs pointwise dressed potential, probe w=1 (units: mu_hat = E/(pi int w^2)):")
print(f"{'om^2':>10s} {'mu_hat radial-incl':>20s} {'mu_hat pointwise':>18s}")
for om2 in [0.0, 1e-4, 1e-3, 1e-2, 3e-2]:
    Er = E_radial(om2); Ep = E_pointwise(om2)
    print(f"{om2:10.1e} {Er/(np.pi*int_w2):20.6e} {Ep/(np.pi*int_w2):18.6e}")
print(f"\n[2s = {2*s:.6e}; static nonlocal Schur (S3, w=1) = 9.81e-04]")
print("=> lim_{om->0} radial-inclusive = static nonlocal Schur (kinetic lifting), NONZERO;")
print("   lim_{om->0} pointwise = 0 exactly. The two limits differ by the kinetic lifting.")
