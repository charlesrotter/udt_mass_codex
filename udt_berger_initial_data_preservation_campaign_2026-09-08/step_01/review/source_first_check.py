"""BI1 independent exact reconstruction; reads no author code or results.

Pinned conditional source brackets/sign; all six K entries are symbolic.
Exact arithmetic only. Outputs JSON to stdout, captured by existing runner.
"""
import itertools
import json
import platform
import sympy as S

I = range(3)
p, q = S.symbols('p q', positive=True)
x, y, z, u, v, w = variables = S.symbols('x y z u v w', real=True)
K = S.Matrix([[x, u, v], [u, y, w], [v, w, z]])
h = -2*K
C = [[[S.Integer(0) for k in I] for j in I] for i in I]
for i,j,k,value in [(0,1,2,q),(1,2,0,p),(2,0,1,p)]:
    C[i][j][k] = value
    C[j][i][k] = -value
G = [[[S.expand((C[i][j][k]-C[j][k][i]+C[k][i][j])/2)
       for k in I] for j in I] for i in I]

# Differentiate the Koszul formula at g=I with fixed brackets and gdot=-2K.
Gd = [[[S.expand(sum(-h[k,l]*G[i][j][l] for l in I)
                    +sum(C[i][j][m]*h[m,k]-C[j][k][m]*h[m,i]
                         +C[k][i][m]*h[m,j] for m in I)/2)
        for k in I] for j in I] for i in I]

def ricci(connection):
    return S.Matrix(3,3,lambda j,k: S.expand(sum(
        connection[j][k][m]*connection[i][m][i]
        -connection[i][k][m]*connection[j][m][i]
        -C[i][j][m]*connection[m][k][i] for i in I for m in I)))

Ric = ricci(G)
Ricd = S.Matrix(3,3,lambda j,k: S.expand(sum(
    Gd[j][k][m]*G[i][m][i]+G[j][k][m]*Gd[i][m][i]
    -Gd[i][k][m]*G[j][m][i]-G[i][k][m]*Gd[j][m][i]
    -C[i][j][m]*Gd[m][k][i] for i in I for m in I)))
Ad = S.simplify(Ricd-h*Ric)
lh, lv = p*q-q*q/2, q*q/2
gap = lv-lh

# A second method differentiates covariant tensors, keeping ordered spatial jets.
first = {(r,b): S.Symbol(f'e{r+1}_{b}', real=True) for r in I for b in variables}
second = {(r,s,b): S.Symbol(f'e{r+1}e{s+1}_{b}', real=True)
          for r in I for s in I if r<=s for b in variables}
def e2(r,s,b):
    if r<=s:
        return second[r,s,b]
    return second[s,r,b]+sum(C[r][s][k]*first[k,b] for k in I)
def E(r,expr):
    return S.expand(sum(S.diff(expr,b)*first[r,b] for b in variables)
        +sum(S.diff(expr,first[s,b])*e2(r,s,b) for s in I for b in variables))
D1 = [[[S.expand(E(r,K[j,k])-sum(G[r][j][m]*K[m,k]
          +G[r][k][m]*K[j,m] for m in I)) for k in I] for j in I] for r in I]
D2 = [[[[S.expand(E(r,D1[s][j][k])-sum(
    G[r][s][m]*D1[m][j][k]+G[r][j][m]*D1[s][m][k]
    +G[r][k][m]*D1[s][j][m] for m in I))
    for k in I] for j in I] for s in I] for r in I]
tau = S.trace(K)
Rop = S.Matrix(3,3,lambda i,j: S.expand(
    sum(-D2[k][i][k][j]-D2[k][j][k][i]+D2[k][k][i][j] for k in I)
    +E(i,E(j,tau))-sum(G[i][j][m]*E(m,tau) for m in I)))
zero_jets = dict.fromkeys(list(first.values())+list(second.values()),0)
Mom = [S.expand(sum(D1[j][j][i] for j in I)-E(i,tau)) for i in I]
Hquad = S.expand((tau*tau-S.trace(K*K))/2)
checks = []
def check(name, actual, expected=0):
    residual = S.simplify(actual-expected)
    ok = residual == S.zeros(*residual.shape) if isinstance(residual,S.MatrixBase) else residual==0
    checks.append({'name':name,'pass':bool(ok),'residual':str(residual)})
