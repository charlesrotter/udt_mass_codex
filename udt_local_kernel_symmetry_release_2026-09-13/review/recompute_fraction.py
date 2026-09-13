#!/usr/bin/env python3
"""Independent metric-two-jet review; no parent/source executable imports.

Original Cartesian metric quadratic terms are evaluated at integer basis
points and polarized. At the regular origin, Gamma=0; differentiating the
original Levi-Civita formula therefore gives the entire Riemann tensor.
Finite exact rational checks are arithmetic checks, not universal proof.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import datetime, hashlib, json, platform, random, resource, sys, time

resource.setrlimit(resource.RLIMIT_AS, (2048*1024**2,2048*1024**2))
resource.setrlimit(resource.RLIMIT_CPU, (115,115))
START=datetime.datetime.now(datetime.timezone.utc).isoformat()
T0=time.monotonic()
ETA=[-1,1,1,1]
OUT=Path(__file__).resolve().parent

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def trans(a): return list(map(list,zip(*a)))
def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def det3(a): return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
def adj(a):
    z=[]
    for i in range(3):
        row=[]
        for j in range(3):
            rr=[k for k in range(3) if k!=j]; cc=[k for k in range(3) if k!=i]
            row.append((-1)**(i+j)*(a[rr[0]][cc[0]]*a[rr[1]][cc[1]]-a[rr[0]][cc[1]]*a[rr[1]][cc[0]]))
        z.append(row)
    return z
def D_at(x,S):
    C=[[0,-x[2],x[1]],[x[2],0,-x[0]],[-x[1],x[0],0]]
    return mm(mm(trans(C),S),C)
def quadratic_metric(x,c,S):
    """Exact quadratic term of candidate full metric, including its lapse."""
    xx=x[1:]; rr=dot(xx,xx); D=D_at(xx,S)
    g=[[F(0) for _ in range(4)] for _ in range(4)]
    g[0][0]=-c*rr
    for i,j in product(range(3),repeat=2): g[i+1][j+1]=-c*xx[i]*xx[j]+D[i][j]
    return g
def differentiate_metric(c,S):
    basis=eye(4); ev=[quadratic_metric(e,c,S) for e in basis]
    dd=[[[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for u,v in product(range(4),repeat=2):
        if u==v:
            for a,b in product(range(4),repeat=2): dd[a][b][u][v]=2*ev[u][a][b]
        else:
            z=quadratic_metric([basis[u][k]+basis[v][k] for k in range(4)],c,S)
            for a,b in product(range(4),repeat=2): dd[a][b][u][v]=z[a][b]-ev[u][a][b]-ev[v][a][b]
    return dd
def riemann_from_metric(dd):
    # dg=0, so d(g^-1)*dg and all Gamma*Gamma vanish exactly at origin.
    def dGamma(a,b,c,d):
        return F(ETA[a],2)*(dd[a][c][b][d]+dd[a][b][c][d]-dd[b][c][a][d])
    return [[[[ETA[a]*(dGamma(a,d,b,c)-dGamma(a,c,b,d)) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
def eps(i,j,k):
    if len({i,j,k})<3:return 0
    return 1 if (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)] else -1
def contract(R,v,k,w): return sum(v[a]*k[b]*w[c]*k[d]*R[a][b][c][d] for a,b,c,d in product(range(4),repeat=4))
def g(a,b):return ETA[a] if a==b else 0
def dfact(n):
    z=1
    while n>0:z*=n;n-=2
    return z
def sphere_monomial(indices):
    counts=[indices.count(i) for i in range(3)]
    if any(k%2 for k in counts):return F(0)
    return F(dfact(counts[0]-1)*dfact(counts[1]-1)*dfact(counts[2]-1),dfact(sum(counts)+1))

cases=[]
for c in [F(0),F(2,3),F(-5,7)]:
    for s in [F(0),F(1,2),F(-3,5)]:
        cases.append((c,[[s,0,0],[0,2*s,0],[0,0,-3*s]],'diagonal'))
rng=random.Random(20260913)
for _ in range(12):
    c=F(rng.randint(-7,7),rng.randint(1,7))
    a,b,d,e,h=[F(rng.randint(-7,7),rng.randint(1,7)) for _ in range(5)]
    cases.append((c,[[a,d,e],[d,b,h],[e,h,-a-b]],'general_tracefree'))

rows=[]; asserts=0; mutations=[]
def check(ok,label):
    global asserts
    asserts+=1
    if not ok:raise AssertionError(label)

for index,(c,S,kind) in enumerate(cases):
    dd=differentiate_metric(c,S); R=riemann_from_metric(dd)
    Ric=[[sum(ETA[a]*R[a][b][a][d] for a in range(4)) for d in range(4)] for b in range(4)]
    scalar=sum(ETA[a]*Ric[a][a] for a in range(4))
    W=[[[[R[a][b][j][k]-F(1,2)*(g(a,j)*Ric[k][b]-g(a,k)*Ric[j][b]-g(b,j)*Ric[k][a]+g(b,k)*Ric[j][a])+scalar*F(1,6)*(g(a,j)*g(k,b)-g(a,k)*g(j,b)) for k in range(4)] for j in range(4)] for b in range(4)] for a in range(4)]
    s2=sum(S[i][j]*S[j][i] for i,j in product(range(3),repeat=2))
    for a,b,j,k in product(range(4),repeat=4):
        check(R[a][b][j][k]==-R[b][a][j][k] and R[a][b][j][k]==-R[a][b][k][j] and R[a][b][j][k]==R[j][k][a][b],f'{index}: Riemann symmetries')
        check(R[a][b][j][k]+R[a][j][k][b]+R[a][k][b][j]==0,f'{index}: first Bianchi')
    for i,j in product(range(3),repeat=2):
        check(R[0][i+1][0][j+1]==c*(i==j),f'{index}: lapse Hessian')
        check(Ric[i+1][j+1]==-3*c*(i==j)+3*S[i][j],f'{index}: Ricci spatial')
        check(W[0][i+1][0][j+1]==F(3,2)*S[i][j],f'{index}: Weyl electric')
    for i,j,k,l in product(range(3),repeat=4):
        target=-c*((i==k)*(j==l)-(i==l)*(j==k))-3*sum(eps(i,j,p)*eps(k,l,q)*S[p][q] for p,q in product(range(3),repeat=2))
        check(R[i+1][j+1][k+1][l+1]==target,f'{index}: full spatial Riemann')
    for i,j,k in product(range(3),repeat=3):check(R[0][i+1][j+1][k+1]==0,f'{index}: static mixed Riemann')
    check(Ric[0][0]==3*c and scalar==-12*c,f'{index}: Ricci00 scalar')
    norms=[]
    for tensor in (R,W):norms.append(sum(ETA[a]*ETA[b]*ETA[j]*ETA[k]*tensor[a][b][j][k]**2 for a,b,j,k in product(range(4),repeat=4)))
    ricnorm=sum(ETA[a]*ETA[b]*Ric[a][b]**2 for a,b in product(range(4),repeat=2))
    check(norms==[24*c*c+36*s2,18*s2] and ricnorm==36*c*c+9*s2,f'{index}: three invariants')
    screens=[]
    for axis in range(3):
        n=eye(3)[axis]; k=[F(1)]+n; screen=[eye(3)[i] for i in range(3) if i!=axis]
        matrix=[]
        for v in screen:
            line=[]
            for w in screen:
                actual=contract(R,[F(0)]+v,k,[F(0)]+w)
                expect=-3*sum(cross(v,n)[i]*S[i][j]*cross(w,n)[j] for i,j in product(range(3),repeat=2))
                check(actual==expect,f'{index}: signed full screen');line.append(actual)
            matrix.append(line)
        screens.append(matrix)
    x=[F(2,3),F(-3,7),F(5,11)]; v=[F(-1,5),F(3,4),F(2,7)]
    D=D_at(x,S); rr=dot(x,x); I=eye(3)
    check(all(sum(D[i][j]*x[j] for j in range(3))==0 for i in range(3)),f'{index}: radial annihilation')
    actual_det=det3([[I[i][j]+D[i][j] for j in range(3)] for i in range(3)])
    check(actual_det==1-dot(x,[dot(row,x) for row in S])+rr*dot(x,[dot(row,x) for row in adj(S)]),f'{index}: tangent determinant')
    mean_b=sum(adj(S)[i][j]*sphere_monomial([i,j]) for i,j in product(range(3),repeat=2))
    mean_a2=sum(S[i][j]*S[k][l]*sphere_monomial([i,j,k,l]) for i,j,k,l in product(range(3),repeat=4))
    M4=F(1,2)*mean_b-F(1,8)*mean_a2
    check(M4==-s2/10,f'{index}: integrated area correction')
    h2=quadratic_metric([0]+x,c,S)
    m2jet=c*rr*dot(v,v)+sum(v[i]*h2[i+1][j+1]*v[j] for i,j in product(range(3),repeat=2))
    check(m2jet==c*(rr*dot(v,v)-dot(x,v)**2)+sum(v[i]*D[i][j]*v[j] for i,j in product(range(3),repeat=2)),f'{index}: full pair density')
    rows.append({'index':index,'kind':kind,'c':str(c),'S':[[str(z) for z in r] for r in S],'R':str(scalar),'Riemann2':str(norms[0]),'Ricci2':str(ricnorm),'Weyl2':str(norms[1]),'screen_axes':[[[str(z) for z in r] for r in mat] for mat in screens],'M4':str(M4)})
    if kind=='diagonal' and S[0][0]!=0:
        s=S[0][0]
        check(screens[2]==[[-6*s,0],[0,-3*s]],f'{index}: sign-sensitive witness')

# Deliberate geometry/readout defects, with saved original-definition values.
c=F(2,3); S=[[1,0,0],[0,2,0],[0,0,-3]]
R=riemann_from_metric(differentiate_metric(c,S)); tide=contract(R,[0,1,0,0],[1,0,0,1],[0,1,0,0])
for name,Sm in [('reverse angular metric term', [[-z for z in row] for row in S]),('drop angular metric term',[[0]*3 for _ in range(3)])]:
    Rm=riemann_from_metric(differentiate_metric(c,Sm))
    tide_m=contract(Rm,[0,1,0,0],[1,0,0,1],[0,1,0,0])
    mutations.append({'name':name,'mutant_tide':str(tide_m),'original_tide':str(tide),'rejected':tide_m!=tide})
mean_b=sum(adj(S)[i][j]*sphere_monomial([i,j]) for i,j in product(range(3),repeat=2))
mean_a2=sum(S[i][j]*S[k][l]*sphere_monomial([i,j,k,l]) for i,j,k,l in product(range(3),repeat=4))
uncorrected_area4=F(1,2)*mean_b-F(1,8)*mean_a2
mutations.append({'name':'omit area correction q','claimed_area4':'0','recomputed_area4':str(uncorrected_area4),'rejected':uncorrected_area4!=0})
check(all(m['rejected'] for m in mutations),'mutation controls')
result={'status':'PASS','start_utc':START,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-T0,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'versions':{'python':sys.version,'platform':platform.platform()},'cases':len(cases),'exact_assertions':asserts,'independence':'Separate context; stdlib Fraction metric polynomial evaluation/polarization -> differentiated original Levi-Civita connection -> full Riemann. No parent executable imports or output reads. Candidate formulas are comparison targets after recomputation.','limits':'21 rational cases do not prove universal identities; full analytic geometry reviewed in prose. No finite-radius curvature integration, numerical certification, or physical adoption.','mutations':mutations,'rows':rows}
(OUT/'FRACTION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
