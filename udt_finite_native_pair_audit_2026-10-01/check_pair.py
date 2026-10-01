"""FNA1 exact symbolic audit; supplied curvature/profile/query, no physics selection."""
import json, sys
import sympy as S

checks = []
def eq(name, a, b=0):
    d = a-b
    vals = list(d) if isinstance(d, S.MatrixBase) else [d]
    assert all(S.factor(S.simplify(x)) == 0 for x in vals), (name, str(d))
    checks.append(name)

# FREE supplied values. p!=1 here represents either sign; flat is separate.
p, m = S.symbols('p m', positive=True)
l = S.Symbol('lambda', real=True)
kap = (p*p-1)/(m*m)
ambient = S.diag(1/kap, -1, 1, 1, 1)
dot = lambda v,w: (v.T*ambient*w)[0]
basis = [S.eye(5)[:,i] for i in range(5)]
X,U,n,e2,e3 = basis
D = m*(U+n)
B = X+D
UB = (p*p*U+kap*m*X+kap*m*m*n)/p
nB = (n-kap*m*X)/p
source = [U,n,e2,e3]; target = [UB,nB,e2,e3]
eta = S.diag(-1,1,1,1)
eq('null_chord',dot(D,D)); eq('quadric_target',dot(B,B),1/kap)
eq('target_tetrad_gram',S.Matrix(4,4,lambda i,j:dot(target[i],target[j])),eta)
for i,V in enumerate(target): eq('target_tetrad_tangent_'+str(i),dot(B,V))
J = (1-l)*U+l*p*UB
point = X+l*D
eq('ribbon_tangent_clock',dot(point,J)); eq('ribbon_tangent_affine',dot(point,D))
A = 1+kap*m*m*l*(2-l)
h = S.Matrix([[dot(J,J),dot(J,D)],[dot(J,D),dot(D,D)]])
expected = S.Matrix([[-A,-m],[-m,0]])
eq('full_ribbon_pullback',h,expected)
eq('full_ribbon_determinant',h.det(),-m*m)
eq('orthogonal_ruler_positive_expression',h[1,1]-h[0,1]**2/h[0,0],m*m/A)
cal = S.diag(1,1/m)*h*S.diag(1,1/m)
eq('completed_shifted_metric',cal,S.Matrix([[-A,-1],[-1,0]]))
eq('completed_determinant',cal.det(),-1)
eq('completed_reconstruction',S.diag(1,m)*cal*S.diag(1,m),h)
eq('source_clock_normalization',A.subs(l,0),1)
eq('receiver_clock_normalization',A.subs(l,1),p*p)
eq('emission_frequency',-dot(D,U),m)
eq('reception_frequency',-dot(D,UB),m/p)
eq('clock_ratio_from_contractions',dot(D,U)/dot(D,UB),p)
eq('density_time_derivative',-dot(kap*X,D)-dot(U,p*UB-U),p*p-1)

def transported(V,t): return V-kap*dot(D,V)*(t*X+t*t*D/2)
P = [transported(V,1) for V in source]
for i,V in enumerate(source):
    Vt=transported(V,l)
    eq('transport_initial_'+str(i),Vt.subs(l,0),V)
    eq('transport_tangency_'+str(i),dot(point,Vt))
    eq('transport_ambient_ODE_'+str(i),S.diff(Vt,l),-kap*dot(D,Vt)*point)
eq('transport_preserves_full_gram',S.Matrix(4,4,lambda i,j:dot(P[i],P[j])),eta)
eq('transport_null_direction',transported(D,1),D)
Lam=S.Matrix(4,4,lambda i,j: eta[i,i]*dot(target[i],P[j]))
gamma=(p+1/p)/2; sh=(1/p-p)/2
expectedL=S.diag(S.ones(2),S.eye(2))
expectedL[:2,:2]=S.Matrix([[gamma,sh],[sh,gamma]])
eq('full_endpoint_morphism',Lam,expectedL)
eq('morphism_Lorentz',Lam.T*eta*Lam,eta)
eq('morphism_determinant',Lam.det(),1)
eq('outgoing_null_multiplier',Lam*S.Matrix([1,1,0,0]),S.Matrix([1,1,0,0])/p)
eq('projective_clock_component',Lam[1,0]/Lam[0,0],(1-p*p)/(1+p*p))
eq('inverse_is_same_arrow_reverse',expectedL.subs(p,1/p)*expectedL,S.eye(4))

