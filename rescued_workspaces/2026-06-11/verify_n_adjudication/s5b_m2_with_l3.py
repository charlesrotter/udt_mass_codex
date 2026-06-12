"""
S5b: m=+-2 probe (g2, lambda=6) with the CONSISTENT responder class:
include the Delta-l = 1 partner h2 = Y_{3,2} (lambda=12), which couples at
O(kappa) -- same status as g1 for the a1 probe. Also redo the m=0 bonus
(g0 probe) with h0 = Y_{3,0} included.
Far-collar: kappa^2/F -> 6s, kappa^2 -> 0.
"""
import sympy as sp

c, ph, kap, F = sp.symbols('c phi kappa F', real=True)
e = sp.symbols('e0:9', real=True)
sdef = sp.Rational(1,9)

Y = {
 'u'  : 1,
 'a0' : sp.sqrt(3/(4*sp.pi))*c,
 'g0' : sp.sqrt(5/(16*sp.pi))*(3*c**2-1),
 'h0' : sp.sqrt(7/(16*sp.pi))*(5*c**3-3*c),
 'g2' : sp.sqrt(15/(16*sp.pi))*(1-c**2)*sp.cos(2*ph),
 'h2' : sp.sqrt(105/(16*sp.pi))*c*(1-c**2)*sp.cos(2*ph),
}
names = list(Y.keys())
for i, ni in enumerate(names):
    for j, nj in enumerate(names):
        I = sp.integrate(sp.integrate(Y[ni]*Y[nj], (ph, 0, 2*sp.pi)), (c, -1, 1))
        expect = 4*sp.pi if (ni == nj == 'u') else (1 if ni == nj else 0)
        assert sp.simplify(I - expect) == 0, (ni, nj, sp.simplify(I))
print("orthonormality (incl l=3): PASS")

f0 = F*(1+kap*c)
f = f0 + sum(e[i]*Y[names[i]] for i in range(len(names)))
grad2 = (1-c**2)*sp.diff(f, c)**2 + sp.diff(f, ph)**2/(1-c**2)
integrand = grad2/f

V = {}
for i, ni in enumerate(names):
    for j, nj in enumerate(names):
        if j < i: continue
        d2 = sp.diff(integrand, e[i], e[j]).subs([(ee,0) for ee in e])
        d2 = sp.expand(sp.series(d2, kap, 0, 3).removeO())
        I = sp.integrate(sp.integrate(d2, (ph, 0, 2*sp.pi)), (c, -1, 1))
        Vij = sp.simplify(sp.Rational(1,4)*I)
        if Vij != 0:
            V[(ni,nj)] = Vij
            print("  V_%s%s = %s" % (ni, nj, Vij))

def classify(expr):
    Fq = sp.Symbol('yq', positive=True)
    expr = sp.expand(sp.simplify(expr)).subs(F, 1/Fq)
    expr = sp.expand(expr).subs(kap**2, 6*sdef/Fq)
    expr = sp.expand(sp.simplify(expr))
    return sp.simplify(expr.coeff(Fq,1)), sp.simplify(expr.coeff(Fq,0))

print()
print("== m=+-2: probe g2, responder h2 (pointwise static Schur) ==")
Vd = V[('g2','g2')] - V[('g2','h2')]**2/V[('h2','h2')]
op = sp.series(sp.simplify(2*Vd), kap, 0, 3).removeO()
lam, mu = classify(op)
n = sp.simplify(1 - mu/(2*sdef))
print("  lambda-part =", lam, "  mu_full =", mu, "  n_full =", n, "  [N1 target: 11/14, mu=1/21]")

print()
print("== m=0 bonus: probe g0, responders {u, a0, h0} ==")
Mr = sp.zeros(4,4)
chan = ['u','a0','h0','g0']
def getV(a,b):
    return V.get((a,b), V.get((b,a), 0))
for i,ci in enumerate(chan):
    for j,cj in enumerate(chan):
        v = getV(ci,cj)
        if ci=='u': v = v/sp.sqrt(4*sp.pi)
        if cj=='u': v = v/sp.sqrt(4*sp.pi)
        Mr[i,j] = v
B = Mr[0:3,0:3]; cv = sp.Matrix([Mr[0,3],Mr[1,3],Mr[2,3]])
Vd0 = Mr[3,3] - (cv.T*B.inv()*cv)[0,0]
op0 = sp.series(sp.simplify(sp.expand(Vd0*2)), kap, 0, 3).removeO()
lam0, mu0 = classify(op0)
print("  lambda-part =", lam0, "  mu_full =", mu0, "  n_full =", sp.simplify(1-mu0/(2*sdef)))
