#!/usr/bin/env python3
"""
INDEPENDENT VERIFIER: breathing/fluctuation Hessian spectrum of a hedgehog
soliton at deep core depth, computed in mpmath (dps>=50) because float64
gives spurious negative omega^2 deep due to e^{3phi} conditioning.

DATA-BLIND: no empirical masses loaded; only the model's intrinsic numbers.

QUESTION: does deepening the metric core EVER manufacture an EXPONENTIAL
level spacing (E_n ~ e^{c n} with c>>1), or does spacing stay O(1) and
saturate?

Built from scratch from the FROZEN reduced 1D energy functional in the
task spec; existing lepton_soliton_spectrum*.py NOT read.

Model (xi=kappa=1):
  E[Theta] = int_{r_core}^{r_int} [ a(r,Theta) Theta'^2 + b(r,Theta) ] dr
  a = (2pi/3) e^{-phi} [ r^2 sin^2 Th + 2 r^2 + 2 sin^4 Th + 2 sin^2 Th ]
  b = (2pi/3) e^{-phi} [ 4 e^{2phi} sin^2 Th + e^{2phi} sin^4 Th / r^2 ]
  phi(r) = -p ln(r_int/r),  phi'(r) = p/r
  Background depth dial p; phi(r_int)=0, phi(r_core)=-p ln(r_int/r_core).

Ground state: EL BVP, Theta(r_core)=pi, Theta(r_int)=0 (float64 solve_bvp).
Hessian (2nd variation):
  H u = -(d/dr)(2 a u') + V u
  V = a_ThTh Th0'^2 + b_ThTh - d/dr(2 a_Th Th0')
  generalized eigenproblem H u = omega^2 W u, Dirichlet,
  weight W = e^{3phi} r^2.
Hessian eigenproblem solved in mpmath (dps>=50).
"""

import numpy as np
from scipy.integrate import solve_bvp
import mpmath as mp

C = 2.0*np.pi/3.0   # overall prefactor (cancels in ratios; kept for fidelity)

R_CORE = 0.05
CELL_LEN = 14.0
R_INT = R_CORE + CELL_LEN   # 14.05

# ---------------------------------------------------------------------------
# Background phi and derivative (numpy / float64 for ground state)
# ---------------------------------------------------------------------------
def phi_f(r, p):
    return -p*np.log(R_INT/r)

def phip_f(r, p):
    return p/r

# ---------------------------------------------------------------------------
# a, b and their partial derivatives.  Theta-derivatives are partials at fixed
# r; the r-derivative needed for da/dr includes explicit-r, phi(r), and Theta(r)
# dependence.  Below, all expressions are written out symbolically.
#
# Let s = sin(Theta), c = cos(Theta), e = e^{phi}.
#   a = C e^{-1*phi} [ r^2 s^2 + 2 r^2 + 2 s^4 + 2 s^2 ]      (e^{-phi} = 1/e)
#   b = C e^{-phi} [ 4 e^{2phi} s^2 + e^{2phi} s^4 / r^2 ]
#     = C e^{phi}  [ 4 s^2 + s^4 / r^2 ]    (since e^{-phi} e^{2phi} = e^{phi})
# ---------------------------------------------------------------------------
def a_f(r, Th, p):
    s = np.sin(Th); e = np.exp(phi_f(r,p))
    return C/e * ( r*r*s*s + 2*r*r + 2*s**4 + 2*s*s )

def aTh_f(r, Th, p):
    # partial a / partial Theta  (fixed r)
    s = np.sin(Th); c = np.cos(Th); e = np.exp(phi_f(r,p))
    # d/dTh [ r^2 s^2 + 2 r^2 + 2 s^4 + 2 s^2 ]
    inner = 2*r*r*s*c + 8*s**3*c + 4*s*c
    return C/e * inner

def b_f(r, Th, p):
    s = np.sin(Th); e = np.exp(phi_f(r,p))
    return C*e * ( 4*s*s + s**4/(r*r) )

def bTh_f(r, Th, p):
    s = np.sin(Th); c = np.cos(Th); e = np.exp(phi_f(r,p))
    inner = 8*s*c + 4*s**3*c/(r*r)
    return C*e * inner

