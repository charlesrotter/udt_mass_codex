"""Independent exact controls. All examples freely supplied; no physical fit."""
from fractions import Fraction as F
import json
import platform
import sys

checks = []
wrong = []

def check(label, condition):
    if not condition:
        raise AssertionError(label)
    checks.append(label)

def reject(label, condition):
    if condition:
        raise AssertionError('wrong identity survived: ' + label)
    wrong.append(label)

def dot(a, b):
    return -a[0]*b[0] + sum(x*y for x,y in zip(a[1:],b[1:]))

def scale(a, x):
    return tuple(x*q for q in a)

def omega(u, k):
    return -dot(u, k)

def moment(rays, weights):
    lower = [(-k[0],)+k[1:] for k in rays]
    return [[sum(w*k[i]*k[j] for k,w in zip(lower,weights))
             for j in range(4)] for i in range(4)]

def mixed_apply(M, u):
    out = [sum(M[i][j]*u[j] for j in range(4)) for i in range(4)]
    out[0] = -out[0]
    return tuple(out)

k = (F(1), F(1), F(0), F(0))
km = (F(1), F(-1), F(0), F(0))
ue = (F(1), F(0), F(0), F(0))
uo = (F(5,4), F(3,4), F(0), F(0))
aux = (F(13,5), F(12,5), F(0), F(0))
check('future null ray', dot(k,k)==0 and k[0]>0)
for name,u in [('source',ue),('receiver',uo),('auxiliary',aux)]:
    check(name+' future proper clock',dot(u,u)==-1 and u[0]>0)
Z = omega(ue,k)/omega(uo,k)
check('endpoint ratio equals two',Z==2)
# Direct flat ray x=t-s; receiver t=gamma*r, x=L+gamma*v*r.
L=F(3)
arrival = lambda s: (L+s)/(uo[0]-uo[1])
for s in [F(0),F(2,7),F(2)]:
    r=arrival(s)
    check('flat null incidence '+str(s),L+uo[1]*r==uo[0]*r-s)
check('incidence-derived finite interval ratio',
      (arrival(F(2))-arrival(F(0)))/2==Z)
for a in [F(1,9),F(7),F(11,3)]:
    check('affine normalization '+str(a),omega(ue,scale(k,a))/omega(uo,scale(k,a))==Z)
reject('independent endpoint rescaling is one affine ray',
       omega(ue,scale(k,F(2)))/omega(uo,scale(k,F(3)))==Z)
left=omega(ue,k)/omega(aux,k)
right=omega(aux,k)/omega(uo,k)
check('auxiliary cancellation',left*right==Z and left==5 and right==F(2,5))
reject('auxiliary factor equals whole comparison',left==Z)
uo_reverse=(uo[0],-uo[1],F(0),F(0))
check('actual endpoint change changes ratio',omega(ue,k)/omega(uo_reverse,k)==F(1,2))
# Analytic family u_q=((q+q^-1)/2,(q-q^-1)/2,0,0), q>=1:
# proper norm -1, one-ray objective 1/q^2 -> 0 but never zero at finite q.
previous=None
for q in [F(1),F(2),F(5),F(20)]:
    u=((q+1/q)/2,(q-1/q)/2,F(0),F(0))
    Q=omega(u,k)**2
    check('beam hyperbola '+str(q),dot(u,u)==-1 and Q==1/q**2 and Q>0)
    if previous is not None: check('beam descent '+str(q),Q<previous)
    previous=Q
# Discrete pushforward uses no density. F(s)=s+s^3 increasing on R.
arrival2=lambda s:s+s**3
derivative=lambda s:1+3*s*s
atoms=[(F(0),F(1)),(F(1),F(2)),(F(2),F(1))]
received=[(arrival2(s),w) for s,w in atoms]
check('atomic times and multiplicities',received==[(F(0),F(1)),(F(2),F(2)),(F(10),F(1))])
source_count=sum(w for s,w in atoms if 0<=s<2)
received_count=sum(w for t,w in received if 0<=t<10)
check('half-open finite count conservation',source_count==received_count==3)
check('finite interval integral',arrival2(F(2))-arrival2(F(0))==10)
reject('initial instantaneous Z times finite interval',derivative(F(0))*2==10)
reject('midpoint instantaneous Z times finite interval',derivative(F(1))*2==10)
check('finite discrete spacings differ',received[1][0]-received[0][0]==2 and received[2][0]-received[1][0]==8)
check('conditional density change of variable',F(3)/derivative(F(1))==F(3,4))
shifted=lambda s:arrival2(s)+5
check('arrival origin affects fixed-window counts despite same derivative',
      sum(w for s,w in atoms if 0<=shifted(s)<10)==3 and
      sum(w for s,w in atoms if 0<=arrival2(s)<4)==3 and
      sum(w for s,w in atoms if 0<=shifted(s)<4)==0)
# Two constant-rate channels with Z=(2,1/2), common receiver proper time.
def total(rates): return rates[0]/F(2)+rates[1]/F(1,2)
check('specified channels give total',total((F(2),F(1)))==3)
check('same geometry different source rates different total',total((F(4),F(1)))==4)
check('same total does not recover channel source rates',total((F(4),F(1,2)))==3)
reject('ratios alone fix total',total((F(2),F(1)))==total((F(4),F(1))))
# Compare full-vector measures with equal atomic weights. Squared null
# components give a distinct implementation from closed rapidity formulas.
M0=moment([k,km],[F(1),F(1)])
check('balanced moment has source-clock eigenvector',mixed_apply(M0,ue)==scale(ue,F(-2)))
M1=moment([scale(k,F(9)),scale(km,F(4))],[F(1),F(1)])
# sqrt(A/B)=9/4; rational unit minimizer u=(13/12,5/12,0,0).
uM=(F(13,12),F(5,12),F(0),F(0))
check('rescaled-population observer proper norm',dot(uM,uM)==-1)
check('rescaled-population moment eigen equation',mixed_apply(M1,uM)==scale(uM,F(-72)))
reject('direction-dependent spectral changes preserve rest observer',mixed_apply(M1,ue)==scale(ue,-M1[0][0]))
M2=moment([scale(k,F(63)),scale(km,F(28))],[F(1),F(1)])
check('global spectral normalization scales moment',M2==[[49*x for x in row] for row in M1])
check('global spectral normalization preserves observer',mixed_apply(M2,uM)==scale(uM,F(-3528)))
check('population change preserves geometric endpoint ratios',
      omega(ue,scale(k,F(9)))/omega(uo,scale(k,F(9)))==Z)
print(json.dumps({'verdict':'PASS','exact_checks':len(checks),'rejected_wrong_identities':len(wrong),
                  'checks':checks,'wrong_identities':wrong,'python':sys.version,
                  'implementation':platform.python_implementation(),
                  'method':'stdlib Fraction; no producer code or outputs'},indent=2))
