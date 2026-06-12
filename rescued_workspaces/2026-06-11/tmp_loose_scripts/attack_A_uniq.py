"""Attack A(iv): is D* forced? Independent re-derivation of the constraint
system and a hunt for admissible terms the a-power matching might miss."""
import sympy as sp

r = sp.Symbol("r", positive=True)
a, C = sp.symbols("a C", real=True)

# Independent approach: avoid jets entirely. Impose that
# rho = r, f = C + a/r solves both function-space EL equations of
# L = (1/4) rho^2 f'^2 + D, identically in (r, C, a),
# where D = A(f,rho) + B(f,rho) rho'^2 + E(f,rho) f' rho' + G(f,rho) f'^2
#        + P(f,rho) rho' + Q(f,rho) f'.
f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)
A_ = sp.Function("A")
B_ = sp.Function("B")
E_ = sp.Function("E")
G_ = sp.Function("G")
P_ = sp.Function("P")
Q_ = sp.Function("Q")

D = (A_(f, rho) + B_(f, rho)*rho.diff(r)**2 + E_(f, rho)*f.diff(r)*rho.diff(r)
     + G_(f, rho)*f.diff(r)**2 + P_(f, rho)*rho.diff(r) + Q_(f, rho)*f.diff(r))
L = sp.Rational(1, 4)*rho**2*f.diff(r)**2 + D

def EL(Lag, v):
    return (Lag.diff(v) - sp.diff(Lag.diff(v.diff(r)), r)).doit()

ELf = EL(L, f)
ELr = EL(L, rho)

fb = C + a/r
ELf_b = ELf.subs([(f, fb), (rho, r)]).doit()
ELr_b = ELr.subs([(f, fb), (rho, r)]).doit()

# On the banked family, the function arguments are (fb, r). Since C is free,
# treat the f-slot value as an independent symbol F at fixed (r, a):
F, R = sp.symbols("F R", real=True)

def normalize(expr):
    # replace f-value by F, r by R inside the unknown functions and jets
    e = expr
    e = e.replace(lambda x: x == fb, lambda x: F)
    return e

# safer: substitute C = F - a/r so the f-value becomes literally F
ELf_b = sp.expand(ELf_b.subs(C, F - a/r))
ELr_b = sp.expand(ELr_b.subs(C, F - a/r))
ELf_b = sp.simplify(ELf_b)
ELr_b = sp.simplify(ELr_b)

polyf = sp.Poly(sp.expand(ELf_b), a)
polyr = sp.Poly(sp.expand(ELr_b), a)
print("EL_f coefficients in a:")
condsf = []
for k in range(polyf.degree() + 1):
    c = sp.simplify(polyf.coeff_monomial(a**k))
    print(f"  a^{k}: {c}")
    condsf.append(c)
print("EL_rho coefficients in a:")
condsr = []
for k in range(polyr.degree() + 1):
    c = sp.simplify(polyr.coeff_monomial(a**k))
    print(f"  a^{k}: {c}")
    condsr.append(c)
