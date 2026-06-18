# VERIF_deep_phi_sign_D2345.py
# DECISIVE deep-phi SIGN of the intrinsic l=0 fluctuation mode, with the EXACT
# native coefficient operator (D1/D1b), mpmath log-grid x=ln r, dps>=50.
#
# D2: real stabilized Theta(r) from the L2+L4 EOM (finite cell, E0~45.6).
# D3: THE SIGN -- lowest non-Goldstone omega^2, >=2 depths, >=3 grid sizes,
#     convergence + CAUSAL TOGGLE (well ON vs OFF -> box-control returns?).
# D4: intrinsic vs box (R-independent magnitude? omega^2 R^2 grows? well-OFF box?).
# D5: Goldstone (breathing/dilation zero mode) removal + interpretation.
#
# EXACT operator (D1b, full native xi,kappa):
#   delta^2 E = INT [ P u'^2 + 2 Rmix u' u + Q u^2 ] dr   (l=0 breathing/radial)
#   Generalized eigenproblem:  -(d/dr)(P u') + Veff u = omega^2 W u,
#     P    = 2[ 2k(sin^4 T+sin^2 T) + r^2 xi(sin^2 T+2) ] e^{-phi}
#     Rmix = -4 T' [ 2k(cos2T-2) - r^2 xi ] e^{-phi} sinT cosT
#     Q    = (-k( T'^2 r^2(64 s4-32 s2-8) + (3cos4T-3)e^{2phi}+8 e^{2phi} s4 )/2
#             + 2 r^2 xi (T'^2 r^2 + 4 e^{2phi}) cos2T ) e^{-phi}/r^2
#     Veff = Q - d/dr(Rmix)|along Theta0
#     W    = (2pi/3)[ 2k(s4+s2) + r^2 xi(s2+2) ] e^{3phi}    (EXACT breathing weight)
#   (overall 2pi/3 cancels in omega^2; we keep it for clarity.)
#
# CAUSAL TOGGLE: "well OFF" = drop the attractive part of Veff (set Q->0 and Rmix->0,
#   keeping only the kinetic P and weight W) -> a pure SL kinetic-in-a-box; if that
#   reverts to omega^2 R^2 -> const (box), the assembly is sound and the negative
#   mode is causally the native well.
import math, numpy as np, mpmath as mp
from scipy.integrate import solve_bvp
mp.mp.dps = 60

XI = 1.0; KAPPA = 1.0     # native couplings (the SCALE; ratio kappa/xi tested below)
TWO_PI_3 = 2*math.pi/3

# ---------- background profile (D2): EXACT EOM (matches lepton_soliton_spectrum) ----------
def phi_bg(r, p, r_int):
    # deep cell: phi = -p ln(r_int/r) = p ln(r/r_int)  (phi -> -inf at core; deep-phi)
    if p == 0.0:
        return np.zeros_like(r), np.zeros_like(r)
    return p*np.log(r/r_int), p/r

