"""Exact original-metric second-jet checks; no imported physical equations."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

checks = []
def eq(name, lhs, rhs=0):
    diff = lhs-rhs
    vals = list(diff) if isinstance(diff, s.MatrixBase) else [diff]
    assert all(s.expand(z)==0 for z in vals), (name, diff)
    checks.append(name)

c = s.symbols('c', real=True)
k1,k2,k12,k13,k23 = s.symbols('k1 k2 k12 k13 k23', real=True)
t1,t2,t12,t13,t23 = s.symbols('s1 s2 s12 s13 s23', real=True)
K=s.Matrix([[k1,k12,k13],[k12,k2,k23],[k13,k23,-k1-k2]])
S=s.Matrix([[t1,t12,t13],[t12,t2,t23],[t13,t23,-t1-t2]])
A=c*s.eye(3)+K; B=c*s.eye(3)+S
xx=s.symbols('x y z', real=True); x=s.Matrix(xx)
C=s.Matrix([[0,-xx[2],xx[1]],[xx[2],0,-xx[0]],[-xx[1],xx[0],0]])
q2=(x.T*A*x)[0]; D=C.T*B*C
G2=-q2*s.eye(3)+D
eq('strong_radial_quadratic',G2*x,-q2*x)
eq('old_class_recovered_at_K_zero',G2.subs(dict.fromkeys([k1,k2,k12,k13,k23],0)), -c*x*x.T+C.T*S*C)
eq('leading_area_trace_relation',s.trace(B),s.trace(A))
v=s.Matrix(s.symbols('v1 v2 v3'))
eq('full_density_quadratic',(v.T*G2*v)[0]+q2*(v.T*v)[0],(v.T*D*v)[0])

coords=(s.symbols('x0'),)+xx
eta=s.diag(-1,1,1,1); signs=[-1,1,1,1]
g=s.diag(-1-q2,1,1,1)
g[1:4,1:4]=s.eye(3)+G2
H=[[[[s.diff(g[a,b],coords[i],coords[j]) for j in range(4)] for i in range(4)] for b in range(4)] for a in range(4)]
R=[[[[s.expand((H[a][d][b][cc]+H[b][cc][a][d]-H[a][cc][b][d]-H[b][d][a][cc])/2) for d in range(4)] for cc in range(4)] for b in range(4)] for a in range(4)]
Ric=s.Matrix(4,4,lambda b,d:s.expand(sum(signs[a]*R[a][b][a][d] for a in range(4))))
scalar=s.expand(sum(signs[a]*Ric[a,a] for a in range(4)))
target=s.diag(3*c,0,0,0);target[1:4,1:4]=-3*c*s.eye(3)+3*S
eq('original_metric_Ricci',Ric,target)
eq('scalar_curvature',scalar,-12*c)
TF=Ric-scalar*eta/4
targettf=s.zeros(4);targettf[1:4,1:4]=3*S
eq('tracefree_Ricci',TF,targettf)
eq('clock_curvature',s.Matrix(3,3,lambda i,j:R[0][i+1][0][j+1]),A)
for i in range(3):
    for j in range(3):
        for l in range(3):
            for m in range(3):
                d=lambda a,b: int(a==b)
                expected=d(i,l)*A[j,m]+d(j,m)*A[i,l]-d(i,m)*A[j,l]-d(j,l)*A[i,m]-3*sum(s.LeviCivita(i,j,p)*s.LeviCivita(l,m,q)*B[p,q] for p in range(3) for q in range(3))
                assert s.expand(R[i+1][j+1][l+1][m+1]-expected)==0
checks.append('all_spatial_Riemann_components')
W=[[[[s.expand(R[a][b][cc][d]-(eta[a,cc]*Ric[d,b]-eta[a,d]*Ric[cc,b]-eta[b,cc]*Ric[d,a]+eta[b,d]*Ric[cc,a])/2+scalar*(eta[a,cc]*eta[d,b]-eta[a,d]*eta[cc,b])/6) for d in range(4)] for cc in range(4)] for b in range(4)] for a in range(4)]
electric=s.Matrix(3,3,lambda i,j:W[0][i+1][0][j+1])
eq('electric_Weyl',electric,K+s.Rational(3,2)*S)
assert all(W[0][i][j][l]==0 for i in range(1,4) for j in range(1,4) for l in range(1,4))
checks.append('magnetic_Weyl_zero')
w2=s.expand(sum(signs[a]*signs[b]*signs[cc]*signs[d]*W[a][b][cc][d]**2 for a in range(4) for b in range(4) for cc in range(4) for d in range(4)))
eq('full_Weyl_contraction',w2,8*s.trace((K+s.Rational(3,2)*S)**2))
aa,bb=s.symbols('a b')
E=aa*Ric+bb*scalar*eta
eq('conditional_response_TF',E-s.trace(eta*E)*eta/4,aa*targettf)
zS=dict.fromkeys([t1,t2,t12,t13,t23],0)
eq('permitted_trace',E.subs(zS),-3*(aa+4*bb)*c*eta)
params=[c,k1,k2,k12,k13,k23,t1,t2,t12,t13,t23]
response_map=s.Matrix(list(TF)).jacobian(params)
assert response_map.rank()==5; checks.append('response_map_rank_5')
assert s.Matrix(list(electric.subs(zS))).jacobian([k1,k2,k12,k13,k23]).rank()==5
checks.append('surviving_electric_map_rank_5')

def tidal(n,v,w):
    kl=[1]+list(n);vl=[0]+list(v);wl=[0]+list(w)
    return s.expand(sum(vl[a]*kl[b]*wl[cc]*kl[d]*R[a][b][cc][d] for a in range(4) for b in range(4) for cc in range(4) for d in range(4)))
n=s.Matrix([s.Rational(3,5),s.Rational(4,5),0])
screens=[s.Matrix([-s.Rational(4,5),s.Rational(3,5),0]),s.Matrix([0,0,1])]
for i,vv in enumerate(screens):
    for j,ww in enumerate(screens):
        expected=2*(vv.T*K*ww)[0]+(n.T*K*n)[0]*(vv.dot(ww))-3*(vv.cross(n).T*S*ww.cross(n))[0]
        eq(f'general_coefficients_screen_{i}{j}',tidal(n,vv,ww),expected)
eq('screen_trace',sum(tidal(n,vv,vv) for vv in screens),3*(n.T*S*n)[0])
witness={c:0,k1:1,k2:-1,k12:0,k13:0,k23:0,**zS}
eq('witness_Ricci_zero',Ric.subs(witness),s.zeros(4))
eq('witness_Weyl_squared',w2.subs(witness),16)
e1=s.Matrix([1,0,0]);e2=s.Matrix([0,1,0]);e3=s.Matrix([0,0,1])
eq('witness_tide_positive',tidal(e3,e1,e1).subs(witness),2)
eq('witness_tide_negative',tidal(e3,e2,e2).subs(witness),-2)

# Exact adverse comparisons. A nonzero defect is the expected result here.
wrong_G2=-c*x*x.T+C.T*S*C
assert any(s.expand(z)!=0 for z in wrong_G2*x+q2*x)
checks.append('hostile_omitted_spatial_clock_coupling_detected')
spatial_Ric=Ric[1:4,1:4]+A
assert spatial_Ric != Ric[1:4,1:4]
checks.append('hostile_omitted_lapse_curvature_detected')
assert w2.subs(witness)!=0;checks.append('hostile_S_zero_implies_quiet_detected')
assert E.subs({aa:1,bb:0,c:1,**zS})!=s.zeros(4)
checks.append('hostile_DDR_means_E_zero_detected')
alpha=s.symbols('alpha');eq('hostile_area_trace_defect',(s.trace(B+alpha*s.eye(3))-s.trace(A))/3,alpha)
print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'named_check_count':len(checks),'parameter_count':len(params),'response_rank':5,'surviving_electric_rank':5,'witness':{'Ricci':'zero at center only','Weyl_squared':16,'screen_diagonal':[2,-2]},'not_checked':['neighborhood Einstein PDE','physical admission','time evolution','empirical prediction'],'scope':'exact symbolic second-jet checks; analytic class/converse proof reviewed separately'},indent=2))
