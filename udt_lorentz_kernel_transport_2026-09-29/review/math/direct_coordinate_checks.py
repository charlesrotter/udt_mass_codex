"""Coordinate-first independent reviewer implementation; no author code imported."""
import sympy as s
import json, platform
x0,x1=s.symbols('t x',real=True); coords=[x0,x1]
T=s.Function('T')(x0,x1); L=s.Function('L')(x0,x1); b=s.Function('b')(x0,x1)
def clean(z): return s.factor(s.cancel(s.together(z)))
results={}
def chk(name,z):
    if isinstance(z,s.MatrixBase): ok=all(clean(v)==0 for v in z)
    else: ok=clean(z)==0
    results[name]=bool(ok)
    assert ok,(name,z)
g=s.Matrix([[-T*T,-T*T*b],[-T*T*b,L*L-T*T*b*b]])
gi=g.inv()
Gamma=[[[clean(sum(gi[i,a]*(s.diff(g[a,j],coords[k])+s.diff(g[a,k],coords[j])-s.diff(g[j,k],coords[a])) for a in range(2))/2) for k in range(2)] for j in range(2)] for i in range(2)]
# Derived frame connection from coordinate connection, without torsion equations.
frame=s.Matrix([[1/T,-b/L],[0,1/L]])
coframe=frame.inv()
conn=[]
for mu in range(2):
    gm=s.Matrix([[Gamma[i][mu][j] for j in range(2)] for i in range(2)])
    conn.append((coframe*(frame.diff(coords[mu])+gm*frame)).applyfunc(clean))
w0=(s.diff(T,x1)-s.diff(T*b,x0))/L
w1=w0*b+s.diff(L,x0)/T
J=s.Matrix([[0,1],[1,0]])
chk('frame_connection_t',conn[0]-w0*J)
chk('frame_connection_x',conn[1]-w1*J)
# Direct coordinate curvature R^rho_{sigma mu nu}, then Ric_{sigma nu}.
def riem(rho,sig,mu,nu):
    return s.diff(Gamma[rho][nu][sig],coords[mu])-s.diff(Gamma[rho][mu][sig],coords[nu])+sum(Gamma[rho][mu][z]*Gamma[z][nu][sig]-Gamma[rho][nu][z]*Gamma[z][mu][sig] for z in range(2))
ric=s.Matrix([[clean(sum(riem(rho,sig,rho,nu) for rho in range(2))) for nu in range(2)] for sig in range(2)])
rsc=clean(sum(gi[i,j]*ric[i,j] for i in range(2) for j in range(2)))
r_cartan=2*(s.diff(w1,x0)-s.diff(w0,x1))/(T*L)
chk('coordinate_curvature_matches_candidate',rsc-r_cartan)
chk('ricci_symmetric',ric-ric.T)
chk('two_dimensional_ricci_trace',ric-rsc*g/2)
# Affine geodesic derivative of omega=T*(k^t+b*k^x), calculated in coordinates.
w=s.symbols('omega',positive=True)
clock_cov=s.Matrix([T,T*b])
for eps in [-1,1]:
    k=frame*s.Matrix([w,eps*w])
    kdot=s.Matrix([-sum(Gamma[i][j][m]*k[j]*k[m] for j in range(2) for m in range(2)) for i in range(2)])
    wdot=sum(s.diff(clock_cov[i],coords[j])*k[j]*k[i] for i in range(2) for j in range(2))+(clock_cov.dot(kdot))
    chk('affine_frequency_orientation_'+str(eps),wdot+eps*w*(w0*k[0]+w1*k[1]))
phi=s.Function('phi')(x0,x1)
subs={T:s.exp(-phi),L:s.exp(phi),b:s.Integer(0)}
def sub(z):return s.simplify(z.subs(subs).doit())
rec0=sub(w0);rec1=sub(w1)
chk('reciprocal_connection_t',rec0+s.exp(-2*phi)*s.diff(phi,x1))
chk('reciprocal_connection_x',rec1-s.exp(2*phi)*s.diff(phi,x0))
chk('reciprocal_curvature',sub(rsc)-2*(s.diff(s.exp(2*phi)*s.diff(phi,x0),x0)+s.diff(s.exp(-2*phi)*s.diff(phi,x1),x1)))
for eps in [-1,1]:
    xd=eps*s.exp(-2*phi)
    # Derivative of Phi_clock along t = -eps*(w_t+w_x*x').
    chk('dynamic_clock_depth_orientation_'+str(eps),-eps*(rec0+rec1*xd)-(s.diff(phi,x0)+s.diff(phi,x1)*xd-2*s.diff(phi,x0)))
flat={T:s.Integer(1),L:1+x0,b:s.Integer(0)}
chk('flat_expanding_control_curvature',rsc.subs(flat).doit())
chk('flat_expanding_control_w_t',w0.subs(flat).doit())
chk('flat_expanding_control_w_x',w1.subs(flat).doit()-1)
# Curvature sign is checked against both temporal and static coordinate sectors.
a=s.Function('a')(x0)
chk('flrw_curvature_sign',rsc.subs({T:s.Integer(1),L:a,b:s.Integer(0)}).doit()-2*s.diff(a,x0,2)/a)
f=s.Function('f')(x1)
chk('static_curvature_sign',rsc.subs({T:s.sqrt(f),L:1/s.sqrt(f),b:s.Integer(0)}).doit()+s.diff(f,x1,2))
# Every Lorentz generator is a bracket, with explicit elementary matrices.
boost=[]
for i in range(1,4):
    M=s.zeros(4);M[0,i]=M[i,0]=1;boost.append(M)
rot=[]
for i,j in [(2,3),(3,1),(1,2)]:
    M=s.zeros(4);M[i,j]=-1;M[j,i]=1;rot.append(M)
def comm(A,B):return A*B-B*A
for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]:
    chk('rotation_bracket_'+str(k),comm(rot[i],rot[j])-rot[k])
    chk('boost_rotation_bracket_'+str(k),comm(rot[i],boost[j])-boost[k])
    chk('boost_bracket_'+str(k),comm(boost[i],boost[j])+rot[k])
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,'arithmetic':'symbolic exact','checks':results,'count':len(results),'curvature_expression':str(rsc)},indent=2))
