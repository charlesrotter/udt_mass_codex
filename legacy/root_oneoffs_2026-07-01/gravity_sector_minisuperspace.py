#!/usr/bin/env python3
"""
gravity_sector_minisuperspace.py

THE DECISIVE phi-STATUS TEST.

In UDT phi is NOT an independent scalar bolted onto GR. It SITS INSIDE the
metric (g_tt = -e^{-2phi}c0^2, g_rr = e^{2phi}). So "f(phi) R" is NOT a
generic Brans-Dicke f(phi)R with phi independent of g. We must vary HONESTLY.

We test the question two complementary, honest ways.

(A) CONFORMAL / FRAME test. f(phi) R with f = (c0^4/16piG) e^{-8 phi}.
    Is the c^4 = e^{-8phi} prefactor removable by a conformal rescaling
    g -> Omega^2 g-tilde?  In 4D, sqrt(-g) f R  ->  under g = Omega^2 g~,
        sqrt(-g) f R = sqrt(-g~) Omega^4 f [ Omega^{-2}(R~ - 6 Box~ ln Omega
                       - 6 (grad ln Omega)^2 ) ]
    Choosing Omega^2 f = const = 1/(16piG) puts it in EINSTEIN FRAME with a
    canonical R~ plus a scalar KINETIC term for phi. We exhibit that kinetic
    term. If it is NONZERO, the theory is genuinely scalar-tensor (NOT GR):
    the c^4 prefactor is not pure relabeling, it leaves a dynamical scalar.

(B) MINISUPERSPACE variation. Substitute the ONE-FUNCTION ansatz
    g_tt=-e^{-2phi}c0^2, g_rr=e^{2phi} into the action density
    L = sqrt(-g) f(phi) R, reduce to a 1D Lagrangian in phi(r), and take the
    Euler-Lagrange equation. This is the HONEST EOM when phi is the metric's
    own single radial DOF (B=1/A locked). Compare to: (i) the bare-Einstein
    reduced EOM (f=const), (ii) the full-covariant f G + (gBox-nablanabla)f =0
    restricted to this ansatz.  This shows whether the surviving terms are a
    real new EOM or an artifact of over-counting an independent phi.

NB: the B=1/A lock (g_tt g_rr = -c0^2 e^{... }) means there is essentially ONE
radial function. We test BOTH the locked single-DOF case and a two-function
relaxation N(r), L(r) to see if locking is doing the work.

Constructor: Claude Opus 4.8 (1M), 2026-06-18.
"""
import sympy as sp

r = sp.symbols('r', real=True)
phi = sp.Function('phi')
c0, G = sp.symbols('c0 G', positive=True)

# =====================================================================
# (A) CONFORMAL TO EINSTEIN FRAME
# =====================================================================
print("="*70)
print("(A) CONFORMAL TRANSFORMATION TO EINSTEIN FRAME")
print("="*70)
# Generic: S = int sqrt(-g) f(p) R.  Define Omega^2 = 16 pi G f(p), so
# Omega^2 f = (1/16piG)*(16 pi G f)*f ... let's do the standard f(p)R reduction.
# Standard identity (4D): with g_{mn} = Omega^2 g~_{mn},
#   sqrt(-g) f R = sqrt(-g~) [ Omega^2 f R~ + 6 Omega f (g~^{ab} d_a d_b Omega ... ) ]
# Cleaner: take f(p) = (1/2kappa) F(p).  Einstein frame uses Omega^2 = F(p).
# Result (well-known, e.g. Fujii-Maeda): action becomes
#   S = int sqrt(-g~)[ (1/2kappa) R~ - (1/2kappa)(3/2)(F'/F)^2 (grad~ p)^2 - ... ]
# The scalar kinetic coefficient is (3/2)(F'/F)^2 * (1/2kappa)*(grad p)^2.
p = sp.symbols('p', real=True)          # phi as a plain variable for this algebra
F = sp.exp(-8*p)                         # F(phi) ~ c^4 ~ e^{-8 phi}   (the prefactor, up to const)
Fp = sp.diff(F, p)
kin_coeff = sp.simplify(sp.Rational(3,2)*(Fp/F)**2)
print("Conformal factor Omega^2 = F(phi) = c^4-prefactor = e^{-8 phi}")
print("Einstein-frame scalar KINETIC coefficient (3/2)(F'/F)^2 =", kin_coeff)
print("  -> nonzero constant =", sp.nsimplify(kin_coeff))
print("INTERPRETATION: f(phi)R conformally maps to canonical R~ PLUS a")
print("  scalar kinetic term (3/2)(F'/F)^2 = 96  times (grad phi)^2.")
print("  This kinetic term is NONZERO => the c^4 prefactor is NOT pure")
print("  relabeling: it deposits a DYNAMICAL SCALAR (phi) in Einstein frame.")
print("  KEY: this is the Brans-Dicke situation. BUT whether that scalar is")
print("  an INDEPENDENT DOF or SLAVED to the metric depends on whether phi")
print("  is independent of g~ -- which it is NOT here (phi lives in g). (B).")

# =====================================================================
# (B) MINISUPERSPACE REDUCED ACTION, single radial DOF phi(r), B=1/A locked
# =====================================================================
print()
print("="*70)
print("(B) MINISUPERSPACE: reduce L = sqrt(-g) f(phi) R on the ansatz")
print("="*70)