def dadr_total_f(r, Th, Thp, p):
    """ total da/dr along the solution = a_r + a_phi*phi' + a_Th*Th' """
    s = np.sin(Th); c = np.cos(Th)
    e = np.exp(phi_f(r,p)); pp = phip_f(r,p)
    P = ( r*r*s*s + 2*r*r + 2*s**4 + 2*s*s )   # bracket
    # a = C/e * P
    # explicit r partial of (C/e*P) at fixed Th, phi:
    #   a_r = C/e * dP/dr,  dP/dr = 2 r s^2 + 4 r
    aP_r = C/e * (2*r*s*s + 4*r)
    # phi partial: a = C P e^{-phi}; da/dphi = -C P e^{-phi} = -a
    a_phi = -a_f(r,Th,p)
    # Theta partial
    a_Th = aTh_f(r,Th,p)
    return aP_r + a_phi*pp + a_Th*Thp

# ---------------------------------------------------------------------------
# Euler-Lagrange RHS for ground-state BVP:
#   d/dr(2 a Th') = a_Th Th'^2 + b_Th
# =>  2 a Th'' + 2 (da/dr) Th' = a_Th Th'^2 + b_Th
#     Th'' = [ a_Th Th'^2 + b_Th - 2 (da/dr) Th' ] / (2 a)
# ---------------------------------------------------------------------------
def el_rhs(r, y, p):
    Th, Thp = y
    a   = a_f(r, Th, p)
    aTh = aTh_f(r, Th, p)
    bTh = bTh_f(r, Th, p)
    dadr = dadr_total_f(r, Th, Thp, p)
    Thpp = (aTh*Thp*Thp + bTh - 2*dadr*Thp) / (2*a)
    return np.vstack([Thp, Thpp])

def bc(ya, yb):
    return np.array([ya[0] - np.pi, yb[0] - 0.0])

def solve_ground(p, n0=4001):
    r = np.linspace(R_CORE, R_INT, n0)
    # initial guess: smooth monotone pi -> 0
    Th0 = np.pi*(R_INT - r)/(R_INT - R_CORE)
    Thp0 = -np.pi/(R_INT - R_CORE)*np.ones_like(r)
    y0 = np.vstack([Th0, Thp0])
    sol = solve_bvp(lambda r,y: el_rhs(r,y,p), bc, r, y0,
                    max_nodes=400000, tol=1e-8, verbose=0)
    return sol

# ---------------------------------------------------------------------------
# Hessian potential V(r) and 2a(r), weight W(r) — evaluated on a grid using
# the ground-state Theta0(r), Theta0'(r).
#
#   V = a_ThTh Th0'^2 + b_ThTh - d/dr(2 a_Th Th0')
# We need second Theta-derivatives a_ThTh, b_ThTh, and the total r-derivative
# of (2 a_Th Th0').
# ---------------------------------------------------------------------------
def aThTh_f(r, Th, p):
    s=np.sin(Th); c=np.cos(Th); e=np.exp(phi_f(r,p))
    # inner1 = 2 r^2 s c + 8 s^3 c + 4 s c ; d/dTh:
    # d/dTh(s c)=c^2-s^2 ; d/dTh(s^3 c)=3 s^2 c^2 - s^4
    d = 2*r*r*(c*c - s*s) + 8*(3*s*s*c*c - s**4) + 4*(c*c - s*s)
    return C/e * d

def bThTh_f(r, Th, p):
    s=np.sin(Th); c=np.cos(Th); e=np.exp(phi_f(r,p))
    # inner = 8 s c + 4 s^3 c / r^2 ; d/dTh:
    d = 8*(c*c - s*s) + (4/(r*r))*(3*s*s*c*c - s**4)
    return C*e * d

def aTh_r_total_f(r, Th, Thp, p):
    """ total d/dr of a_Th = a_Th_r + a_Th_phi*phi' + a_Th_Th*Th' """
    s=np.sin(Th); c=np.cos(Th); e=np.exp(phi_f(r,p)); pp=phip_f(r,p)
    # a_Th = C/e * inner1,  inner1 = 2 r^2 s c + 8 s^3 c + 4 s c
    # explicit r partial: d/dr(2 r^2 s c)=4 r s c
    aTh_r = C/e * (4*r*s*c)
    # phi partial: a_Th = C e^{-phi} inner1; d/dphi = -a_Th
    aTh_phi = -aTh_f(r,Th,p)
    aTh_Th = aThTh_f(r,Th,p)
    return aTh_r + aTh_phi*pp + aTh_Th*Thp

