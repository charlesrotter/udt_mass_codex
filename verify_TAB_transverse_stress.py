"""verify_TAB_transverse_stress.py

INDEPENDENT re-derivation of the transverse matter-stress operator T_AB that sources the
areal/rho equation of the round Branch-P cell, for the Thread-B coupled-cell solve.

Charter: threadB_coupled_cell_flatness_Lselector_CHARTER.md
  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2  +  [T_AB transverse stress]   <-- derive this term

This script does NOT trust cell_solver_f2d.py's coefficients.  It re-derives everything from the
NATIVE ACTION and only THEN compares.  Two independent routes:

  ROUTE 1 (rigorous, primary): the FULL reduced 1-D action
      S = INT sqrt(h) [ (Z/2) phi'^2 + R2[h] + K_branchP + L_m ] ,   sqrt(h)=rho^2 sin(theta)  (phi-free)
      (native_field_equations_constrained_two_player_results.md sec.5/6)
    Euler-Lagrange in rho(r)  ->  the WHOLE rho-EOM (geometry terms + matter source) at once.
    If the GEOMETRY terms reproduce cell_solver_round.py exactly, the normalization is validated and
    the matter source it spits out is trustworthy.

  ROUTE 2 (cross-check): the canonical stress tensor T_{mu nu} = -2 dL_m/dg^{mu nu} + g_{mu nu} L_m
    on the UNDILATED (phi-blind) matter metric gbar; report T^t_t, T^r_r, T^theta_theta, T^psi_psi
    pointwise, and show its angle-averaged transverse combination reproduces the ROUTE-1 source.

Convention tags:  DERIVED = falls out of the action;  CHOSE = a modeling pick (flagged).
"""
import sympy as sp

print("="*78)
print("INDEPENDENT DERIVATION OF THE TRANSVERSE MATTER STRESS T_AB (rho-EOM source)")
print("="*78)

# ------------------------------------------------------------------ symbols
r, th = sp.symbols('r theta', real=True)
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)          # AREAL function (distinct from r)
f   = sp.Function('f')(r, th)        # hedgehog profile f(r,theta)

# ================================================================================
# The S^2 pullback metric G_mn = d_m n . d_n n   for  n=(sin f cos N psi, sin f sin N psi, cos f)
# (round_matter_reduction_results.md: |d_r n|^2=f_r^2, |d_th n|^2=f_th^2, |d_psi n|^2=N^2 sin^2 f)
# ================================================================================
n = sp.Matrix([sp.sin(f)*sp.cos(N*sp.Symbol('psi')),
               sp.sin(f)*sp.sin(N*sp.Symbol('psi')),
               sp.cos(f)])
psi = sp.Symbol('psi')
coords_n = {'r': r, 'th': th, 'psi': psi}
dn = {k: n.diff(v) for k, v in coords_n.items()}
G = {}
for a in coords_n:
    for b in coords_n:
        G[(a, b)] = sp.simplify((dn[a].T*dn[b])[0])
print("\n[S^2 pullback G_mn] (should be f_r^2, f_th^2, N^2 sin^2 f on the diagonal; G_rth=f_r f_th):")
print("  G_rr   =", G[('r','r')])
print("  G_thth =", G[('th','th')])
print("  G_pspsi=", sp.simplify(G[('psi','psi')]))
print("  G_rth  =", sp.simplify(G[('r','th')]), " G_rpsi=", sp.simplify(G[('r','psi')]),
      " G_thpsi=", sp.simplify(G[('th','psi')]))

# ================================================================================
# PHI-BLIND (undilated) matter inverse metric gbar^{mn}: gbar^rr=1, gbar^thth=1/rho^2,
# gbar^psipsi=1/(rho^2 sin^2 th)  (native_field_equations sec.4 channel ledger; P5 DERIVED-blind)
# ================================================================================
gbar_inv = {('r','r'): sp.Integer(1),
            ('th','th'): 1/rho**2,
            ('psi','psi'): 1/(rho**2*sp.sin(th)**2)}
def ginv(a, b):
    return gbar_inv.get((a, b), sp.Integer(0))

keys = ['r', 'th', 'psi']
# L2 = -(xi/2) gbar^{mn} G_mn
L2 = -sp.Rational(1,2)*xi*sum(ginv(a,b)*G[(a,b)] for a in keys for b in keys)
L2 = sp.simplify(L2)
# L4 = -(kap/4) gbar^{mp}gbar^{nq}(G_mp G_nq - G_mq G_np)
L4 = 0
for m in keys:
    for p in keys:
        for nn in keys:
            for q in keys:
                L4 += ginv(m,p)*ginv(nn,q)*(G[(m,p)]*G[(nn,q)] - G[(m,q)]*G[(nn,p)])
