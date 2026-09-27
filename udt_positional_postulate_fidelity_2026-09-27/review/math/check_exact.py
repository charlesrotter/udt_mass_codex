"""Independent source-first algebra, no repository implementation imported."""
import json
import platform
import sympy as s

checks = []
expressions = {}

def zero(name, expression):
    entries = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    residuals = [s.simplify(s.trigsimp(x)) for x in entries]
    passed = all(x == 0 for x in residuals)
    checks.append({'name': name, 'passed': passed,
                   'residuals': [str(x) for x in residuals]})
    if not passed:
        raise AssertionError((name, residuals))

def einstein(g, coords):
    n = len(coords)
    inverse = g.inv()
    gamma = [[[s.simplify(sum(inverse[a,d] * (
        s.diff(g[d,c],coords[b]) + s.diff(g[d,b],coords[c])
        - s.diff(g[b,c],coords[d])) for d in range(n))/2)
        for c in range(n)] for b in range(n)] for a in range(n)]
    ric = s.zeros(n)
    for a in range(n):
        for b in range(n):
            ric[a,b] = s.simplify(sum(
                s.diff(gamma[c][a][b],coords[c])
                - s.diff(gamma[c][a][c],coords[b])
                + sum(gamma[c][c][d]*gamma[d][a][b]
                      - gamma[c][b][d]*gamma[d][a][c] for d in range(n))
                for c in range(n)))
    scalar = s.simplify(s.trace(inverse*ric))
    mixed = (inverse*ric - scalar*s.eye(n)/2).applyfunc(s.simplify)
    return mixed, scalar

u,v = s.symbols('u v', positive=True)
K = s.Matrix([[0,1],[1,0]])
eta = s.diag(-1,1)
P = s.diag(u,v)
zero('F2 conversion pairing', P.T*K*P-u*v*K)
D = s.diag(u,1/u)
zero('reciprocity preserves K',D.T*K*D-K)
zero('fixed Lorentz readout deforms',D.T*eta*D-s.diag(-u*u,1/(u*u)))

T,L,m = s.symbols('T L m', positive=True)
beta = s.symbols('beta',real=True)
h = s.Matrix([[-T*T,-T*T*beta],[-T*T*beta,L*L-T*T*beta*beta]])
zero('shifted determinant',h.det()+T*T*L*L)
J = s.diag(1,T*L)
hn = J.inv().T*h*J.inv()
zero('W1 normalized determinant',hn.det()+1)
zero('W1 reconstruct with density',J.T*hn*J-h)
zero('clock entry unaffected',hn[0,0]+T*T)
expressions['normalized_pair'] = str(hn)

x0,r,theta,az = s.symbols('x0 r theta az',real=True)
A,B,f = [s.Function(k)(r) for k in ('A','B','f')]
g = s.diag(-A,B,r*r,r*r*s.sin(theta)**2)
G,R = einstein(g,[x0,r,theta,az])
Gt = (1/B-1)/r**2-s.diff(B,r)/(r*B**2)
Gr = (1/B-1)/r**2+s.diff(A,r)/(r*A*B)
Gangular = (s.diff(A,r,2)/(2*A)-s.diff(A,r)**2/(4*A**2)
    -s.diff(A,r)*s.diff(B,r)/(4*A*B)
    +(s.diff(A,r)/A-s.diff(B,r)/B)/(2*r))/B
zero('generic areal Einstein all components',G-s.diag(Gt,Gr,Gangular,Gangular))
delta = (s.diff(A,r)/A+s.diff(B,r)/B)/(r*B)
zero('areal mixed Einstein difference',G[1,1]-G[0,0]-delta)
expressions['generic_G_t_t'] = str(s.factor(G[0,0]))
expressions['generic_G_r_r'] = str(s.factor(G[1,1]))
expressions['generic_G_r_r_minus_G_t_t'] = str(s.factor(delta))
expressions['generic_scalar_curvature'] = str(R)

Gf = G.subs({A:f,B:1/f}).doit().applyfunc(s.simplify)
E0 = r*s.diff(f,r)+f-1
E1 = r*s.diff(f,r)+r*r*s.diff(f,r,2)/2
zero('primary full four-dimensional Einstein',Gf-s.diag(E0/r**2,E0/r**2,E1/r**2,E1/r**2))
zero('reduced Bianchi relation',r*s.diff(E0,r)-2*E1)
Apar = (r*r*s.diff(f,r,2)-r*s.diff(f,r))/2
Aperp = 1-f+r*s.diff(f,r)/2
zero('angular trace and GR residual join',Apar+Aperp-E1+E0)
zero('PJC1 interlock',Apar-r*s.diff(Aperp,r))
C,a,b = s.symbols('C a b')
zero('vacuum full tensor',Gf.subs(f,1+C/r).doit())
zero('trace-balanced full tensor',Gf.subs(f,1+a*r*r+b/r).doit()-3*a*s.eye(4))
zero('trace-balanced angular sum',(Apar+Aperp).subs(f,1+a*r*r+b/r).doit())
zero('flat-screen missing sphere failure',(r*s.diff(f,r)+f).subs(f,1+C/r).doit()-1)
G2,R2 = einstein(s.diag(-f,1/f),[x0,r])
zero('two-dimensional Einstein is identically vacuous',G2)

# Positive exact diagnostic A=1+r², B=1, r>0. It is not a physical UDT model.
control_delta=s.simplify(delta.subs({A:1+r*r,B:1}).doit())
zero('nonreciprocal diagnostic difference',control_delta-2/(1+r*r))
expressions['nonreciprocal_control_G_difference'] = str(control_delta)
hc = s.diag(-(1+r*r),1)
Jc = s.diag(1,s.sqrt(1+r*r))
hnc = s.simplify(Jc.inv().T*hc*Jc.inv())
zero('nonreciprocal metric still pair-normalizes',hnc-s.diag(-(1+r*r),1/(1+r*r)))
expressions['control_areal_radius_after_tape_change'] = 'r remains areal radius; ds=sqrt(1+r^2) dr does not make s areal radius'
expressions['static_clock_and_null_speed'] = {
    'proper_time': 'd_tau=sqrt(A) dt', 'radial_proper_length':'d_ell=sqrt(B) dr',
    'radial_coordinate_null_speed':'abs(dr/dt)=c_E sqrt(A/B)',
    'radial_local_speed':'abs(d_ell/d_tau)=c_E',
    'reciprocal_specialization':'A=f, B=1/f: abs(dr/dt)=c_E f'}
print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),
    'expressions':expressions,'python':platform.python_version(),'sympy':s.__version__,
    'method':'Christoffel to Ricci to mixed Einstein; exact symbolic; no repository code',
    'scope':'positive C2 A,B on r>0 regular static spherical areal chart; external GR diagnostic only'},indent=2))
