"""Direct-review exact checks constructed before ICN1 author code/output exposure.

Metric-led conditional Lorentz2/product sector and conformal4 controls only.
All supplied geometry coefficients and initial data are free-and-explored.
No new UDT premise, numeric fit, grid, floating-point tolerance, or GPU.
60s/512MiB wrapper and threads=1. Stop on first mismatch; preserve failed run.
Maximum claim: check candidate's bounded algebra/geometry, no physical admission.
"""
import hashlib
import json
import pathlib
import platform
import sys
import sympy as S

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
records = []


def eq(label, lhs, rhs=0):
    if lhs == rhs:
        residual = S.Integer(0)
    elif isinstance(lhs, S.MatrixBase):
        residual = S.simplify((lhs-rhs).norm())
    else:
        residual = S.simplify(S.sympify(lhs-rhs).rewrite(S.exp))
    if residual != 0:
        raise RuntimeError(label + ': ' + str(residual))
    records.append(dict(label=label, kind='exact_identity', residual=str(residual)))


def reject(label, actual, wrong):
    residual = S.simplify(actual-wrong)
    if residual == 0:
        raise RuntimeError('wrong rule survived: '+label)
    records.append(dict(label=label, kind='wrong_rule_rejected', residual=str(residual)))


freeze = json.loads((PKG/'CANDIDATE_FREEZE.json').read_text())
pins = {p:hashlib.sha256((PKG/p).read_bytes()).hexdigest()
        for p in freeze['candidate_and_checks']}
if pins != freeze['candidate_and_checks']:
    raise RuntimeError('candidate freeze mismatch')
seal = json.loads((HERE/'SOURCE_FIRST_SEAL.json').read_text())
if any(hashlib.sha256((HERE/p).read_bytes()).hexdigest()!=h for p,h in seal['sha256'].items()):
    raise RuntimeError('source-first seal mismatch')


def connection(g, x):
    n, gi = len(x), g.inv()
    return [[[S.simplify(sum(gi[a,d]*(S.diff(g[d,b],x[c])+S.diff(g[d,c],x[b])-
                                         S.diff(g[b,c],x[d])) for d in range(n))/2)
              for c in range(n)] for b in range(n)] for a in range(n)]


# Full product metric connection, with no imported author geodesic formula.
T,R,Y,Z,c = S.symbols('T R Y Z c', real=True)
phi = S.Function('phi')(T,R)
x = [T,R,Y,Z]
g = S.diag(-c**2*S.exp(2*phi),S.exp(2*phi),1,1)
Gamma = connection(g,x)
beta, dbeta = S.symbols('beta dbeta', real=True)
velocity = [1,c*beta,0,0]
spray = [S.simplify(sum(Gamma[a][b][d]*velocity[b]*velocity[d]
                        for b in range(4) for d in range(4))) for a in range(4)]
eq('no transverse acceleration in product sector', S.Matrix(spray[2:]), S.zeros(2,1))
nonaffine = S.factor((c*dbeta+spray[1]-velocity[1]*spray[0])/c)
eq('original connection gives candidate beta equation', nonaffine,
   dbeta+(1-beta**2)*(c*S.diff(phi,R)+beta*S.diff(phi,T)))
eq('reference clock radial acceleration at beta0', spray[1].subs(beta,0), c**2*S.diff(phi,R))

# Extract gradient from the original geodesic constraint plus measured metric drift.
kt,st,pt,pr = S.symbols('Kdot Sdot phiT phiR', real=True)
gradient = S.solve([kt-pt-c*beta*pr, st+c*pr+beta*pt],[pt,pr])
eq('independent gradient linear solve time', gradient[pt], (kt+beta*st)/(1-beta**2))
eq('independent gradient linear solve space', c*gradient[pr], (-st-beta*kt)/(1-beta**2))

# Recover the coefficient from proper normalization in null radar labels, without eq(6).
p,q = S.symbols('p q',positive=True)
dTdb = (1/p+q)/2
dRdb = c*(q-1/p)/2
om2 = S.simplify(1/(dTdb**2-dRdb**2/c**2))
eq('normalization directly recovers Omega squared',om2,p/q)
eq('coordinate velocity directly from null labels',dRdb/(c*dTdb),(p*q-1)/(p*q+1))

# Finite generic local data reject swapped signs, omitted factors, and missing denominator.
point={beta:S.Rational(3,5),c:3,pt:S.Rational(1,7),pr:-S.Rational(2,11)}
kd=(pt+c*beta*pr).subs(point)
sd=(-c*pr-beta*pt).subs(point)
sub={beta:point[beta],kt:kd,st:sd}
eq('finite gradient time from measured drift',gradient[pt].subs(sub),point[pt])
eq('finite gradient space from measured drift',(c*gradient[pr]).subs(sub),point[c]*point[pr])
for label,wrong in [
    ('wrong time cross sign',(kt-beta*st)/(1-beta**2)),
    ('time denominator omitted',kt+beta*st),
    ('time beta cross term omitted',kt/(1-beta**2)),
    ('space main sign reversed',(st-beta*kt)/(1-beta**2)),
    ('space beta cross sign reversed',(-st+beta*kt)/(1-beta**2)),
    ('space denominator omitted',-st-beta*kt),
]:
    actual=point[pt] if label.startswith('time') or label.startswith('wrong time') else point[c]*point[pr]
    reject(label,actual,wrong.subs(sub))

