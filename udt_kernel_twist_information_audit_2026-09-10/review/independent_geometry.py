#!/usr/bin/env python3
"""Independent direct-coordinate KTI1 review; no author/source implementation imports."""
import json
import platform
import sympy as s

t, x, y, z, b = s.symbols('t x y z b', real=True)
q = (t, x, y, z)
eta = s.diag(-1, 1, 1, 1)
U = s.Matrix([1, 0, 0, 0])
A = s.Matrix([-b*y/2, b*x/2, 0])
theta = s.Matrix([1, *A])
# Construct the metric by expanding the declared one-form square, not a pullback utility.
g = s.diag(0, 1, 1, 1) - theta*theta.T
ginv = s.simplify(g.inv())
E = s.eye(4)
E[0, :] = theta.T
positive = []
negative = []

def equal(name, lhs, rhs):
    if isinstance(lhs, s.MatrixBase) or isinstance(rhs, s.MatrixBase):
        lhs, rhs = s.Matrix(lhs), s.Matrix(rhs)
        if lhs.shape != rhs.shape:
            raise AssertionError(name + ': incompatible shapes')
        residuals = list(lhs-rhs)
    else:
        residuals = [lhs-rhs]
    residuals = [s.simplify(v) for v in residuals]
    if any(v != 0 for v in residuals):
        raise AssertionError(name + ': ' + str(residuals))
    return True

def check(name, lhs, rhs):
    equal(name, lhs, rhs)
    positive.append(name)

def reject(name, callback):
    try:
        callback()
    except AssertionError as exc:
        negative.append({'name': name, 'actual_rejection': str(exc)})
    else:
        raise AssertionError('MUTANT SURVIVED: '+name)

def regular(h):
    if h.shape != (2, 2) or h[0, 0].is_negative is not True or s.simplify(h.det()).is_negative is not True:
        raise AssertionError('outside declared regular pair stratum')

check('metric determinant', g.det(), -1)
check('coframe direct correspondence', E.T*eta*E, g)
check('coframe invertibility', E.det(), 1)
check('inverse spatial block', ginv[1:4, 1:4], s.eye(3))
check('unit observer', (U.T*g*U)[0], -1)
check('time Killing direct coordinate Lie derivative', g.diff(t), s.zeros(4))

Jcoord, Jorth, Hcoord, Horth, Vorth = [], [], [], [], []
for i in range(3):
    ei = s.eye(4)[:, i+1]
    jc = U.row_join(ei)
    jo = U.row_join(ei-A[i]*U)
    hc, ho = s.simplify(jc.T*g*jc), s.simplify(jo.T*g*jo)
    Jcoord.append(jc); Jorth.append(jo); Hcoord.append(hc); Horth.append(ho)
    Vorth.append(s.simplify(E*jo))
    check(f'coordinate metric {i}', hc, s.Matrix([[-1, -A[i]], [-A[i], 1-A[i]**2]]))
    regular(hc); positive.append(f'coordinate regularity {i}')
    check(f'coordinate m squared {i}', -hc.det(), 1)
    check(f'coordinate completed Phi {i}', -s.log(-hc[0, 0])/2, 0)
    check(f'coordinate extracted shift {i}', hc[0, 1]/hc[0, 0], A[i])
    check(f'central complete metric for all t {i}', hc.subs({x:0, y:0, z:0}), s.diag(-1, 1))
    check(f'all-point time derivative identically zero {i}', hc.diff(t), s.zeros(2))
    check(f'along-own-strip derivative zero {i}', hc.diff(q[i+1]), s.zeros(2))
    check(f'orthogonal metric {i}', ho, s.diag(-1, 1))
    regular(ho); positive.append(f'orthogonal regularity {i}')
    check(f'adapted V {i}', E*jo, jc)
    for a in range(4):
        check(f'ordinary adapted V coordinate derivative {i},{a}', (E*jo).diff(q[a]), s.zeros(4, 2))
    check(f'orthogonal clock-space commutator {i}', jo[:, 1].diff(t), s.zeros(4, 1))

