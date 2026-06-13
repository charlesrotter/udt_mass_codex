#!/usr/bin/env python3
"""(1) Same-operator settlement: fold and gap from ONE EL.
   (2) Cancellation robustness: is it special to m=t/a parameterization,
       or does it survive a generic monotone reparam of the domain?
   (3) Is 'same SL operator governs fold and gap' generic or flat-only?"""
import sympy as sp
a, au, u, kap, T0, t, v = sp.symbols('a a_u u kappa T0 t v', positive=True)
beta = sp.Symbol('beta', real=True)

# ---- (1) ONE EL, both objects are features of it ----
# EL operator L[v] = (p v')' - (b/8k)[(1-2k/f)e^-2v - beta e^v].
# FOLD = saddle-node of the static OFF (beta=0) BVP.
# GAP  = zero of the linearization about v=0 of the ON (beta=1) BVP.
# Both use the SAME p, b, weight. Show the linearized operator about
# v=0 is -(p psi')' - (b/8k)(-2(1-2k/f) - beta) psi.  Truncated gamma:
#   (1-2k/f)->1 => coefficient -(b/8k)(-2-beta).  beta=1 => +3b/(8k).
vf = sp.Symbol('v', real=True)
b, p = sp.symbols('b p', positive=True)
src = (b/(8*kap))*(sp.exp(-2*vf) - beta*sp.exp(vf))   # gamma->1
coef = sp.simplify(sp.diff(src, vf).subs(vf, 0))
print("linearized source slope d/dv|0 =", coef, "  (=> -3b/8k at beta=1)")
print("  beta=1:", sp.simplify(coef.subs(beta,1)))   # -3b/(8k)

# So the gap pencil is -(p psi')' = +3b/(8k) psi (move sign), exactly
# the same p,b as the fold's nonlinear operator. SAME Sturm-Liouville
# weight (p, and b as the spectral weight). CONFIRMED structurally.

# ---- (2) cancellation under generic monotone domain reparam ----
# Suppose someone picks a different chart m=h(t). Does the ratio still
# cancel? Ratio cancels because BOTH ks and kc carry the SAME
# (1-u^2)au^2 T0^2/a^2 prefactor and the SAME domain length. The only
# difference is the pure-number eigenvalue (fold: G*/8 via s*; gap:
# pi^2). Reparam rescales BOTH identically (both are the lowest
# Dirichlet object of the SAME interval), so the ratio is reparam-
# invariant. Demonstrate by inserting an arbitrary domain scale L:
L = sp.Symbol('L', positive=True)  # generic domain length in the working chart
Gs = sp.Symbol('Gstar', positive=True)
# fold: Phi L^2/4 = G*/8 (with appropriate Phi);  gap: (pi/L)^2 = wt.
# Both Phi and wt share the b/(8k)-type structure. Ratio = (G*/8 obj)/(pi^2 obj):
# fold weight: ks from  Phi = G*/(2 L^2);  gap: kc from wt = (pi/L)^2 form.
# Symbolic: let Phi = Q/(8 ks), wt-coef = 3 Q/(8 kc) with SAME Q (the
# shared b-structure).  Q cancels => ratio depends only on G*, pi.
Q = sp.Symbol('Q', positive=True)
ks = sp.solve(sp.Eq(Q/(8*kap), Gs/(2*L**2)), kap)[0]
kc = sp.solve(sp.Eq(3*Q/(8*kap), (sp.pi/L)**2), kap)[0]
ratio = sp.simplify(ks/kc)
print("\ngeneric-chart ratio ks/kc =", ratio, " free:", ratio.free_symbols)
print("  == 2 pi^2/(3 G*)?", sp.simplify(ratio - 2*sp.pi**2/(3*Gs))==0)

# ---- (3) flat-only vs generic: does cancellation need C=0 (flat weights)? ----
# On a NON-flat member p,b are functions of t. Then fold uses the
# nonlinear Liouville/Bratu on a VARIABLE-weight SL (no closed s*),
# and gap uses variable-weight Dirichlet eigenproblem (no pi^2). The
# 'value' 2pi^2/(3G*) is then NOT exact -- it's the flat limit. So the
# THEOREM (member-param cancellation to an exact constant) is genuinely
# special to the flat (C=0, f~1/r) member: there both reduce to
# CONSTANT-coefficient problems whose eigen-numbers (G*/8, pi^2) are
# universal. Demonstrate: add a weak slope to p and watch pi^2 move.
print("\n--- non-flat sensitivity: gap eig of -(p psi')'=lam b psi on [0,1] ---")
import mpmath as mp
# p(t)=1+eps t, b=1: shooting for lowest Dirichlet eigenvalue.
def gap_eig(eps):
    def F(lam):
        # solve (p y')' + lam y =0, y(0)=0,y'(0)=1, return y(1)
        def rhs(tt, Y):
            y, yp = Y
            pp = 1+eps*tt; ppp = eps
            # (p y')' = p y'' + p' y' = -lam y => y'' = (-lam y - ppp yp)/pp
            return [yp, (-lam*y - ppp*yp)/pp]
        sol = mp.odefun(rhs, 0, [0,1])
        return sol(1)[0]
    return mp.findroot(F, mp.pi**2)
for eps in [0, 0.3, 1.0]:
    print(f"  eps={eps}: lowest eig ~ {mp.nstr(gap_eig(eps),8)}  (flat={mp.nstr(mp.pi**2,8)})")
print("=> non-flat moves the eigen-number off pi^2; the EXACT 2pi^2/(3G*)")
print("   is a flat-member theorem (consistent w/ banked 1.89-1.90 spread on real cells)")
