"""TRI1 mathematical controls; independent stdlib exact rational implementation."""
from fractions import Fraction as F
from collections import Counter
import json, platform, sys

checks = []
def check(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    checks.append(name)
def dot(a,b):
    return -a[0]*b[0]+sum(x*y for x,y in zip(a[1:],b[1:]))
def clock(p):
    p=F(p)
    return ((p+1/p)/2,(p-1/p)/2,F(0),F(0))
def scale(a,k): return tuple(a*x for x in k)
def om(u,k): return -dot(u,k)
def mom(pop):
    low=[(w,(-k[0],*k[1:])) for w,k in pop]
    return [[sum(w*k[a]*k[b] for w,k in low) for b in range(4)] for a in range(4)]
def eigen(M,u,rho):
    return [(-1 if a==0 else 1)*sum(M[a][b]*u[b] for b in range(4))+rho*u[a] for a in range(4)]
kp=(F(1),F(1),F(0),F(0)); km=(F(1),F(-1),F(0),F(0))
for p in [F(1,3),F(1,2),F(1),F(2),F(3)]:
    u=clock(p)
    check('unit clock '+str(p),dot(u,u),F(-1))
    v=u[1]/u[0]
    arrival_slope=1/(u[0]*(1-v))
    check('incidence/contraction '+str(p),arrival_slope,om(clock(1),kp)/om(u,kp))
    check('incidence slope '+str(p),arrival_slope,p)
    for a in [F(1,5),F(1),F(7)]:
        check('affine scaling '+str((p,a)),om(clock(1),scale(a,kp))/om(u,scale(a,kp)),p)
    for q in [F(1,2),F(1),F(3)]:
        middle=clock(q)
        check('intermediate cancellation '+str((p,q)),(om(clock(1),kp)/om(middle,kp))*(om(middle,kp)/om(u,kp)),p)
check('changed endpoint changes Z',om(clock(1),kp)/om(clock(2),kp) != om(clock(1),kp)/om(clock(3),kp),True)
M0=mom([(F(1),kp),(F(1),km)])
check('symmetric beams rest eigenvector',eigen(M0,clock(1),F(2)),[0]*4)
M1=mom([(F(1),scale(F(4),kp)),(F(1),km)])
check('spectral change rest eigenvector',eigen(M1,clock(2),F(8)),[0]*4)
check('spectral change destroys old rest eigenvector',eigen(M1,clock(1),F(17)) != [0]*4,True)
check('direction scaling changes moment',M1 != M0,True)
Mc=mom([(F(1),scale(F(3),kp)),(F(1),scale(F(3),km))])
check('common scale moment',Mc,[[9*x for x in row] for row in M0])
check('common scale preserves observer',eigen(Mc,clock(1),F(18)),[0]*4)
ellplus=scale(F(5),kp); alphaplus=F(4,5)
check('compensated representative change',mom([(F(1),scale(alphaplus,ellplus)),(F(1),km)]),M1)
Mweights=mom([(F(16),kp),(F(1),km)])
check('weighted minimizer eigenvector',eigen(Mweights,clock(2),F(8)),[0]*4)
J=tuple(16*a+b for a,b in zip(kp,km))
check('current norm',dot(J,J),F(-64))
uJ=tuple(x/8 for x in J)
check('current observer normalized',dot(uJ,uJ),F(-1))
check('current velocity',uJ[1]/uJ[0],F(15,17))
check('second moment velocity',clock(2)[1]/clock(2)[0],F(3,5))
check('criteria distinct',uJ != clock(2),True)
for p,z in [(F(1,2),F(2)),(F(2),F(1,2))]:
    ue=clock(p)
    check('common receiver contraction '+str(p),om(ue,kp)/om(clock(1),kp),z)
    for s in [F(0),F(1,4),F(1)]:
        te=ue[0]*s; xe=-10+ue[1]*s; arrival=te-xe
        check('source left of receiver '+str((p,s)),xe<0,True)
        check('arrival map incidence '+str((p,s)),arrival,10+z*s)
        check('future null interval '+str((p,s)),dot((arrival-te,-xe,F(0),F(0)),(arrival-te,-xe,F(0),F(0))),F(0))
check('unit source aggregate rate',1/F(2)+1/F(1,2),F(5,2))
check('changed source aggregate rate',3/F(2)+1/F(1,2),F(7,2))
check('geometry does not select aggregate count rate',F(5,2)!=F(7,2),True)
source1=[F(1,8),F(1,4)]; source2=[F(1,2),F(1)]
record=Counter(10+2*s for s in source1)+Counter(10+s/2 for s in source2)
check('labelled coincident multiplicities',record,Counter({F(41,4):2,F(21,2):2}))
window_count=sum(v for t,v in record.items() if F(10)<t<=F(21,2))
preimage_count=sum(F(10)<10+2*s<=F(21,2) for s in source1)+sum(F(10)<10+s/2<=F(21,2) for s in source2)
check('discrete preimage counts',window_count,preimage_count)
check('collapsing timestamps changes record',sum(record.values())!=len(record),True)
print(json.dumps({'status':'PASS','arithmetic':'fractions.Fraction, exact','python':sys.version,'platform':platform.platform(),'check_count':len(checks),'checks':checks,'controls':{'endpoint_Z_values':['1/3','1/2','1','2','3'],'spectral_population_new_u_M':['5/4','3/4','0','0'],'aggregate_rates':['5/2','7/2'],'discrete_total':window_count}},indent=2))