beta = s.Matrix([hc[0, 1]/hc[0, 0] for hc in Hcoord])
curl = s.diff(beta[1], x)-s.diff(beta[0], y)
check('marked transverse shift curl', curl, b)
check('cross-query x beta_y', s.diff(beta[1], x), b/2)
check('cross-query y beta_x', s.diff(beta[0], y), -b/2)

# Demonstrate actual smooth local immersions through arbitrary base points.
tau, sigma, t0, x0, y0, z0 = s.symbols('tau sigma t0 x0 y0 z0', real=True)
F = [s.Matrix([t0+tau+b*y0*sigma/2, x0+sigma, y0, z0]),
     s.Matrix([t0+tau-b*x0*sigma/2, x0, y0+sigma, z0]),
     s.Matrix([t0+tau, x0, y0, z0+sigma])]
for i, fi in enumerate(F):
    df = fi.jacobian([tau, sigma])
    sub = dict(zip(q, fi))
    check(f'orthogonal immersion Jacobian {i}', df, Jorth[i].subs(sub, simultaneous=True))
    check(f'orthogonal immersion pullback {i}', df.T*g.subs(sub, simultaneous=True)*df, s.diag(-1, 1))
    check(f'orthogonal immersion rank witness {i}', df.extract([0, i+1], [0, 1]).det(), 1)

def bracket(v, w):
    return s.simplify(w.jacobian(q)*v-v.jacobian(q)*w)

check('nonintegrable spatial distribution bracket', bracket(Jorth[0][:, 1], Jorth[1][:, 1]), -b*U)

# Direct Levi-Civita computation: no use of DCI/NCI source geometry functions.
Gamma = [[[s.simplify(sum(ginv[a,d]*(s.diff(g[d,c],q[e])+s.diff(g[d,e],q[c])-s.diff(g[c,e],q[d]))/2
                            for d in range(4))) for e in range(4)] for c in range(4)] for a in range(4)]
u = g*U
nabla = s.Matrix(4,4,lambda a,c:s.simplify(s.diff(u[c],q[a])-sum(Gamma[d][a][c]*u[d] for d in range(4))))
acc = s.Matrix([Gamma[a][0][0] for a in range(4)])
check('direct coordinate acceleration', acc, s.zeros(4,1))
check('direct Killing symmetric derivative', nabla+nabla.T, s.zeros(4))
P = s.eye(4)+u*U.T
w = s.simplify(P*((nabla-nabla.T)/2)*P.T)
expected_w = s.zeros(4); expected_w[1,2]=-b/2; expected_w[2,1]=b/2
check('projected vorticity direct connection', w, expected_w)
W = s.simplify(sum(w[a,c]*ginv[a,d]*ginv[c,e]*w[d,e] for a in range(4) for c in range(4) for d in range(4) for e in range(4)))
check('vorticity norm from inverse metric contraction', W, b*b/2)
Ric00 = s.simplify(sum(s.diff(Gamma[a][0][0],q[a])-s.diff(Gamma[a][a][0],t)
    +sum(Gamma[a][a][d]*Gamma[d][0][0]-Gamma[a][0][d]*Gamma[d][a][0] for d in range(4)) for a in range(4)))
check('direct R00 corroboration only', Ric00, b*b/2)
k = s.Matrix(s.symbols('k0:4', real=True))
check('affine geodesic U-dot-k conservation identity', (k.T*nabla*k)[0], 0)

# Same coordinate transformation versus reselected coordinate directions.
f = x*y+x+x*x*z/3+y*y/5
dfsp = s.Matrix([s.diff(f,c) for c in (x,y,z)])
K = s.eye(4); K[0,1:4] = dfsp.T
Eprime = s.simplify(E*K.inv())
Aprime = A-dfsp
for i in range(3):
    j = Jcoord[i]
    jprime = K*j
    check(f'matched full coframe covariance {i}', Eprime*jprime, E*j)
    check(f'matched h covariance {i}', jprime.T*Eprime.T*eta*Eprime*jprime, Hcoord[i])
    reselection = s.simplify(j.T*Eprime.T*eta*Eprime*j)
    check(f'reselected coordinate shift {i}', reselection[0,1]/reselection[0,0], Aprime[i])
