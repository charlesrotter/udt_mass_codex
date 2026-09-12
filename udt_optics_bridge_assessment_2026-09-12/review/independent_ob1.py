#!/usr/bin/env python3
"""OB1 review: metric quadratic roots, inertial arrival, rational-circle algebra.

No author scientific imports. Exact arithmetic only; finite anchors support the
analytical argument in SOURCE_FIRST_RECONSTRUCTION and REVIEW, not class sampling.
"""
import datetime
from fractions import Fraction as Q
import itertools
import json
import platform
import sympy as s

if not __debug__:
    raise RuntimeError('Assertions must be enabled')
checks=[]
catches=[]
def equal(name,a,b):
    r=s.simplify(a-b)
    if r != 0:
        raise AssertionError((name,a,b,r))
    checks.append(name)
def truth(name,value):
    if not value:
        raise AssertionError(name)
    checks.append(name)
def catch(name,fn):
    try:
        fn()
    except AssertionError:
        catches.append(name)
    else:
        raise AssertionError('Mutant survived: '+name)
def mod1(q): return q % 1
def circle(q):
    r=mod1(q)
    return min(r,1-r)

# Full-metric pullback, followed by independent quadratic solving on each edge.
x,y,z,u,r=s.symbols('x y z u r',real=True)
n=2+x/4
M=s.Matrix([[4,1,0],[1,9,2],[0,2,16]])
beta=s.Matrix([y/10,x*x/5+x/20,0])
theta=s.Matrix([1,*beta])
G=s.diag(0,0,0,0)
G[1:,1:]=n*n*M
G-=n*n*theta*theta.T
equal('rest SPD first minor',M[:1,:1].det(),4)
equal('rest SPD second minor',M[:2,:2].det(),35)
equal('rest SPD determinant',M.det(),544)
# On 0<=x,y<=1, Gershgorin gives lambda_min(M)>=3 and |beta|^2<=29/400<3.
truth('coordinate-slice sufficient strict margin',Q(29,400)<3)
vertices=[s.Matrix([0,0,0]),s.Matrix([1,0,0]),s.Matrix([1,1,0]),s.Matrix([0,1,0])]
def traverse(order):
    total=0
    roots=[]
    for j in range(4):
        a=order[j]; v=order[(j+1)%4]-a; p=a+u*v
        metric=G.subs(dict(zip([x,y,z],p)))
        tangent=s.Matrix([r,*v])
        poly=(tangent.T*metric*tangent)[0]
        sol=s.solve(poly,r)
        b=(beta.subs(dict(zip([x,y,z],p))).dot(v))
        future=[q for q in sol if (q+b).subs(u,Q(1,2))>0]
        truth('unique future root '+str(len(checks)),len(future)==1)
        root=future[0]
        equal('original null polynomial '+str(len(checks)),poly.subs(r,root),0)
        truth('positive coordinate root '+str(len(checks)),min(root.subs(u,0),root.subs(u,1))>0)
        total+=s.integrate(root,(u,0,1))
        roots.append(str(root))
    return s.simplify(total),roots
xp,roots_plus=traverse(vertices)
xm,roots_minus=traverse([vertices[0],vertices[3],vertices[2],vertices[1]])
equal('direct plus coordinate duration',xp,s.Rational(197,20))
equal('direct minus coordinate duration',xm,s.Rational(203,20))
detector_n=n.subs({x:0,y:0})
delay=detector_n*(xp-xm)
equal('nonconstant-lapse proper delay',delay,-s.Rational(3,5))
# Independent area integral: Stokes integrand d beta = ((2x/5+1/20)-1/10) dx dy.
area=s.integrate(s.diff(beta[1],x)-s.diff(beta[0],y),(x,0,1),(y,0,1))
equal('area circulation',area,s.Rational(3,20))
equal('line-root versus area route',delay,-2*detector_n*area)
catch('reversed delay sign',lambda:equal('bad sign',2*detector_n*area,delay))
catch('omitted detector clock',lambda:equal('bad clock',xp-xm,delay))

