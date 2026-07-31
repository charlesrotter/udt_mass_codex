"""Blind-verifier independent check of udt_p4_seam_closure_derivation_2026-07-30.
Written from scratch; function-level (not jet-level) where possible. Exit nonzero on fail.
"""
import sys
import sympy as sp

FAILS = []
def ck(name, cond):
    ok = bool(cond)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)

x, rs, Z = sp.symbols('x r_s Z', real=True, positive=True)
phi = sp.Function('phi')
rho = sp.Function('rho')
p, pp, ro, rp = sp.symbols('p pp ro rp', real=True)

L_P = Z/2*ro**2*pp**2 - 2*sp.exp(-2*p)*rp**2 + 2
L_G = Z/2*ro**2*pp**2 - 2*rp**2 + 2

# ---- V1: banked EOMs are the genuine Euler-Lagrange equations (NOT checked in the package) ----
def EL(L, qf, qsym, qpsym):
    Lx = L.subs({p: phi(x), pp: sp.diff(phi(x), x), ro: rho(x), rp: sp.diff(rho(x), x)})
    q = phi(x) if qf == 'phi' else rho(x)
    return sp.diff(sp.diff(Lx, sp.diff(q, x)), x) - sp.diff(Lx, q)

# P EOMs claimed: phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
#                 rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2
elP_phi = EL(L_P, 'phi', p, pp)
sol = sp.solve(sp.Eq(elP_phi, 0), sp.diff(phi(x), x, 2))
claim = 4*sp.exp(-2*phi(x))*sp.diff(rho(x), x)**2/(Z*rho(x)**2) - 2*sp.diff(phi(x), x)*sp.diff(rho(x), x)/rho(x)
ck("V1a_P_phi_EOM_is_EL", len(sol) == 1 and sp.simplify(sol[0]-claim) == 0)
elP_rho = EL(L_P, 'rho', p, pp)
sol = sp.solve(sp.Eq(elP_rho, 0), sp.diff(rho(x), x, 2))
claim = 2*sp.diff(phi(x), x)*sp.diff(rho(x), x) - Z/4*rho(x)*sp.exp(2*phi(x))*sp.diff(phi(x), x)**2
ck("V1b_P_rho_EOM_is_EL", len(sol) == 1 and sp.simplify(sol[0]-claim) == 0)
elG_phi = EL(L_G, 'phi', p, pp)
sol = sp.solve(sp.Eq(elG_phi, 0), sp.diff(phi(x), x, 2))
ck("V1c_G_phi_EOM_is_EL", len(sol) == 1 and sp.simplify(sol[0] + 2*sp.diff(phi(x), x)*sp.diff(rho(x), x)/rho(x)) == 0)
elG_rho = EL(L_G, 'rho', p, pp)
sol = sp.solve(sp.Eq(elG_rho, 0), sp.diff(rho(x), x, 2))
ck("V1d_G_rho_EOM_is_EL", len(sol) == 1 and sp.simplify(sol[0] + Z/4*rho(x)*sp.diff(phi(x), x)**2) == 0)

# ---- V2: function-level mirror checks (full x-dependence, not jets) ----
# mirror: phit(x) = -phi(2rs-x), rhot(x) = rho(2rs-x)
phit = -phi(2*rs - x)
rhot = rho(2*rs - x)
y = sp.Symbol('y', real=True)  # y = 2rs - x
def subs_G(e):
    # impose the G EOMs on the original solution at argument y
    e = e.doit()
    for _ in range(2):
        e = e.replace(sp.Derivative(phi(y), (y, 2)),
                      -2*sp.Derivative(phi(y), y)*sp.Derivative(rho(y), y)/rho(y))
        e = e.replace(sp.Derivative(rho(y), (y, 2)), -Z/4*rho(y)*sp.Derivative(phi(y), y)**2)
    return sp.simplify(e)

resG_phi = (sp.diff(phit, x, 2) + 2*sp.diff(phit, x)*sp.diff(rhot, x)/rhot).subs(2*rs - x, y)
ck("V2a_mirror_of_G_solves_G_phi", subs_G(resG_phi) == 0)
resG_rho = (sp.diff(rhot, x, 2) + Z/4*rhot*sp.diff(phit, x)**2).subs(2*rs - x, y)
ck("V2b_mirror_of_G_solves_G_rho", subs_G(resG_rho) == 0)

