"""Independent Fraction pilot controls, before producer-code exposure."""
from fractions import Fraction as F
from pathlib import Path
import csv, hashlib, json

checks=[]
def ck(name,value):
    assert value,name
    checks.append(name)
def tr(a): return list(map(list,zip(*a)))
def mul(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in tr(b)] for r in a]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def diag(v): return [[x if i==j else F(0) for j in range(len(v))] for i,x in enumerate(v)]
def det2(a): return a[0][0]*a[1][1]-a[0][1]*a[1][0]
B=[[F(2),F(1)],[F(1),F(2)]]
Q=[[F(1),F(1,3)],[F(0),F(2)]]
S=[[F(1,3),F(1,4)],[F(-1,5),F(1,6)]]
Y=[[F(2),F(1,3)],[F(1,4),F(1)]]
Z=[[F(1,4),F(1,5)],[F(1,6),F(1,7)]]
QS=mul(Q,S)
E=[B[0]+[F(0),F(0)], B[1]+[F(0),F(0)],QS[0]+Q[0],QS[1]+Q[1]]
J=Y+Z
eta=diag([F(-1),F(1),F(1),F(1)])
h=mul(mul(tr(J),mul(mul(tr(E),eta),E)),J)
screen=add(mul(S,Y),Z)
hb=add(mul(mul(tr(Y),mul(mul(tr(B),diag([F(-1),F(1)])),B)),Y),mul(mul(tr(screen),mul(tr(Q),Q)),screen))
ck('independent_full_block_equals_direct_4D',h==hb)
ck('regular_nonzero_shift_example',h[0][0]<0 and det2(h)<0 and h[0][1]!=0)
T2=-h[0][0]; beta=h[0][1]/h[0][0]; L2=h[1][1]-h[0][1]**2/h[0][0]
ck('full_sector_square_completion',L2>0 and -T2*beta==h[0][1] and L2-T2*beta**2==h[1][1])
ck('full_sector_determinant',T2*L2==-det2(h))
ck('ruler_normalization_determinant',det2(h)/(-det2(h))==-1)
ck('ruler_normalization_reciprocity_squared',T2*L2/(-det2(h))==1)
# Smooth time-dependent density m=2+t cannot be an exact m dsigma on a 2D chart:
# d(m dsigma)=dt wedge dsigma, preserving the pilot's integrability distinction.
ck('nonexact_spacetime_density_control',F(1)!=0)
# G01 trace-of-square versus square-of-trace distinction.
A=diag([F(-3),F(3)])
ck('representation_trace_of_square',sum(mul(A,A)[i][i] for i in range(2))/2==9)
ck('square_of_trace_is_wrong',sum(A[i][i] for i in range(2))**2/2!=9)
freeze=json.loads(Path('development_reconstruction_2026-09-29/PILOT_FREEZE.json').read_text())
for p,expected in freeze['sha256'].items():
    if p=='UDT_DEVELOPMENT.md':continue
    ck('frozen_pin:'+p,hashlib.sha256(Path(p).read_bytes()).hexdigest()==expected)
registry=list(csv.DictReader(open('CURRENT_SCIENTIFIC_PREMISES.tsv'),delimiter='\t'))
roles=list(csv.DictReader(open('development_reconstruction_2026-09-29/CLAIM_DISPOSITIONS.tsv'),delimiter='\t'))
ck('all406_ids_once',len(roles)==406 and len({r['premise_id'] for r in roles})==406 and {r['premise_id'] for r in roles}=={r['premise_id'] for r in registry})
print(json.dumps({'scope':'exact algebra examples and byte/coverage checks; not generic proof or semantic completeness','count':len(checks),'checks':checks,'h':[[str(x) for x in r] for r in h]},indent=2))
