"""
S7: probe gamma1 (l=2, m=+-1, lambda=6), responders {a1 (l=1,m=1), h1 (l=3,m=1)}
pointwise static Schur, far-collar constant. Hypothesis: this is N1's
"lambda=6" rational (n_full = 11/14, mu_full = 1/21).
Also compute the full table of far-collar dressed constants for all l<=2
channels with consistent Delta-l=1 responder classes, for the record.
"""
import sympy as sp

c, ph, kap, F = sp.symbols('c phi kappa F', real=True)
e = sp.symbols('e0:12', real=True)
sdef = sp.Rational(1,9)

Y = {
 'u'  : sp.Integer(1),
 'a0' : sp.sqrt(3/(4*sp.pi))*c,
 'a1' : sp.sqrt(3/(4*sp.pi))*sp.sqrt(1-c**2)*sp.cos(ph),
 'g0' : sp.sqrt(5/(16*sp.pi))*(3*c**2-1),
 'g1' : sp.sqrt(15/(4*sp.pi))*c*sp.sqrt(1-c**2)*sp.cos(ph),
 'g2' : sp.sqrt(15/(16*sp.pi))*(1-c**2)*sp.cos(2*ph),
 'h0' : sp.sqrt(7/(16*sp.pi))*(5*c**3-3*c),
 'h1' : sp.sqrt(21/(32*sp.pi))*sp.sqrt(1-c**2)*(5*c**2-1)*sp.cos(ph),
 'h2' : sp.sqrt(105/(16*sp.pi))*c*(1-c**2)*sp.cos(2*ph),
}
names = list(Y.keys())
for i, ni in enumerate(names):
    for j, nj in enumerate(names):
        I = sp.integrate(sp.integrate(Y[ni]*Y[nj], (ph, 0, 2*sp.pi)), (c, -1, 1))
        expect = 4*sp.pi if (ni == nj == 'u') else (1 if ni == nj else 0)
        assert sp.simplify(I - expect) == 0, (ni, nj, sp.simplify(I))
print("orthonormality l<=3: PASS")

f = F*(1+kap*c) + sum(e[i]*Y[names[i]] for i in range(len(names)))
integrand = ((1-c**2)*sp.diff(f, c)**2 + sp.diff(f, ph)**2/(1-c**2))/f

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
def getV(a,b): return V.get((a,b), V.get((b,a), sp.Integer(0)))

print("m=1 sector entries:")
for pair in [('a1','a1'),('a1','g1'),('g1','g1'),('g1','h1'),('h1','h1'),('a1','h1')]:
    print("  V_%s%s = %s" % (pair[0], pair[1], getV(*pair)))

def classify(expr):
    Fq = sp.Symbol('yq', positive=True)
    expr = sp.expand(sp.simplify(expr)).subs(F, 1/Fq)
    expr = sp.expand(expr).subs(kap**2, 6*sdef/Fq)
    expr = sp.expand(sp.simplify(expr))
    return sp.simplify(expr.coeff(Fq,1)), sp.simplify(expr.coeff(Fq,0))

print()
print("== probe g1 (lambda=6, m=+-1), responders {a1, h1}, pointwise Schur ==")
B = sp.Matrix([[getV('a1','a1'), getV('a1','h1')],[getV('a1','h1'), getV('h1','h1')]])
cv = sp.Matrix([getV('a1','g1'), getV('g1','h1')])
Vd = getV('g1','g1') - (cv.T*B.inv()*cv)[0,0]
lam, mu = classify(sp.series(sp.simplify(sp.expand(2*Vd)), kap, 0, 3).removeO())
print("  lambda-part =", lam, "  mu_full =", mu, "  n_full =", sp.simplify(1-mu/(2*sdef)),
      "   [hypothesis target: mu=1/21, n=11/14]")

print()
print("== full far-collar dressed table (consistent Delta-l=1 responder classes) ==")
# a1 probe, responders {g1} (+h1 coupling is O(k^2): include full inverse anyway)
B = sp.Matrix([[getV('g1','g1'), getV('g1','h1')],[getV('g1','h1'), getV('h1','h1')]])
cv = sp.Matrix([getV('a1','g1'), getV('a1','h1')])
Vd = getV('a1','a1') - (cv.T*B.inv()*cv)[0,0]
lam, mu = classify(sp.series(sp.simplify(sp.expand(2*Vd)), kap, 0, 3).removeO())
print("  a1 (lambda=2,m=1):  mu_full =", mu, " n_full =", sp.simplify(1-mu/(2*sdef)))
# g2 probe, responder {h2}
Vd = getV('g2','g2') - getV('g2','h2')**2/getV('h2','h2')
lam, mu = classify(sp.series(sp.simplify(sp.expand(2*Vd)), kap, 0, 3).removeO())
print("  g2 (lambda=6,m=2):  mu_full =", mu, " n_full =", sp.simplify(1-mu/(2*sdef)))
# g0 probe, responders {u, a0, h0} (rescale u-channel)
chan = ['u','a0','h0']
B = sp.zeros(3,3); cv = sp.zeros(3,1)
for i,ci in enumerate(chan):
    for j,cj in enumerate(chan):
        v = getV(ci,cj)
        if ci=='u': v = v/sp.sqrt(4*sp.pi)
        if cj=='u': v = v/sp.sqrt(4*sp.pi)
        B[i,j] = v
    vv = getV(ci,'g0')
    cv[i] = vv/sp.sqrt(4*sp.pi) if ci=='u' else vv
Vd = getV('g0','g0') - (cv.T*B.inv()*cv)[0,0]
lam, mu = classify(sp.series(sp.simplify(sp.expand(2*Vd)), kap, 0, 3).removeO())
print("  g0 (lambda=6,m=0):  mu_full =", mu, " n_full =", sp.simplify(1-mu/(2*sdef)))
# a0 probe (lambda=2, m=0), responders {u, g0} -- the amplitude channel itself
chan = ['u','g0']
B = sp.zeros(2,2); cv = sp.zeros(2,1)
for i,ci in enumerate(chan):
    for j,cj in enumerate(chan):
        v = getV(ci,cj)
        if ci=='u': v = v/sp.sqrt(4*sp.pi)
        if cj=='u': v = v/sp.sqrt(4*sp.pi)
        B[i,j] = v
    vv = getV(ci,'a0')
    cv[i] = vv/sp.sqrt(4*sp.pi) if ci=='u' else vv
Vd = getV('a0','a0') - (cv.T*B.inv()*cv)[0,0]
lam, mu = classify(sp.series(sp.simplify(sp.expand(2*Vd)), kap, 0, 3).removeO())
print("  a0 (lambda=2,m=0):  mu_full =", mu, " n_full =", sp.simplify(1-mu/(2*sdef)),
      "  [m=0: exact screening makes this probe-vs-responder split delicate]")
