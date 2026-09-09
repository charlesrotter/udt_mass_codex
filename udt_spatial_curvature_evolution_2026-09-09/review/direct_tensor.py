"""Direct-stage independent metric-jet extraction of author's other datum.

Reuses only the reviewer's sealed 4D reconstruction. Its import repeats the
source-first checks (regression), then the new checks below run. No author
functions or numerical outputs are used as calculation inputs.
"""
import json
import sympy as S
import source_first_tensor as engine

x=engine.x
eps=S.Rational(1,9)  # FREE rational check of author's distinct analytic datum.
u=eps*S.cos(x)
# Constant transverse coordinate rescaling makes the event frame orthonormal.
g0=[S.Integer(1),S.exp(2*(u-eps)),S.exp(-2*(u-eps))]
kk=[S.Rational(1,3)-3*S.diff(u,x)**2/4,-S.Rational(2,3),-S.Rational(2,3)]
a,b,c=g0
ap,bp,cp=[S.diff(v,x) for v in g0]
bpp,cpp=S.diff(b,x,2),S.diff(c,x,2)
# Ricci of an arbitrary diagonal spatial metric depending only on x.
ric=[-bpp/(2*b)-cpp/(2*c)+bp*bp/(4*b*b)+cp*cp/(4*c*c)
     +ap*bp/(4*a*b)+ap*cp/(4*a*c),
     -bpp/(2*a)+ap*bp/(4*a*a)+bp*bp/(4*a*b)-bp*cp/(4*a*c),
     -cpp/(2*a)+ap*cp/(4*a*a)+cp*cp/(4*a*c)-bp*cp/(4*a*b)]
tau=sum(kk)
gt=[-2*g*k for g,k in zip(g0,kk)]
kt=[r+tau*g*k-2*g*k*k for r,g,k in zip(ric,g0,kk)]
gtt=[-2*v for v in kt]
# At x=0 all first spatial metric/time-metric derivatives vanish. Differentiate
# the displayed diagonal Ricci formulas, retaining the inverse-metric terms.
r0=[S.simplify(r.subs(x,0)) for r in ric]
g1=[S.simplify(v.subs(x,0)) for v in gt]
second=[S.simplify(S.diff(v,x,2).subs(x,0)) for v in g0]
g1second=[S.simplify(S.diff(v,x,2).subs(x,0)) for v in gt]
rdot=[(-g1second[1]+second[1]*g1[1]-g1second[2]+second[2]*g1[2])/2,
      (-g1second[1]+second[1]*g1[0])/2,
      (-g1second[2]+second[2]*g1[0])/2]
k0=[S.simplify(k.subs(x,0)) for k in kk]
tau0=sum(k0)
taudot=sum(r0)+tau0*tau0
kt0=[S.simplify(v.subs(x,0)) for v in kt]
gttt=[-2*(rd+taudot*k+(tau0-4*k)*v-4*k**3)
       for rd,k,v in zip(rdot,k0,kt0)]
engine.k=kk
engine.covjets=[g0,gt,gtt,gttt]
result,Q,W=engine.metric_reconstruction(S.Integer(0))
expectedE=S.diag(-S.Rational(4,9),S.Rational(2,9)+eps,S.Rational(2,9)-eps)
expectedW=S.diag(S.Rational(8,9),-S.Rational(4,9)+eps,-S.Rational(4,9)-eps)
assert Q==expectedE
assert W==expectedW
assert result['normal_A']=='68040/28561'

# New matched m=0 check. This direct reconstruction is post-candidate exposure.
q=S.Rational(1,6)
kc=[S.Rational(1,3)-3*q*q/4,-S.Rational(2,3)-q,-S.Rational(2,3)+q]
tc=sum(kc)
engine.k=kc
engine.covjets=[[S.Integer(1)]*3,[-2*v for v in kc],
    [-2*tc*v+4*v*v for v in kc],
    [-4*tc*tc*v+12*tc*v*v-8*v**3 for v in kc]]
homogeneous,Qh,Wh=engine.metric_reconstruction(S.Integer(0))
assert Qh==S.diag(-S.Rational(5,12),S.Rational(5,32),S.Rational(25,96))
assert Wh==2*tc*Qh
assert homogeneous['normal_A']=='0'
print(json.dumps({'direct_distinct_author_datum_e_1_9':result,
    'direct_matched_homogeneous_e_1_6':homogeneous,
    'independence':'Reused reviewer full 4D engine; new supplied metric jets and direct Ricci variation, no author functions; source-first repeat above is regression'},indent=2))