check('common synchronization curl unchanged', s.diff(Aprime[1],x)-s.diff(Aprime[0],y), b)
check('flat pure-gradient shift zero curl', (s.diff(Aprime[1],x)-s.diff(Aprime[0],y)).subs(b,0), 0)
check('common coframe assumption inverse recovery', E.inv()*Vorth[0], Jorth[0])

# Current scalar and older control differ under a lawful auxiliary ruler rescaling.
hc = Hcoord[0]
rescale = s.diag(1,3)
hr = s.simplify(rescale.T*hc*rescale)
check('rescaled auxiliary density', -hr.det(), 9)
check('rescaled completed scalar remains zero', -s.log(-hr[0,0])/2, 0)
check('historical control rescales', s.log(-hr.det()/hr[0,0]**2)/4, s.log(3)/2)

# Negative controls invoke the same equality/regularity guards and must be rejected.
reject('wrong extracted shift sign', lambda: equal('shift sign', -beta[0], A[0]))
reject('wrong transverse curl sign', lambda: equal('curl sign', -curl, b))
reject('wrong transverse curl half factor', lambda: equal('curl factor', curl/2, b))
reject('wrong vorticity factor', lambda: equal('W factor', W, b*b))
reject('erasing retained coordinate shift', lambda: equal('shift deletion', Hcoord[0], s.diag(-1,1)))
reject('pointwise shift implies invariant twist', lambda: equal('gradient is not twist', (Aprime.T*Aprime)[0].subs({b:0,x:0,y:0,z:0}), 0))
reject('unmatched coordinate transform called same query', lambda: equal('unmatched transformation', Eprime*Jcoord[0], E*Jcoord[0]))
reject('adapted V equality means same coordinate tangent', lambda: equal('missing common E', Jorth[0].subs(b,2), Jorth[0].subs(b,0)))
reject('ordinary V derivatives supply ambient tangent derivatives', lambda: equal('missing frame derivative', Jorth[0].diff(y), (E*Jorth[0]).diff(y)))
reject('orthogonal 3-frame assumed holonomic', lambda: equal('spatial integrability', bracket(Jorth[0][:,1],Jorth[1][:,1]),s.zeros(4,1)))
reject('along-strip data substitutes for cross-query jets', lambda: equal('transverse derivative absent', s.diff(beta[1],y)-s.diff(beta[0],x),b))
reject('independent strip clock potentials assumed a common scalar', lambda: equal('mixed partial obstruction', s.diff(beta[1],x),s.diff(beta[0],y)))
reject('positive first leg admitted as clock', lambda: regular(s.eye(2)))
reject('degenerate pair admitted regular', lambda: regular(s.diag(-1,0)))
reject('dependent tangent columns admitted regular', lambda: regular(U.row_join(U).T*g*U.row_join(U)))
reject('historical control substituted for completed Phi', lambda: equal('wrong scalar ownership', s.log(-hr.det()/hr[0,0]**2)/4, -s.log(-hr[0,0])/2))
reject('time evaluated before derivative', lambda: equal('retained time dependency', s.Matrix([[-1,t],[t,1-t*t]]).diff(t),s.zeros(2)))
reject('matrix shape mismatch treated as equality', lambda: equal('shape guard', s.zeros(4,2),s.zeros(2,2)))

print(json.dumps({'status':'PASS','implementation':'independent direct metric expansion, connection, projection and explicit maps; no source code imports',
 'python':platform.python_version(),'sympy':s.__version__,'platform':platform.platform(),'parameters':'t,x,y,z,b real; exact symbolic identities for every real b',
 'arrays':{'metric':[4,4],'pair_germs':[4,2],'pair_metrics':[2,2],'vorticity':[4,4]},'positive_count':len(positive),'negative_count':len(negative),
 'positive_checks':positive,'negative_controls':negative,'derived':{'beta':str(beta),'curl':str(curl),'W':str(W),'Ric00':str(Ric00),'vorticity':str(w)},
 'limitations':'exact symbolic regression supports the independent analytic argument; no all-source replay, physical protocol, global branch domain or metric inversion claim'},indent=2))
