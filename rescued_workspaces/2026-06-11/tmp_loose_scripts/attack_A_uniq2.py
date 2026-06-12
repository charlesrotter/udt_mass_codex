"""Attack A(iv) continued: (a) confirm the script's 'general solution'
exhausts the six conditions (my own integration done by hand; here verify
the W(rho'-1)^2 direction is covered by the Phi-sector mod total derivative);
(b) show uniqueness is CLASS-RELATIVE: a quartic term also cancels the
obstruction, so the 'at most quadratic' caveat is load-bearing."""
import sympy as sp

r = sp.Symbol("r", positive=True)
a, C = sp.symbols("a C", real=True)
f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)

def EL(Lag, v):
    return sp.simplify((Lag.diff(v) - sp.diff(Lag.diff(v.diff(r)), r)).doit())

fb = C + a/r
def on_banked(e):
    return sp.simplify(e.subs([(f, fb), (rho, r)]).doit())

print("(a) W(f,rho)(rho'-1)^2 = Phi-sector + total derivative, Phi = int W drho:")
W = sp.Function("W")
# concrete W to avoid abstract-integral issues: W = f**2*rho**3
Wc = f**2*rho**3
Phi = f**2*rho**4/4          # int Wc drho
term = Wc*(rho.diff(r) - 1)**2
phisector = sp.diff(Phi, rho)*(1 + rho.diff(r)**2)/sp.S(1) + 2*sp.diff(Phi, f)*f.diff(r)
# careful: Phi here is an expression in f(r),rho(r); partials:
Phi_r = f**2*rho**3          # dPhi/drho
Phi_f = f*rho**4/2           # dPhi/df
phisector = Phi_r*(1 + rho.diff(r)**2) + 2*Phi_f*f.diff(r)
totald = sp.diff(-2*Phi, r)  # -2 dPhi/dr = -2(Phi_f f' + Phi_r rho')
print("  term - [phisector + totald] =", sp.simplify(term - (phisector + totald)))
print("  EL_f[term]|banked =", on_banked(EL(term, f)))
print("  EL_rho[term]|banked =", on_banked(EL(term, rho)))

print("\n(b) quartic alternative: D_alt = (1/4)f^2 rho'^4 + (1/2) rho f f' rho'^3")
L_C1 = sp.Rational(1,4)*rho**2*f.diff(r)**2
D_alt = sp.Rational(1,4)*f**2*rho.diff(r)**4 + sp.Rational(1,2)*rho*f*f.diff(r)*rho.diff(r)**3
L_alt = L_C1 + D_alt
print("  EL_f[L_C1+D_alt]|banked =", on_banked(EL(L_alt, f)))
print("  EL_rho[L_C1+D_alt]|banked =", on_banked(EL(L_alt, rho)))
Dstar = sp.Rational(1,4)*f**2*rho.diff(r)**2 + sp.Rational(1,2)*rho*f*f.diff(r)*rho.diff(r)
print("  D_alt == D* on banked jets but D_alt != D* as densities:",
      sp.simplify(on_banked(D_alt - Dstar)) == 0,
      sp.simplify(D_alt - Dstar) != 0)
# and the resulting dynamics differ off the banked family:
print("  EL_rho[L_C1+D_alt] - EL_rho[L_C1+D*] (general) simplifies to 0? ",
      sp.simplify(EL(L_alt, rho) - EL(L_C1 + Dstar, rho)) == 0)
