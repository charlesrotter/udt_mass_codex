"""verify_f2d_virial_step0.py — Step 0 CAS (MAP §8): virial / free-boundary analysis of the
finite mirrored round cell (Class A), on the DERIVED frame. No solving; identities only.
V1 rigid residual (OBS-3) | V2 reduced Lagrangian reproduces all 3 recorded EOMs (linchpin)
V3 scale symmetry: xi-sector invariant, kappa breaks (OBS-1) | V4 Noether/radial-Hamiltonian
conservation (pointwise) | V5 H at a mirror point = -Lbar; rigid N=1 seal illustration
V6 Derrick scaling identity | V7 second variation about f=theta (N=1): kappa theta-form
manifestly positive; xi theta-form has the BPS zero mode h=sin(theta).
"""
import sympy as sp

r, th, lam, eps = sp.symbols('r theta lambda epsilon', positive=True)
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r); f = sp.Function('f')(r, th)

# ---- densities (per 4pi; theta-density carries sin(th)/2 so that Ibar = integral of density)
s = sp.sin(th)
# matter theta-density (undilated channel, phi-blind; from round_matter_reduction_results.md)
Dm = sp.Rational(1,2)*( (xi/2)*( rho**2*sp.diff(f,r)**2*s + sp.diff(f,th)**2*s + N**2*sp.sin(f)**2/s )
     + (kap*N**2/2)*( sp.sin(f)**2/s*sp.diff(f,r)**2 + sp.sin(f)**2/(s*rho**2)*sp.diff(f,th)**2 ) )
# geometry (P, W=1): per-4pi reduced Lagrangian; theta-density = (s/2)*[...]
Dg = (s/2)*( (Z/2)*rho**2*sp.diff(phi,r)**2 + 2 - 2*sp.exp(-2*phi)*sp.diff(rho,r)**2 )
Lbar_density = Dg - Dm          # total theta-density of the reduced Lagrangian
def th_int(e): return sp.integrate(e, (th, 0, sp.pi))

# ---- V2: EL of Lbar reproduces the three recorded EOMs -------------------------------------
def EL_1d(D, q):
    return sp.diff(th_int(sp.diff(D, sp.diff(q, r))), r) - th_int(sp.diff(D, q))
# phi-EOM (matter is phi-blind: Dm has no phi) -> Z rho^2 phi'' + 2Z rho rho' phi' - 4 e^{-2phi} rho'^2 = 0
ELphi = sp.simplify(EL_1d(Lbar_density, phi))
rec_phi = sp.diff(phi,r,2) - ( 4*sp.exp(-2*phi)*sp.diff(rho,r)**2/(Z*rho**2) - 2*sp.diff(phi,r)*sp.diff(rho,r)/rho )
V2a = sp.simplify(ELphi - (Z*rho**2)*rec_phi) == 0
# rho-EOM with matter moments: do it with f generic; recorded source uses I_r, I_4th
Ir  = th_int(s*sp.diff(f,r)**2)/2; I4t = th_int(sp.sin(f)**2/s*sp.diff(f,th)**2)/2
ELrho = EL_1d(Lbar_density, rho)
rec_rho = sp.diff(rho,r,2) - ( 2*sp.diff(phi,r)*sp.diff(rho,r) - (Z/4)*rho*sp.exp(2*phi)*sp.diff(phi,r)**2
          + (sp.exp(2*phi)/4)*( xi*rho*Ir - kap*N**2*I4t/rho**3 ) )
V2b = sp.simplify(sp.expand(ELrho - (-4*sp.exp(-2*phi))*rec_rho)) == 0
# f-PDE (pointwise EL of -Dm, i.e. of the matter ENERGY density Em = Dm):
ELf = sp.diff(sp.diff(Dm, sp.diff(f,r)), r) + sp.diff(sp.diff(Dm, sp.diff(f,th)), th) - sp.diff(Dm, f)
A = xi*rho**2*s + kap*N**2*sp.sin(f)**2/s
B = xi*s + kap*N**2*sp.sin(f)**2/(rho**2*s)
rec_f = sp.diff(A*sp.diff(f,r), r) + sp.diff(B*sp.diff(f,th), th) \
        - (N**2*sp.sin(f)*sp.cos(f)/s)*( xi + kap*sp.diff(f,r)**2 + kap*sp.diff(f,th)**2/rho**2 )
