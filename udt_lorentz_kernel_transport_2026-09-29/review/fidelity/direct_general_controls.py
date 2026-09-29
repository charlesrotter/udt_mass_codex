import json
import platform
import sympy as s

checks={}
def check(name, expr):
    ok = expr if isinstance(expr,bool) else s.simplify(expr)==0
    if not ok: raise AssertionError((name,expr))
    checks[name]=True

def geometry(g,coords):
    n=len(coords); gi=s.simplify(g.inv())
    G=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(n))) for c in range(n)] for b in range(n)] for a in range(n)]
    Ric=s.zeros(n)
    for b in range(n):
        for d in range(n):
            Ric[b,d]=s.simplify(sum(s.diff(G[a][d][b],coords[a])-s.diff(G[a][a][b],coords[d])+sum(G[a][a][c]*G[c][d][b]-G[a][d][c]*G[c][a][b] for c in range(n)) for a in range(n)))
    scalar=s.simplify(sum(gi[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
    return G,Ric,scalar

t,x=s.symbols('t x',real=True); co=[t,x]
T=s.Function('T')(t,x); L=s.Function('L')(t,x); b=s.Function('b')(t,x)
g=s.Matrix([[-T*T,-T*T*b],[-T*T*b,L*L-T*T*b*b]])
G,Ric,R=geometry(g,co)
# Coordinate basis columns of orthonormal frame, inverted independently from theta.
Theta=s.Matrix([[T,T*b],[0,L]]); E=Theta.inv(); eta=s.diag(-1,1)
check('frame_metric',s.simplify(E.T*g*E)==eta)
check('determinant_complete_shift',g.det()+T*T*L*L)
A=(s.diff(T,x)-s.diff(T*b,t))/L
claimed=[A,A*b+s.diff(L,t)/T]
J=s.Matrix([[0,1],[1,0]])
for j in range(2):
    G_j=s.Matrix([[G[a][j][c] for c in range(2)] for a in range(2)])
    W=s.simplify(Theta*(E.diff(co[j])+G_j*E))
    check('full_frame_connection_'+str(j),s.simplify(W-claimed[j]*J)==s.zeros(2))
curv=2*(s.diff(claimed[1],t)-s.diff(claimed[0],x))/(T*L)
check('full_coordinate_Ricci_scalar',R-curv)
check('Ricci_symmetry',Ric[0,1]-Ric[1,0])
check('two_dimensional_Ricci_trace',s.simplify(Ric-R*g/2)==s.zeros(2))
# Null k = E*(1,epsilon) at a point, choosing omega=1 there.
# omega=T*(k^t+b*k^x), covector cov=T*(1,b).
# Differentiating omega along the affine geodesic gives (partial cov)*kk-cov*Gamma*kk.
cov=[T,T*b]
for eps in [-1,1]:
    k=E*s.Matrix([1,eps])
    check('null_norm_'+str(eps),(k.T*g*k)[0])
    check('clock_frequency_'+str(eps),sum(cov[a]*k[a] for a in range(2))-1)
    coordinate_derivative=sum(s.diff(cov[a],co[c])*k[c]*k[a]-sum(cov[d]*G[d][c][a]*k[c]*k[a] for d in range(2)) for c in range(2) for a in range(2))
    claimed_derivative=-eps*sum(claimed[j]*k[j] for j in range(2))
    check('full_coordinate_null_frequency_'+str(eps),coordinate_derivative-claimed_derivative)

# Active shift and time/spatial derivatives; positivity T,L follows from exponentials.
subs={T:s.exp(t+x),L:s.exp(2*t-x),b:t*x}
gex=s.simplify(g.subs(subs)); _,_,Rex=geometry(gex,co)
claimex=s.simplify(curv.subs(subs).doit())
check('active_shift_independent_reconstruction',Rex-claimex)
check('active_shift_curvature_nonzero',s.simplify(Rex.subs({t:0,x:0}))!=0)
# Flat expanding-coordinate timing example.
gm=s.diag(-1,(1+t)**2); _,_,Rm=geometry(gm,co)
check('Milne_flat',Rm)
e=s.symbols('e',real=True)
arrival=2*e+1
check('Milne_null_incidence',s.simplify(s.log((1+arrival)/(1+e))-s.log(2)))
check('Milne_clock_ratio',s.diff(arrival,e)-2)

phi=s.Function('phi')(t,x)
gp=s.diag(-s.exp(-2*phi),s.exp(2*phi)); _,_,Rp=geometry(gp,co)
check('reciprocal_curvature',Rp-2*(s.diff(s.exp(2*phi)*s.diff(phi,t),t)+s.diff(s.exp(-2*phi)*s.diff(phi,x),x)))
y=s.symbols('y',positive=True)
S=s.Matrix([[1,1],[-1,1]])/s.sqrt(2); D=s.diag(1/y,y); K=s.Matrix([[0,1],[1,0]])
check('candidate_dual_form_basis',S.T*K*S==eta)
check('candidate_physical_form_basis',S.T*eta*S==-K)
check('candidate_boost_conjugacy',S.inv()*D*S==s.Matrix([[(y+1/y)/2,(1/y-y)/2],[(1/y-y)/2,(y+1/y)/2]]))
print(json.dumps({'status':'PASS','count':len(checks),'checks':checks,'active_shift_R_at_origin':str(s.simplify(Rex.subs({t:0,x:0}))),'python':platform.python_version(),'sympy':s.__version__},indent=2))