check('Koszul Ricci eigenvalues',Ric,S.diag(lh,lh,lv))
check('covariant uncommuted versus direct Koszul derivative',Rop.subs(zero_jets),Ricd)
check('smooth Ricci variation symmetric after bracket commutator',Rop,Rop.T)
check('all-six homogeneous momentum',S.Matrix(Mom).subs(zero_jets),S.Matrix([(q-p)*w,(p-q)*v,0]))
check('Hamiltonian all six entries',Hquad,x*y+x*z+y*z-u*u-v*v-w*w)
check('homogeneous constrained image numerator',S.Matrix([Ad[0,2],Ad[1,2]]).subs({v:0,w:0}),S.zeros(2,1))
check('homogeneous constrained projector complementary block',S.Matrix([Ad[2,0],Ad[2,1]]).subs({v:0,w:0}),S.zeros(2,1))
check('raising-index mixed-block difference',Ad[0,2]-Ad[2,0],2*gap*v)
check('raising-index mixed-block difference second',Ad[1,2]-Ad[2,1],2*gap*w)
check('round momentum unrestricted',S.Matrix(Mom).subs(zero_jets).subs(q,p),S.zeros(3,1))

# Analytic two-branch parametrization; no division on its s=0 branch.
s,d,b,Etarget = S.symbols('s d b Etarget', real=True)
sub = {x:s/2+d,y:s/2-d,u:b,v:0,w:0}
check('s nonzero parametrization',Hquad.subs(sub).subs(z,(Etarget+d*d+b*b-s*s/4)/s),Etarget)
check('s zero original quadratic',Hquad.subs(sub).subs(s,0),-d*d-b*b)
check('complete sign reversal preserves Hamiltonian',Hquad.xreplace({a:-a for a in variables}),Hquad)

# Fixed geometry a=1,c=3/2 gives p=4/3,q=3,R=7/2.
geometry = {p:S.Rational(4,3),q:S.Integer(3)}
Rscalar = 2*lh+lv
check('declared rational Berger scalar',Rscalar.subs(geometry),S.Rational(7,2))
witnesses = []
for sign in [-1,1]:
    for name, entries, lam in [
        ('nonaxisymmetric', [1,0,S.Rational(9,4),1,0,0], S.Integer(3)),
        ('singular s=0 circle', [1,-1,2,0,0,0], S.Rational(3,4)),
        ('singular s=0 point', [0,0,-3,0,0,0], S.Rational(7,4))]:
        data = dict(zip(variables,[sign*a for a in entries]))
        residual = S.simplify((Rscalar+2*Hquad-2*lam).subs(geometry).subs(data))
        check(name+f' sign {sign} original Hamiltonian',residual)
        check(name+f' sign {sign} original momentum',S.Matrix(Mom).subs(zero_jets).subs(geometry).subs(data),S.zeros(3,1))
        witnesses.append({'name':name,'sign':sign,'entries':list(map(str,[sign*a for a in entries])),
                          'Lambda':str(lam),'Hamiltonian_residual':str(residual)})

# Hostile controls are explicitly unconstrained where stated; they are not lawful witnesses.
hostile = []
mixed = {x:0,y:0,z:0,u:0,v:1,w:0}
for name, residual in [
    ('drop raising index changes mixed image numerator', (Ad[0,2]-Ricd[0,2]).subs(geometry).subs(mixed)),
    ('treat invariant K components as parallel loses Ricci derivative',Ricd[0,2].subs(geometry).subs(mixed)),
    ('drop momentum connection admits invalid mixed K',S.Matrix(Mom).subs(zero_jets).subs(geometry).subs(mixed)[1]),
    ('image versus projector difference', (Ad[0,2]-Ad[2,0]).subs(geometry).subs(mixed))]:
    residual = S.simplify(residual)
    hostile.append({'name':name,'detected':residual!=0,'nonzero_residual':str(residual),
                    'lawful_witness':False})

out = {'python':platform.python_version(),'sympy':S.__version__,
       'method':'symbolic differentiated Koszul curvature versus uncommuted covariant tensor jets',
       'brackets':{'p':'2/c','q':'2c/a^2'},'K_entries':'x y z u=12 v=13 w=23',
       'Ricci':str(Ric),'homogeneous_Ricci_dot':str(Ricd),
       'homogeneous_endomorphism_dot':str(Ad),'smooth_momentum':list(map(str,Mom)),
       'smooth_mixed_Ricci_dot':[str(Rop[0,2]),str(Rop[1,2])],
       'checks':checks,'witnesses':witnesses,'hostile_controls':hostile,
       'all_pass':all(c['pass'] for c in checks) and all(c['detected'] for c in hostile)}
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['all_pass'] else 1)