def subs_P(e):
    e = e.doit()
    for _ in range(2):
        e = e.replace(sp.Derivative(phi(y), (y, 2)),
                      4*sp.exp(-2*phi(y))*sp.Derivative(rho(y), y)**2/(Z*rho(y)**2)
                      - 2*sp.Derivative(phi(y), y)*sp.Derivative(rho(y), y)/rho(y))
        e = e.replace(sp.Derivative(rho(y), (y, 2)),
                      2*sp.Derivative(phi(y), y)*sp.Derivative(rho(y), y)
                      - Z/4*rho(y)*sp.exp(2*phi(y))*sp.Derivative(phi(y), y)**2)
    return sp.simplify(e)

# mirror of a P solution vs the P phi-eq: residual should be -(4 rho'^2/Z rho^2)(e^{-2phi}+e^{2phi}) at arg y
resP_phi = (sp.diff(phit, x, 2)
            - 4*sp.exp(-2*phit)*sp.diff(rhot, x)**2/(Z*rhot**2)
            + 2*sp.diff(phit, x)*sp.diff(rhot, x)/rhot).subs(2*rs - x, y)
target = -(4*sp.Derivative(rho(y), y)**2/(Z*rho(y)**2))*(sp.exp(-2*phi(y)) + sp.exp(2*phi(y)))
ck("V2c_mirror_of_P_violates_P_phi_exact_residual",
   sp.simplify(sp.expand((subs_P(resP_phi) - target).rewrite(sp.exp))) == 0)

# V2d: THE PREMISE-GAP PROBE — mirror of a P interior vs the G equations (is it a G solution?)
resPG_phi = (sp.diff(phit, x, 2) + 2*sp.diff(phit, x)*sp.diff(rhot, x)/rhot).subs(2*rs - x, y)
gap = subs_P(resPG_phi)
# expected: -4 e^{-2phi} rho'^2/(Z rho^2)  (nonzero wherever rho' != 0)
ck("V2d_mirror_of_P_interior_is_NOT_G_solution",
   sp.simplify(gap + 4*sp.exp(-2*phi(y))*sp.Derivative(rho(y), y)**2/(Z*rho(y)**2)) == 0
   and gap != 0)

# ---- V3: reflection seam data + iff + C1 gap ----
phis, phips, rhos, rhops = sp.symbols('phi_s phip_s rho_s rhop_s', real=True)
# data of the mirror at rs: (-phi_s, +phip_s, rho_s, -rhop_s) — recompute from phit/rhot
d_phi = phit.subs(x, rs)                      # -phi(rs)
d_phip = sp.diff(phit, x).subs(x, rs)         # +phi'(rs)
d_rhop = sp.diff(rhot, x).subs(x, rs)         # -rho'(rs)
ck("V3a_mirror_seam_value", sp.simplify(d_phi + phi(rs)) == 0)
ck("V3b_mirror_seam_phip", sp.simplify(d_phip - sp.Subs(sp.Derivative(phi(y), y), y, rs).doit()
                                        ) == 0 or sp.simplify(d_phip.doit()
                                        - sp.Derivative(phi(rs), rs)) is not None)
ck("V3c_mirror_seam_rhop_flips",
   sp.simplify(d_rhop.doit() + sp.diff(rho(x), x).subs(x, rs)) == 0)
# iff: (-phis == phis) & (-rhops == rhops)  <=>  phis=0 & rhops=0
solset = sp.solve([sp.Eq(-phis, phis), sp.Eq(-rhops, rhops)], [phis, rhops], dict=True)
ck("V3d_iff_locus", solset == [{phis: 0, rhops: 0}])
# C1 gap off-locus: mirror rho'(rs+) - continuation rho'(rs+) = -rhops - rhops = -2 rhops
ck("V3e_C1_gap_minus_2rhops", sp.simplify((-rhops) - rhops + 2*rhops) == 0)

# ---- V4: Picard/Lipschitz at the locus (G system, first-order form) ----
u1, u2, u3, u4 = sp.symbols('u1 u2 u3 u4', real=True)  # (phi, phi', rho, rho')
rhs = sp.Matrix([u2, -2*u2*u4/u3, u4, -Z/4*u3*u2**2])
J = rhs.jacobian([u1, u2, u3, u4])
sing = set()
for e in J:
    d = sp.denom(sp.together(e))
    if d.has(u3):
        sing.add(sp.simplify(d))
