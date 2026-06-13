"""
offdiagIII_sealbound.py
=======================
Question (METRIC-LED, anti-invention): can the seal AREA-FORM / boundary
transgression (registry #36) enter the angular fluctuation operator as MORE
THAN a boundary condition -- i.e. can it BOUND BELOW a BULK wrong-sign 2nd-order
angular Laplacian (the K_th<0 unbounded-below pathology of registry #38 /
offdiagII_verifier_results.md)?

#36's own words: the structure is d ln f ^ omega_H1 = d[(ln f) omega_H1], an
EXACT BOUNDARY TRANSGRESSION, "invisible to the bulk EL", delivered AT THE
CLOSURE. #37: it is sigma-EVEN, r/theta/phi/f/omega_H1 all sigma-invariant;
dynamics-invisible because EXACT (not by parity).

CLAIM UNDER TEST: a pure boundary term (even maximal = Dirichlet) cannot bound
a BULK wrong-sign Laplacian, because the unbounded-below pathology is driven by
high-frequency BULK modes in the K_th<0 interior band, which vanish at the
boundary and are thus untouched by any endpoint penalty.

We reproduce a minimal 1D analogue of the angular bilinear form
    a(u,u) = INT_0^pi K_th(th) (u')^2 sin(th) dth   (self-adjoint weight W=sin th)
with K_th NEGATIVE over an extended equator-peaked interior band (as the
records describe), and the L2 mass m(u,u)=INT u^2 sin th dth. We solve the
generalized eigenproblem a u = lam m u and watch lam0 under refinement, with
and without a boundary penalty alpha*(u(0)^2+u(pi)^2).
"""
import numpy as np
import sys

