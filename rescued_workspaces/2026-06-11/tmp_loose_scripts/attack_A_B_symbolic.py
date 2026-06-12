"""Independent adversarial re-derivation (blind verification).

A. Wave operator reduction; tortoise form; Coulomb-tail question.
B. Tortoise potential V, Schwarzschild control, core inverse-square
   coefficient, indicial roots; limit-circle audit of the center endpoint.
"""
import sympy as sp

r, a, lam, w, M, kap, p, C = sp.symbols(
    "r a lam omega M kappa p C", positive=True)

print("=" * 72)
print("(1) Is the probe equation the massless wave op on the stated metric?")
print("=" * 72)
# ds^2 = -f dt^2 + f^-1 dr^2 + r^2 dOmega^2; phi = e^{-iwt} Y_lm R(r)
# Box phi = (1/sqrt(-g)) d_mu( sqrt(-g) g^munu d_nu phi ) = 0
# sqrt(-g) = r^2 sin(th); g^tt=-1/f, g^rr=f, angular gives -lam/r^2
f = sp.Function("f", positive=True)(r)
R = sp.Function("R")(r)
box = (w**2 / f) * R + sp.diff(r**2 * f * sp.diff(R, r), r) / r**2 \
    - lam * R / r**2
claimed = -sp.diff(r**2 * f * sp.diff(R, r), r) + lam * R - w**2 * (r**2 / f) * R
print("  Box*(-r^2) - claimed_eq =", sp.simplify(-r**2 * box - claimed))

print("=" * 72)
print("(2) Tortoise reduction from scratch: u = rR, d rho = dr / f")
print("=" * 72)
u = sp.Function("u")(r)
Rsub = u / r
E = (-sp.diff(r**2 * f * sp.diff(Rsub, r), r) + lam * Rsub
     - w**2 * (r**2 / f) * Rsub)
# u_{rho rho} = f d/dr ( f du/dr )
u_rr = f * sp.diff(f * sp.diff(u, r), r)
V_claim = f * (lam / r**2 + sp.diff(f, r) / r)
resid = sp.simplify((f / r) * E - (-u_rr + (V_claim - w**2) * u))
print("  residual of (f/r)E = -u_rhorho + (V - w^2)u :", resid)
print("  --> omega^2 enters with coefficient EXACTLY 1 (no omega^2*a/r term")
print("      survives in tortoise form; that term is a coordinate artifact).")

print("=" * 72)
print("(3) Schwarzschild control")
print("=" * 72)
Vs = sp.expand(V_claim.subs(f, 1 - 2 * M / r).doit())
target = lam / r**2 + 2 * M * (1 - lam) / r**3 - 4 * M**2 / r**4
print("  V(f=1-2M/r) - RW form =", sp.simplify(Vs - target))

print("=" * 72)
print("(4) Tail potential with f = 1 + a/r: is there ANY Coulomb 1/rho term?")
print("=" * 72)
ft = 1 + a / r
Vt = sp.expand(V_claim.subs(f, ft).doit())
print("  V(r) =", Vt, "   [lam/r^2 + (lam-1)a/r^3 - a^2/r^4]")
ser = sp.series(Vt, r, sp.oo, 5)
print("  large-r series:", ser)
# rho(r) for the tail:
rho_expr = sp.integrate(1 / ft, r)  # = r - a*log(a + r)
print("  rho(r) =", rho_expr, " (+const)  -->  r = rho + a ln rho + ...")
# In rho, V ~ lam/rho^2 + O(ln rho / rho^3): strictly shorter range than 1/rho.
rho = sp.symbols("rho", positive=True)
r_of_rho = rho + a * sp.log(rho)  # leading inversion
V_in_rho = Vt.subs(r, r_of_rho)
serr = sp.series(sp.expand(V_in_rho), rho, sp.oo, 3).removeO()
print("  V(rho) large-rho:", sp.simplify(serr), "+ O(log(rho)/rho^3)")
coul = sp.limit(sp.expand(serr - lam / rho**2) * rho, rho, sp.oo)
print("  coefficient of 1/rho (Coulomb term) in V(rho):", coul)

print("=" * 72)
print("(5) The Coulomb-bound-state question, exactly")
print("=" * 72)
# omega^2 = -kappa^2: tortoise solutions u ~ e^{+-kappa rho}(1+O(1/rho)).
# Decaying branch back in r:  e^{-kappa rho} = e^{-kappa(r - a ln r)}
decay = sp.exp(-kap * (r - a * sp.log(r)))
print("  decaying branch u_- = e^{-kappa rho} =", sp.simplify(decay),
      "= e^{-kappa r} * r^{a kappa}")
# Hydrogen comparison: u ~ e^{-kappa r} r^{Z/kappa}. Effective Z here:
Z_eff = a * kap * kap
print("  matching r-power a*kappa = Z_eff/kappa  ==>  Z_eff =", Z_eff)
print("  -> effective Coulomb charge is omega-dependent: Z_eff = a*kappa^2,")
print("     vanishing QUADRATICALLY at threshold. Coulomb level count ~")
print("     Z/kappa = a*kappa -> 0 as kappa -> 0: NO Rydberg accumulation.")
# Verify directly: substitute u = e^{-kappa rho} into exact tail tortoise eq;
# show the residual is the SHORT-RANGE V only (no 1/rho piece to cancel).
u_trial = sp.exp(-kap * (r - a * sp.log(r + a)))
lhs = ft * sp.diff(ft * sp.diff(u_trial, r), r) - (kap**2 + Vt) * u_trial
print("  residual of e^{-kappa rho} in exact tail eq, *e^{+kappa rho}:")
resid5 = sp.simplify(lhs / u_trial)
print("   ", sp.simplify(sp.expand(resid5)))
print("  large-r order:", sp.series(resid5, r, sp.oo, 3))
print()
print("  STRUCTURAL REASON NO BINDING: a/r enters the WEIGHT w = r^2/f of")
print("  L R = omega^2 w R, not the operator L. For omega^2 = -kappa^2 the")
print("  whole weighted term -kappa^2 w |R|^2 is NEGATIVE-definite while")
print("  <R, L R> = Q[R] > 0 (f>0, lam>0). Hydrogen binds because -Z/r sits")
print("  inside the OPERATOR and makes the form indefinite. Here it cannot.")

