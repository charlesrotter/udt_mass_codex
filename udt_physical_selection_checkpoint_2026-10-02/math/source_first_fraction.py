"""Independent stdlib metric-series calculation from original spatial E_f.

No trace ODE, symbolic library, parent code or generated coefficients are loaded.
"""
from fractions import Fraction as Q
import json, platform

N = 12
def const(x):return [Q(x)]+[Q(0)]*N
def add(a,b):return [x+y for x,y in zip(a,b)]
def scale(a,c):return [Q(c)*x for x in a]
def mul(a,b):return [sum((a[j]*b[k-j] for j in range(k+1)),Q(0)) for k in range(N+1)]
def inv(a):
    v=const(1/a[0])
    for k in range(1,N+1):v[k]=-sum((a[j]*v[k-j] for j in range(1,k+1)),Q(0))/a[0]
    return v
def derivative(a):return [(k+1)*a[k+1] for k in range(N)]+[Q(0)]
def integrate(a):return [Q(0)]+[a[k-1]/k for k in range(1,N+1)]
def compose(a,b):
    out=const(0)
    for c in a[::-1]:out=add(mul(out,b),const(c))
    return out
def log_one(a):
    x=add(a,const(-1)); power=const(1);out=const(0)
    for k in range(1,N+1):
        power=mul(power,x);out=add(out,scale(power,Q((-1)**(k+1),k)))
    return out

# FREE comparison coefficients in declared formal units, never physical calibration.
alpha,beta,P0=Q(2),Q(1,3),Q(3,5)
def original_components(a):
    adot=derivative(a);addot=derivative(adot);ai=inv(a)
    H=mul(adot,ai); acc=mul(addot,ai);H2=mul(H,H)
    R=scale(add(acc,H2),6)
    R2=mul(R,R);R3=mul(R2,R)
    f=add(add(R,scale(R2,alpha)),scale(R3,beta))
    F=add(add(const(1),scale(R,2*alpha)),scale(R2,3*beta))
    Fdot=derivative(F);Fddot=derivative(Fdot)
    # Ric00=-3 a''/a and Ricii/a²=a''/a+2(a'/a)².
    C=add(add(scale(mul(F,acc),-3),scale(f,Q(1,2))),scale(mul(H,Fdot),3))
    D=add(add(mul(F,add(acc,scale(H2,2))),scale(f,Q(-1,2))),
          add(scale(Fddot,-1),scale(mul(H,Fdot),-2)))
    return C,D,R

a=const(1);a[3]=P0/36
recurrence=[]
for n in range(4,N+1):
    a[n]=Q(0);e0=original_components(a)[1][n-4]
    a[n]=Q(1);e1=original_components(a)[1][n-4]
    slope=e1-e0
    assert slope != 0
    a[n]=-e0/slope
    assert original_components(a)[1][n-4] == 0
    recurrence.append({'degree':n,'slope':str(slope),'coefficient':str(a[n])})
C,D,R=original_components(a)
assert all(v==0 for v in C[:N-2]), C[:N-2]
assert all(v==0 for v in D[:N-3]), D[:N-3]
assert R[0] == 0 and R[1] == P0
eta=integrate(inv(a));arrival=const(0)
for n in range(1,N+1):
    target=Q(1) if n==1 else Q(0)
    arrival[n]=target-compose(eta,arrival)[n]
identity=const(0);identity[1]=Q(1)
assert compose(eta,arrival)==identity
logp=log_one(compose(a,arrival))
logq=[(2**n-1)*v for n,v in enumerate(logp)]
expected={3:P0/36,4:-beta*P0**2/(48*alpha),
          5:-P0/(4320*alpha)+3*beta**2*P0**3/(80*alpha**2)}
for n,v in expected.items():assert logp[n]==v,(n,logp[n],v)
alpha_clock=-logp[3]/(120*(logp[5]-Q(12,5)*logp[4]**2/logp[3]))
beta_clock=-alpha_clock*logp[4]/(27*logp[3]**2)
assert (alpha_clock,beta_clock)==(alpha,beta)

# Catch the omitted quartic and the uncorrected R² fifth-order law.
mutant4=a[:];mutant4[4]=Q(0)
mutant5=a[:];mutant5[5]=-P0/(4320*alpha)
bad4=original_components(mutant4)[1][0]
bad5=original_components(mutant5)[1][1]
assert bad4 != 0 and bad5 != 0
print(json.dumps({'python':platform.python_version(),'library':'stdlib Fraction only',
    'N':N,'alpha':str(alpha),'beta':str(beta),'P0':str(P0),
    'recurrence_from_original_spatial_E':recurrence,
    'original00_supported_zero_coefficients':[str(v) for v in C[:N-2]],
    'original_spatial_supported_zero_coefficients':[str(v) for v in D[:N-3]],
    'a_coefficients':[str(v) for v in a],
    'logp_coefficients':[str(v) for v in logp],
    'logq_coefficients':[str(v) for v in logq],
    'recovered_alpha':str(alpha_clock),'recovered_beta':str(beta_clock),
    'incorrect_R2_only_alpha':str(-logp[3]/(120*logp[5])),
    'catch_omitted_quartic_original_D0':str(bad4),
    'catch_R2_only_quintic_original_D1':str(bad5),
    'scope':'Finite formal jet, not global convergence or observational evidence'},indent=2))