V2c = sp.simplify(sp.expand(2*ELf - rec_f)) == 0     # factor 2 from the 1/2 in Dm

# ---- V1: rigid residual (OBS-3) -------------------------------------------------------------
res_rigid = sp.simplify(rec_f.subs(f, th).doit())
V1 = sp.simplify(res_rigid - xi*(1-N**2)*sp.cos(th)) == 0

# ---- V3: scaling (r,rho)->(lam r, lam rho), f(r)->f(r/lam): xi-sector covariant, kappa breaks
u = sp.symbols('u', positive=True)
P, R, F = sp.Function('P')(u), sp.Function('R')(u), sp.Function('F')(u, th)
subs_sc = {phi: P.subs(u, r/lam), rho: lam*R.subs(u, r/lam), f: F.subs(u, r/lam)}
def weight(term):
    e = term.subs(subs_sc).doit().subs(r, lam*u)
    return sp.simplify(e)
# each Lagrangian piece picks up lam^w; with dr = lam du a solution maps to a solution iff all
# EOM pieces share one weight. Report weights:
pieces = { 'geo_kin_phi': (Z/2)*rho**2*sp.diff(phi,r)**2, 'geo_R2': sp.Integer(2),
           'geo_K': -2*sp.exp(-2*phi)*sp.diff(rho,r)**2,
           'mat_xi_r': (xi/2)*rho**2*sp.diff(f,r)**2, 'mat_xi_th': (xi/2)*sp.diff(f,th)**2,
           'mat_xi_s': (xi/2)*N**2*sp.sin(f)**2,
           'mat_k_r': (kap*N**2/2)*sp.sin(f)**2*sp.diff(f,r)**2,
           'mat_k_th': (kap*N**2/2)*sp.sin(f)**2*sp.diff(f,th)**2/rho**2 }
# scaled forms; weight read off as power of lam multiplying the u-form
V3_report = {k: sp.simplify(weight(v)) for k, v in pieces.items()}

# ---- V4: pointwise Noether identity for radial translation (H conservation) ----------------
D = Lbar_density
T = sp.diff(phi,r)*sp.diff(D, sp.diff(phi,r)) + sp.diff(rho,r)*sp.diff(D, sp.diff(rho,r)) \
    + sp.diff(f,r)*sp.diff(D, sp.diff(f,r)) - D
ELphi_pt = sp.diff(sp.diff(D, sp.diff(phi,r)), r) - sp.diff(D, phi)
ELrho_pt = sp.diff(sp.diff(D, sp.diff(rho,r)), r) - sp.diff(D, rho)
ELf_pt   = sp.diff(sp.diff(D, sp.diff(f,r)), r) + sp.diff(sp.diff(D, sp.diff(f,th)), th) - sp.diff(D, f)
lhs = sp.diff(T, r)
rhs = sp.diff(phi,r)*ELphi_pt + sp.diff(rho,r)*ELrho_pt + sp.diff(f,r)*ELf_pt \
      - sp.diff( sp.diff(f,r)*sp.diff(D, sp.diff(f,th)), th )
V4 = sp.simplify(sp.expand(lhs - rhs)) == 0

# ---- V5: H at a mirror point (all radial derivatives zero) ----------------------------------
mirror = {sp.diff(phi,r): 0, sp.diff(rho,r): 0, sp.diff(f,r): 0}
T_mirror = sp.simplify(T.subs(mirror))
V5a = sp.simplify(T_mirror + D.subs(mirror)) == 0          # T|mirror = -D|mirror
# rigid N=1 illustration: H=0 at seal -> 2 = xi(I_th+I_s)/... compute:
D0 = th_int(D.subs(mirror).subs(f, th).doit())
seal_cond = sp.simplify(D0)                                 # H=0 <=> this = 0 at the seal
rho_s2 = sp.solve(sp.Eq(seal_cond.subs({N:1}), 0), rho**2)