# Extract raw Gram records from the full metric at a marked rational event.
event={x:s.Rational(1,3),y:s.Rational(2,5),z:0}
g=G.subs(event); dirs=[s.eye(3)[:,i] for i in range(3)]
dirs += [dirs[0]+dirs[1],dirs[0]+dirs[2],dirs[1]+dirs[2]]
records=[]
for v in dirs:
    J=s.zeros(4,2);J[0,0]=1;J[1:,1]=v
    h=J.T*g*J
    T=s.sqrt(-h[0,0]);m=s.sqrt(-h.det());B=-h[0,1]/(T*T*m)
    records.append((T,m,s.simplify(B)))
q=[s.simplify((m/T)**2) for T,m,B in records]
brebuilt=s.Matrix([s.simplify(m*B) for T,m,B in records[:3]])
grebuilt=s.diag(*q[:3])
for k,(i,j) in enumerate([(0,1),(0,2),(1,2)]):
    grebuilt[i,j]=grebuilt[j,i]=(q[k+3]-q[i]-q[j])/2
for i in range(3):
    equal('raw record beta '+str(i),brebuilt[i],beta[i].subs(event))
    for j in range(3):
        equal('raw record gamma '+str(i)+str(j),grebuilt[i,j],(n*n*M)[i,j].subs(event))
catch('normalized shift without density',lambda:equal('bad density',records[1][2],brebuilt[1]))

# A full normalized-record omission witness on a half-unit square, from source G405.
normalized=[];omission_delays=[]
for lam in [s.Integer(1),s.Integer(2)]:
    bet=s.Matrix([0,lam*x,0]);th=s.Matrix([1,*bet])
    gl=s.diag(0,lam*lam,lam*lam,lam*lam)-th*th.T
    allH=[]
    for v in dirs:
        J=s.zeros(4,2);J[0,0]=1;J[1:,1]=v
        h=J.T*gl*J;m=s.sqrt(-h.det())
        normalizer=s.diag(1,1/m)
        allH.append(s.simplify(normalizer.T*h*normalizer))
    normalized.append(allH)
    omission_delays.append(-2*s.integrate(s.diff(bet[1],x),(x,0,s.Rational(1,2)),(y,0,s.Rational(1,2))))
for j in range(6):
    for i in range(2):
        for k in range(2):equal('density omission H'+str((j,i,k)),normalized[0][j][i,k],normalized[1][j][i,k])
equal('density omission delay1',omission_delays[0],-s.Rational(1,2))
equal('density omission delay2',omission_delays[1],-1)

# Alternate sign/factor anchor: intercept two constrained light beams in inertial flat cylinder.
R=s.Integer(2);Omega=s.Rational(1,10)
inertial_plus=2*s.pi/(1/R-Omega)
inertial_minus=2*s.pi/(1/R+Omega)
J=s.Matrix([[1,0],[Omega,1]]) # inertial (t,Theta) versus rotating (t,theta)
rotating=J.T*s.diag(-1,R*R)*J
NR=s.sqrt(-rotating[0,0]); beta_theta=rotating[0,1]/rotating[0,0]
inertial_delay=s.simplify(NR*(inertial_plus-inertial_minus))
metric_delay=s.simplify(-2*NR*2*s.pi*beta_theta)
equal('inertial arrival versus threading delay',inertial_delay,metric_delay)
equal('rotating explicit signed value',inertial_delay,2*s.sqrt(6)*s.pi/3)
truth('co-rotating beam arrives later',inertial_delay>0)
catch('clock inverse mutant',lambda:equal('bad clock inverse',(inertial_plus-inertial_minus)/NR,metric_delay))

# Common-detection phase, with candidate's positive input phasor and minus/plus order.
omega,tau,Tp,Tm,bp,bm=s.symbols('omega tau Tp Tm bp bm',real=True)
phasep=omega*(tau-Tp)+bp;phasem=omega*(tau-Tm)+bm
equal('common-event comparator sign',phasem-phasep,omega*(Tp-Tm)+bm-bp)
catch('comparator order mutant',lambda:equal('bad phase order',phasep-phasem,omega*(Tp-Tm)+bm-bp))

# Exact phase turns on R/Z: no floating phase extraction or author phasor formula.
f0=Q(7,3);step=Q(11,5);D=Q(13,17);b=Q(-5,19)
freq=[f0+j*step for j in range(3)]
obs=[mod1(f*D+b) for f in freq]
equal('wrapped heldout exact',mod1(2*obs[1]-obs[0]),obs[2])
for k in range(-4,5):
    dk=D+k/step;bk=b-f0*k/step
    for j in range(3):equal('compensated alias '+str((k,j)),mod1(freq[j]*dk+bk),obs[j])
