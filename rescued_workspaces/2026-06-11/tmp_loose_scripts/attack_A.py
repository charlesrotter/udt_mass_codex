"""Independent adversarial re-derivation of A3 (existence result).
All code written from scratch; nothing reused from the repo script."""
import sympy as sp

r = sp.Symbol("r", positive=True)
a, C = sp.symbols("a C", real=True)
al, ga, J, b0 = sp.symbols("alpha gamma J b_0", real=True)
f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)

def EL(L, v):
    return sp.simplify(L.diff(v) - sp.diff(L.diff(v.diff(r)), r)
                       + sp.diff(L.diff(v.diff(r, 2)), r, 2))

print("== (i) perfect square ==")
L_C1 = sp.Rational(1,4)*rho**2*f.diff(r)**2
Dstar = sp.Rational(1,4)*f**2*rho.diff(r)**2 + sp.Rational(1,2)*rho*f*f.diff(r)*rho.diff(r)
print("L_C1 + D* - (1/4)[(f rho)']^2 =", sp.simplify(L_C1 + Dstar - sp.Rational(1,4)*sp.diff(f*rho, r)**2))

print("\n== (ii) EL equations of S = (1/4)int[(f rho)']^2 + int beta(rho)(1+(rho')^2) ==")
beta = sp.Function("beta")
L_full = sp.Rational(1,4)*sp.diff(f*rho, r)**2 + beta(rho)*(1 + rho.diff(r)**2)
ELf = EL(L_full, f)
ELr = EL(L_full, rho)
u2 = sp.diff(f*rho, r, 2)
print("ELf + (rho/2)(f rho)'' =", sp.simplify(ELf + rho/2*u2))
bp = sp.Derivative(beta(rho), rho)
target_r = -f/2*u2 + bp*(1 - rho.diff(r)**2) - 2*beta(rho)*rho.diff(r,2)
print("ELr - [-(f/2)(f rho)'' + beta'(1-rho'^2) - 2 beta rho''] =",
      sp.simplify((ELr - target_r).doit()))

# Also: what does the (1-rho'^2) ACTION form give (user prompt wording)?
L_minus = beta(rho)*(1 - rho.diff(r)**2)
ELr_minus = EL(L_minus, rho)
print("EL_rho[beta(1-rho'^2)] =", sp.simplify(ELr_minus.doit()),
      " (on banked rho=r: ", sp.simplify(ELr_minus.doit().subs(rho, r).doit()), ")")

print("\n== (ii-a) J=0 / banked family ==")
fb = C + a/r
subs_b = [(f, fb), (rho, r)]
print("ELf|banked =", sp.simplify(ELf.subs(subs_b).doit()))
print("ELr|banked =", sp.simplify(ELr.doit().subs(subs_b).doit()))
# (f rho)'' on banked:
print("(f rho)''|banked =", sp.simplify(sp.diff(fb*r, r, 2)))
# beta equation on banked: beta'(rho)(1-1) - 2 beta * 0 = 0 trivially.

print("\n== (ii-b) throat family: WHICH beta does it need? ==")
rho_t = sp.sqrt(J + r**2)
f_t = (al*r + ga)/rho_t
# generic beta: on-shell residual of the rho-equation
res = target_r.subs([(f, f_t), (rho, rho_t)]).doit()
res = sp.simplify(res)
print("ELr residual on throat with GENERIC beta:", res)
# substitute beta as a function evaluated at rho_t; express condition
B = sp.Function("B")  # beta
res2 = sp.simplify((-f/2*u2 + sp.Derivative(B(rho), rho)*(1-rho.diff(r)**2)
                    - 2*B(rho)*rho.diff(r,2)).subs([(f, f_t), (rho, rho_t)]).doit())
print("residual (explicit):", res2)
# check (f rho)''=0 on throat:
print("(f rho)''|throat =", sp.simplify(sp.diff(f_t*rho_t, r, 2)))
# condition: B'(rho)*J/rho^2 - 2B(rho)*J/rho^3 = 0  =>  B = b0 rho^2 (for J != 0)
x = sp.Symbol("x", positive=True)
sol = sp.dsolve(sp.Eq(sp.Function("B")(x).diff(x)*J/x**2 - 2*sp.Function("B")(x)*J/x**3, 0),
                sp.Function("B")(x))
print("dsolve of throat beta-condition:", sol)

print("\n== (ii-c) concrete check beta = b0 rho^2, full EL on throat ==")
L_b = sp.Rational(1,4)*sp.diff(f*rho, r)**2 + b0*rho**2*(1 + rho.diff(r)**2)
print("ELf|throat =", sp.simplify(EL(L_b, f).subs([(f, f_t), (rho, rho_t)]).doit()))
print("ELr|throat =", sp.simplify(EL(L_b, rho).subs([(f, f_t), (rho, rho_t)]).doit()))
print("ELf|banked =", sp.simplify(EL(L_b, f).subs(subs_b).doit()))
print("ELr|banked =", sp.simplify(EL(L_b, rho).subs(subs_b).doit()))
# first-integral value on throat: beta(1-rho'^2) = b0*rho^2*(J/rho^2) = b0*J
print("first integral value on throat:", sp.simplify((b0*rho_t**2*(1 - sp.diff(rho_t, r)**2))))

print("\n== (iii) first integral from the EL system ==")
# d/dr[beta(1-rho'^2)] vs rho' * (beta-part of EL_rho)
FI = sp.diff(beta(rho)*(1 - rho.diff(r)**2), r)
beta_EL = (bp.doit()*(1 - rho.diff(r)**2) - 2*beta(rho)*rho.diff(r,2))
print("d/dr[beta(1-rho'^2)] - rho'*EL_beta =", sp.simplify((FI - rho.diff(r)*beta_EL).doit()))
# cross-coupling: full EL_rho = -(f/2)u'' + EL_beta. On full shell ELf=0 => u''=0 (rho>0),
# hence EL_beta=0 on shell, hence first integral holds ON SOLUTIONS of the full system.
print("(cross-coupling check) full ELr - [-(f/2)u'' + EL_beta] =",
      sp.simplify((ELr - (-f/2*u2 + beta_EL)).doit()))