# ---- V7: second variation of Em about f=theta (N=1) -----------------------------------------
g = sp.Function('g')(r); h = sp.Function('h')(th)
Em = Dm.subs(N, 1)
pert = Em.subs(f, th + eps*g*h).doit()
d2 = sp.simplify(sp.diff(pert, eps, 2).subs(eps, 0)/2)
d2 = sp.expand_trig(sp.expand(d2))
# kappa theta-form after IBP of the cross term 2*sin(2th)*h*h' -> +2*sin(th)*h^2 (poles: h free,
# but the pole factor sin(2th)/s * ... boundary term = 2 cos(th) h^2 |_0^pi — NONZERO unless h(0)=h(pi)=0.
# We verify the INTEGRAND identity and record the boundary term explicitly:
hp = sp.diff(h, th)
# extract kappa-part of d2 exactly:
d2_kap = sp.simplify(sp.expand(d2 - d2.subs(kap, 0)))
d2_xi  = sp.simplify(d2.subs(kap, 0))
# Verified identity used in the results doc: cos(2th)+2 sin^2 th = 1
V7_id = sp.simplify(sp.cos(2*th) + 2*sp.sin(th)**2 - 1) == 0
# xi theta-operator zero mode h = sin(theta):
Q_xi_density = s*hp**2 + (sp.cos(2*th)/s)*h**2
V7_zero = sp.simplify(sp.integrate(Q_xi_density.subs(h, sp.sin(th)).doit(), (th, 0, sp.pi))) == 0

# ========================================================================================
# BLIND-VERIFIER HARDENING (2026-07-01, agent af0a5fdd): the original V5/V6/V7 above passed
# via TRIVIAL identities (H=-Lbar at a mirror is true for ANY Lagrangian; a bare trig identity;
# one zero mode) while the load-bearing claims lived only in prose. These blocks test the actual
# content. NOTE: the transversality THEOREM (free-endpoint variation forces Lbar(r_s)=0) is
# standard variable-endpoint calculus of variations, hand-verified by the blind agent -- NOT a
# CAS identity. What CAS can and does test are its INGREDIENTS (below).
# Momenta depend ONLY on the geometry part (Dm has no phi and no rho'); integrating the generic-f
# matter density over theta is not symbolically closed, so use Lg = th_int(Dg) for the momenta.
Lg = th_int(Dg)                                 # = (Z/2)rho^2 phi'^2 + 2 - 2 e^{-2phi} rho'^2
piphi = sp.diff(Lg, sp.diff(phi, r))            # canonical momentum of phi
pirho = sp.diff(Lg, sp.diff(rho, r))            # canonical momentum of rho
# V5-i: momenta are PURELY first-order (no linear/cross term) => mirror q'=0 IS the natural BC.
V5_piphi_form = sp.simplify(piphi - Z*rho**2*sp.diff(phi, r)) == 0        # pi_phi = Z rho^2 phi'
V5_pirho_form = sp.simplify(pirho + 4*sp.exp(-2*phi)*sp.diff(rho, r)) == 0  # pi_rho = -4 e^{-2phi} rho'
V5_nat_phi = sp.simplify(piphi.subs(mirror)) == 0                         # natural BC holds at mirror
V5_nat_rho = sp.simplify(pirho.subs(mirror)) == 0
V5_nat_f   = sp.simplify(sp.diff(Lbar_density, sp.diff(f, r)).subs(mirror)) == 0  # f natural BC (~ f_r)
# V5-ii: H=0 is a GENUINE independent condition -- H|mirror = -Lb|mirror = -seal_cond is NOT
# identically 0 (seal_cond computed above = Lbar at a rigid mirror, generically nonzero).
V5_indep = sp.simplify(seal_cond) != 0