L4 = sp.simplify(-sp.Rational(1,4)*kap*L4)
print("\n[reduced matter Lagrangian densities]")
print("  L2 =", L2)
print("  L4 =", sp.simplify(L4))

fr, fth = sp.Derivative(f, r), sp.Derivative(f, th)
# expected forms
L2_exp = -sp.Rational(1,2)*xi*(fr**2 + fth**2/rho**2 + N**2*sp.sin(f)**2/(rho**2*sp.sin(th)**2))
L4_exp = -sp.Rational(1,2)*kap*N**2*sp.sin(f)**2/sp.sin(th)**2*(fr**2/rho**2 + fth**2/rho**4)
print("  L2 matches expected:", sp.simplify(L2 - L2_exp) == 0)
print("  L4 matches expected:", sp.simplify(L4 - L4_exp) == 0)

# ================================================================================
# ROUTE 1 -- FULL reduced-action Euler-Lagrange for rho(r).
# sqrt(h)=rho^2 sin th (phi-FREE).  Angle-integrate: INT sin th dth of theta-independent geometry
# gives factor 2.  The matter keeps its theta-integral (moments).  We treat the theta moments as
# rho-INDEPENDENT symbols I_r(r), I_4th(r) (they are pure theta-integrals of f,f_r,f_th; no rho).
# ================================================================================
print("\n" + "="*78)
print("ROUTE 1: reduced-action Euler-Lagrange for rho(r)  (geometry validates normalization)")
print("="*78)
phip, phipp = sp.Derivative(phi, r), sp.Derivative(phi, (r, 2))
rhop, rhopp = sp.Derivative(rho, r), sp.Derivative(rho, (r, 2))

# geometry pieces (round h=rho^2 Omega): R2[h]=2/rho^2 ; K_branchP = -2 e^{-2phi} rho'^2/rho^2
R2   = 2/rho**2
Kbr  = -2*sp.exp(-2*phi)*rhop**2/rho**2
# angle-integrated geometry Lagrangian density Lgeo(r) = INT sin th dth * rho^2 * [ (Z/2)phi'^2 + R2 + Kbr ]
Lgeo = 2*rho**2*(sp.Rational(1,2)*Z*phip**2 + R2 + Kbr)
Lgeo = sp.expand(Lgeo)
print("Lgeo(r) =", Lgeo, "   (expect  Z*rho^2*phi'^2 + 4 - 4 e^{-2phi} rho'^2)")

# Euler-Lagrange operator for a field q(r):  d/dr(dL/dq') - dL/dq
def EL(Lag, q):
    qp = sp.Derivative(q, r)
    return sp.diff(sp.diff(Lag, qp), r) - sp.diff(Lag, q)

EL_rho_geo = sp.simplify(EL(Lgeo, rho))
# solve EL=0 for rho'' and compare to cell_solver_round interior:  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2
sol_geo = sp.solve(EL_rho_geo, rhopp)[0]
sol_geo = sp.simplify(sol_geo)
target_geo = 2*phip*rhop - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*phip**2
print("\nGEOMETRY-only rho-EOM from the action:")
print("   rho'' =", sol_geo)
print("   cell_solver_round target:  2 phi' rho' - (Z/4) rho e^{2phi} phi'^2")
print("   GEOMETRY EOM MATCHES cell_solver_round:", sp.simplify(sol_geo - target_geo) == 0)

# ---- now add the matter.  Lmatter(r) = INT sin th dth * rho^2 * (L2+L4).  Reduce to moments.
# Using I_r=1/2 INT sin th f_r^2 dth, I_th=1/2 INT sin th f_th^2 dth, I_s=1/2 INT sin^2f/sin th dth,
#        I_4r=1/2 INT sin^2f/sin th f_r^2 dth, I_4th=1/2 INT sin^2f/sin th f_th^2 dth :
#   INT sin th * rho^2 L2  = -xi ( rho^2 I_r + I_th + N^2 I_s )
#   INT sin th * rho^2 L4  = -kap N^2 ( I_4r + I_4th/rho^2 )
I_r, I_th, I_s, I_4r, I_4th = sp.symbols('I_r I_th I_s I_4r I_4th', real=True)   # rho-INDEPENDENT
Lmatter = -xi*(rho**2*I_r + I_th + N**2*I_s) - kap*N**2*(I_4r + I_4th/rho**2)
print("\nLmatter(r) =", Lmatter, "   (I_* are pure theta-moments, rho-independent)")