def build_coeffs(sol, p, rgrid):
    """ return arrays 2a(r), V(r), W(r) on rgrid (float64) using ground sol. """
    Th  = sol.sol(rgrid)[0]
    Thp = sol.sol(rgrid)[1]
    a   = a_f(rgrid, Th, p)
    two_a = 2.0*a
    aThTh = aThTh_f(rgrid, Th, p)
    bThTh = bThTh_f(rgrid, Th, p)
    # d/dr(2 a_Th Th0') = 2 [ (d/dr a_Th) Th0' + a_Th Th0'' ]
    aTh = aTh_f(rgrid, Th, p)
    daTh_dr = aTh_r_total_f(rgrid, Th, Thp, p)
    # Th0'' from EOM
    aa  = a_f(rgrid, Th, p)
    bTh = bTh_f(rgrid, Th, p)
    dadr= dadr_total_f(rgrid, Th, Thp, p)
    Thpp = (aTh*Thp*Thp + bTh - 2*dadr*Thp)/(2*aa)
    d_2aThThp_dr = 2.0*( daTh_dr*Thp + aTh*Thpp )
    V = aThTh*Thp*Thp + bThTh - d_2aThThp_dr
    W = np.exp(3.0*phi_f(rgrid, p)) * rgrid*rgrid
    return two_a, V, W

# ---------------------------------------------------------------------------
# Float64 generalized eigensolve (to exhibit the artifact).
# Discretize Sturm-Liouville:  H u = -(d/dr)(2a u') + V u = omega^2 W u
# interior points i=1..N on uniform grid spacing h.
# Use conservative FD: -(d/dr)(2a u') at i:
#   -( P_{i+1/2}(u_{i+1}-u_i) - P_{i-1/2}(u_i-u_{i-1}) )/h^2 , P=2a
# Build symmetric H (since this stencil is symmetric), diagonal W.
# ---------------------------------------------------------------------------
def assemble_HW(rgrid, two_a, V, W):
    N = len(rgrid) - 2  # interior count (drop both Dirichlet ends)
    h = rgrid[1]-rgrid[0]
    # half-point P via average
    Hm = np.zeros((N,N))
    # interior indices in rgrid are 1..N
    Ph = 0.5*(two_a[:-1]+two_a[1:])  # length len-1, Ph[k] = P at k+1/2
    for k in range(N):
        i = k+1  # rgrid index
        Pl = Ph[i-1]   # P_{i-1/2}
        Pr = Ph[i]     # P_{i+1/2}
        Hm[k,k] = (Pl+Pr)/h**2 + V[i]
        if k>0:
            Hm[k,k-1] = -Pl/h**2
        if k<N-1:
            Hm[k,k+1] = -Pr/h**2
    Wd = W[1:-1].copy()
    return Hm, Wd, h

def eig_float64(Hm, Wd, k=6):
    # symmetric reduce: solve (Hm) u = w (diag Wd) u
    Wi = 1.0/np.sqrt(Wd)
    A = (Wi[:,None]*Hm)*Wi[None,:]
    A = 0.5*(A+A.T)
    ev = np.linalg.eigvalsh(A)
    return np.sort(ev)[:k]

def eig_float64_naive(Hm, Wd, k=6):
    """ Naive non-symmetric generalized solve W^{-1} H u = lam u via
        scipy.linalg.eig(H, diag(W)).  This is the conditioning-sensitive
        path that the prompt says should spawn spurious negatives deep. """
    from scipy.linalg import eig as geig
    Wm = np.diag(Wd)
    ev = geig(Hm, Wm, right=False)
    ev = np.real(ev[np.abs(np.imag(ev)) < 1e-6*np.abs(np.real(ev) + 1e-30)])
    ev = np.sort(ev)
    return ev[:k]