# V6 Derrick: genuine single-breaker STRUCTURE. Under (r,rho)->(lam r,lam rho), f(r)->f(r/lam):
# geometry + every xi piece is scale-INVARIANT (density weight 0); both kappa pieces carry lam^-2.
# => action S(lam) = lam*A + lam^-1*B (dr = lam du) => stationarity forces the Derrick identity A=B.
_geo_xi = ['geo_kin_phi', 'geo_R2', 'geo_K', 'mat_xi_r', 'mat_xi_th', 'mat_xi_s']
_kap    = ['mat_k_r', 'mat_k_th']
V6_geoxi_invariant = all(not V3_report[k].has(lam) for k in _geo_xi)
V6_kappa_breaks    = all(not sp.simplify(V3_report[k]*lam**2).has(lam) for k in _kap)

# V7 hardening: the kappa-part g^2 theta-integrand, AFTER integration by parts, equals the
# manifestly-positive form (kappa/4 rho^2) g^2 (sin h'^2 + h^2/sin). Test the definite integrals
# match for TWO independent admissible h (h(0)=h(pi)=0); test the IBP boundary term vanishes.
d2_kap_g2 = sp.simplify(d2_kap.subs(sp.diff(g, r), 0))  # g^2 potential piece (kill the g'^2 kinetic term; g,g' independent)
claimed_pos = (kap/(4*rho**2))*g**2*(s*sp.diff(h, th)**2 + h**2/s)
def _v7_match(htest):
    raw = sp.integrate(sp.simplify(d2_kap_g2.subs(h, htest).doit()), (th, 0, sp.pi))
    cl  = sp.integrate(sp.simplify(claimed_pos.subs(h, htest).doit()), (th, 0, sp.pi))
    return sp.simplify(raw - cl) == 0
V7_pos_h1 = _v7_match(sp.sin(th)**2)
V7_pos_h2 = _v7_match(sp.sin(th)*sp.sin(2*th))
# IBP boundary term sin(2th) h^2 |_0^pi = 0 (sin(2th)=0 at both poles, for ANY h):
_bt = sp.sin(2*th)*h**2
V7_bdry = (sp.simplify(_bt.subs(th, 0)) == 0) and (sp.simplify(_bt.subs(th, sp.pi)) == 0)

print("V1 rigid residual == xi(1-N^2)cos(th):", V1)
print("V2a phi-EOM reproduced:", V2a, "| V2b rho-EOM+source reproduced:", V2b, "| V2c f-PDE reproduced:", V2c)
print("V3 scaled Lagrangian pieces (weight = power of lam):")
for k, v in V3_report.items(): print("   ", k, "->", v)
print("V4 pointwise Noether identity (H conservation):", V4)
print("V5 [TRIVIAL, kept for context] T|mirror = -D|mirror:", V5a, "(true for ANY Lagrangian)")
print("   rigid N=1 seal condition:", sp.nsimplify(seal_cond), "= 0  -> rho_s^2 =", rho_s2, " (xi=kappa=1 -> 1/2)")
print("V5 [GENUINE ingredients of the transversality argument]:")
print("   pi_phi = Z rho^2 phi' (purely 1st order):", V5_piphi_form, "| pi_rho = -4 e^{-2phi} rho':", V5_pirho_form)
print("   natural BC at mirror pi_phi=0:", V5_nat_phi, "| pi_rho=0:", V5_nat_rho, "| pi_f~f_r=0:", V5_nat_f)
print("   H=0 is a NONtrivial independent condition (Lb|mirror != 0):", V5_indep)
print("   [transversality THEOREM Lb(r_s)=0 = standard variable-endpoint CoV; hand-verified, not CAS]")
print("V6 [GENUINE] Derrick single-breaker: geo+xi scale-invariant:", V6_geoxi_invariant,
      "| kappa carries lam^-2:", V6_kappa_breaks, "=> action S=lam A + lam^-1 B => Derrick A=B")
print("V7 [context] cos2t+2sin^2t=1:", V7_id, "| Q_xi[sin th]=0 (BPS zero mode):", V7_zero)
print("V7 [GENUINE] kappa g^2 form = manifestly-positive (sin h'^2 + h^2/sin) after IBP:")
print("   match for h=sin^2:", V7_pos_h1, "| h=sin*sin2:", V7_pos_h2, "| IBP boundary term=0:", V7_bdry)
print("d2 xi-part:", sp.simplify(d2_xi))
print("d2 kappa-part:", sp.simplify(d2_kap))