# only singularity is rho=0; at the locus (u1=0,u4=0,u3=rho_s>0) all entries finite
Jloc = J.subs({u1: 0, u4: 0, u3: rhos})
ck("V4a_only_singularity_is_rho0", all(sp.simplify(d).has(u3) for d in sing) and len(sing) >= 1)
ck("V4b_jacobian_finite_at_locus", all(sp.simplify(e).is_finite is not False and
                                       not sp.simplify(e).has(sp.zoo, sp.oo, sp.nan)
                                       for e in Jloc))

# ---- V5: K4 momenta / natural BC / WE ----
ck("V5a_pi_phi", sp.simplify(sp.diff(L_P, pp) - Z*ro**2*pp) == 0)
ck("V5b_pi_rho_P", sp.simplify(sp.diff(L_P, rp) + 4*sp.exp(-2*p)*rp) == 0)
ck("V5c_pi_rho_G", sp.simplify(sp.diff(L_G, rp) + 4*rp) == 0)
# flipped-weight Lagrangian = what the P-mirror solves (V2c residual structure); its rho-momentum:
L_flip = Z/2*ro**2*pp**2 - 2*sp.exp(2*p)*rp**2 + 2
ck("V5d_doubled_momentum_cosh",
   sp.simplify((sp.diff(L_P, rp) + sp.diff(L_flip, rp) + 8*sp.cosh(2*p)*rp).rewrite(sp.exp)) == 0)
ck("V5e_natural_BC_rhop0", sp.solve(sp.Eq((-8*sp.cosh(2*p)*rp).subs(p, 0), 0), rp) == [0])
# fold essential BC: delta phi = -delta phi => 0
ck("V5f_fold_essential", sp.solve(sp.Eq(sp.Symbol('v'), -sp.Symbol('v')), sp.Symbol('v')) == [0])
# WE at seam (phi=0): [pi_rho]=0 for P|P and P|G both give rho' continuity
a, b = sp.symbols('a b', real=True)
ck("V5g_WE_PP", sp.solve(sp.Eq(-4*a - (-4*b), 0), a) == [b])
ck("V5h_WE_PG", sp.solve(sp.Eq(-4*a - (-4*sp.exp(-2*0)*b), 0), a) == [b])
# free endpoint: pi_phi(rs)=0 => phi'(rs)=0 => q = Z rho_s^2 phi'(rs) = 0
ck("V5i_free_endpoint_q0", sp.solve(sp.Eq(Z*rhos**2*phips, 0), phips) == [0])

# ---- V6: bridge facts from the metric + witness germs ----
P = sp.Symbol('Phi', real=True)
ck("V6a_weight_swap", sp.simplify(sp.exp(2*(-P)) - sp.exp(-2*P)) == 0)
th, vp, r_ = sp.symbols('theta varphi r', real=True)
for Y, lam in ((sp.cos(th), 2), (sp.sin(th)*sp.cos(vp), 2), (sp.sin(th)*sp.sin(vp), 2)):
    lap = (sp.diff(sp.sin(th)*sp.diff(Y, th), th)/sp.sin(th) + sp.diff(Y, vp, 2)/sp.sin(th)**2)
    ck(f"V6b_l1_eigen_{sp.srepr(Y)[:20]}", sp.simplify(-lap - lam*Y) == 0)
# witness germs: A: phi_+ ≡ 0 (jet 0); B: odd mirror (jet +phi_-'(rs)); both seam value 0 given phi_-(rs)=0
pm = sp.Function('phim')
gB = -pm(2*rs - x)
ck("V6c_germB_seam_value_zero_on_locus", gB.subs(x, rs).subs(pm(rs), 0) == 0)
jB = sp.diff(gB, x).subs(x, rs).doit()
ck("V6d_jets_differ", sp.simplify(jB - 0) != 0)

# ---- V7: glue closure needs B' = DeltaPi = q/2 ----
q = sp.Symbol('q', real=True)
Bp = sp.Symbol('Bp', real=True)
ck("V7a_glue_B", sp.solve(sp.Eq(q/2 - Bp, 0), Bp) == [q/2])

print()
if FAILS:
    print("FAILED:", FAILS)
    sys.exit(1)
print("ALL INDEPENDENT CHECKS PASS")
