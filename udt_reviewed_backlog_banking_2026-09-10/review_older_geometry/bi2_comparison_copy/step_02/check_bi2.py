"""BI2 exact anchors from Lorentz Koszul, not numerical evolution.
DERIVED conditional G315 sign/equation; FREE positive diagonal sizes and all rates.
Checks support the analytic homogeneous theorem, not arbitrary smooth data.
"""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

I=range(4)
n=s.symbols('n1:4',positive=True)
k=s.symbols('k1:4',real=True)
lam=s.Symbol('Lambda',real=True)
tau=sum(k)
r=[(n[i]**2-(n[(i+1)%3]-n[(i+2)%3])**2)/2 for i in range(3)]
kd=[r[i]+tau*k[i]-lam for i in range(3)]
nd=[n[i]*(tau-2*k[i]) for i in range(3)]
def dt(f):
    return s.expand(sum(s.diff(f,k[i])*kd[i]+s.diff(f,n[i])*nd[i]
                        for i in range(3)))

br=[[[s.S.Zero for c in I] for b in I] for a in I]
for i in range(3):
    br[0][i+1][i+1]=k[i]
    br[i+1][0][i+1]=-k[i]
for i,j,l in [(0,1,2),(1,2,0),(2,0,1)]:
    br[i+1][j+1][l+1]=n[l]
    br[j+1][i+1][l+1]=-n[l]
signature=[-1,1,1,1]
G=[[[s.expand((signature[c]*br[a][b][c]-signature[a]*br[b][c][a]
              +signature[b]*br[c][a][b])/(2*signature[c]))
      for c in I] for b in I] for a in I]
Ric4=s.Matrix(4,4,lambda j,l:s.expand(sum(
    (dt(G[j][l][i]) if i==0 else 0)-(dt(G[i][l][i]) if j==0 else 0)
    +sum(G[j][l][m]*G[i][m][i]-G[i][l][m]*G[j][m][i]
         -br[i][j][m]*G[m][l][i] for m in I) for i in I)))
Ric3=s.Matrix(3,3,lambda j,l:s.expand(sum(
    G[j+1][l+1][m+1]*G[i+1][m+1][i+1]
    -G[i+1][l+1][m+1]*G[j+1][m+1][i+1]
    -br[i+1][j+1][m+1]*G[m+1][l+1][i+1]
    for i in range(3) for m in range(3))))
H=sum(r)+tau**2-sum(ki**2 for ki in k)-2*lam
checks=[]
def zero(name,f):
    vals=list(f) if isinstance(f,s.MatrixBase) else [f]
    residual=[s.factor(x) for x in vals]
    assert all(x==0 for x in residual),(name,residual)
    checks.append(dict(name=name,residual=list(map(str,residual))))
zero('spatial Ricci from Koszul',Ric3-s.diag(*r))
zero('original full Lorentz Ricci after diagonal evolution',Ric4-s.diag(H-lam,lam,lam,lam))
zero('original Hamiltonian propagation',dt(H)-2*tau*H)
zero('scalar derivative',dt(sum(r))-2*sum(k[i]*r[i] for i in range(3)))

A,B,C=s.symbols('A B C',positive=True)
lengths=[A,B,C]
sub={n[i]:2*lengths[i]/(lengths[(i+1)%3]*lengths[(i+2)%3]) for i in range(3)}
rr=[s.factor(Ric3[i,i].subs(sub)) for i in range(3)]
x=[A*A,B*B,C*C]
for i in range(3):
    zero('diagonal size Ricci '+str(i),rr[i]-2*(x[i]**2-(x[(i+1)%3]-x[(i+2)%3])**2)/(x[0]*x[1]*x[2]))
gaps=[4*(x[2]-x[i])*(x[2]+x[i]-x[1-i])/(x[0]*x[1]*x[2]) for i in range(2)]
for i in range(2):
    zero('vertical gap factor '+str(i),rr[2]-rr[i]-gaps[i])
