"""Exact local constraint reduction/two-jet checks; CK theorem owns realization.
FREE supplied local data h,epsilon; DERIVED conditional G315/G330 frame/equations.
No numerical solution, global gluing, physical source or author-code import.
"""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

m,r,w,E=s.symbols('m r w E',real=True)
h,eps=s.symbols('h epsilon',real=True,nonzero=True)
p,q=s.symbols('p q',positive=True)
U=[m,r,w]
z=(E-m*m+r*r+w*w)/(2*m)
F=m+z
K=s.Matrix([[m,0,r],[0,m,w],[r,w,z]])
tau=s.trace(K)
D=s.Matrix(3,3,lambda i,j:s.Symbol('D'+str(i+1)+str(j+1),real=True))
def ei(i,f):
    return s.expand(sum(s.diff(f,U[j])*D[i,j] for j in range(3)))
br=[[[s.S.Zero for l in range(3)] for j in range(3)] for i in range(3)]
for i,j,l,n in [(0,1,2,q),(1,2,0,p),(2,0,1,p)]:
    br[i][j][l]=n
    br[j][i][l]=-n
G=[[[s.expand((br[i][j][l]-br[j][l][i]+br[l][i][j])/2)
     for l in range(3)] for j in range(3)] for i in range(3)]
M=s.Matrix([s.expand(sum(ei(j,K[j,i])-sum(G[j][j][l]*K[l,i]+G[j][i][l]*K[j,l]
    for l in range(3)) for j in range(3))-ei(i,tau)) for i in range(3)])
expectedM=s.Matrix([-ei(0,F)+D[2,1]+(q-p)*w,
                    -ei(1,F)+D[2,2]+(p-q)*r,
                    D[0,1]+D[1,2]-2*D[2,0]])
checks=[]
def zero(name,expr):
    values=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    residues=[s.factor(x) for x in values]
    assert all(x==0 for x in residues),(name,residues)
    checks.append(dict(name=name,residuals=list(map(str,residues))))
zero('full nonlinear original Hamiltonian identity',tau*tau-s.trace(K*K)-2*E)
zero('all three original momentum equations with connection',M-expectedM)

# General analytic flow-box frame: tangential derivatives plus b_A normal parts.
b1,b2=s.symbols('b1 b2',real=True)
normal=s.Matrix(s.symbols('Nm Nr Nw',real=True))
tangent=s.Matrix(2,3,lambda i,j:s.Symbol('T'+str(i+1)+str(j+1),real=True))
dx={D[2,j]:normal[j] for j in range(3)}
dx.update({D[i,j]:tangent[i,j]+[b1,b2][i]*normal[j] for i in range(2) for j in range(3)})
system=s.Matrix([D[2,0]-(D[0,1]+D[1,2])/2,
                 D[2,1]-ei(0,F)-(p-q)*w,
                 D[2,2]-ei(1,F)-(q-p)*r]).subs(dx)
A=system.jacobian(normal)
expectedA=s.Matrix([[1,-b1/2,-b2/2],
    [-b1*s.diff(F,m),1-b1*s.diff(F,r),-b1*s.diff(F,w)],
    [-b2*s.diff(F,m),-b2*s.diff(F,r),1-b2*s.diff(F,w)]])
zero('actual noncharacteristic matrix',A-expectedA)
zero('normal matrix at base point identity',A.subs({b1:0,b2:0})-s.eye(3))
zero('normal matrix determinant at base point',s.factor(A.det()).subs({b1:0,b2:0})-1)
base={m:h,r:0,w:0,E:3*h*h}
zero('control algebraic K',K.subs(base)-h*s.eye(3))
zero('control F and first partials',s.Matrix([F,s.diff(F,m),s.diff(F,r),s.diff(F,w)]).subs(base)-s.Matrix([2*h,-1,0,0]))
zero('constant control solves full momentum',M.subs(base).subs({v:0 for v in D}))