LOG = open("/tmp/offdiagIII_sealbound.log", "w")
def out(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()

# ----- model K_th(theta): extended equator-peaked NEGATIVE band -----
# Records: K_th<0 over extended interior, min at equator, +/- outside.
def K_th(theta, Kneg=-5.0, Kpos=1.0, lo=0.3*np.pi, hi=0.7*np.pi):
    return np.where((theta >= lo) & (theta <= hi), Kneg, Kpos)

W = lambda th: np.sin(th)   # bare self-adjoint angular measure (#38 tooling fix: bare sin)

# =====================================================================
# Discretization A: continuous-P1 FEM on [0,pi], nodes u_0..u_N.
# a(u,u) = sum_elements INT K_th (u')^2 sin th ;   m = INT u^2 sin th.
# Boundary penalty adds alpha to A[0,0] and A[N,N]  (== alpha*u(0)^2+alpha*u(pi)^2).
# alpha -> inf  is the Dirichlet limit (the MOST GENEROUS #36-consistent boundary term).
# =====================================================================
from numpy.polynomial.legendre import leggauss
GP, GW = leggauss(4)   # 4-pt Gauss on [-1,1]

def assemble_P1(N, alpha=0.0):
    nodes = np.linspace(0.0, np.pi, N + 1)
    A = np.zeros((N + 1, N + 1))
    M = np.zeros((N + 1, N + 1))
    for e in range(N):
        a0, a1 = nodes[e], nodes[e + 1]
        h = a1 - a0
        # map gauss pts
        th = 0.5 * (a1 - a0) * GP + 0.5 * (a1 + a0)
        wq = 0.5 * h * GW
        Kq = K_th(th)
        Wq = W(th)
        # P1 shape fns on element: phi0=(a1-th)/h, phi1=(th-a0)/h
        dphi = np.array([-1.0 / h, 1.0 / h])           # constant grads
        ph0 = (a1 - th) / h
        ph1 = (th - a0) / h
        phi = np.array([ph0, ph1])                      # (2, nq)
        idx = [e, e + 1]
        for i in range(2):
            for j in range(2):
                # stiffness: INT K (dphi_i)(dphi_j) W
                A[idx[i], idx[j]] += np.sum(wq * Kq * Wq) * dphi[i] * dphi[j]
                # mass: INT phi_i phi_j W
                M[idx[i], idx[j]] += np.sum(wq * Wq * phi[i] * phi[j])
    # boundary penalty (the maximal #36-consistent endpoint term)
    A[0, 0] += alpha
    A[N, N] += alpha
    return A, M

def lam0_P1(N, alpha=0.0):
    A, M = assemble_P1(N, alpha)
    from scipy.linalg import eigh
    w = eigh(A, M, eigvals_only=True)
    return w[0]

# =====================================================================
# Discretization B: global spectral sine-Galerkin on [0,pi].
# Basis b_k(th)=sin(k th), k=1..Nmode  -> AUTOMATICALLY vanishes at 0 and pi
# (this IS the Dirichlet / alpha->inf space: every basis fn is zero at the
# endpoints, so NO boundary penalty can act -- the cleanest proof that the
# interior modes are untouched by any endpoint term).
# =====================================================================
def lam0_sine(Nmode, nq=4000):
    th = np.linspace(0, np.pi, nq)
    dth = th[1] - th[0]
    Kq = K_th(th); Wq = W(th)
    ks = np.arange(1, Nmode + 1)
    B = np.sin(np.outer(ks, th))        # (Nmode, nq)
    dB = ks[:, None] * np.cos(np.outer(ks, th))
    # A_ij = INT K dB_i dB_j W ;  M_ij = INT B_i B_j W   (trapezoid)
    def quad(fI, fJ, weight):
        integ = fI[:, None, :] * fJ[None, :, :] * weight[None, None, :]
        return np.trapz(integ, dx=dth, axis=2)
    A = quad(dB, dB, Kq)
    M = quad(B, B, Wq)
    from scipy.linalg import eigh
    w = eigh(A, M, eigvals_only=True)
    return w[0]

# =====================================================================
out("="*72)
out("offdiagIII: does the #36 boundary transgression bound the bulk K_th<0 op?")
out("="*72)
out("K_th model: -5 on [0.3pi,0.7pi] (extended equator band), +1 outside; W=sin th")
out("")

out("--- TEST 1: P1 FEM, NO boundary term (alpha=0) : reproduce the pathology")
for N in [40, 80, 160, 320, 640]:
    l = lam0_P1(N, alpha=0.0)
    out(f"   N={N:5d}   lam0 = {l: .4e}   lam0*dth^2 = {l*(np.pi/N)**2: .4e}")

out("")
out("--- TEST 2: P1 FEM WITH boundary penalty (the maximal #36-consistent term)")
for alpha in [1.0, 1e2, 1e4, 1e8]:
    out(f"   alpha = {alpha:.0e}  (alpha->inf == Dirichlet, the MOST GENEROUS endpoint term)")
    for N in [40, 80, 160, 320, 640]:
        l = lam0_P1(N, alpha=alpha)
        out(f"      N={N:5d}   lam0 = {l: .4e}")

out("")
out("--- TEST 3: sine-Galerkin (every basis fn ALREADY vanishes at 0,pi =")
out("    the Dirichlet/alpha->inf space; boundary penalty has literally nothing")
out("    to act on). If lam0 -> -inf here, the pathology is purely interior.")
for Nm in [16, 32, 64, 128, 256]:
    l = lam0_sine(Nm)
    out(f"   Nmode={Nm:4d}   lam0 = {l: .4e}   lam0/Nmode^2 = {l/Nm**2: .4e}")

out("")
out("--- CONTROL: flip K_th POSITIVE everywhere (K=+1) -> must converge to FINITE +")
def K_pos(theta): return np.ones_like(theta)
_orig = K_th.__defaults__
# monkeypatch via closure: rebuild assemble with positive K
def lam0_P1_pos(N):
    nodes = np.linspace(0.0, np.pi, N + 1)
    A = np.zeros((N + 1, N + 1)); M = np.zeros((N + 1, N + 1))
    for e in range(N):
        a0, a1 = nodes[e], nodes[e+1]; h=a1-a0
        th = 0.5*(a1-a0)*GP + 0.5*(a1+a0); wq=0.5*h*GW
        Kq = np.ones_like(th); Wq=W(th)
        dphi=np.array([-1/h,1/h]); ph0=(a1-th)/h; ph1=(th-a0)/h; phi=np.array([ph0,ph1])
        idx=[e,e+1]
        for i in range(2):
            for j in range(2):
                A[idx[i],idx[j]] += np.sum(wq*Kq*Wq)*dphi[i]*dphi[j]
                M[idx[i],idx[j]] += np.sum(wq*Wq*phi[i]*phi[j])
    from scipy.linalg import eigh
    return eigh(A,M,eigvals_only=True)[0]
for N in [40,80,160,320,640]:
    out(f"   N={N:5d}   lam0(K>0 control) = {lam0_P1_pos(N): .6f}")

out("")
out("="*72)
out("DONE.")
LOG.close()
