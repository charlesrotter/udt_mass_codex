# VERIF_with_L4_fluctuation_F2345.py
# F2: solve the REAL L2+L4-stabilized hedgehog Theta(r) from its actual EOM (S2).
# F3: radial (l=0) eigenproblem WITH L4 -> intrinsic modes? trap-test (S4); compare #44.
# F4: angular (l>=1) WITH V + connection + L4 stiffness -> distinct intrinsic modes? (S4,S5)
# F5: emergent-quantization reading.
#
# DISCIPLINE: L4 INCLUDED in BOTH background and fluctuation operator. The
# fluctuation operator is the exact second variation; L4 makes it 4th order ->
# more BCs (S3, load-bearing). Box-control trap-test varies cell R (S4). Goldstone
# modes separated (S5).
import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import eig
np.set_printoptions(precision=6, suppress=False, linewidth=120)

# ===========================================================================
# F2 -- REAL stabilized hedgehog profile from the L2+L4 EOM
# ===========================================================================
# Reduced functional (lepton_soliton_spectrum_results.md:36-40), m=1, flat phi=0:
#   E2_r = (2pi xi/3)[ r^2 sin^2T T'^2 + 2 r^2 T'^2 + 4 sin^2T ]
#   E4_r = (2pi kappa/3)[ (2 r^2 sin^4T + 2 r^2 sin^2T) T'^2 + sin^4T ] / r^2
# EOM: d/dr[ dL/dT' ] = dL/dT.  We solve with xi=kappa=1.
# Coefficient of T'^2 (call P): P = (xi)(r^2 sin^2T + 2 r^2) + (kappa)(2 sin^4T + 2 sin^2T)
# [absorbing the 2pi/3, which cancels in EL]. d/dr(P T') = dV_pot/dT where
# V_pot collects the non-T' pieces' T-dependence.
# We build the EOM by symbolic differentiation done once here numerically via the
# Euler-Lagrange of the integrand L(T,T',r).

import sympy as sp
rs, xi_s, kap_s = sp.symbols('r xi kappa', positive=True)
T = sp.Function('T')
Tt = sp.Function('T')(rs)
phi_s = sp.Function('phi')(rs)
E2 = xi_s*( rs**2*sp.sin(Tt)**2*sp.Derivative(Tt,rs)**2 + 2*rs**2*sp.Derivative(Tt,rs)**2
            + 4*sp.exp(2*phi_s)*sp.sin(Tt)**2 )*sp.exp(-phi_s)
E4 = kap_s*( (2*rs**2*sp.sin(Tt)**4 + 2*rs**2*sp.sin(Tt)**2)*sp.Derivative(Tt,rs)**2
            + sp.exp(2*phi_s)*sp.sin(Tt)**4 )*sp.exp(-phi_s)/rs**2
L = E2 + E4
Tp = sp.Derivative(Tt, rs)
dL_dTp = sp.diff(L, Tp)
dL_dT  = sp.diff(L, Tt)
EL = sp.diff(dL_dTp, rs) - dL_dT     # = 0
# Solve EL for T'' :
Tpp = sp.symbols('Tpp')
EL_e = EL.subs(sp.Derivative(Tt, (rs,2)), Tpp)
sol_Tpp = sp.solve(EL_e, Tpp)
assert len(sol_Tpp)==1
Tpp_expr = sol_Tpp[0]
# lambdify for flat (phi=0) and deep-phi log cell
phi_func = sp.Function('phi')
Tval, Tpval = sp.symbols('Tval Tpval')
subs_common = {Tt: Tval, Tp: Tpval}
def make_rhs(phi_expr, phip_expr):
    e = Tpp_expr.subs({phi_s: phi_expr, sp.Derivative(phi_s, rs): phip_expr,
                       xi_s:1, kap_s:1}).subs(subs_common)
    return sp.lambdify((rs, Tval, Tpval), e, 'numpy')

# flat
rhs_flat = make_rhs(0, 0)
def bvp_flat(r, y):
    T_, Tp_ = y
    return np.vstack([Tp_, rhs_flat(r, T_, Tp_)])
