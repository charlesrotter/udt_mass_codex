"""
S5: Far-collar dressed rational limits (spot-check of N1's claims):
  lambda=2, m=+-1 channel:  n_full = 11/10  <=> mu_full = 2s(1-11/10) = -s/5 = -1/45
  lambda=6, m=+-2 channel:  n_full = 11/14  <=> mu_full = 2s(3/14)   = s*3/7 = 1/21

Method (from scratch): exact second variation of P = (1/4)int dOmega |grad f|^2/f
around f0 = F(1+kappa cos th), channels = real orthonormal harmonics l<=2.
Series in kappa to O(kappa^2). Far-collar demand: kappa^2 -> 6 s y^-q (leading).
Per-channel SL normalization: kinetic (1/4) y^2 eps'^2 => (y^2 eps')' = 2 V_dressed eps
 = (lambda y^q + mu_full) eps. Pointwise static Schur within the m-sector
(kinetic lifting is subleading far-collar: O(y^2 kappa'^2) ~ kappa^2 -> 0 while
kappa^2 y^q -> 6s).
Also: calibration of the O(kappa) couplings against the recorded
V_a1g1 = -sqrt(5) kappa/(2F), V_a0g0 = -sqrt(15) kappa/(3F)  [recorded normalization].
"""
import sympy as sp

c, ph, kap, F, y, q, s = sp.symbols('c phi kappa F y q s', real=True)
e = sp.symbols('e0:9', real=True)   # channel amplitudes

# real orthonormal harmonics l<=2 (cos-type m>0; sin-type omitted: same by symmetry)
Y = {
 'u'  : 1,                                            # delta F enters directly
 'a0' : sp.sqrt(3/(4*sp.pi))*c,
 'a1' : sp.sqrt(3/(4*sp.pi))*sp.sqrt(1-c**2)*sp.cos(ph),
 'g0' : sp.sqrt(5/(16*sp.pi))*(3*c**2-1),
 'g1' : sp.sqrt(15/(4*sp.pi))*c*sp.sqrt(1-c**2)*sp.cos(ph),
 'g2' : sp.sqrt(15/(16*sp.pi))*(1-c**2)*sp.cos(2*ph),
}
names = list(Y.keys())
# orthonormality sanity (u channel: integral of 1*1 dOmega = 4pi -> handled separately)
for i, ni in enumerate(names):
    for j, nj in enumerate(names):
        I = sp.integrate(sp.integrate(Y[ni]*Y[nj], (ph, 0, 2*sp.pi)), (c, -1, 1))
        expect = 4*sp.pi if (ni == nj == 'u') else (1 if ni == nj else 0)
        assert sp.simplify(I - expect) == 0, (ni, nj, I)
print("harmonic orthonormality: PASS")

f0 = F*(1+kap*c)
h = sum(e[i]*Y[names[i]] for i in range(len(names)))
f = f0 + h

# |grad_Omega f|^2 = (1-c^2) f_c^2 + f_ph^2/(1-c^2)
grad2 = (1-c**2)*sp.diff(f, c)**2 + sp.diff(f, ph)**2/(1-c**2)
integrand = grad2/f

# second-order jet in the epsilons
jet2 = sp.Rational(0)
poly = sp.Poly(sp.expand(integrand.series(e[0], 0, 3).removeO()), *e) if False else None
# direct: take second derivatives
V = {}
print("computing Hessian entries (series to O(kappa^2)) ...")
for i, ni in enumerate(names):
    for j, nj in enumerate(names):
        if j < i: continue
        d2 = sp.diff(integrand, e[i], e[j])
        d2 = d2.subs([(ee, 0) for ee in e])
        d2 = sp.series(d2, kap, 0, 3).removeO()
        d2 = sp.expand(d2)
        I = sp.integrate(sp.integrate(d2, (ph, 0, 2*sp.pi)), (c, -1, 1))
        Vij = sp.simplify(sp.Rational(1,4)*I)   # P = (1/4) int ; V_ij = d^2 P
        if Vij != 0:
            V[(ni,nj)] = Vij
for k_, v_ in sorted(V.items()):
    print("  V_%s%s = %s" % (k_[0], k_[1], sp.simplify(v_)))

print()
print("CALIBRATION vs recorded couplings (recorded uses 4x potential):")
print("  4*V_a1g1 =", sp.simplify(4*V[('a1','g1')]), "   [recorded: -sqrt(5) kappa/(2F)]")
print("  4*V_a0g0 =", sp.simplify(4*V[('a0','g0')]), "   [recorded: -sqrt(15) kappa/(3F)]")

# rank-1 m=0 check at O(kappa^2): null vector (deltaF, a0) ~ (F0, a0bg), a0bg = sqrt(4pi/3) kap F
print()
a0bg = sp.sqrt(4*sp.pi/3)*kap*F
r1 = sp.simplify(sp.series(V[('u','u')]*F + V[('u','a0')]*a0bg, kap, 0, 3).removeO())
print("m=0 Euler check O(k^2):  V_uu*F + V_ua0*a0bg =", r1, " [0 => rank-1/null verified at this order]")

