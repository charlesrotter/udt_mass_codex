"""
running_rate_philaw.py (agent 2026-06-18) MODE: OBSERVE
Task 4: the phi-law implied by G_munu = kappa(phi) T_munu, using Box_g phi = -G^th_th.
Also: chart-level confirmation of the T~ conservation absorbability claim (Task 3),
done honestly in the radial chart with a perfect-fluid-like static source.
"""
import sympy as sp

r, c0 = sp.symbols('r c0', positive=True)
phi = sp.Function('phi')(r)
G = sp.symbols('G', positive=True)

# From running_rate_geometry.py (verified):
#   G^t_t = G^r_r = (1 - e^{2phi} - 2 r phi')/r^2 * e^{-2phi}
#   G^th_th = G^ph_ph = (2 r phi'^2 - r phi'' - 2 phi')/r * e^{-2phi}
#   Box_g phi = -G^th_th   (identity, verified)
phip = sp.diff(phi, r); phipp = sp.diff(phi, r, 2)
Gtt = (1 - sp.exp(2*phi) - 2*r*phip)/r**2*sp.exp(-2*phi)
Gthth = (2*r*phip**2 - r*phipp - 2*phip)/r*sp.exp(-2*phi)
Box_phi = -Gthth

print("="*70)
print("TASK 4 — phi-law from the trace of  G_munu = kappa(phi) T_munu")
print("="*70)
# Mixed trace: G^mu_mu = -R = kappa T^mu_mu = kappa T  (T = trace of stress).
# Also the th-th component: G^th_th = kappa T^th_th.  Box phi = -G^th_th = -kappa T^th_th.
# So the phi-law is:   Box_g phi = -kappa(phi) T^th_th .
kappa, Tthth, T = sp.symbols('kappa T_thth T_trace')
print("Pointwise phi-law:  Box_g phi = -G^th_th = -kappa(phi) * T^th_th")
print()
print("  Box_g phi = -(8 pi G/c0^4) e^{8 phi} * T^th_th      [UDT running coupling]")
print("  Box_g phi = -(8 pi G/c0^4)          * T^th_th      [GR, constant coupling]")
print()
print("DEPARTURE FROM GR's phi-law: an explicit e^{8 phi} WEIGHT multiplying the source.")
print("This is a 0th-order-in-derivatives multiplicative weight on T^th_th — a depth-")
print("dependent source enhancement (NOT a kinetic/mu^2 screening term; none inserted).")
print()
print("BUT (Task 3 carryover): absorb e^{8phi} into T~^th_th := e^{8phi} T^th_th and the")
print("phi-law is GR's again with source T~. Whether the WEIGHT is physical is decided by")
print("whether real matter's T^th_th itself already carries the compensating e^{-8phi}")
print("(=> a=metric-locked, GR) or not (=> genuine). Same fork as Task 3.")

print()
print("="*70)
print("CHART-LEVEL CONFIRMATION of absorbability (honest, static source)")
print("="*70)
# Static diagonal source T^mu_nu = diag(-rho, p_r, p_t, p_t) (mixed). Conservation
# nabla_mu T^mu_r = 0 in GR gives the TOV-like relation. Under UDT:
#   nabla_mu T^mu_r = -8 phi' T^r_r ... we test that T~ = e^{8phi} T is conserved.
rho, pr, pt = sp.symbols('rho p_r p_t', cls=sp.Function)
rho = rho(r); pr = pr(r); pt = pt(r)
# covariant divergence of a static diagonal mixed tensor, radial component:
# nabla_mu T^mu_r = dT^r_r/dr + Gamma^mu_{mu r} T^r_r - Gamma^lam_{r mu} T^mu_lam
# Use metric to get the needed Christoffels.
gtt = -sp.exp(-2*phi)*c0**2; grr = sp.exp(2*phi); gthth = r**2; gphph = r**2*sp.sin(sp.Symbol('th'))**2
th = sp.Symbol('th')
gphph = r**2*sp.sin(th)**2
g = sp.diag(gtt, grr, gthth, gphph); ginv = g.inv(); x=[sp.Symbol('t'),r,th,sp.Symbol('ph')]
def christ(g,ginv,x):
    n=4; Gam=[[[0]*n for _ in range(n)] for _ in range(n)]
    for aa in range(n):
        for bb in range(n):
            for cc in range(n):
                s=0
                for dd in range(n):
                    s+=ginv[aa,dd]*(sp.diff(g[dd,bb],x[cc])+sp.diff(g[dd,cc],x[bb])-sp.diff(g[bb,cc],x[dd]))
                Gam[aa][bb][cc]=sp.simplify(s/2)
    return Gam
Gam=christ(g,ginv,x)
# mixed stress components, static: T^t_t=-rho, T^r_r=pr, T^th_th=T^ph_ph=pt
Tmix = sp.diag(-rho, pr, pt, pt)
# nabla_mu T^mu_nu for nu=r:
nu=1
div_r = 0
for mu in range(4):
    div_r += sp.diff(Tmix[mu,nu],x[mu])
    for lam in range(4):
        div_r += Gam[mu][mu][lam]*Tmix[lam,nu] - Gam[lam][nu][mu]*Tmix[mu,lam]
div_r = sp.simplify(div_r)
print("nabla_mu T^mu_r (raw GR-conservation expression) =")
print("  ", div_r)
# UDT requires this to equal -8 phi' T^r_r  (the nu=r component of -8 partial phi T,
# with partial_r phi = phi', T^r_r = pr ... but careful: -8 (partial^mu phi) T_{mu r}
# = -8 g^{rr} phi' T_{r r} -> mixed: = -8 phi' T^r_r). Test the residual:
udt_rhs = -8*phip*Tmix[1,1]
residual = sp.simplify(div_r - udt_rhs)
print("\nUDT source law residual  [nabla T]_r - (-8 phi' T^r_r) =", residual)
print("(this is the modified hydrostatic-equilibrium / TOV relation UDT imposes)")

# Now test conservation of T~ = e^{8phi} T:
Ttil = sp.exp(8*phi)*Tmix
div_r_til = 0
for mu in range(4):
    div_r_til += sp.diff(Ttil[mu,nu],x[mu])
    for lam in range(4):
        div_r_til += Gam[mu][mu][lam]*Ttil[lam,nu] - Gam[lam][nu][mu]*Ttil[mu,lam]
# but div of (scalar * T) needs the scalar derivative; we computed it directly above. Compare:
div_r_til = sp.simplify(div_r_til)
print("\nnabla_mu T~^mu_r  with T~=e^{8phi}T  =")
print("  ", div_r_til)
print("\nIs T~ conserved exactly when UDT's law holds (residual==0)?  Substitute the")
print("UDT relation div_r = -8 phi' pr into div_r_til:")
check = sp.simplify(div_r_til.subs(sp.diff(pr,r), sp.solve(sp.Eq(div_r, udt_rhs), sp.diff(pr,r))[0]))
print("  nabla_mu T~^mu_r  on-shell =", check)
