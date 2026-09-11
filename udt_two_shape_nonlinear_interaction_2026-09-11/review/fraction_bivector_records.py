#!/usr/bin/env python3
"""Post-exposure independent rational Gauss/Codazzi, frame and record checks.

Python fractions only: no SymPy or author/scientific imports. This is finite
exact arithmetic, not an independent proof of general CK or all-jet identities.
"""
from fractions import Fraction as F
from itertools import product, permutations
import json
import platform

RANGE=range(4)
I3=range(3)
keys=list(product(RANGE,repeat=4))
checks=[]
controls=[]
def eq(name,a,b):
    if a!=b: raise AssertionError((name,a,b))
    checks.append(name)
def neq(name,a,b):
    if a==b: raise AssertionError(('false pass',name,a))
    controls.append({'name':name,'difference':str(a-b)})
def eps4(a,b,c,d):
    arr=[a,b,c,d]
    if len(set(arr))!=4:return 0
    return (-1)**sum(arr[i]>arr[j] for i in RANGE for j in range(i+1,4))
def datum(p,r,px,rx,s):
    k=(p*p+r*r-s*s)/(2*s)
    K=[[k,F(0),F(0)],[F(0),s-p,-r],[F(0),-r,s+p]]
    Kx=[[(p*px+r*rx)/s,F(0),F(0)],[F(0),-px,-rx],[F(0),-rx,px]]
    return K,Kx
def tensor(K,Kx):
    # Spatial Gauss tensor, then spatial Ricci contraction determines electric
    # entries through Ric4_ij=0. Codazzi supplies mixed components directly.
    spatial={(i,j,k,l):K[i][k]*K[j][l]-K[i][l]*K[j][k] for i,j,k,l in product(I3,repeat=4)}
    E=[[sum(spatial[k,i,k,j] for k in I3) for j in I3] for i in I3]
    pairs=list((a,b) for a in RANGE for b in range(a+1,4))
    raw={}
    for a,b in pairs:
        for c,d in pairs:
            if a==0 and c==0: value=E[b-1][d-1]
            elif a==0:
                value=(Kx[b-1][d-1] if c==1 else 0)-(Kx[b-1][c-1] if d==1 else 0)
            elif c==0:
                value=(Kx[d-1][b-1] if a==1 else 0)-(Kx[d-1][a-1] if b==1 else 0)
            else:value=spatial[a-1,b-1,c-1,d-1]
            raw[a,b,c,d]=value
    R={}
    for a,b,c,d in keys:
        if a==b or c==d:R[a,b,c,d]=F(0)
        else:R[a,b,c,d]=(-1 if a>b else 1)*(-1 if c>d else 1)*raw[min(a,b),max(a,b),min(c,d),max(c,d)]
    return R
def hodge(R,gdiag=(-1,1,1,1),volume=F(1)):
    inv=[1/F(x) for x in gdiag]
    return {(a,b,c,d):sum(F(eps4(a,b,e,f),2)*volume*inv[e]*inv[f]*R[e,f,c,d]
            for e,f in product(RANGE,repeat=2)) for a,b,c,d in keys}
def pseudoscalar(R,gdiag=(-1,1,1,1),volume=F(1)):
    star=hodge(R,gdiag,volume)
    return sum(R[a,b,c,d]*star[a,b,c,d]/F(gdiag[a]*gdiag[b]*gdiag[c]*gdiag[d]) for a,b,c,d in keys)
def transform(R,L):
    sparse=[[(b,L[a][b]) for b in RANGE if L[a][b]] for a in RANGE]
    return {(a,b,c,d):sum(x*y*z*w*R[i,j,k,l] for (i,x),(j,y),(k,z),(l,w)
        in product(sparse[a],sparse[b],sparse[c],sparse[d])) for a,b,c,d in keys}
def solve(matrix,rhs):
    rows=[list(map(F,row))+[F(y)] for row,y in zip(matrix,rhs)]
    n=len(rhs)
    for i in range(n):
        pivot=next(j for j in range(i,n) if rows[j][i])
        rows[i],rows[pivot]=rows[pivot],rows[i]
        val=rows[i][i]; rows[i]=[x/val for x in rows[i]]
        for j in range(n):
            if j!=i:
                val=rows[j][i]; rows[j]=[x-val*y for x,y in zip(rows[j],rows[i])]
    return [r[-1] for r in rows]
dirs=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
design=[[v[0]**2,v[1]**2,v[2]**2,2*v[0]*v[1],2*v[0]*v[2],2*v[1]*v[2]] for v in dirs]
def evaluate(M):return [sum(M[i][j]*v[i]*v[j] for i,j in product(I3,repeat=2)) for v in dirs]
def unpack(q):
    v=solve(design,q)
    return [[v[0],v[3],v[4]],[v[3],v[1],v[5]],[v[4],v[5],v[2]]]