P3=(s.diag(*rr)-rr[0]*s.eye(3))*(s.diag(*rr)-rr[1]*s.eye(3))/(gaps[0]*gaps[1])
zero('full triaxial projector',P3-s.diag(0,0,1))
zero('Berger initial gap',gaps[0].subs(B,A)-4*(C*C-A*A)/A**4)

# Fixed Lie automorphisms, full K and metric; no continuous axial assumption.
Xbr={(0,1):s.Matrix([0,0,2]),(1,2):s.Matrix([2,0,0]),(2,0):s.Matrix([0,2,0])}
for signs in [(1,-1,-1),(-1,1,-1),(-1,-1,1)]:
    J=s.diag(*signs)
    for (i,j),vec in Xbr.items():
        zero('discrete bracket automorphism '+str((signs,i,j)),J*vec-signs[i]*signs[j]*vec)
    zero('diagonal metric invariance '+str(signs),J*s.diag(*x)*J-s.diag(*x))
    zero('full diagonal K invariance '+str(signs),J*s.diag(*[x[i]*k[i] for i in range(3)])*J-s.diag(*[x[i]*k[i] for i in range(3)]))

# ad(X3) on Xi; exact Lie derivative of horizontal covariant tensor.
ad=s.Matrix([[0,-2,0],[2,0,0],[0,0,0]])
horizontal=s.diag(A*A,B*B,0)
Lie=-ad.T*horizontal-horizontal*ad
zero('quotient direct descent Lie obstruction',Lie-s.Matrix([[0,2*(A*A-B*B),0],[2*(A*A-B*B),0,0],[0,0,0]]))
dd,ss,mm=s.symbols('d ss m',real=True)
K0=s.Matrix([[mm+dd,ss,0],[ss,mm-dd,0],[0,0,k[2]]])
LieK=-ad.T*K0-K0*ad
zero('unrotated initial full shear obstruction',LieK-s.Matrix([[-4*ss,4*dd,0],[4*dd,4*ss,0],[0,0,0]]))
zero('normalized form helicity',(-2)*(2*s.pi**2)/(4*s.pi**2)+1)

controls=[]
for sizes in [(1,1,s.Rational(9,4)),(4,4,1),(1,3,2),(3,1,2),(1,1,1),(1,2,4)]:
    v=[s.Rational(z) for z in sizes]
    rv=[s.factor(2*(v[i]**2-(v[(i+1)%3]-v[(i+2)%3])**2)/(v[0]*v[1]*v[2])) for i in range(3)]
    gs=[s.factor(rv[2]-rv[i]) for i in range(2)]
    controls.append(dict(squared_sizes=list(map(str,v)),Ricci=list(map(str,rv)),
                         gaps=list(map(str,gs)),direct_descent=v[0]==v[1]))
assert controls[2]['gaps'][0]=='0' and controls[3]['gaps'][1]=='0'
assert all(controls[i]['squared_sizes'][2] not in controls[i]['squared_sizes'][:2] for i in [2,3])
fixtureK=s.diag(1,2,-s.Rational(1,4))
zero('lawful asymmetric initial Hamiltonian',s.Rational(7,2)+s.trace(fixtureK)**2-s.trace(fixtureK**2)-6)
zero('actual initial horizontal splitting rate',-2*(fixtureK[0,0]-fixtureK[1,1])-2)
assert (Lie.subs({A:1,B:2})!=s.zeros(3))
print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=s.__version__,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    exact_checks=checks,controls=controls,full_Ricci4=str(Ric4),
    momentum='off-diagonal Ricci4_0i identically zero; all original projections reconstructed',
    Ricci3=list(map(str,rr)),vertical_gaps=list(map(str,gaps)),
    quotient_Lie=str(Lie),initial_shear_Lie=str(LieK),
    limitations=['not numerical evolution','general proof owns local-time quantifier',
                 'gap controls not claimed reached by a chosen development',
                 'direct quotient descent differs from existence of any quotient metric']),indent=2))