# ---------------------------------------------------------------------------
# mpmath generalized eigensolve (the trustworthy one).
# Rebuild Hm, Wd in mpmath, symmetric-reduce with mp sqrt, eigsy.
# To keep mpmath tractable, use a modest interior count (a few hundred).
# ---------------------------------------------------------------------------
def build_tridiag_mp(rgrid, sol, p, dps=60):
    """ Build the symmetric tridiagonal reduced matrix A = D^{-1/2} H D^{-1/2}
        (D=diag W) in mpmath precision.  H tridiagonal => A symmetric tridiag.
        Returns diag d[0..N-1], offdiag e[0..N-2] as mpf lists. """
    mp.mp.dps = dps
    Th  = sol.sol(rgrid)[0]
    Thp = sol.sol(rgrid)[1]
    N = len(rgrid)-2
    h = mp.mpf(rgrid[1]) - mp.mpf(rgrid[0])
    rA = [mp.mpf(x) for x in rgrid]
    pmp = mp.mpf(p); RINT = mp.mpf(R_INT)
    def phimp(r): return -pmp*mp.log(RINT/r)
    two_a = []; V = []; W = []
    for idx in range(len(rgrid)):
        r = rA[idx]; th = mp.mpf(Th[idx]); thp = mp.mpf(Thp[idx])
        s = mp.sin(th); c = mp.cos(th); e = mp.e**phimp(r); pp = pmp/r
        a = C/e*( r*r*s*s + 2*r*r + 2*s**4 + 2*s*s )
        two_a.append(2*a)
        aThTh = C/e*( 2*r*r*(c*c-s*s) + 8*(3*s*s*c*c - s**4) + 4*(c*c-s*s) )
        bThTh = C*e*( 8*(c*c-s*s) + (4/(r*r))*(3*s*s*c*c - s**4) )
        aTh   = C/e*( 2*r*r*s*c + 8*s**3*c + 4*s*c )
        aTh_r   = C/e*(4*r*s*c)
        aTh_phi = -aTh
        daTh_dr = aTh_r + aTh_phi*pp + aThTh*thp
        bTh = C*e*( 8*s*c + 4*s**3*c/(r*r) )
        aP_r = C/e*(2*r*s*s+4*r)
        a_phi = -a
        dadr = aP_r + a_phi*pp + aTh*thp
        thpp = (aTh*thp*thp + bTh - 2*dadr*thp)/(2*a)
        d_2aThThp_dr = 2*( daTh_dr*thp + aTh*thpp )
        Vi = aThTh*thp*thp + bThTh - d_2aThThp_dr
        V.append(Vi)
        W.append(mp.e**(3*phimp(r)) * r*r)
    Ph = [ (two_a[i]+two_a[i+1])/2 for i in range(len(two_a)-1) ]
    Wi = [ 1/mp.sqrt(W[k_+1]) for k_ in range(N) ]
    d = []; off = []
    for k_ in range(N):
        i = k_+1
        Pl = Ph[i-1]; Pr = Ph[i]
        Hkk = (Pl+Pr)/h**2 + V[i]
        d.append(Wi[k_]*Hkk*Wi[k_])
    for k_ in range(N-1):
        i = k_+1
        Pr = Ph[i]               # H[k_,k_+1] = -Pr/h^2
        off.append(Wi[k_]*(-Pr/h**2)*Wi[k_+1])
    return d, off

def sturm_count(d, off, mu):
    """ number of eigenvalues of symmetric tridiag (d,off) strictly less than
        mu, via the standard Sturm sequence (count negative pivots of A-mu I).
    """
    N = len(d)
    cnt = 0
    q = d[0] - mu
    if q < 0: cnt += 1
    for i in range(1, N):
        if q == 0:
            q = mp.mpf('1e-400')  # avoid div-by-zero
        q = (d[i]-mu) - off[i-1]*off[i-1]/q
        if q < 0: cnt += 1
    return cnt

