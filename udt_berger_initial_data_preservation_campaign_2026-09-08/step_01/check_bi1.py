"""Exact homogeneous checks; analytic proof owns quantifiers, not sample count.
FREE data p,q,K; DERIVED brackets and negative-K convention from G330/G315.
No production solver or old-carrier imports. Shared G337 formula is regression.
"""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

p,q=s.symbols('p q', positive=True)
u,w,v,z,r,t=s.symbols('u w v z r t', real=True)
K=s.Matrix([[u,z,r],[z,w,t],[r,t,v]])
br=[[[s.S.Zero for k in range(3)] for j in range(3)] for i in range(3)]
for i,j,k,n in [(0,1,2,q),(1,2,0,p),(2,0,1,p)]:
    br[i][j][k]=n
    br[j][i][k]=-n
G=[[[s.expand((br[i][j][k]-br[j][k][i]+br[k][i][j])/2)
     for k in range(3)] for j in range(3)] for i in range(3)]
DK=[s.Matrix(3,3,lambda j,k:-sum(G[i][j][l]*K[l,k]+G[i][k][l]*K[j,l]
    for l in range(3))) for i in range(3)]
D2=[[s.Matrix(3,3,lambda i,j:-sum(G[h][k][l]*DK[l][i,j]
    +G[h][i][l]*DK[k][l,j]+G[h][j][l]*DK[k][i,l]
    for l in range(3))) for k in range(3)] for h in range(3)]
S=s.Matrix(3,3,lambda i,j:s.expand(sum(-D2[k][i][k,j]-D2[k][j][k,i]
    +D2[k][k][i,j] for k in range(3))))
M=s.Matrix([s.expand(sum(DK[i][i,j] for i in range(3))) for j in range(3)])
Ric=s.Matrix(3,3,lambda k,j:s.expand(sum(
    G[j][k][m]*G[i][m][i]-G[i][k][m]*G[j][m][i]-br[i][j][m]*G[m][k][i]
    for i in range(3) for m in range(3))))
lh=p*q-q*q/2
lv=q*q/2
gap=lv-lh
P=s.diag(0,0,1)
Pi=s.eye(3)-P
Bdot=S+2*K*Ric
Pd=(Pi*Bdot*P+P*Bdot*Pi)/gap
checks=[]
def zero(name, expr):
    values=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    ok=all(s.simplify(x)==0 for x in values)
    checks.append(dict(name=name,pass_=ok))
    if not ok:
        raise AssertionError((name,expr))
zero('Ricci from Koszul',Ric-s.diag(lh,lh,lv))
zero('all six momentum entries',M-s.Matrix([(q-p)*t,(p-q)*r,0]))
zero('Ricci variation symmetric',S-S.T)
zero('projector derivative idempotence',Pd*P+P*Pd-Pd)
zero('full differentiated commutator',Bdot*P+Ric*Pd-Pd*Ric-P*Bdot)
zero('moving-metric self adjointness',(-2*K*P+Pd)-(-2*K*P+Pd).T)
zero('homogeneous full projector stationarity',Pd.subs({r:0,t:0}))
zero('round momentum control',M.subs(q,p))
C,d,ss,V,E,mm=s.symbols('C d ss V E mm',real=True)
block=s.Matrix([[C-V+d,ss,0],[ss,C-V-d,0],[0,0,V]])
zero('full Hamiltonian quadric',s.trace(block)**2-s.trace(block*block)
    -2*(C*C-V*V-d*d-ss*ss))
zero('nonzero horizontal mean branch',(mm*mm+2*mm*V-d*d-ss*ss-E).subs(
    V,(E-mm*mm+d*d+ss*ss)/(2*mm)))
zero('zero horizontal mean branch',(mm*mm+2*mm*V-d*d-ss*ss-E).subs(
    {mm:0,E:-d*d-ss*ss}))

# Formal mixed-jet control only: not claimed to satisfy spatial/vacuum data.
S0=s.Matrix([[0,0,-2*lv*r],[0,0,-2*lv*t],[-2*lv*r,-2*lv*t,0]])
Qd=(Pi*(S0+2*K*Ric)*P+P*(S0+2*K*Ric)*Pi)/gap
zero('image fixed formal control',Pi*Qd*P)
zero('projector need not fixed formal control',P*Qd*Pi+2*P*K*Pi)

fixtures=[]
for aa,cc in [(s.Rational(1),s.Rational(3,2)),(s.Rational(2),s.Rational(1))]:
    R=8/aa**2-2*cc**2/aa**4
    for lam in [-2,0,3]:
        ee=lam-R/2
        for m0,d0,s0 in [(1,0,0),(-1,s.Rational(1,3),s.Rational(2,3)),
                          (s.Rational(3,2),s.Rational(-1,2),0)]:
            vv=(ee-m0*m0+d0*d0+s0*s0)/(2*m0)
            sub={p:2/cc,q:2*cc/aa**2,u:m0+d0,w:m0-d0,v:vv,z:s0,r:0,t:0}
            kval=K.subs(sub)
            zero('fixture H',R+s.trace(kval)**2-s.trace(kval*kval)-2*lam)
            zero('fixture M',M.subs(sub))
            zero('fixture Pdot',Pd.subs(sub))
            fixtures.append(dict(a=str(aa),c=str(cc),Lambda=lam,
                K=[[str(x) for x in kval.row(i)] for i in range(3)]))

# Catch proofs are actual nonzero differences/residuals, not tautological flags.
hostiles={
 'omit raising term':Pi*(2*K*Ric)*P,
 'symmetric projector for mixed K':Pd-Pd.T,
 'omit momentum connection':M,
 'allow vertical shear off constraint':M.subs({r:1,t:1}),
 'erase horizontal shear Hamiltonian':2*(d*d+ss*ss),
 'wrong norm sign Hamiltonian':2*s.trace(block*block),
 'wrong negative K sign':2*S,
 'drop derivative-index connection':s.Matrix(3,3,lambda i,j:sum(
      G[k][i][l]*DK[l][k,j]+G[k][j][l]*DK[l][k,i]-G[k][k][l]*DK[l][i,j]
      for k in range(3) for l in range(3))),
}
for name,expr in hostiles.items():
    values=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    if all(s.simplify(x)==0 for x in values):
        raise AssertionError('vacuous hostile '+name)
print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=s.__version__,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    checks=checks,fixtures=fixtures,hostiles_caught=list(hostiles),
    symbolic_momentum=[str(x) for x in M],
    symbolic_S=[[str(x) for x in S.row(i)] for i in range(3)],
    symbolic_Pdot=[[str(s.simplify(x)) for x in Pd.row(i)] for i in range(3)],
    limitations=['finite checks support but do not prove analytic quantifiers',
      'formal mixed-jet control not a lawful-data witness',
      'no time persistence or inhomogeneous constraint census']),indent=2))