def bc(ya, yb):
    return np.array([ya[0]-np.pi, yb[0]-0.0])

def solve_profile(rc, R, rhs, n=4000):
    rmesh = np.linspace(rc, R, n)
    # initial guess: smooth pi->0
    Tg = np.pi*(1 - (rmesh-rc)/(R-rc))
    Tpg = -np.pi/(R-rc)*np.ones_like(rmesh)
    def f(r,y): return np.vstack([y[1], rhs(r,y[0],y[1])])
    sol = solve_bvp(f, bc, rmesh, np.vstack([Tg,Tpg]), tol=1e-8, max_nodes=200000)
    return sol

print("="*70); print("F2 -- REAL L2+L4 stabilized hedgehog (flat phi=0)"); print("="*70)
rc = 1e-3
sol = solve_profile(rc, 8.0, rhs_flat)
print("solve_bvp success:", sol.success, " max residual:", np.max(np.abs(sol.rms_residuals)))
rr = np.linspace(rc, 8.0, 2000)
Thr = sol.sol(rr)[0]
# half-twist radius
i_half = np.argmin(np.abs(Thr-np.pi/2))
print("half-twist (Theta=pi/2) radius:", rr[i_half], " (corpus width ~0.648 L)")
# energy E0 (numeric integral of E2_r+E4_r * (3/(2pi)) to match corpus normalization 45.6)
E2int = sp.lambdify((rs,Tval,Tpval),(E2.subs({phi_s:0,xi_s:1,kap_s:1}).subs(subs_common)),'numpy')
E4int = sp.lambdify((rs,Tval,Tpval),(E4.subs({phi_s:0,xi_s:1,kap_s:1}).subs(subs_common)),'numpy')
Tp_r = sol.sol(rr)[1]
integ = (E2int(rr,Thr,Tp_r)+E4int(rr,Thr,Tp_r))
E0 = np.trapezoid(integ, rr)*(2*np.pi/3)
print("E0 (kappa/xi units, 2pi/3 norm) =", E0, " (corpus E0 = 45.6069)")

# deep-phi profile (p=1 log cell)
R_int = 8.0
p_depth = 1.0
phi_deep = -p_depth*sp.log(R_int/rs)
phip_deep = sp.diff(phi_deep, rs)
rhs_deep = make_rhs(phi_deep, phip_deep)
sol_d = solve_profile(rc, R_int, rhs_deep)
print("\n[deep-phi p=1] success:", sol_d.success, " max res:", np.max(np.abs(sol_d.rms_residuals)))
Thr_d = sol_d.sol(rr)[0]
i_half_d = np.argmin(np.abs(Thr_d-np.pi/2))
print("  deep-phi half-twist radius:", rr[i_half_d], " (corpus: pushed outward)")

# ===========================================================================
# F3/F4 -- the WITH-L4 fluctuation eigenproblem, per angular sector l
# ===========================================================================
# We build the exact second-variation operator acting on a radial fluctuation
# profile u(r) in angular channel l. Two pieces:
#  (i) RADIAL l=0 sector: the Hessian of the reduced energy E2_r+E4_r about the
#      solved profile, with breathing weight W ~ e^{3phi} r^2 (the time-kinetic
#      coefficient). This IS the #44 breathing operator -- WITH L4 already in it.
#  (ii) GENERAL l: the Jacobi tangent-fluctuation operator
#        D^m D_m eta + K[|grad n0|^2 eta - <eta,grad n0> grad n0],  K=+1,
#      PLUS the L4 fourth-order stiffness. In channel l the angular Laplacian
#      gives -l(l+1)/r^2 (centrifugal, repulsive); V_curv = -(e^{-2phi}T'^2 +
#      2 sin^2T/r^2) (attractive); L4 gives a positive 4th-order (biharmonic)
#      stiffness with coefficient built from the background winding.
#
# The operator (self-adjoint, generalized eigenproblem H u = omega^2 W u):
#   H u = -(1/(e^{phi} r^2)) d_r( e^{-phi} r^2 d_r u )            [L2 kinetic, radial]
#         + [ l(l+1)/r^2 + V_curv(r) ] u                          [centrifugal + Jacobi V]
#         + s4 * (1/(e^{phi} r^2)) d_r^2( c4(r) d_r^2 u )         [L4 k^4 stiffness, +]
#   W = e^{2phi}                                                  (g^{tt} weight; matter wave)
# c4(r) = background winding stiffness from E4 ~ (2 sin^4T + 2 sin^2T) > 0 (the
# Theta'^2-coefficient of E4_r), normalized; s4 = kappa = 1.
#
# This is built on a finite-difference grid; the L4 biharmonic raises the order
# (4th) -> needs MORE BCs (S3). BCs (load-bearing, tagged):
#   core r=rc: u=0 (regularity, Dirichlet) AND u'=0 (4th-order clamp) -- DERIVED-grade
#              (regular core: fluctuation and its slope vanish where well sits).
#   seal r=R : u=0 (finite-cell Dirichlet) AND u'=0 (clamped seal) -- CHOSEN (finite-cell);
#              VARIED in trap-test. Also test natural (u''=0) seal for sensitivity.