def eig_tridiag_mp(d, off, k=6, dps=60):
    """ lowest k eigenvalues of symmetric tridiag via Sturm bisection.

    NOTE on conditioning: the reduced matrix has a huge dynamic range
    (diag entries span ~10^{very large p}), so a Gershgorin lower bound is
    a wildly negative huge number.  Bisecting from there with a tolerance
    RELATIVE to the Gershgorin span is meaningless for the small (O(1..100))
    physical eigenvalues.  We instead (i) require dps to exceed the dynamic
    range, and (ii) use an ABSOLUTE tolerance near the small eigenvalues.
    """
    mp.mp.dps = dps
    N = len(d)
    # Gershgorin bounds (true spectral bracket)
    lo = mp.inf; hi = -mp.inf
    for i in range(N):
        rad = (abs(off[i-1]) if i>0 else mp.mpf(0)) + (abs(off[i]) if i<N-1 else mp.mpf(0))
        lo = min(lo, d[i]-rad); hi = max(hi, d[i]+rad)
    # The smallest eigenvalues are O(1)-O(1e4); bracket them tightly first.
    # Find an upper bracket Bk such that count(Bk) >= k by doubling from 0.
    Bk = mp.mpf(1)
    while sturm_count(d, off, Bk) < k:
        Bk *= 2
        if Bk > hi: Bk = hi; break
    # absolute tolerance: ~1e-(dps-10) relative to Bk magnitude
    tol = abs(Bk)*mp.mpf(10)**(-(dps-12))
    evals = []
    for j in range(k):
        # j-th eigenvalue (0-indexed): smallest mu with count(mu) >= j+1
        # left bracket: lo if no smaller eigenvalue found, but use 0-margin
        a = lo; b = Bk
        # tighten left bracket using a small negative floor relative to Bk
        while (b-a) > tol:
            mid = (a+b)/2
            if sturm_count(d, off, mid) >= j+1:
                b = mid
            else:
                a = mid
        evals.append((a+b)/2)
    return [float(x) for x in evals]

def eig_mpmath(rgrid, sol, p, dps=60, k=6):
    # adapt precision to the dynamic range: diag spans ~ (r_int/r_core)^{3p}
    # ~ 281^{3p}; log10 ~ 3p*2.45.  Need dps comfortably above that.
    need = int(3*p*np.log10(R_INT/R_CORE)) + 50
    dps_use = max(dps, need)
    d, off = build_tridiag_mp(rgrid, sol, p, dps=dps_use)
    return eig_tridiag_mp(d, off, k=k, dps=dps_use)

# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def run():
    print("="*78)
    print("INDEPENDENT VERIFIER: deep-phi hedgehog breathing Hessian spectrum")
    print(f"r_core={R_CORE}  r_int={R_INT}  cell_len={CELL_LEN}")
    print("="*78)

    # mpmath uses a coarser grid for tractability; float64 finer for artifact
    N_MP   = 300   # interior pts for mpmath
    N_F64  = 800   # interior pts for float64 artifact demo
    DPS    = 60
    KEEP   = 4

    mp_results = {}
    f64_results = {}
    f64_naive_results = {}
    soft = {}

    for p in [0,1,2,3,4,5,6,8,10]:
        sol = solve_ground(p)
        if not sol.success:
            print(f"[p={p}] ground BVP FAILED: {sol.message}")
            continue
        # ----- mpmath spectrum -----
        rmp = np.linspace(R_CORE, R_INT, N_MP+2)
        ev_mp = eig_mpmath(rmp, sol, p, dps=DPS, k=KEEP+2)
        mp_results[p] = ev_mp
        soft[p] = ev_mp[0]
        # ----- float64 spectrum (artifact) -----
        rf = np.linspace(R_CORE, R_INT, N_F64+2)
        two_a, V, W = build_coeffs(sol, p, rf)
        Hm, Wd, h = assemble_HW(rf, two_a, V, W)
        ev_f = eig_float64(Hm, Wd, k=KEEP+2)
        f64_results[p] = ev_f
        if p in (2,4,6,8):
            try:
                ev_naive = eig_float64_naive(Hm, Wd, k=KEEP+2)
                f64_naive_results[p] = ev_naive
            except Exception as ex:
                f64_naive_results[p] = f"err: {ex}"
        print(f"[p={p}] ground solved (nodes={sol.x.size}); "
              f"mp omega^2: {[f'{x:.6g}' for x in ev_mp[:KEEP]]}")

    # ---- Table 1: lowest omega_n^2 ----
    print("\n" + "="*78)
    print("TABLE 1a: lowest omega_n^2 (mpmath dps=%d, N_int=%d)" % (DPS,N_MP))
    print("p   |   omega0^2        omega1^2        omega2^2        omega3^2")
    for p in sorted(mp_results):
        e = mp_results[p]
        print(f"{p}   | " + "  ".join(f"{e[i]:14.7g}" for i in range(4)))

    print("\nTABLE 1b: float64 SYM-REDUCED (N_int=%d) — artifact check" % N_F64)
    print("p   |   omega0^2        omega1^2        omega2^2        omega3^2")
    for p in sorted(f64_results):
        e = f64_results[p]
        print(f"{p}   | " + "  ".join(f"{e[i]:14.7g}" for i in range(4)))

    print("\nTABLE 1c: float64 NAIVE geig(H,diag(W)) — conditioning-sensitive")
    print("        (prompt predicts spurious negatives deep)")
    print("p   |   omega0^2        omega1^2        omega2^2        omega3^2")
    for p in sorted(f64_naive_results):
        e = f64_naive_results[p]
        if isinstance(e, str):
            print(f"{p}   | {e}")
        else:
            neg = "  <-- has spurious neg!" if e[0] < -1e-6 else ""
            print(f"{p}   | " + "  ".join(f"{e[i]:14.7g}" for i in range(4)) + neg)

    # ---- Table 2: ratios ----
    print("\n" + "="*78)
    print("TABLE 2: ratios (mpmath).  R1=om1^2/om0^2, R2=om2^2/om0^2, "
          "R3=om3^2/om0^2")
    print("p   |   R1            R2            R3            "
          "sqrt-ratio om1/om0")
    for p in sorted(mp_results):
        e = mp_results[p]
        if e[0] <= 0:
            print(f"{p}   | (om0^2<=0, soft mode) om0^2={e[0]:.4g}")
            continue
        R1 = e[1]/e[0]; R2 = e[2]/e[0]; R3 = e[3]/e[0]
        sr = (e[1]/e[0])**0.5
        print(f"{p}   | {R1:12.6g}  {R2:12.6g}  {R3:12.6g}      {sr:10.5g}")

    # ---- Table 3: exponential-fit slope c in log(omega_n) ~ c n ----
    print("\n" + "="*78)
    print("TABLE 3: exp-fit slope c of log(omega_n) vs n  (omega_n=sqrt(om_n^2))")
    print("        c>>1 would mean exponential hierarchy. n=0..3 used.")
    print("p   |   slope c (lin fit)   omega_n geometric? (om_n/om_{n-1})")
    for p in sorted(mp_results):
        e = mp_results[p]
        if e[0] <= 0:
            print(f"{p}   | soft mode, skip")
            continue
        om = np.sqrt(np.array(e[:4]))
        n = np.arange(4)
        # log(om) ~ c n + d
        c, d = np.polyfit(n, np.log(om), 1)
        steps = om[1:]/om[:-1]
        print(f"{p}   | c = {c:10.5f}        steps om_n/om_(n-1) = "
              + ", ".join(f"{s:.4f}" for s in steps))

    # ---- Table 4: ground softening ----
    print("\n" + "="*78)
    print("TABLE 4: ground mode omega0^2(p) — softening / instability check")
    for p in sorted(soft):
        flag = "  <-- SOFT/UNSTABLE" if soft[p] <= 0 else ""
        print(f"p={p}:  omega0^2 = {soft[p]:.7g}{flag}")

    # ---- Convergence spot check at p=4: compare N_MP vs finer ----
    print("\n" + "="*78)
    print("CONVERGENCE spot-check at p=4: mpmath N=300 vs N=500")
    p=4
    sol = solve_ground(p)
    r5 = np.linspace(R_CORE,R_INT,502)
    ev5 = eig_mpmath(r5, sol, p, dps=DPS, k=6)
    print(f"  N=300: {[f'{x:.6g}' for x in mp_results[4][:4]]}")
    print(f"  N=500: {[f'{x:.6g}' for x in ev5[:4]]}")

    return mp_results, f64_results, soft

if __name__ == "__main__":
    run()
