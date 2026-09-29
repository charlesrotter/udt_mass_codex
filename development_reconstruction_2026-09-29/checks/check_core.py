"""Independent exact anchors for the central algebra; prose owns hypotheses/proof."""
import json
import sympy as s
u,v=s.symbols('u v',positive=True)
K=s.Matrix([[0,1],[1,0]]);P=s.diag(u,v)
assert P.T*K*P==u*v*K
x,y=s.symbols('x y',real=True)
D=lambda z:s.diag(s.exp(-z),s.exp(z))
assert s.simplify(D(x)*D(y)-D(x+y))==s.zeros(2)
# Full coframe and query, selected as exact controls, not UDT-selected geometry.
B=s.Matrix([[3,1],[1,1]]);Q=s.Matrix([[2,1],[0,1]])
S=s.Matrix([[1,2],[-1,1]]);Y=s.Matrix([[2,0],[1,1]])
Z=s.Matrix([[1,1],[0,-1]])
E=B.row_join(s.zeros(2)).col_join((Q*S).row_join(Q));J=Y.col_join(Z)
eta=s.diag(-1,1,1,1)
h=J.T*E.T*eta*E*J
assert h==Y.T*B.T*s.diag(-1,1)*B*Y+(S*Y+Z).T*Q.T*Q*(S*Y+Z)
# Construct regular independent witness via arbitrary Lorentz columns and a full mixing.
E=s.Matrix([[4,1,0,0],[1,2,1,0],[0,1,2,1],[1,0,1,2]])
J=s.Matrix([[2,0],[0,1],[0,1],[0,0]])
h=J.T*E.T*eta*E*J
assert h[0,0]<0 and h.det()<0
T2=-h[0,0];beta=h[0,1]/h[0,0];L2=h[1,1]-h[0,1]**2/h[0,0]
assert s.Matrix([[-T2,-T2*beta],[-T2*beta,L2-T2*beta**2]])==h
assert T2*L2==-h.det()
m=s.sqrt(-h.det()); hs=s.diag(1,1/m)*h*s.diag(1,1/m)
assert s.simplify(hs.det())==-1
assert s.simplify(T2*L2/m**2)==1
# Ruler reparameterization and common scale are different transformations.
k=s.Integer(3);hparam=s.diag(1,k)*h*s.diag(1,k)
assert s.sqrt(-hparam.det())==k*m
hc=4*h
assert s.sqrt(-hc.det())==4*m and -hc[0,0]==4*T2
wrong_density=s.sqrt(L2)  # metric arclength alone omits reciprocal clock factor
assert s.simplify(T2*L2/wrong_density**2)!=1
assert s.simplify((-h.det()/h[0,0]**2)-(-hc.det()/hc[0,0]**2))==0
assert -h[0,0]!=-hc[0,0]  # raw invariant cannot be completed clock scalar
print(json.dumps({'result':'PASS','sympy':s.__version__,'regular_h':str(h),'det_h':str(h.det()),'anchors':['dual pairing','continuous-character algebra','complete block pullback','shifted decomposition','completed determinant','reparameterization vs rescaling'],'adverse_controls':['arclength-only normalization rejected','raw scalar substitution rejected'],'scope':'Exact algebra controls; no selected geometry, dynamics, all-domain numerical certification or proof of semantic completeness.'},indent=2))