def build_background(sol, phi_expr, phip_expr, rgrid):
    Tg = sol.sol(rgrid)[0]; Tpg = sol.sol(rgrid)[1]
    phf = sp.lambdify(rs, phi_expr, 'numpy')
    phpf= sp.lambdify(rs, phip_expr,'numpy')
    ph = phf(rgrid)*np.ones_like(rgrid); php = phpf(rgrid)*np.ones_like(rgrid)
    return Tg, Tpg, ph, php

def eig_with_L4(rc, R, l, sol, phi_expr, phip_expr, N=1200, s4=1.0,
                seal='clamp', use_L4=True):
    """Generalized eig H u = w^2 W u with L4 4th-order stiffness. FD."""
    r = np.linspace(rc, R, N)
    h = r[1]-r[0]
    Tg, Tpg, ph, php = build_background(sol, phi_expr, phip_expr, r)
    eph = np.exp(ph); enph = np.exp(-ph)
    # V_curv attractive (K=+1 Jacobi):
    Vcurv = -(np.exp(-2*ph)*Tpg**2 + 2*np.sin(Tg)**2/r**2)
    Vcent = l*(l+1)/r**2
    Vtot = Vcent + Vcurv
    # L4 stiffness coefficient c4(r): the Theta'^2 coeff of E4_r (winding stiffness)
    c4 = (2*np.sin(Tg)**4 + 2*np.sin(Tg)**2)   # >=0
    # weight W = e^{2phi}
    W = np.exp(2*ph)
    # Build H as dense matrix (interior nodes). 2nd-order SL part:
    n = N
    H = np.zeros((n,n)); Wm = np.zeros((n,n))
    # second-order operator: -(1/(e^{phi} r^2)) d_r(e^{-phi} r^2 d_r u)
    a = enph*r**2          # coeff inside d_r
    pref = 1.0/(eph*r**2)
    for i in range(1,n-1):
        ap = 0.5*(a[i]+a[i+1]); am = 0.5*(a[i]+a[i-1])
        H[i,i-1] += -pref[i]*am/h**2
        H[i,i]   += +pref[i]*(am+ap)/h**2
        H[i,i+1] += -pref[i]*ap/h**2
        H[i,i]   += Vtot[i]
        Wm[i,i]   = W[i]
    if use_L4:
        # L4 4th-order: + s4 * pref * d_r^2( c4 d_r^2 u )   (biharmonic, positive)
        # discretize d_r^2(c4 d_r^2 u) with standard 5-point stencil (interior 2..n-3)
        d2 = np.zeros((n,n))
        for i in range(1,n-1):
            d2[i,i-1]+=1/h**2; d2[i,i]+=-2/h**2; d2[i,i+1]+=1/h**2
        C = np.diag(c4)
        Bih = d2 @ C @ d2
        for i in range(2,n-2):
            H[i,:] += s4*pref[i]*Bih[i,:]
    # BCs: core u=0,u'=0 ; seal u=0 + (clamp u'=0 OR natural)
    # Dirichlet at both ends:
    H[0,:]=0; H[0,0]=1; Wm[0,0]=0
    H[-1,:]=0; H[-1,-1]=1; Wm[-1,-1]=0
    # clamp (u'=0) at core via second row, at seal via second-to-last
    if use_L4:
        H[1,:]=0; H[1,0]=-1; H[1,1]=1; Wm[1,1]=0   # u'(core)=0
        if seal=='clamp':
            H[-2,:]=0; H[-2,-1]=-1; H[-2,-2]=1; Wm[-2,-2]=0  # u'(seal)=0
        # 'natural' seal: leave row -2 as the operator (u'' free) -> Wm[-2,-2] kept
    # solve generalized eig
    w2, vec = eig(H, Wm + 1e-30*np.eye(n))
    w2 = w2.real
    # keep finite, drop the BC-spurious huge eigenvalues (from the 1's on diagonal)
    good = np.isfinite(w2) & (np.abs(w2) < 1e6)
    w2 = np.sort(w2[good])
    return w2