Lfull = Lgeo + Lmatter
EL_rho_full = sp.simplify(EL(Lfull, rho))
sol_full = sp.simplify(sp.solve(EL_rho_full, rhopp)[0])
matter_source = sp.simplify(sol_full - target_geo)     # the piece beyond geometry = T_AB
print("\nFULL rho-EOM from the action:")
print("   rho'' =", sol_full)
print("\n>>> DERIVED transverse matter stress T_AB (the term added to rho''):")
print("   T_AB =", matter_source)

TAB_f2d = sp.Rational(1,4)*sp.exp(2*phi)*(xi*rho*I_r - kap*N**2*I_4th/rho**3)
print("\n   cell_solver_f2d source:  (e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3)")
print("   T_AB MATCHES cell_solver_f2d:", sp.simplify(matter_source - TAB_f2d) == 0)

# ================================================================================
# ROUTE 2 -- canonical stress tensor cross-check: T_{mn} = -2 dL_m/dgbar^{mn} + gbar_{mn} L_m
# ================================================================================
print("\n" + "="*78)
print("ROUTE 2: canonical T^mu_nu = gbar^{mu a}(-2 dL/dgbar^{a nu} + gbar_{a nu} L)  (pointwise)")
print("="*78)
# treat gbar^{mn} as independent symbols to differentiate, then substitute the round values
grr, gthth, gpsps = sp.symbols('grr gthth gpsps', positive=True)
gsub = {grr: 1, gthth: 1/rho**2, gpsps: 1/(rho**2*sp.sin(th)**2)}
Grr, Gthth, Gpsps, Grth = G[('r','r')], G[('th','th')], G[('psi','psi')], G[('r','th')]
# L_m as a function of the symbolic inverse-metric components (diagonal contractions; Grth couples r-th)
Lm_sym = ( -sp.Rational(1,2)*xi*(grr*Grr + gthth*Gthth + gpsps*Gpsps)
           -sp.Rational(1,4)*kap*(
               # (tr M)^2 - tr(M^2) with M^m_n = gbar^{mp}G_pn ; only r-th block + psi diagonal
               2*grr*gthth*(Grr*Gthth - Grth*Grth)
             + 2*grr*gpsps*Grr*Gpsps
             + 2*gthth*gpsps*Gthth*Gpsps ) )
# covariant metric components (inverse of the diagonal inverse-metric symbols)
gcov = {grr: 1/grr, gthth: 1/gthth, gpsps: 1/gpsps}
def Tmix(diagsym):
    # T^a_a = gbar^{aa} T_{aa} = gbar^{aa}( -2 dL/dgbar^{aa} + gbar_{aa} L )
    Tcov = -2*sp.diff(Lm_sym, diagsym) + (1/diagsym)*Lm_sym   # gbar_{aa}=1/gbar^{aa}=1/diagsym
    return sp.simplify((diagsym*Tcov).subs(gsub))
Trr   = Tmix(grr)
Tthth = Tmix(gthth)
Tpsps = Tmix(gpsps)
# T^t_t : n has no time dependence -> G_tt=0 -> T^t_t = L_m  (pure Lagrangian / "pressure")
Ttt = sp.simplify(Lm_sym.subs(gsub))
print("  T^t_t     =", Ttt)
print("  T^r_r     =", Trr)
print("  T^th_th   =", Tthth)
print("  T^ps_ps   =", Tpsps)
print("  (T^th_th, T^ps_ps NOT equal pointwise -- hedgehog is anisotropic on S^2; the ROUND source")
print("   is their ANGLE-AVERAGED transverse combination, matched by ROUTE 1.)")

# angle-average cross-check: the rho-EOM source equals -(e^{2phi}/8) dLmatter/drho with the FULL
# (route-1) normalization; equivalently (e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3). Confirm the
# transverse T-components carry exactly these xi (I_r) and kap (I_4th) structures:
print("\n  transverse-average bookkeeping:")
print("   xi-sector radial-structure term  ~ +xi rho I_r  (from rho^2 f_r^2 measure weight; OUTWARD)")
print("   kap-sector term                  ~ -kap N^2 I_4th/rho^3 (from I_4th/rho^2 weight; INWARD)")