# The analytic seed fixes tangential jets; CK fixes the remaining nine.
Q=[]
unknown=[]
for label in ['m','r','w']:
    a13,a23,a33=s.symbols(label+'13 '+label+'23 '+label+'33',real=True)
    unknown.extend([a13,a23,a33])
    Q.append(s.Matrix([[eps if label=='w' else 0,0,a13],[0,0,a23],[a13,a23,a33]]))
jet_eq=[]
for j in range(3):
    jet_eq.extend([Q[0][2,j]-(Q[1][0,j]+Q[2][1,j])/2,
                   Q[1][2,j]+Q[0][0,j],Q[2][2,j]+Q[0][1,j]])
L,bb=s.linear_eq_to_matrix(jet_eq,unknown)
solution=s.linsolve((L,bb),unknown)
assert solution==s.FiniteSet(tuple(s.S.Zero for _ in unknown)),solution
checks.append(dict(name='CK second-jet recursion uniquely fixes all nine normal entries',determinant=str(L.det()),solution=str(solution)))
Q=[qq.subs(dict.fromkeys(unknown,0)) for qq in Q]
# Since T and DT vanish, coordinate Hessians are covariant Hessians exactly.
T2=[[[[s.factor(sum(s.diff(K[i,j],U[l]).subs(base)*Q[l][a,b] for l in range(3)))
        for j in range(3)] for i in range(3)] for b in range(3)] for a in range(3)]
Sdot=s.Matrix(3,3,lambda i,j:s.expand(sum(-T2[k][i][k][j]-T2[k][j][k][i]
    +T2[k][k][i][j]+T2[i][j][k][k] for k in range(3))))
zero('full Ricci variation of realized two-jet',Sdot-s.Matrix([[0,0,0],[0,0,eps],[0,eps,0]]))
for a in range(3):
    for i in range(3):
        zero('differentiated original momentum '+str((a,i)),sum(T2[a][j][j][i]-T2[a][i][j][j] for j in range(3)))
    for b in range(3):
        zero('second original Hamiltonian '+str((a,b)),4*h*sum(T2[a][b][i][i] for i in range(3)))
gap=q*(q-p)
B=s.diag(p*q-q*q/2,p*q-q*q/2,q*q/2)
P=s.diag(0,0,1)
Pi=s.eye(3)-P
Bdot=Sdot+2*h*B
Pdot=(Pi*Bdot*P+P*Bdot*Pi)/gap
zero('full raising and projector contribution',Pdot-Sdot/gap)
zero('pointwise control raising contributes no drift',Pi*(2*h*B)*P)
zero('epsilon zero drift control',Pdot.subs(eps,0))

fixtures=[]
for aa,cc in [(s.Rational(1),s.Rational(3,2)),(s.Rational(2),s.Rational(1))]:
    R=8/aa**2-2*cc**2/aa**4
    Delta=4*(cc**2-aa**2)/aa**4
    for hh in [-1,1]:
        ll=R/2+3*hh**2
        for ee in [-2,0,2]:
            yy=s.Rational(ee)/Delta
            zero('fixed sector control H',R+6*hh**2-2*ll)
            zero('fixture full projector drift',Pdot.subs({p:2/cc,q:2*cc/aa**2,h:hh,eps:ee})
                 -s.Matrix([[0,0,0],[0,0,yy],[0,yy,0]]))
            fixtures.append(dict(a=str(aa),c=str(cc),h=hh,Lambda=str(ll),epsilon=ee,Y2=str(yy)))
assert s.factor(s.diff(F,m).subs(base))==-1
print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=s.__version__,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),checks=checks,
    F=str(F),noncharacteristic_matrix=str(A),normal_determinant=str(s.factor(A.det())),
    normal_second_jet_solution=str(solution),Ricci_dot_difference=str(Sdot),Pdot=str(Pdot),
    fixtures=fixtures,
    limits=['CK analytic convergence/realization is a theorem application, not a finite-check result',
            'only local open Berger patch; no global compact data or gluing',
            'two-jet control alone is not the existence argument',
            'no stability or orbit-closure consequence']),indent=2))
