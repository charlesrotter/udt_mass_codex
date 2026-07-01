#!/usr/bin/env python3
"""
fermion_forcing3.py  — post-process the pickled G_tr, G_ttheta.
Runs: forcing nonzero check; STATIC LIMIT (A=B=0 and all derivs); STATIONARY ARM
(A_t=B_t=0); LINEAR-IN-ARM piece (drop O(A^2,B^2,AB)); derivative content.
"""
import sympy as sp, pickle
d = pickle.load(open('/home/udt-admin/udt_mass_codex/fermion_forcing2_dump.pkl','rb'))
Gtr, Gtth = d['Gtr'], d['Gtth']
t, r, th = sp.symbols('t r theta', real=True)
phi = sp.Function('phi')(r, th)
A = sp.Function('A')(t, r, th); B = sp.Function('B')(t, r, th)

def kill(expr, funcs):
    """Replace funcs and ALL their derivatives by 0."""
    reps = {}
    for f in funcs:
        for a in expr.atoms(sp.Derivative):
            if a.expr in funcs:
                reps[a] = sp.S(0)
        reps[f] = sp.S(0)
    return sp.simplify(expr.subs(reps))

def kill_tderiv(expr, funcs):
    """Replace only t-derivatives of funcs by 0 (stationary arm)."""
    reps = {}
    for a in expr.atoms(sp.Derivative):
        if a.expr in funcs:
            vars_ = [v for (v,_) in a.variable_count]
            if t in vars_:
                reps[a] = sp.S(0)
    return sp.simplify(expr.subs(reps))

print("=== FORCING (numerator nonzero?) ===")
print("G_tr   nonzero:", sp.simplify(Gtr) != 0)
print("G_ttheta nonzero:", sp.simplify(Gtth) != 0)

print("\n=== STATIC LIMIT A=B=0 (all derivs) ===")
print("G_tr   ->", kill(Gtr,(A,B)))
print("G_ttheta ->", kill(Gtth,(A,B)))

print("\n=== STATIONARY ARM (A_t=B_t=0, arm nonzero) ===")
gtr_stat = kill_tderiv(Gtr,(A,B)); gtth_stat = kill_tderiv(Gtth,(A,B))
print("G_tr   ->", "ZERO" if gtr_stat==0 else "NONZERO (stationary arm already sources)")
print("G_ttheta ->", "ZERO" if gtth_stat==0 else "NONZERO (stationary arm already sources)")

print("\n=== TIME-DERIVATIVE CONTENT (genuinely nonstationary terms) ===")
for nm,e in [("G_tr",Gtr),("G_ttheta",Gtth)]:
    tder = set()
    for a in e.atoms(sp.Derivative):
        if a.expr in (A,B):
            vars_=[v for (v,_) in a.variable_count]
            if t in vars_: tder.add(a)
    print(f"{nm}: time-deriv terms present:", sorted([str(x) for x in tder]))

# LINEARIZED-IN-ARM (leading order: keep only terms linear in A,B; drop A^2,B^2,AB...)
# This is a HYPOTHESIS-DEVELOPMENT linearization (principle 2: short-lived, to read
# the leading source structure), NOT a stated result. Tagged loudly.
print("\n=== LEADING (LINEAR-IN-ARM) PIECE [hypothesis-development linearization] ===")
eps = sp.symbols('eps', positive=True)
def linearize(expr):
    e = expr.subs({A: eps*A, B: eps*B})
    e = sp.series(e, eps, 0, 2).removeO()
    e = e.coeff(eps, 1)
    return sp.simplify(e)
Ltr = linearize(Gtr); Ltth = linearize(Gtth)
print("G_tr  (linear) =", Ltr)
print()
print("G_ttheta (linear) =", Ltth)

# In the linear piece, which time-derivatives of the arm survive?
for nm,e in [("G_tr linear",Ltr),("G_ttheta linear",Ltth)]:
    tder = sorted([str(a) for a in e.atoms(sp.Derivative)
                   if a.expr in (A,B) and t in [v for (v,_) in a.variable_count]])
    print(f"{nm}: time-deriv terms:", tder)

pickle.dump({'Ltr':Ltr,'Ltth':Ltth}, open('/home/udt-admin/udt_mass_codex/fermion_forcing3_dump.pkl','wb'))
print("\nDONE3")