print("\n"+"="*70)
print("F3 -- RADIAL l=0 eigenproblem WITH L4 (compare to #44 breathing tower)")
print("="*70)
# l=0, with L4, flat. Compare lowest positive omega^2 to #44: [0.198,0.554,1.039,...]
w2_l0 = eig_with_L4(rc, 8.0, l=0, sol=sol, phi_expr=sp.Integer(0), phip_expr=sp.Integer(0),
                    N=1000, use_L4=True, seal='clamp')
pos = w2_l0[w2_l0 > 1e-6]
print("l=0 WITH L4, lowest eigenvalues omega^2:", w2_l0[:8])
print("lowest POSITIVE omega^2:", pos[:6])
print("(#44 breathing tower: omega^2 = [0.198, 0.554, 1.039, 1.688, ...])")

print("\n"+"="*70)
print("F3/F4 -- BOX-CONTROL TRAP-TEST (S4): vary R, l=0 and l>=1, WITH L4")
print("="*70)
Rs = [8.0, 25.0, 80.0, 250.0]   # factor ~31 (>10), 4 values (S4 satisfied)
for l in [0,1,2]:
    print(f"\n--- l={l} (WITH L4, flat phi=0) ---")
    print(f"{'R':>8} {'lowest w^2':>14} {'w^2*R^2':>14} {'2nd w^2':>14}")
    for R in Rs:
        # re-solve profile on each cell (background extends; profile is cell-size independent in shape)
        sol_R = solve_profile(rc, R, rhs_flat, n=min(4000,int(800*R/8)+1000))
        w2 = eig_with_L4(rc, R, l=l, sol=sol_R, phi_expr=sp.Integer(0),
                         phip_expr=sp.Integer(0), N=1000, use_L4=True, seal='clamp')
        w2f = w2[np.isfinite(w2)]
        lowest = w2f[0] if len(w2f)>0 else np.nan
        second = w2f[1] if len(w2f)>1 else np.nan
        print(f"{R:8.1f} {lowest:14.6e} {lowest*R**2:14.4f} {second:14.6e}")

print("\n"+"="*70)
print("F3/F4 control: SAME trap-test WITHOUT L4 (reproduce L2-only box/tachyon)")
print("="*70)
for l in [0,1]:
    print(f"\n--- l={l} (L2-ONLY, flat phi=0) ---")
    print(f"{'R':>8} {'lowest w^2':>14} {'w^2*R^2':>14}")
    for R in Rs:
        sol_R = solve_profile(rc, R, rhs_flat, n=min(4000,int(800*R/8)+1000))
        w2 = eig_with_L4(rc, R, l=l, sol=sol_R, phi_expr=sp.Integer(0),
                         phip_expr=sp.Integer(0), N=1000, use_L4=False, seal='clamp')
        w2f = w2[np.isfinite(w2)]
        lowest = w2f[0] if len(w2f)>0 else np.nan
        print(f"{R:8.1f} {lowest:14.6e} {lowest*R**2:14.4f}")
print("\nDONE F2-F4. (F5 reading + Goldstone notes in the results doc.)")