catch('absolute delay identification mutant',lambda:truth('false unique D',D==D+1/step))
catch('third frequency simply repeated mutant',lambda:equal('bad third prediction',obs[1],obs[2]))
for extra in [Q(1,8),Q(1,2)]:
    altered=[mod1(obs[j]+extra*j*j) for j in range(3)]
    closure=mod1(altered[2]+altered[0]-2*altered[1])
    equal('quadratic circular closure '+str(extra),closure,mod1(2*extra))
equal('known geometry first residual',mod1(obs[1]-obs[0]-step*D),0)
equal('known geometry second residual',mod1(obs[2]-obs[0]-2*step*D),0)
for transfer in [Q(0),Q(2,7),Q(-3,11)]:
    physical=D-transfer;total=physical+transfer
    equal('instrument delay confounding '+str(transfer),total,D)

# Error budgets are checked in phase turns and cycles/s, consistently divided by 2pi.
ub=[Q(1,100),Q(1,80),Q(1,60)];vb=[Q(1,900),Q(1,800),Q(1,700)]
Dmax=Q(5,4);weights=[1,-2,1]
bound=sum(abs(w)*(ui+Dmax*vi) for w,ui,vi in zip(weights,ub,vb))
max_seen=Q(0)
for signs in itertools.product([-1,1],repeat=6):
    for delay_sign in [-1,1]:
        e=[ub[j]*signs[j] for j in range(3)]
        eta=[vb[j]*signs[j+3] for j in range(3)]
        residual=sum(weights[j]*(e[j]+delay_sign*Dmax*eta[j]) for j in range(3))
        dist=circle(residual)
        truth('closure error box corner '+str(len(checks)),dist<=bound)
        max_seen=max(max_seen,dist)
equal('closure error bound attained',max_seen,bound)
catch('training error omitted',lambda:truth('bad training bound',max_seen<=ub[2]+Dmax*vb[2]))
catch('frequency error omitted',lambda:truth('bad frequency bound',max_seen<=sum(abs(w)*ui for w,ui in zip(weights,ub))))
D0=Q(3,4);ud=Q(1,9)
geometry_max={}
for j in [1,2]:
    Bj=ub[j]+ub[0]+j*step*ud+(abs(D0)+ud)*(vb[j]+vb[0])
    maxj=Q(0)
    for signs in itertools.product([-1,1],repeat=5):
        du=ud*signs[0];eta0=vb[0]*signs[1];etaj=vb[j]*signs[2]
        e0=ub[0]*signs[3];ej=ub[j]*signs[4]
        residual=j*step*du+(D0+du)*(etaj-eta0)+ej-e0
        dist=circle(residual)
        truth('geometry error corner '+str((j,len(checks))),dist<=min(Q(1,2),Bj))
        maxj=max(maxj,dist)
    geometry_max[str(j)]={'bound_turns':str(Bj),'max_corner_distance_turns':str(maxj)}
aliasD=Q(1000000);tiny_error=1/(2*aliasD)
equal('unbounded-alias frequency-error counterexample',circle(aliasD*tiny_error),Q(1,2))
truth('counterexample frequency error is small',tiny_error<Q(1,1000000))

print(json.dumps({'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'python':platform.python_version(),'sympy':s.__version__,'arithmetic':'exact symbolic and rational phase turns',
 'scientific_imports':'sympy and standard library only; no author or source scientific code imports',
 'check_count':len(checks),'mutation_catches':catches,'checks':checks,
 'anchors':{'nonconstant_lapse_roots_plus':roots_plus,'nonconstant_lapse_roots_minus':roots_minus,
 'coordinate_plus':str(xp),'coordinate_minus':str(xm),'detector_lapse':str(detector_n),
 'proper_delay':str(delay),'circulation':str(area),'rotating_inertial_proper_delay':str(inertial_delay),
 'density_omission_delays':list(map(str,omission_delays)),'phase_turns':list(map(str,obs)),
 'closure_bound_turns':str(bound),'closure_max_corner_turns':str(max_seen),
 'geometry_error_corners':geometry_max,'alias_counterexample_frequency_error':str(tiny_error)},
 'verdict':'PASS'},indent=2))