def theta_ddot(r, Th, Thp, phi, phip, xi, kappa):
    # EXACT EOM (full EL of E2_r+E4_r), from lepton_soliton_spectrum_mpmath.py:22
    s = np.sin(Th)
    num = ((0.5)*Thp*r**2*(-4*Thp*kappa*np.sin(2*Th)+Thp*kappa*np.sin(4*Th)
        -Thp*r**2*xi*np.sin(2*Th)+kappa*phip*(1-np.cos(2*Th))**2-2*kappa*phip*np.cos(2*Th)
        +2*kappa*phip-phip*r**2*xi*np.cos(2*Th)+5*phip*r**2*xi+2*r*xi*np.cos(2*Th)-10*r*xi)
        +2*kappa*np.exp(2*phi)*s**3*np.cos(Th)+2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
    den = r**2*(2*kappa*s**4+2*kappa*s**2+r**2*xi*s**2+2*r**2*xi)
    return num/den

def solve_ground(r_core, r_int, xi, kappa, p, N=900):
    x0 = np.linspace(r_core, r_int, N)
    def rhs(r, y):
        Th, Thp = y; phi, phip = phi_bg(r, p, r_int)
        return np.vstack([Thp, theta_ddot(r, Th, Thp, phi, phip, xi, kappa)])
    def bc(ya, yb): return np.array([ya[0]-math.pi, yb[0]])
    L = math.sqrt(kappa/xi); w = 2*L
    Th0 = math.pi*0.5*(1-np.tanh((x0-(r_core+w))/(0.8*L)))
    sol = solve_bvp(rhs, bc, x0, np.vstack([Th0, np.gradient(Th0, x0)]),
                    tol=1e-9, max_nodes=600000)
    return sol

def energy_E0(sol, r_core, r_int, xi, kappa, p):
    rr = np.linspace(r_core, r_int, 4000)
    Th = sol.sol(rr)[0]; Thp = sol.sol(rr)[1]; phi, _ = phi_bg(rr, p, r_int)
    s = np.sin(Th); em = np.exp(-phi); e2p = np.exp(2*phi)
    E2 = xi*em*(rr**2*s**2*Thp**2 + 2*rr**2*Thp**2 + 4*e2p*s**2)
    E4 = kappa*em*((2*rr**2*s**4+2*rr**2*s**2)*Thp**2 + e2p*s**4)/rr**2
    return np.trapezoid((E2+E4)*TWO_PI_3, rr)

# ---------- EXACT mpmath fluctuation eigensolve (D1b operator) ----------
def fluct_exact_mpmath(rg, Th0, phi, xi, kappa, nev=6, well='ON'):
    """EXACT l=0 second-variation generalized SL eigensolve, mpmath, log-grid-aware.
       well='ON' : full Veff (P,Q,Rmix,W).
       well='OFF': causal toggle -> Q=0, Rmix=0 (kinetic+weight only) -> should be box.
    """
    r = [mp.mpf(x) for x in rg]; Th = [mp.mpf(x) for x in Th0]; ph = [mp.mpf(x) for x in phi]
    N = len(r); xi = mp.mpf(xi); kappa = mp.mpf(kappa); c = mp.mpf(TWO_PI_3)
    # background Theta' via centered FD on the (possibly non-uniform) grid
    Tp0 = [ (Th[i+1]-Th[i-1])/(r[i+1]-r[i-1]) if 0<i<N-1 else mp.mpf(0) for i in range(N) ]
    P = [None]*N; Q = [None]*N; Rmix = [None]*N; W = [None]*N
    for i in range(N):
        ri = r[i]; T = Th[i]; pp = ph[i]; Tp = Tp0[i]
        s = mp.sin(T); cs = mp.cos(T); s2 = s*s; s4 = s2*s2
        em = mp.e**(-pp); e2p = mp.e**(2*pp); e3p = mp.e**(3*pp)
        c2T = mp.cos(2*T); c4T = mp.cos(4*T); s2T = mp.sin(2*T); s4T = mp.sin(4*T)
        # P = 2[2k(s4+s2)+r^2 xi(s2+2)] e^{-phi}
        P[i] = 2*(2*kappa*(s4+s2) + ri**2*xi*(s2+2))*em
        # W = (2pi/3)[2k(s4+s2)+r^2 xi(s2+2)] e^{3phi}
        W[i] = c*(2*kappa*(s4+s2) + ri**2*xi*(s2+2))*e3p
        # Rmix = -4 Tp [2k(cos2T-2) - r^2 xi] e^{-phi} sinT cosT
        Rmix[i] = -4*Tp*(2*kappa*(c2T-2) - ri**2*xi)*em*s*cs
        # Q = (-k( Tp^2 r^2(64 s4-32 s2-8) + (3cos4T-3)e2p + 8 e2p s4 )/2
        #      + 2 r^2 xi (Tp^2 r^2 + 4 e2p) cos2T ) e^{-phi}/r^2
        Q[i] = (-kappa*( Tp**2*ri**2*(64*s4-32*s2-8) + (3*c4T-3)*e2p + 8*e2p*s4 )/2
                + 2*ri**2*xi*(Tp**2*ri**2 + 4*e2p)*c2T )*em/ri**2
    if well == 'OFF':
        Q = [mp.mpf(0)]*N; Rmix = [mp.mpf(0)]*N
    # Veff = Q - d/dr(Rmix) along bg
    dRmix = [ (Rmix[i+1]-Rmix[i-1])/(r[i+1]-r[i-1]) if 0<i<N-1 else mp.mpf(0) for i in range(N) ]
    Veff = [ Q[i]-dRmix[i] for i in range(N) ]
    # assemble tridiagonal generalized eigenproblem, Dirichlet interior nodes
    n = N-2
    Hm = mp.zeros(n); Wd = [None]*n
    for i in range(1, N-1):
        Pr = (P[i]+P[i+1])/2; Pl = (P[i-1]+P[i])/2
        hr = r[i+1]-r[i]; hl = r[i]-r[i-1]; hc = (hr+hl)/2; k = i-1
        Hm[k,k] = (Pr/hr+Pl/hl)/hc + Veff[i]
        if k+1 < n: Hm[k,k+1] = -Pr/hr/hc
        if k-1 >= 0: Hm[k,k-1] = -Pl/hl/hc
        Wd[k] = W[i]
    Winv = [1/mp.sqrt(w) for w in Wd]
    A = mp.zeros(n)
    for a in range(n):
        for b in range(max(0,a-1), min(n,a+2)):
            A[a,b] = Hm[a,b]*Winv[a]*Winv[b]
    for a in range(n):
        for b in range(a+1, n):
            A[a,b] = A[b,a] = (A[a,b]+A[b,a])/2
    ev = mp.eigsy(A, eigvals_only=True)
    evs = sorted([ev[i] for i in range(n)])
    return [float(x) for x in evs[:nev]]

def log_grid(r_core, r_int, N):
    # uniform in x=ln r -> clusters near core; the conditioning-beating grid (S4)
    x = np.linspace(math.log(r_core), math.log(r_int), N)
    return np.exp(x)

# ===========================================================================
print("="*72); print("D2 -- real stabilized profile (EXACT EOM), E0 check"); print("="*72)
r_core = 0.05; L = 1.0
for p in [0.0, 1.0]:
    r_int = r_core + 14*L
    g = solve_ground(r_core, r_int, XI, KAPPA, p)
    rr = np.linspace(r_core, r_int, 3000); Th = g.sol(rr)[0]
    ihalf = np.argmin(np.abs(Th-math.pi/2))
    E0 = energy_E0(g, r_core, r_int, XI, KAPPA, p)
    print(f" p={p}: bvp success={g.success} maxres={np.max(np.abs(g.rms_residuals)):.1e} "
          f"half-twist r={rr[ihalf]:.3f}  E0={E0:.4f} (corpus ~45.6 at p=0)")

# ===========================================================================
print("\n"+"="*72)
print("D3/D4 -- THE SIGN: lowest omega^2, EXACT coeff, mpmath log-grid")
print("  convergence (>=3 grids) x depth (p=0 control, p=1, p=2) x causal toggle")
print("="*72)
depths = [0.0, 1.0, 2.0]
Rs = [r_core+10*L, r_core+18*L, r_core+30*L]   # vary cell for intrinsic-vs-box
grids = [120, 160, 220]

for p in depths:
    print(f"\n----- depth p={p} -----")
    # convergence in grid at a FIXED cell
    r_int = r_core + 18*L
    g = solve_ground(r_core, r_int, XI, KAPPA, p, N=1200)
    print(f"  [grid convergence @ R={r_int:.2f}]  (well ON, EXACT coeff)")
    for N in grids:
        rg = log_grid(r_core, r_int, N)
        Tg = g.sol(rg)[0]; phg, _ = phi_bg(rg, p, r_int)
        ev = fluct_exact_mpmath(rg, Tg, phg, XI, KAPPA, nev=4, well='ON')
        print(f"    N={N:4d}: lowest omega^2 = {ev[0]:+.6e}   next: {ev[1]:+.4e} {ev[2]:+.4e}")
    # intrinsic-vs-box: vary R at fixed N
    print(f"  [intrinsic-vs-box: vary cell R, N=180, well ON]")
    for R in Rs:
        gR = solve_ground(r_core, R, XI, KAPPA, p, N=1200)
        rg = log_grid(r_core, R, 180)
        Tg = gR.sol(rg)[0]; phg, _ = phi_bg(rg, p, R)
        ev = fluct_exact_mpmath(rg, Tg, phg, XI, KAPPA, nev=4, well='ON')
        w2R2 = ev[0]*R**2
        print(f"    R={R:6.2f}: omega^2 = {ev[0]:+.6e}   omega^2*R^2 = {w2R2:+.4e}")
    # CAUSAL TOGGLE: well OFF -> box-control should return
    print(f"  [CAUSAL TOGGLE: well OFF (Q=Rmix=0), N=180]")
    for R in Rs:
        gR = solve_ground(r_core, R, XI, KAPPA, p, N=1200)
        rg = log_grid(r_core, R, 180)
        Tg = gR.sol(rg)[0]; phg, _ = phi_bg(rg, p, R)
        ev = fluct_exact_mpmath(rg, Tg, phg, XI, KAPPA, nev=4, well='OFF')
        w2R2 = ev[0]*R**2
        print(f"    R={R:6.2f}: omega^2 = {ev[0]:+.6e}   omega^2*R^2 = {w2R2:+.4e}")

print("\nDONE D2-D4. (Goldstone D5 + kappa/xi sensitivity in companion script.)")