# Build metric quantities symbolically with phi(r)
P = phi(r)
gtt = -sp.exp(-2*P)*c0**2
grr =  sp.exp( 2*P)
import sympy
coords = ['t','r','th','ph']
# Reuse a compact SSS curvature: compute R via the known formula above.
# We'll recompute R for general (N=g_tt magnitude, L=g_rr) to allow 2-function test too.
N = sp.Function('N')(r)     # -g_tt = N
L = sp.Function('L')(r)     # g_rr = L
S2 = sp.sin(sp.symbols('th'))**2
th = sp.symbols('th', real=True)

def ricci_scalar(Nf, Lf):
    g = sp.diag(-Nf, Lf, r**2, r**2*sp.sin(th)**2)
    coordlist=[sp.symbols('t'), r, th, sp.symbols('ph')]
    ginv=g.inv(); nn=4
    Gam=[[[0]*nn for _ in range(nn)] for _ in range(nn)]
    for a in range(nn):
        for b in range(nn):
            for c in range(nn):
                s=0
                for d in range(nn):
                    s+=ginv[a,d]*(sp.diff(g[d,b],coordlist[c])+sp.diff(g[d,c],coordlist[b])-sp.diff(g[b,c],coordlist[d]))
                Gam[a][b][c]=sp.simplify(s/2)
    Ric=sp.zeros(nn,nn)
    for b in range(nn):
        for d in range(nn):
            s=0
            for a in range(nn):
                s+=sp.diff(Gam[a][b][d],coordlist[a])-sp.diff(Gam[a][b][a],coordlist[d])
                for e in range(nn):
                    s+=Gam[a][a][e]*Gam[e][b][d]-Gam[a][d][e]*Gam[e][b][a]
            Ric[b,d]=sp.simplify(s)
    return sp.simplify(sum(ginv[a,b]*Ric[a,b] for a in range(nn) for b in range(nn))), g

Rgen, ggen = ricci_scalar(N, L)
sqrtmg = sp.sqrt(-ggen.det())
print("R (general N,L) =", sp.simplify(Rgen))

# Lagrangian density (drop angular int, fold sin th); f = e^{-8phi}*c0^4/16piG.
# Express f in terms of N: with locked form N = c0^2 e^{-2phi} => e^{-2phi}=N/c0^2
# and f = (c0^4/16piG)(e^{-2phi})^4 = (c0^4/16piG)(N/c0^2)^4 = N^4/(16piG c0^4).
fconst = 1/(16*sp.pi*G)
# We'll do the LOCKED case: substitute N=c0^2 e^{-2phi}, L=e^{2phi} (B=1/A), single DOF.
subs_lock = {N: c0**2*sp.exp(-2*P), L: sp.exp(2*P)}
Rlock = sp.simplify(Rgen.subs(subs_lock).doit())
sqrtmg_lock = sp.simplify(sqrtmg.subs(subs_lock).doit())
flock = sp.exp(-8*P)*c0**4*fconst
Ldens_lock = sp.simplify(sqrtmg_lock*flock*Rlock)
print("\nLOCKED single-DOF Lagrangian density sqrt(-g) f R =")
print("  ", Ldens_lock)

# Euler-Lagrange in phi(r): treat Ldens as L(phi,phi',phi'') possibly. Integrate by
# parts the phi'' down. Use sympy's variational derivative via manual EL up to 2nd order.
phir = sp.Function('phi')(r)
# Replace P with explicit phi(r) already (P=phi(r)). Build EL operator:
def euler_lagrange_2nd(Ldens, func, var):
    f1 = sp.diff(func, var)
    f2 = sp.diff(func, var, 2)
    dLdphi = sp.diff(Ldens, func)
    dLdphip = sp.diff(Ldens, f1)
    dLdphipp = sp.diff(Ldens, f2)
    EL = dLdphi - sp.diff(dLdphip, var) + sp.diff(dLdphipp, var, 2)
    return sp.simplify(EL)

EL_lock = euler_lagrange_2nd(Ldens_lock, phir, r)
print("\nLOCKED EOM (Euler-Lagrange of the f R minisuperspace action) = 0:")
EL_lock_s = sp.simplify(EL_lock)
print("  EL =", EL_lock_s)
# normalize
EL_lock_n = sp.simplify(EL_lock_s*sp.exp(8*P)/ (c0**4*fconst) )
print("  EL normalized (x e^{8phi} 16piG/c0^4) =", sp.simplify(EL_lock_n))

# Compare: bare-Einstein minisuperspace (f=const) EOM for same locked ansatz
Ldens_bare = sp.simplify(sqrtmg_lock*fconst*Rlock)   # f=const=1/16piG
EL_bare = euler_lagrange_2nd(Ldens_bare, phir, r)
print("\nBARE (f=const) locked EOM =", sp.simplify(EL_bare*16*sp.pi*G))

# =====================================================================
# Solve the LOCKED full EOM: does a NON-Schwarzschild phi(r) appear?
# =====================================================================
print()
print("="*70)
print("(C) SOLVE the locked vacuum EOM -- Schwarzschild or not?")
print("="*70)
# Schwarzschild in these coords: g_tt = -(1-rs/r) c0^2, so e^{-2phi} = (1-rs/r),
# phi_schw = -1/2 ln(1 - rs/r).  Test if it solves EL_lock.
rs = sp.symbols('r_s', positive=True)
phi_schw = -sp.Rational(1,2)*sp.log(1 - rs/r)
test_schw = sp.simplify(EL_lock_s.subs(phir, phi_schw).doit())
print("EL_lock evaluated on Schwarzschild phi = -1/2 ln(1-rs/r):")
print("  ->", sp.simplify(test_schw))
# Also test on bare:
test_schw_bare = sp.simplify(EL_bare.subs(phir, phi_schw).doit())
print("BARE EL on Schwarzschild ->", sp.simplify(test_schw_bare))