# ---------------- far-collar dressed constants ----------------
# demand: kappa^2 = 6 s y^-q with F = y^-q  =>  kappa^2/F = 6 s  (leading);  kappa^2 -> 0
# SL form: (y^2 eps')' = 2 V_dressed eps = (lambda y^q + mu_full) eps,  y^q = 1/F
sdef = sp.Rational(1,9)
def far_collar(expr):
    """substitute kappa^2 = 6 s / F ... wait: kappa^2 = 6 s y^-q and 1/F = y^q
       => kappa^2 = 6 s * F. Then expand, keep terms; finally F->0? No:
       kappa^2/F -> 6 s * 1 = ... CAREFUL: kappa^2 = 6 s y^{-q}, 1/F = y^{q}
       => kappa^2 * (1/F) = 6 s y^{-q} y^{q} = 6 s ; and kappa^2 alone -> 0.
       So write expr in powers of kappa and 1/F; substitute kappa^2 = 6*s*X/Fi
       with 1/F = Fi... simplest: kappa^2 -> 6*s*Fq, 1/F -> Fq, then collect in Fq:
       coefficient of Fq^1 with kappa absorbed = lambda-part + mu... no:
       lambda-part ~ Fq (pure), mu-part ~ kappa^2*Fq = 6 s Fq^2?? WRONG.
    """
    raise NotImplementedError

# Correct bookkeeping: y^q = 1/F. A term  A * kappa^2 / F = A * 6 s y^{-q} y^{q} = 6 A s : CONSTANT (mu-type)
# A term  B/F = B y^q : lambda-type.  A term  C*kappa^2 (no 1/F) -> 0 far collar.
Fq = sp.Symbol('yq', positive=True)   # stands for y^q = 1/F
def classify(expr):
    expr = sp.expand(sp.simplify(expr))
    expr = expr.subs(F, 1/Fq)
    expr = sp.expand(expr)
    # substitute kappa^2 = 6 s Fq^{-1}... kappa^2 = 6 s y^-q = 6 s / Fq
    expr = expr.subs(kap**2, 6*sdef/Fq)
    expr = sp.expand(sp.simplify(expr))
    lam_part = expr.coeff(Fq, 1)
    mu_part = expr.coeff(Fq, 0)
    other = sp.simplify(expr - lam_part*Fq - mu_part)
    return sp.simplify(lam_part), sp.simplify(mu_part), other

print()
print("== m = +-1 sector: probe a1 (lambda=2), responder g1 (lambda=6), pointwise Schur ==")
Vd_m1 = V[('a1','a1')] - V[('a1','g1')]**2/V[('g1','g1')]
op_m1 = sp.series(sp.simplify(2*Vd_m1), kap, 0, 3).removeO()
lam1, mu1, oth1 = classify(op_m1)
print("  2*V_dressed(a1) far-collar: lambda-part =", lam1, "  mu_full =", mu1, " (target -1/45 =", sp.Rational(-1,45), ")")
n1 = sp.simplify(1 - mu1/(2*sdef))
print("  n_full =", n1, " (target 11/10)")

print()
print("== m = +-2 sector: probe g2 (lambda=6), no in-class responder: self-energy only ==")
op_m2 = sp.series(sp.simplify(2*V[('g2','g2')]), kap, 0, 3).removeO()
lam2, mu2, oth2 = classify(op_m2)
print("  2*V_g2g2 far-collar: lambda-part =", lam2, "  mu_full =", mu2, " (target 1/21 =", sp.Rational(1,21), ")")
n2 = sp.simplify(1 - mu2/(2*sdef))
print("  n_full =", n2, " (target 11/14)")

print()
print("== bonus: m=0 trio {u, a0, g0}: probe g0 (lambda=6), eliminate {u,a0} pointwise ==")
M = sp.Matrix([[4*sp.pi*0 + V[('u','u')], V[('u','a0')], V[('u','g0')]],
               [V[('u','a0')], V[('a0','a0')], V[('a0','g0')]],
               [V[('u','g0')], V[('a0','g0')], V[('g0','g0')]]])
# NOTE: u-channel kinetic is pi y^2 u'^2 = 4pi*(1/4) y^2 u'^2: to use uniform
# (1/4)y^2 kinetic per channel, rescale u-channel: e_u = sqrt(4pi) u  => V entries
# transform: V_uu -> V_uu/(4pi), V_u,x -> V_u,x/sqrt(4pi).
Mr = sp.Matrix(3,3, lambda i,j: M[i,j])
Mr[0,0] = M[0,0]/(4*sp.pi); Mr[0,1] = M[0,1]/sp.sqrt(4*sp.pi); Mr[1,0] = Mr[0,1]
Mr[0,2] = M[0,2]/sp.sqrt(4*sp.pi); Mr[2,0] = Mr[0,2]
B = Mr[0:2,0:2]; cvec = sp.Matrix([Mr[0,2], Mr[1,2]])
Vd_g0 = Mr[2,2] - (cvec.T*B.inv()*cvec)[0,0]
op_g0 = sp.series(sp.simplify(sp.expand(2*Vd_g0)), kap, 0, 3).removeO()
lam0, mu0, oth0 = classify(op_g0)
print("  2*V_dressed(g0) far-collar: lambda-part =", lam0, "  mu_full =", mu0, " n_full =", sp.simplify(1-mu0/(2*sdef)))
