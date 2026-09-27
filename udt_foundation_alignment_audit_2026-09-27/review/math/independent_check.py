#!/usr/bin/env python3
"""Independent exact-arithmetic source-fidelity checks; no production imports.

Domain: positive supplied clock/ruler factors and regular Minkowski null query
controls. These checks verify algebra, not premise adoption or physical laws.
"""
from fractions import Fraction as F
from itertools import product
import json
import platform
import sys

counts = {}

def check(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1

def mm(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def trans(a):
    return list(map(list,zip(*a)))

def det2(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]

def diag(*xs):
    return [[x if i==j else F(0) for j in range(len(xs))] for i,x in enumerate(xs)]

eta2=diag(F(-1),F(1))
K=[[F(0),F(1)],[F(1),F(0)]]
for u in [F(2,3),F(3,2),F(7,5)]:
    D=diag(u,1/u)
    check('duality',mm(mm(trans(D),K),D)==K)
    check('duality',mm(mm(trans(D),eta2),D)!=eta2)
    ordinary=diag(u,u)
    check('conversion_countercase',mm(mm(trans(ordinary),K),ordinary)!=K)

for T,L,beta in product([F(2,3),F(3,2),F(7,5)],
                         [F(4,5),F(5,4),F(9,7)],
                         [F(-2,3),F(0),F(5,7)]):
    h=[[-T*T,-T*T*beta],[-T*T*beta,L*L-T*T*beta*beta]]
    check('pair_decomposition',h[0][0]<0 and det2(h)<0)
    check('pair_decomposition',h[1][1]-h[0][1]**2/h[0][0]==L*L)
    check('pair_decomposition',-det2(h)==T*T*L*L)
    m=T*L
    J=diag(F(1),1/m)
    hn=mm(mm(trans(J),h),J)
    check('W1_normalization',det2(hn)==-1)
    check('W1_normalization',hn[0][1]/hn[0][0]==beta/m)
    check('W1_normalization',hn[1][1]-hn[0][1]**2/hn[0][0]==1/(T*T))
    omega=F(11,6)
    check('rescaling_type_separation',(omega*T)/(omega*L)==T/L)
    renormalized_q=(omega*T)**2
    check('rescaling_type_separation',renormalized_q==omega**2*T**2 and renormalized_q!=T*T)

for a,b,c in product([F(2,5),F(7,4),F(9,2)],repeat=3):
    qab=b/a; qbc=c/b; qac=c/a
    xa=(1-qab)/(1+qab); xb=(1-qbc)/(1+qbc)
    check('matched_endpoint_composition',qab*qbc==qac)
    check('matched_endpoint_composition',(xa+xb)/(1+xa*xb)==(1-qac)/(1+qac))
    check('matched_endpoint_composition',(1-1/qab)/(1+1/qab)==-xa)
check('unmatched_middle_failure',(F(2)/F(1))*(F(3)/F(4))!=F(3)/F(1))

# Generate unit future timelike clocks independently of the identity being tested.
# Rational stereographic parametrization of the unit hyperboloid.
transverse_cases=0
for p,v in product([F(-1,2),F(-1,4),F(0),F(1,4),F(1,2)],repeat=2):
    s=p*p+v*v
    gamma=(1+s)/(1-s)
    a=2*p/(1-s)
    w=2*v/(1-s)
    check('null_transport_interlock',-gamma*gamma+a*a+w*w==-1)
    omega_a=F(1)
    omega_b=gamma-a  # contraction of (1,1,0) with the generated target clock
    r=omega_a/omega_b
    check('null_transport_interlock',omega_b>0)
    check('null_transport_interlock',gamma==(r+1/r)/2+r*w*w/2)
    M=1/gamma
    sech=2/(r+1/r)
    check('null_transport_interlock',0<M<=sech)
    check('null_transport_interlock',(M==sech)==(w==0))
    transverse_cases += (w!=0)

# Same directional ratio, different transported clock scalar, direct exact witness.
U0=[F(5,4),F(3,4),F(0)]
U1=[F(9,4),F(7,4),F(1)]
for U in [U0,U1]:
    check('fixed_ratio_separator',-U[0]**2+U[1]**2+U[2]**2==-1)
    check('fixed_ratio_separator',U[0]-U[1]==F(1,2))
check('fixed_ratio_separator',1/U0[0]==F(4,5) and 1/U1[0]==F(4,9))

# Projecting one future clock column drops the spatial-frame rotation.
eta3=diag(F(-1),F(1),F(1))
I=diag(F(1),F(1),F(1))
R=[[F(1),F(0),F(0)],[F(0),F(0),F(-1)],[F(0),F(1),F(0)]]
B=[[F(5,4),F(3,4),F(0)],[F(3,4),F(5,4),F(0)],[F(0),F(0),F(1)]]
for A in [I,R,B]:
    check('projective_frame_carry',mm(mm(trans(A),eta3),A)==eta3)
def project(A):
    return (A[1][0]/A[0][0],A[2][0]/A[0][0])
check('projective_frame_carry',project(I)==project(R))
check('projective_frame_carry',project(mm(I,B))!=project(mm(R,B)))

# Static null speed and conserved-frequency readout use distinct ratios.
for N in [F(1,3),F(5,4),F(7,2)]:
    c=F(17,3); dr=F(2,7)
    dt=dr/(c*N*N)
    check('static_local_null_speed',(dr/N)/(N*dt)==c)
Ns,No,E=F(2,3),F(5,4),F(7,9)
check('redshift_attachment',(E/Ns)/(E/No)==No/Ns)
check('redshift_attachment',(No/Ns)**2 != No/Ns)

result={
    'status':'PASS',
    'python':sys.version,
    'platform':platform.platform(),
    'implementation':'standard-library fractions; no scientific-source-code imports',
    'evidence_type':'exact arithmetic witnesses and finite regression; analytic general arguments in SOURCE_FIRST.md',
    'checks':counts,
    'total_assertions':sum(counts.values()),
    'transverse_generated_cases':transverse_cases,
    'parameters':{'pair_cases':27,'endpoint_triples':27,'unit_clock_cases':25,'dtype':'exact Fraction','device':'CPU','grid':'none'},
    'failure_cases_preserved':['ordinary same-side conversion does not preserve K',
      'reciprocal D is not a Lorentz isometry in the physical diagonal basis',
      'unmatched middle endpoint does not telescope',
      'fixed frequency ratio does not fix M_PT',
      'projected clock vector alone does not compose nonradial frame morphisms',
      'auxiliary conformal ratio invariance does not survive W1 renormalization as the same scalar']
}
print(json.dumps(result,indent=2))
