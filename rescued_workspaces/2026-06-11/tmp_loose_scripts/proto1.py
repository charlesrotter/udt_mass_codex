import sympy as sp

# jet formalism prototype
r, a, C = sp.symbols("r a C", real=True)
fv, rv = sp.symbols("f_v rho_v", positive=True)
fp, fpp, fp3 = sp.symbols("f_p f_pp f_p3", real=True)
rp, rpp, rp3 = sp.symbols("r_p r_pp r_p3", real=True)

A = sp.Function("A")(fv, rv)
B = sp.Function("B")(fv, rv)
E = sp.Function("E")(fv, rv)
G = sp.Function("G")(fv, rv)

def Dr(expr):
    return (expr.diff(fv)*fp + expr.diff(fp)*fpp + expr.diff(fpp)*fp3
            + expr.diff(rv)*rp + expr.diff(rp)*rpp + expr.diff(rpp)*rp3
            + expr.diff(r))

def EL(L, v, vp, vppvar):
    return sp.expand(L.diff(v) - Dr(L.diff(vp)) + Dr(Dr(L.diff(vppvar))))

D = A + B*rp**2 + E*fp*rp + G*fp**2
ELf = EL(D, fv, fp, fpp)
ELr = EL(D, rv, rp, rpp)
print("ELf =", ELf)
print()
print("ELr =", ELr)

# banked jets: rho=r (rv is the radial coordinate), f = C + a/r -> fp=-a/rv^2 etc
banked = {rp: 1, rpp: 0, rp3: 0, fp: -a/rv**2, fpp: 2*a/rv**3, fp3: -6*a/rv**4}
ELr_b = sp.expand(ELr.subs(banked))
ELf_b = sp.expand(ELf.subs(banked))
print()
print("ELr banked:", ELr_b)
print()
print("ELf banked:", ELf_b)
print()
for k in range(3):
    print("ELr a^%d:" % k, sp.simplify(ELr_b.coeff(a, k)))
    print("ELf a^%d:" % k, sp.simplify(ELf_b.coeff(a, k)))
