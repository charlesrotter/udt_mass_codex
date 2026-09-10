"""QC2 author exact Laurent probes; continuum/limit claims remain proof-owned."""
from fractions import Fraction as F
import hashlib
import json
import platform
from pathlib import Path

checks=0
records=[]


def eq(a,b,label):
    global checks
    assert a==b,(label,a,b)
    checks+=1


def le(a,b,label):
    global checks
    assert a<=b,(label,a,b)
    checks+=1


def val(poly,x,j=0):
    total=F(0)
    for k,v in poly.items():
        coefficient=v
        for i in range(j): coefficient*=k-i
        total+=coefficient*x**(k-j)
    return total


def add(a,b):
    out=dict(a)
    for k,v in b.items(): out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}


W={2:F(1,3),-1:F(2,3),0:F(-1)}


def defect(poly):
    out={k:v*(F(k*(k-1),2)-1) for k,v in poly.items()}
    return add(out,{0:F(1)})


def curvature(poly,x):
    return [val(poly,x,2)/2,val(poly,x,1)/(2*x),-val(poly,x,1)/(2*x),
            (1-val(poly,x))/x**2]


eq(val(W,F(1)),F(0),'W value anchor')
eq(val(W,F(1),1),F(0),'W slope anchor')
# Direct original residual is C[p+epsilon W], not C[W] alone.
for n in [2,3,5,10,100,1000]:
    eps=F(1,n*n)
    p={0:F(1)}
    y={k:eps*v for k,v in W.items()}
    q=add(p,y)
    eq(defect(q),{0:eps},'grow complete residual identity')
    for j in [0,1]: eq(val(q,F(1),j),val(p,F(1),j),'grow exact anchor')
    for x in [F(1),F(3,2),F(n+1,2),F(n)]:
        le(F(1),val(q,x),'grow floor')
        k=curvature(q,x)
        eq(k[0],eps*(1+2/x**3)/3,'radial independent profile derivative')
        eq(k[1],eps*(1-1/x**3)/3,'tangential derivative')
        eq(k[2],-k[1],'opposite sectional')
        eq(k[3],-eps*(F(1,3)+F(2,3)/x**3-1/x**2),'sphere difference')
        le(abs(k[0]),eps,'radial bound')
        for value in k[1:]: le(abs(value),eps/3,'other sectional bound')
    squared=val(q,F(n))/val(q,F(1))
    target=F(4,3)-eps+F(2,3*n**3)
    eq(squared,target,'exact growing endpoint clock quotient squared')
    # A quantitative convergence bound supports, not proves, the written limit.
    le(abs(squared-F(4,3)),eps,'endpoint distance to rational limiting square')
    le(F(1,6),squared-1,'nonvanishing squared clock difference n>=2')
    records.append({'family':'GROW','n':n,'epsilon':str(eps),'clock_quotient_squared':str(squared)})

for eps in [F(1,4),F(1,9),F(1,100),F(1,10000),F(1,10**12)]:
    p={0:F(1),-1:-F(1,2)+eps}
    y={k:eps*v for k,v in W.items()}
    q=add(p,y)
    eq(defect(p),{},'gap balanced reference')
    eq(defect(q),{0:eps},'gap exact residual')
    for j in [0,1]: eq(val(q,F(1),j),val(p,F(1),j),'gap exact anchor')
    eq(val(p,F(1)),F(1,2)+eps,'bounded varying reference datum0')
    eq(val(p,F(1),1),F(1,2)-eps,'bounded varying reference datum1')
    for x in [F(1,2),F(3,5),F(3,4),F(1)]:
        le(2*eps,val(p,x),'positive reference')
        le(val(p,x),val(q,x),'positive profile')
        le(abs(val(p,x,1)),F(2),'bounded reference slope')
        for j,bound in enumerate([5*eps/12,7*eps/3,34*eps/3]):
            le(abs(val(q,x,j)-val(p,x,j)),bound,'gap C2 profile control')
        diff=[a-b for a,b in zip(curvature(q,x),curvature(p,x))]
        for observed,bound in zip(diff,[17*eps/3,7*eps/3,7*eps/3,5*eps/3]):
            le(abs(observed),bound,'gap curvature control')
    l=F(1,2)
    eq(val(p,l),2*eps,'actual minimum reference gap')
    squared=(val(q,l)/val(q,F(1)))/(val(p,l)/val(p,F(1)))
    eq(squared,F(29,24),'gap nonvanishing relative clock quotient squared')
    records.append({'family':'GAP','epsilon':str(eps),'clock_quotient_squared':str(squared)})

# Specific identity defects actually rejected, not generic certification.
rejected=[]


def reject(label,operation):
    global checks
    try:
        operation()
    except AssertionError:
        rejected.append(label)
        checks+=1
    else:
        raise AssertionError('mutation passed '+label)


reject('omit minus-one and lose anchor match',lambda:eq(val(add(W,{0:F(1)}),F(1)),F(0),'mutant'))
reject('invert relative clock square',lambda:eq(F(24,29),F(29,24),'mutant'))

print(json.dumps({'status':'PASS','assertions':checks,'python':platform.python_version(),
 'method':'standalone Fraction Laurent profiles, original residual and curvature derivatives; clock squares exact',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'records':records,'rejected_formula_mutations':rejected,
 'limits':'Finite probes support identities; analytic proof owns all-domain positivity and nonvanishing limits; no evolution or empirical accuracy'},indent=2))