# Full primary metric, angular diagnostics and a known-germ information check.
r, kappa, f = S.symbols('r kappa f', real=True)
theta=S.Symbol('theta', real=True)
v,w,u=S.symbols('v w u',real=True)
g=S.diag(-f,1/f,r*r,r*r*S.sin(theta)**2)
J0=S.Matrix([1,0,v/r,0]);J1=S.Matrix([0,1,w/r,u/(r*S.sin(theta))])
Jn=J0.row_join(J1); hn=Jn.T*g*Jn
eq('full_nonradial_pullback',hn,S.Matrix([[-f+v*v,v*w],[v*w,1/f+w*w+u*u]]))
eq('nonradial_density_squared',-hn.det(),(f-v*v)*(1/f+w*w+u*u)+v*v*w*w)
f0=1-kappa*r*r
phiprime=-S.diff(f0,r)/(2*f0)
phi2=S.diff(phiprime,r)
Pjet=r*phiprime;Qjet=r*r*phi2
eq('G201_parallel',f0*(2*Pjet**2+Pjet-Qjet))
eq('G201_perpendicular',1-f0*(1+Pjet))
eq('G260_E0',r*S.diff(f0,r)+f0-1,-3*kappa*r*r)
eq('G260_E1',r*S.diff(f0,r)+r*r*S.diff(f0,r,2)/2,-3*kappa*r*r)
eq('full_metric_determinant',g.det(),-r**4*S.sin(theta)**2)
eq('positive_chart_at_first_reception',f0.subs(r,m),2-p*p)

entries=S.symbols('g00 g01 g02 g03 g11 g12 g13 g22 g23 g33')
gm=S.Matrix([[entries[0],entries[1],entries[2],entries[3]],
             [entries[1],entries[4],entries[5],entries[6]],
             [entries[2],entries[5],entries[7],entries[8]],
             [entries[3],entries[6],entries[8],entries[9]]])
ee=[S.eye(4)[:,i] for i in range(4)]
directions=[ee[i] for i in range(1,4)]+[ee[i]+ee[j] for i,j in [(1,2),(1,3),(2,3)]]
records=[ee[0].row_join(d).T*gm*ee[0].row_join(d) for d in directions]
measurement=S.Matrix([q[i,j] for q in records for i,j in [(0,0),(0,1),(1,1)]])
assert measurement.jacobian(entries).rank()==10
checks.append('six_known_pair_rank_ten')
for j,(a,b) in enumerate([(1,2),(1,3),(2,3)]):
    eq('spatial_cross_reconstruction_'+str(j),(records[3+j][1,1]-records[a-1][1,1]-records[b-1][1,1])/2,gm[a,b])

flat_h=S.Matrix([[-1,-m],[-m,0]])
eq('flat_pair_determinant',flat_h.det(),-m*m)
eq('flat_endpoint_morphism_limit',expectedL.subs(p,1),S.eye(4))
eq('deleting_shift_destroys_null_ribbon_pair',S.diag(-A,0).det())
print(json.dumps({'status':'PASS','check_count':len(checks),'checks':checks,
    'ribbon_h':str(expected),'completed_h':str(S.simplify(cal)),
    'morphism':str(expectedL),'six_pair_rank':10,
    'python':sys.version,'sympy':S.__version__,
    'scope':'Exact identities for supplied positive/negative constant curvature and explicit germs; regular domains/nearby-emission extension and source/admission limits require the analytic proof. Not native geometry selection, empirical recovery or global completeness.'},indent=2))
