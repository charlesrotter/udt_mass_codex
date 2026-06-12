"""
VERIFIER v4 (H2-A): dissolution theorem + static-fork emptiness.
All my own derivations; sympy exact unless noted.
"""
import sympy as sp
import mpmath as mp

PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"V4 {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

kap, u, F, A, y, q, n = sp.symbols('kappa u F a y q n', positive=True)
L = sp.log((1+kap)/(1-kap))
G1 = (2*kap + (kap**2-1)*L)/kap**3

# ---- A1: r^2-cancellation: the angular static density is r-FREE ----
r, st = sp.symbols('r s', positive=True)
phi = sp.Function('phi')(r, sp.Symbol('th'))
th = sp.Symbol('th')
f = sp.exp(-2*phi)
ang = -(sp.Rational(1, 2))*f*(1/r**2)*sp.diff(phi, th)**2*r**2*sp.sin(th)
# = -(1/8) f_th^2/f sin: r-free
fth = sp.diff(f, th)
check("A1 angular C1 static density = -(1/8) f_th^2/f sin(th): the r^2 "
      "cancels EXACTLY (no radial measure ambiguity in the angular "
      "sector; coordinate dy emerges)",
      sp.simplify(ang + sp.Rational(1, 8)*fth**2/f*sp.sin(th)) == 0
      and not sp.simplify(ang).has(r))

# ---- A2: exact split on the rotation class ----
# kinetic: (1/4) y^2 <f_r^2> = (1/4) y^2 (F'^2 + a'^2 <C^2>) : cross
# term <C> = 0 => S = S_mono[F] + S_ang[F,a] exactly
Fp, ap = sp.symbols("F' a'", real=True)
cross = sp.integrate((Fp + ap*u)**2, (u, -1, 1))/2
check("A2 radial kinetic sphere-avg = F'^2 + a'^2/3 (cross term exactly "
      "zero => exact S_mono + S_angular split)",
      sp.simplify(cross - (Fp**2 + ap**2/3)) == 0)

# ---- A3: sphere quadrature of the angular term -> G1 ----
J = sp.integrate((1-u**2)/(1+kap*u), (u, -1, 1))
vals = [sp.Rational(1, 7), sp.Rational(3, 10), sp.Rational(7, 10),
        sp.Rational(97, 100)]
ok = all(abs(complex((J - G1).subs(kap, kv).evalf(30))) < 1e-25
         for kv in vals)
check("A3 J(kappa) = Int (1-u^2)/(1+kappa u) du == G1 closed form "
      "(f_u = a const on the class => P = (a^2/8F) G1)", ok)

# ---- A4: H = -2 P_F == L/(2 kappa) - 1 ----
P = A**2/(8*F)*G1.subs(kap, A/F)
H = sp.simplify(-2*sp.diff(P, F))
Hc = (L/(2*kap) - 1).subs(kap, A/F)
ok = all(abs(complex((H - Hc).subs([(A, kv), (F, 1)]).evalf(30))) < 1e-25
         for kv in vals)
check("A4 H := -2 P_F == L/(2k) - 1 exact (the angular sector IS the "
      "monopole source: (y^2 F')' = -H)", ok)

# ---- A5: criticality data, no measure choice ----
s = q*(1-q)/2
lhs = sp.simplify(sp.diff(y**2*sp.diff(y**(-q), y), y))
check("A5 (y^2 (y^-q)')' = -q(1-q) y^-q == -2s y^-q, s = q(1-q)/2 "
      "(sigma = -q(1-q)y^-q; criticality data measure-free)",
      sp.simplify(lhs + q*(1-q)*y**(-q)) == 0)

# ---- A6: static fork EMPTY for the posited family, ANY measure ----
# posited V = C(y) m(y) F^n with ARBITRARY smooth measure factor m(y);
# criticality demand 2pi (y^2 F')' = dV/dF on F = y^-q fixes C(y) m(y)
# as a single product => mu(n) = V''(F)/(2 pi) is m-INDEPENDENT.
m = sp.Function('m', positive=True)(y)
Cm = sp.solve(sp.Eq(sp.Symbol('Cm')*n*(y**(-q))**(n-1),
                    -4*sp.pi*s*y**(-q)), sp.Symbol('Cm'))[0]
mu = sp.simplify(Cm*n*(n-1)*(y**(-q))**(n-2)/(2*sp.pi))
check("A6 mu(n) = (1-n) q(1-q) for the posited family under ANY y-"
      "measure (criticality refixes the prefactor: static fork EMPTY)",
      sp.simplify(mu - (1-n)*q*(1-q)) == 0, f"[mu = {mu}]")

# ---- A7: rank-1 static Hessian (exact screening) ----
hess = sp.diff(P, F, 2)*sp.diff(P, A, 2) - sp.diff(P, F, A)**2
ok = all(abs(complex(hess.subs([(A, kv), (F, 1)]).evalf(30))) < 1e-25
         for kv in vals)
check("A7 P_FF P_aa - P_Fa^2 == 0 (rank-1 angular Hessian: exact "
      "pointwise screening, degree-1 homogeneity)", ok)

# ---- A8: anchor root ----
mp.mp.dps = 30
sv = mp.mpf(1)/9
kroot = mp.findroot(lambda k2: mp.log((1+k2)/(1-k2)) - 2*k2*(1+2*sv), 0.7)
check("A8 interface root kappa(1) = 0.68309514 (s = 1/9)",
      abs(kroot - mp.mpf('0.68309514')) < 1e-7, f"[{mp.nstr(kroot, 10)}]")

n_ = sum(1 for _, ok in PASS if ok)
print(f"\nV4 TOTAL: {n_}/{len(PASS)} PASS")