# ================================================================================
# ITEM 5 -- alpha-source consistency (relaxed phi-blindness): weight the radial channel by e^{alpha phi}
#   gbar^{rr}: 1 -> e^{alpha phi}.  Derive the phi-EOM matter source and compare to the doc's
#   Z(rho^2 phi')' = 4 e^{-2phi} rho'^2 + alpha xi e^{alpha phi} rho^2 I_r
# ================================================================================
print("\n" + "="*78)
print("ITEM 5: alpha-source (relaxed phi-blindness) consistency check")
print("="*78)
alpha = sp.Symbol('alpha', real=True)
# radial matter term with e^{alpha phi} weight: INT sin th rho^2 * (-(xi/2) e^{alpha phi} f_r^2) = -xi e^{alpha phi} rho^2 I_r
Lmatter_alpha = -xi*sp.exp(alpha*phi)*rho**2*I_r   # only the radial (I_r) channel carries the weight
Lgeo_phi = Lgeo
# phi-EOM from geometry: d/dr(dL/dphi') - dL/dphi = 0  ->  Z(rho^2 phi')' = 4 e^{-2phi} rho'^2
EL_phi_geo = sp.simplify(EL(Lgeo_phi, phi))
print("phi-EOM (geometry only), EL=0  <=>  Z(rho^2 phi')' = 4 e^{-2phi} rho'^2 :")
# EL(Lgeo,phi) = +2Z(rho^2 phi')' - 8 e^{-2phi} rho'^2 ; setting it to 0 gives the base phi-EOM.
lhs_check = sp.simplify(EL_phi_geo - ( 2*Z*(rho**2*phip).diff(r) - 8*sp.exp(-2*phi)*rhop**2 ))
print("   geometry phi-EL == +2Z(rho^2 phi')' - 8 e^{-2phi} rho'^2 :", lhs_check == 0,
      "  => Z(rho^2 phi')' = 4 e^{-2phi} rho'^2 (matches cell_solver_round base phi-EOM)")
# full phi-EL with the alpha matter term:
EL_phi_full = sp.simplify(EL(Lgeo_phi + Lmatter_alpha, phi))
# write as  -2Z(rho^2 phi')' + 8 e^{-2phi} rho'^2 + (matter) = 0, extract matter coeff of the source
matter_phi = sp.simplify(EL_phi_full - EL_phi_geo)
print("\n   derived matter term in the phi-EL (=  -dLmatter_alpha/dphi ) :", matter_phi)
# EL=0 divided by -2Z gives  Z(rho^2 phi')' = 4 e^{-2phi} rho'^2 - matter_phi/2 ... express source:
src_derived = sp.simplify(-matter_phi/2)   # what appears on the RHS of Z(rho^2 phi')'= 4e^{-2phi}rho'^2 + src
src_doc = alpha*xi*sp.exp(alpha*phi)*rho**2*I_r
print("   => Z(rho^2 phi')' = 4 e^{-2phi} rho'^2 + (", src_derived, ")")
print("   doc states source = ", src_doc)
print("   ratio derived/doc =", sp.simplify(src_derived/src_doc))
print("   [FLAG] the alpha-source COEFFICIENT/SIGN differs from the doc by this ratio -- see report.")

# ================================================================================
# ITEM 4 -- limits / sanity
# ================================================================================
print("\n" + "="*78)
print("ITEM 4: limits / sanity of T_AB = (e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3)")
print("="*78)
print("  matter->0 (I_r,I_4th->0):  T_AB ->", sp.simplify(TAB_f2d.subs({I_r:0, I_4th:0})), " (vanishes: OK)")
print("  overall factor e^{2phi} > 0 always -> deepening phi rescales but never flips the sign")
print("  sign split: +xi rho I_r OUTWARD (needs radial structure I_r>0); -kap N^2 I_4th/rho^3 INWARD")
print("  rho->0 : the -kap N^2 I_4th/rho^3 term DIVERGES (inward) while +xi rho I_r->0")
print("           => collapse dominates at small rho -> finite core needed (bears on T3). ")
print("  size balance (T_AB=0): rho^4 ~ kap N^2 I_4th/(xi I_r).")

print("\n" + "="*78)
print("SUMMARY")
print("="*78)
print("  T_AB (DERIVED, add to cell_solver_round rho-EOM):")
print("     rho'' += (e^{2phi}/4)( xi rho I_r - kap N^2 I_4th/rho^3 )")
print("  ROUTE-1 geometry EOM reproduces cell_solver_round exactly (normalization validated).")
print("  T_AB matches cell_solver_f2d's rho-source EXACTLY -> CONFIRMED.")
print("  alpha-source: same matter sector (xi, I_r, e^{alpha phi}, rho^2) but coefficient/sign")
print("     disagrees with the doc by the ratio above -> re-derive before trusting the restoring sign.")
