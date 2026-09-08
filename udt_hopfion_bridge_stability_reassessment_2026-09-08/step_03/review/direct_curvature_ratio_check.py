"""Post-exposure exact Christoffel/time-jet reconstruction of saved slopes.

No author/HB2 curvature implementation imports and no 5/2 drift formula.
The auxiliary spatial metric jet has gamma_dot=-2K; it is not a finite-time
Einstein solution. Implicit differentiation of the 2x2 eigenline equation
extracts the angular slope directly from the raised Ricci tensor.
"""
import json
import platform
import sys
from fractions import Fraction as Q
from pathlib import Path
import sympy as s

class Jet:
    def __init__(self, value=0, derivative=0):
        value=int(value) if isinstance(value,bool) else value
        derivative=int(derivative) if isinstance(derivative,bool) else derivative
        self.v, self.d = Q(str(value)), Q(str(derivative))
    def __add__(self, other):
        other=other if isinstance(other,Jet) else Jet(other)
        return Jet(self.v+other.v,self.d+other.d)
    __radd__=__add__
    def __neg__(self): return Jet(-self.v,-self.d)
    def __sub__(self,other): return self+-other if isinstance(other,Jet) else self+Jet(-other)
    def __mul__(self,other):
        other=other if isinstance(other,Jet) else Jet(other)
        return Jet(self.v*other.v,self.d*other.v+self.v*other.d)
    __rmul__=__mul__

def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def asjets(a,h):
    return [[Jet(a[i,j],h[i,j]) for j in range(3)] for i in range(3)]

step=Path(__file__).resolve().parents[1]
saved=json.loads((step/'author_check_final_pin.stdout').read_text())
x=s.symbols('x'); cache={}; records=[]; nonzero_contrasts=[]
for row in saved['saved_HB2_recomputed']:
    p,q=map(s.Rational,row['weights']); z=s.Rational(row['x'])
    C,root=s.Rational(row['C']),s.Rational(row['root_D'])
    key=(p,q,z)
    if key not in cache:
        F=p*x+q*(1-x)
        eta=s.Matrix([0,x/F,(1-x)/F]); zeta=s.Matrix([0,q/F,-p/F])
        g=s.diag(1/(4*x*(1-x)*F),0,0)+x*(1-x)/F*zeta*zeta.T+eta*eta.T
        E=eta*eta.T
        gg=[a.subs(x,z) for a in [g,g.diff(x),g.diff(x,2)]]
        ee=[a.subs(x,z) for a in [E,E.diff(x),E.diff(x,2)]]
        R=24*p*q/F-8*(p+q)-2
        rr=[s.diff(R,x,k).subs(x,z) for k in range(3)]
        cache[key]=(gg,ee,rr,eta.subs(x,z))
    (g0,g1,g2),(e0,e1,e2),(R0,R1,R2),eta0=cache[key]
    b0=-C+root; b1=R1/root; b2=R2/root-R1**2/root**3
    h0=(b0-C)*g0-2*b0*e0
    h1=b1*g0+(b0-C)*g1-2*(b1*e0+b0*e1)
    h2=b2*g0+2*b1*g1+(b0-C)*g2-2*(b2*e0+2*b1*e1+b0*e2)
    ii=g0.inv(); ih=-ii*h0*ii
    I=asjets(ii,ih); Gx=asjets(g1,h1); Gxx=asjets(g2,h2)
    Ix=[[ -v for v in r] for r in mm(mm(I,Gx),I)]
    conn=[[[Jet() for j in range(3)] for i in range(3)] for k in range(3)]
    connx=[[[Jet() for j in range(3)] for i in range(3)] for k in range(3)]
    for k in range(3):
      for i in range(3):
        for j in range(3):
          for l in range(3):
            term=(i==0)*Gx[l][j]+(j==0)*Gx[l][i]-(l==0)*Gx[i][j]
            termx=(i==0)*Gxx[l][j]+(j==0)*Gxx[l][i]-(l==0)*Gxx[i][j]
            conn[k][i][j]+=Q(1,2)*I[k][l]*term
            connx[k][i][j]+=Q(1,2)*(Ix[k][l]*term+I[k][l]*termx)
    ric=[[Jet() for j in range(3)] for i in range(3)]
    for i in range(3):
      for j in range(3):
        ric[i][j]=connx[0][i][j]-(j==0)*sum(connx[k][i][k] for k in range(3))
        for k in range(3):
          for l in range(3):
            ric[i][j]+=conn[k][i][j]*conn[l][k][l]-conn[l][i][k]*conn[k][j][l]
    B=mm(I,ric); xi=[Q(0),Q(str(p)),Q(str(q))]
    assert sum(B[i][i].v for i in range(3))==Q(str(R0))
    assert all(sum(B[i][j].v*xi[j] for j in range(3))==2*xi[i] for i in range(3))
    assert all(ric[0][j].v==ric[0][j].d==0 for j in [1,2])
    ratio=Q(str(p/q))
    slope_equation=B[1][1]*ratio+B[1][2]-ratio*(B[2][1]*ratio+B[2][2])
    assert slope_equation.v==0
    denominator=B[1][1].v-B[2][2].v-2*B[2][1].v*ratio
    assert denominator!=0
    result=-slope_equation.d/denominator
    target=Q(row['qdot'])
    assert result==target, (row,result,target)
    K=-h0/2; S=ii*K
    assert R0+s.trace(S)**2-s.trace(S*S)==2*s.Rational(row['Lambda'])
    inverse_effect=ih*s.Matrix([[ric[i][j].v for j in range(3)] for i in range(3)])
    assert inverse_effect!=s.zeros(3)
    if result:
      # Real residuals, not a word/label test; a single angular derivative
      # or reversed implicit-eigenvalue denominator gives a different result.
      partial=-(B[1][1].d*ratio+B[1][2].d)/denominator
      assert partial!=result and -result!=result
      nonzero_contrasts.append(dict(weights=row['weights'],root=str(root),
        omitted_second_row_residual=str(partial-result),reversed_denominator_residual=str(-2*result)))
    records.append(dict(weights=row['weights'],x=row['x'],C=row['C'],root=row['root_D'],
       Lambda=row['Lambda'],R=str(R0),implicit_eigenline_denominator=str(denominator),
       direct_curvature_qdot=str(result),saved_qdot=row['qdot'],
       full_inverse_variation_retained=True))
print(json.dumps(dict(kind='exact direct 3D connection/Ricci time jet and implicit eigenline differentiation',
  matched=len(records),records=records,hostile_nonzero_contrasts=nonzero_contrasts,
  implementation_imports='standard library and SymPy only; no author/project engine',
  versions=dict(python=sys.version,sympy=s.__version__,platform=platform.platform()),
  limits=['finite exact fixtures only','no actual finite-time metric solve',
          'HB2 family and scalar jets remain exposed source definitions']),indent=2))