# A(T,R)=a*T*R^2 is a nonstatic smooth radar-sector geometry with a free geodesic
# reference clock R=0; local B geodesics exist by the smooth ODE theorem.
a=S.symbols('a',real=True)
phictl=a*T*R**2
eq('nonstatic control A normalization',phictl.subs(R,0),0)
eq('nonstatic control A free fall',S.diff(phictl,R).subs(R,0),0)
kctl=S.diff(phictl,T)+c*beta*S.diff(phictl,R)
sctl=-c*S.diff(phictl,R)-beta*S.diff(phictl,T)
eq('nonstatic control reconstructs phiT',gradient[pt].subs({kt:kctl,st:sctl}),S.diff(phictl,T))
eq('nonstatic control reconstructs c phiR',(c*gradient[pr]).subs({kt:kctl,st:sctl}),c*S.diff(phictl,R))

# Third observer actual arrival geometry and delay derivative, including path domains.
v,s=S.symbols('v s',real=True)
gamma=1/S.sqrt(1-v**2)
direct_t=(s+1)/(1-v)
via_t=(s+3)/(1+v)
eq('direct null incidence at C',direct_t-s,1+v*direct_t)
eq('relay B to C left-null incidence',via_t-(s+2),2-(1+v*via_t))
delay=(via_t-direct_t)/gamma
eq('delay slope from incidence equations',S.diff(delay,s),-2*gamma*v)
samples=[]
for speed in [S.Rational(1,5),-S.Rational(1,5)]:
    dt=direct_t.subs({s:0,v:speed})
    vt=via_t.subs({s:0,v:speed})
    d0=S.simplify(delay.subs({s:0,v:speed}))
    d1=S.simplify(S.diff(delay,s).subs(v,speed))
    assert dt>0 and vt>2 and d0>0
    assert 0<1+speed*dt<2 and 0<1+speed*vt<2
    assert S.sign(d1)==-S.sign(speed)
    samples.append(dict(v=str(speed),direct_t=str(dt),relay_t=str(vt),delay=str(d0),delay_slope=str(d1)))
    records.append(dict(label='three-clock positive delay and opposite drift v='+str(speed),kind='exact_inequality',passed=True))

# Direct 4D curvature from metric, not a conformal scalar-curvature formula.
t,xx,y,z,k=S.symbols('t x y z k',real=True)
xc=[t,xx,y,z]
psi=k*xx**2
gc=S.exp(2*psi)*S.diag(-1,1,1,1)
Gc=connection(gc,xc)
ric=S.zeros(4)
for i in range(4):
    for j in range(4):
        ric[i,j]=S.simplify(sum(S.diff(Gc[r][i][j],xc[r])-S.diff(Gc[r][i][r],xc[j])+
                           sum(Gc[r][r][l]*Gc[l][i][j]-Gc[r][j][l]*Gc[l][i][r]
                               for l in range(4)) for r in range(4)))
scalar=S.simplify(S.trace(gc.inv()*ric))
eq('original metric connection curvature at interior point',scalar.subs(xx,0),-12*k)
reject('curvature sign flip',scalar.subs(xx,0).subs(k,1),12)
reject('nonconstant conformal deformation called flat',scalar.subs(xx,0).subs(k,1),0)

# Same null path retains an affine parametrization after tangent rescaling.
null=S.Matrix([1,1,0,0])
eq('coordinate ray remains null',(null.T*gc*null)[0],0)
affine=S.exp(-2*psi)*null
acc=S.Matrix([sum(affine[j]*S.diff(affine[i],xc[j]) for j in range(4))+
              sum(Gc[i][j][l]*affine[j]*affine[l] for j in range(4) for l in range(4))
              for i in range(4)])
eq('conformal ray affine reparametrization',acc,S.zeros(4,1))

# Taylor bound saturation for a smooth cubic in the allowed normalized sector.
aa,bb,rr=S.symbols('aa bb rr',positive=True)
cubic=aa*rr**2+bb*rr**3
remainder=cubic-S.diff(cubic,rr,2).subs(rr,0)*rr**2/2
eq('third derivative remainder bound sharp control',remainder, S.diff(cubic,rr,3)*rr**3/6)

# A common mass,length,time unit scaling leaves both c and G weights zero but
# does not leave a pure dimensional scale weight zero.
dim=S.Matrix([[0,-1],[1,3],[-1,-2]])
weight=S.Matrix([[1,1,1]])
eq('unit-rescaling stabilizer leaves both constants',weight*dim,S.zeros(1,2))
eq('unit-rescaling stabilizer changes length', (weight*S.Matrix([0,1,0]))[0],1)
eq('unit-rescaling stabilizer changes time', (weight*S.Matrix([0,0,1]))[0],1)

record=dict(stage='DIRECT_CHECKS_BEFORE_AUTHOR_CODE_OUTPUT_EXPOSURE',
            candidate_sha256=pins['INITIAL_CANDIDATE.md'],frozen_pins=pins,
            python=sys.version,sympy=S.__version__,platform=platform.platform(),
            records=records, count=len(records), three_clock_samples=samples,
            curvature_scalar=str(scalar), passed=True,
            script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
with (HERE/'DIRECT_CHECKS.json').open('x') as stream:
    json.dump(record,stream,indent=2);stream.write('\n')
print(json.dumps(dict(passed=True,count=len(records),candidate_sha256=pins['INITIAL_CANDIDATE.md'])))
