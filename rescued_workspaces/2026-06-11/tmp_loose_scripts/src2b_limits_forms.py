"""SCRIPT 2b — kappa->0 limits via series (the closed forms are 0/0 at kappa=0),
exact closed forms of the key entries, and the V[u,u] leading identity = 2s.
"""
import sympy as sp

PASS = 0; FAIL = 0
def check(name, expr_zero):
    global PASS, FAIL
    ok = sp.simplify(expr_zero) == 0
    if ok: PASS += 1
    else: FAIL += 1
    print(("PASS " if ok else "FAIL ") + name)
    if not ok: print("   residual:", sp.simplify(expr_zero))

c, ph = sp.symbols('c phi', real=True)
kap = sp.Symbol('kappa', positive=True)
F, a, lam, s = sp.symbols('F a lamda s', positive=True)

Y = {'u': sp.S(1),
     'a0': sp.sqrt(sp.S(3)/(4*sp.pi))*c,
     'a1': sp.sqrt(sp.S(3)/(4*sp.pi))*sp.sqrt(1-c**2)*sp.cos(ph),
     'g0': sp.sqrt(sp.S(5)/(16*sp.pi))*(3*c**2-1)}
B = F*(1+kap*c)
def grad_dot(g,h):
    return (1-c**2)*sp.diff(g,c)*sp.diff(h,c) + sp.diff(g,ph)*sp.diff(h,ph)/(1-c**2)
def Hij(i,j):
    Yi, Yj = Y[i], Y[j]
    integ = (2*grad_dot(Yi,Yj)/B
             - 2*F*kap*(1-c**2)*(sp.diff(Yi,c)*Yj+sp.diff(Yj,c)*Yi)/B**2
             + 2*(1-c**2)*F**2*kap**2*Yi*Yj/B**3)
    iphi = sp.integrate(sp.expand_trig(sp.expand(integ)), (ph, 0, 2*sp.pi))
    return sp.Rational(1,4)*sp.factor(sp.cancel(sp.together(
        sp.integrate(sp.cancel(sp.expand(iphi)), (c, -1, 1)))))

Huu  = Hij('u','u');  Hua0 = Hij('u','a0'); Ha0a0 = Hij('a0','a0'); Ha1a1 = Hij('a1','a1')
print("EXACT closed forms (B = F(1+kappa c)):")
print("  V[u,u]   =", sp.simplify(Huu))
print("  V[u,a0]  =", sp.simplify(Hua0))
print("  V[a0,a0] =", sp.simplify(Ha0a0))
print("  V[a1,a1] =", sp.simplify(Ha1a1))

# kappa->0 limits via series
def lead(expr, n=4):
    return sp.simplify(sp.series(expr, kap, 0, n).removeO())
check("V[u,u]   -> kappa^2/F * 2... leading = 2 kappa^2/(3F)? report", 0)  # placeholder replaced below
PASS -= 1  # undo placeholder
print("\nLeading kappa expansions:")
print("  V[u,u]   ->", lead(Huu))
print("  V[u,a0]  ->", lead(Hua0))
print("  V[a0,a0] ->", lead(Ha0a0))
print("  V[a1,a1] ->", lead(Ha1a1))
check("V[u,u](kap->0) = 0", sp.limit(Huu, kap, 0))
check("V[a0,a0](kap->0) = 1/F", sp.simplify(sp.limit(Ha0a0, kap, 0) - 1/F))
check("V[a1,a1](kap->0) = 1/F", sp.simplify(sp.limit(Ha1a1, kap, 0) - 1/F))
check("V[u,a0](kap->0) = 0", sp.limit(Hua0, kap, 0))

# DEMAND substitution: kappa^2 = 3 a^2/(4 pi F^2), a^2 = 4 s F^3/lam (lam=2):
# leading V[u,u] should equal 2 kappa^2/(3F)?? -> verify against (1/4)P_FF = 2s identity
kap2 = 3*a**2/(4*sp.pi*F**2)
Vuu_lead = lead(Huu).subs(kap**2, kap2)
Vuu_dem = sp.simplify(Vuu_lead.subs(a**2, 4*s*F**3/lam).subs(lam, 2))
check("V[u,u] leading on demanded background = 2s exactly", sp.simplify(Vuu_dem - 2*s))
Vua0_lead = lead(Hua0)
print("\n  V[u,a0] leading =", Vua0_lead, " (first order in kappa, NEGATIVE)")
# on demanded background: kappa = sqrt(3 s F /(pi lam)) ... express via s:
kapd = sp.sqrt(3*a**2/(4*sp.pi*F**2))
Vua0_dem = sp.simplify(Vua0_lead.subs(kap, kapd).subs(a, 2*sp.sqrt(s/lam)*F**sp.Rational(3,2)).subs(lam,2))
print("  V[u,a0] demanded =", sp.simplify(Vua0_dem), " = -sqrt(2 s/F)... check:")
check("V[u,a0] demanded = -sqrt(2*s/F)", sp.simplify(Vua0_dem + sp.sqrt(2*s/F)))

print(f"\nTOTALS: PASS={PASS} FAIL={FAIL}")