p,r,px,rx,s=map(F,('1/8','1/12','-1/10','1/7','-2/3'))
K,Kx=datum(p,r,px,rx,s)
R=tensor(K,Kx); P=pseudoscalar(R)
eq('Gauss-Codazzi full contraction versus candidate rational value',P,-16*(p*rx-px*r)*(p*p+r*r-s*s)/s)
eq('all original Ricci entries from independent Gauss-Codazzi tensor',
   [[sum((-1 if a==0 else 1)*R[a,b,a,d] for a in RANGE) for d in RANGE] for b in RANGE],[[0]*4 for _ in RANGE])
eq('first-pair Hodge square at generic rational anchor',hodge(hodge(R)),{k:-v for k,v in R.items()})
for name,data in {'zero':(0,0,0,0,s),'p_only':(p,0,px,0,s),'r_only':(0,r,0,rx,s),
 'aligned':(p,2*p,px,2*px,s),'outside_box_cancellation':(s,0,0,s,s)}.items():
    eq(name+' exact P',pseudoscalar(tensor(*datum(*map(F,data)))),0)
# A genuine rational proper Lorentz boost changes the observer to (5/4,0,3/4,0).
boost=[[F(int(i==j)) for j in RANGE] for i in RANGE]
boost[0][0]=boost[2][2]=F(5,4);boost[0][2]=boost[2][0]=F(3,4)
Rb=transform(R,boost)
eq('proper boosted observer full pseudoscalar',pseudoscalar(Rb),P)
eq('boosted electric-magnetic contraction',sum(Rb[i,0,j,0]*hodge(Rb)[i,0,j,0] for i,j in product(range(1,4),repeat=2)),P/16)
neq('boost really changes an electric curvature component',Rb[1,0,1,0],R[1,0,1,0])
# Positive nonorthonormal coordinate rescaling: raising and volume density matter.
scales=[F(2),F(3),F(5),F(7)]
L=[[scales[i] if i==j else F(0) for j in RANGE] for i in RANGE]
Rs=transform(R,L);diag=[-4,9,25,49];volume=F(210)
eq('nonorthonormal coordinates with transformed metric and volume',pseudoscalar(Rs,diag,volume),P)
neq('omitting nonorthonormal volume density is detected',pseudoscalar(Rs,diag,F(1)),P)
reflection=[[F((-1 if i==2 else 1)*int(i==j)) for j in RANGE] for i in RANGE]
Rref=transform(R,reflection)
eq('orientation reversal with positive frame epsilon flips P',pseudoscalar(Rref),-P)
eq('transforming orientation along with reflected coordinates preserves scalar',pseudoscalar(Rref,volume=F(-1)),P)
neq('wrong overall P sign rejected at nonzero anchor',-P,P)
neq('wrong Hodge/contraction half factor rejected',P/2,P)
# q=m^2 jets are obtained from actual compatible initial gamma/K: six evaluations
# are inverted by rational elimination rather than hard-coded polarization formulas.
qd=[-2*q for q in evaluate(K)];qdx=[-2*q for q in evaluate(Kx)]
recK=[[-v/2 for v in row] for row in unpack(qd)]
recKx=[[-v/2 for v in row] for row in unpack(qdx)]
eq('six density time jets recover K by linear-system solve',recK,K)
eq('six common mixed X-time jets recover K_X by linear-system solve',recKx,Kx)
eq('record-only reconstructed curvature pseudoscalar',pseudoscalar(tensor(recK,recKx)),P)
neq('setting mixed X-time density jets to zero changes P',pseudoscalar(tensor(recK,[[F(0)]*3 for _ in I3])),P)
Ksign,Kxsign=datum(p,-r,px,-rx,s)
eq('axis time jets unchanged under offdiagonal sign control',evaluate(Ksign)[:3],evaluate(K)[:3])
eq('axis mixed jets unchanged under offdiagonal sign control',evaluate(Kxsign)[:3],evaluate(Kx)[:3])
eq('same axis records leave oriented P ambiguous',pseudoscalar(tensor(Ksign,Kxsign)),-P)
neq('retained mixed-direction jets resolve that ambiguity',evaluate(Ksign)[5],evaluate(K)[5])
neq('homogeneous completion changes exact P',pseudoscalar(tensor(*datum(p,r,px,rx,F(-7,12)))),P)
bad=[row[:] for row in K];bad[0][0]=-s/2
badH=sum(bad[i][i] for i in I3)**2-sum(bad[i][j]*bad[j][i] for i,j in product(I3,repeat=2))
eq('omitted quadratic completion has original nonzero Hamiltonian',badH,-2*(p*p+r*r))
neq('invalid completion is rejected',badH,F(0))
print(json.dumps({'status':'PASS','python':platform.python_version(),'library':'Python standard fractions only',
 'anchor':dict(zip(('p','r','p_X','r_X','s'),map(str,(p,r,px,rx,s)))),'P':str(P),'checks':checks,
 'adverse_controls':controls,'limits':'Finite exact rational tensor/record/frame checks; not PDE evolution or general theorem proof'},indent=2))