print("=" * 72)
print("(6) Near-center tortoise coefficient for f = C r^{-p}")
print("=" * 72)
fc = C * r**(-p)
rho_c = sp.integrate(1 / fc, r)
print("  rho(r) =", rho_c, "  -> r = (C(1+p) rho)^{1/(1+p)}")
Vc = sp.expand(V_claim.subs(f, fc).doit())
print("  V(r) =", Vc)
# express the -p C^2 r^{-2p-2} piece in rho:
r_sub = (C * (1 + p) * rho) ** (sp.Integer(1) / (1 + p))
piece = (-p * C**2 * r**(-2 * p - 2)).subs(r, r_sub)
g_coeff = sp.simplify(-piece * rho**2)
print("  attractive piece * rho^2 = -g with g =", sp.simplify(g_coeff))
print("  g(p=1/3) =", sp.nsimplify(g_coeff.subs(p, sp.Rational(1, 3))))
# subcriticality on the finite-action branch p<1/2:
gmax_half = g_coeff.subs(p, sp.Rational(1, 2))
print("  g(p=1/2) =", gmax_half, "= 2/9 < 1/4;  g(p)=p/(1+p)^2 max at p=1 ->",
      g_coeff.subs(p, 1))
# the lam piece: C lam r^{-p-2} ~ rho^{-(p+2)/(1+p)}, exponent < 2:
expo = sp.simplify((p + 2) / (1 + p))
print("  lam-term exponent in rho:", expo, "  (= 7/4 at p=1/3, < 2: subdominant)")
# vacuum tail center: f ~ a/r is p=1 => g = 1/4 critical:
print("  vacuum-tail center (p=1): g =", g_coeff.subs(p, 1), " (exactly critical)")

print("=" * 72)
print("(7) Indicial roots p(1-p)/2 = s")
print("=" * 72)
ps = sp.symbols("p_")
for s_val in (sp.Rational(1, 9), sp.Rational(1, 3)):
    sols = sp.solve(sp.Eq(ps * (1 - ps) / 2, s_val), ps)
    print(f"  s = {s_val}: p =", sols)
print("  s=1/3: 1-8s = ", 1 - 8 * sp.Rational(1, 3), "< 0 -> complex roots")
print("  deep-core ODE (W=1): f_xx + f_x + 2s f = 0, char mu^2+mu+2s=0,")
mu = sp.symbols("mu")
print("   mu =", sp.solve(mu**2 + mu + 2 * sp.Rational(1, 3), mu))
print("   -> f = e^{-x/2}[A cos(nu x)+B sin(nu x)], oscillates and changes")
print("      sign as x->-inf for ANY (A,B) != 0: f >= 1 unsatisfiable. The")
print("      no-background claim holds for ALL deep-core solutions, not just")
print("      pure power laws.")

print("=" * 72)
print("(8) ADVERSARIAL: endpoint classification at r=0, softened core p>0")
print("=" * 72)
al = sp.symbols("alpha")
# Frobenius roots of R at the center (dominant balance -(C r^{2-p} R')' = 0
# + lam R subleading? check orders): R ~ r^alpha:
expr = -sp.diff(C * r**(2 - p) * sp.diff(r**al, r), r) + lam * r**al
expr = sp.expand(expr)
print("  -(r^2 f R')' + lam R on r^alpha:", expr)
print("  derivative term ~ r^{alpha-p} dominates lam r^alpha for p>0;")
ind = sp.solve(sp.expand(-C * al * (al + 1 - p)), al)
print("  indicial roots alpha =", ind, " (alpha=0 regular, alpha=p-1 singular)")
# weight integrability of BOTH branches near 0: (r^2/f) R^2 ~ r^{2+p+2alpha}
for alv, name in ((0, "regular"), (p - 1, "singular")):
    e_w = sp.simplify(2 + p + 2 * alv)
    e_form = sp.simplify(2 - p + 2 * (alv - 1))  # r^2 f R'^2
    print(f"  {name} branch alpha={alv}: weight-int exponent {e_w} "
          f"(> -1 iff p > {sp.solve(sp.Eq(e_w, -1), p) or 'always'}), "
          f"form-int exponent {e_form}")
print("  singular branch: weight exponent 3p > -1 ALWAYS -> L^2(w) at 0;")
print("  form exponent p-2 < -1 for p<1 -> infinite probe energy.")
print("  ==> for 0 < p < 1/2 the center endpoint is LIMIT CIRCLE in L^2(w):")
print("      empty point spectrum holds for the Friedrichs (finite-form)")
print("      extension = the stated class N, but other self-adjoint")
print("      extensions exist and can carry point spectrum. (For bounded")
print("      cores p=0: alpha_- = -ell-1, weight exponent 2-2(ell+1) <= -2,")
print("      limit point -> no caveat.)")
e_w_p0 = 2 + 2 * (-2)  # ell=1: alpha=-2
print("      check p=0, ell=1: weight exponent =", e_w_p0, "< -1 -> not L^2. OK")
