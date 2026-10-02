"""Independent ERC1 source-first checks; no ERC1 parent-code imports."""
import json, platform
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

checks = {}
def exact(name, expression):
    reduced = s.simplify(expression)
    checks[name] = {'pass': reduced == 0, 'residual': str(reduced)}
    if reduced != 0:
        raise AssertionError((name, reduced))

# Metric-first FLRW geometry. Diagonal metric, every connection/Ricci index kept.
t,x,y,z = s.symbols('t x y z', real=True)
coords = [t,x,y,z]
b = s.Function('b')(t)
alpha = s.symbols('alpha', nonzero=True)
g = s.diag(-1,b*b,b*b,b*b)
gi = s.diag(-1,1/b**2,1/b**2,1/b**2)
Gamma = [[[s.simplify(sum(gi[i,k]*(s.diff(g[k,j],coords[l])+
    s.diff(g[k,l],coords[j])-s.diff(g[j,l],coords[k]))/2
    for k in range(4))) for l in range(4)] for j in range(4)] for i in range(4)]
Ric = s.zeros(4)
for i in range(4):
    for j in range(4):
        Ric[i,j] = s.simplify(sum(s.diff(Gamma[k][i][j],coords[k])-
            s.diff(Gamma[k][i][k],coords[j])+sum(
            Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k]
            for l in range(4)) for k in range(4)))
R = s.simplify(sum(gi[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
H = s.diff(b,t)/b
exact('FLRW_scalar_metric',R-6*(s.diff(H,t)+2*H**2))
hess = s.Matrix(4,4,lambda i,j:s.diff(R,coords[i],coords[j])-
    sum(Gamma[k][i][j]*s.diff(R,coords[k]) for k in range(4)))
box = s.simplify(sum(gi[i,j]*hess[i,j] for i in range(4) for j in range(4)))
exact('FLRW_box_metric',box+s.diff(R,t,2)+3*H*s.diff(R,t))
E = s.simplify(Ric-R*g/2+alpha*(2*R*Ric-R**2*g/2+2*(g*box-hess)))
F = 1+2*alpha*R
expected00 = 3*F*H**2-alpha*R**2/2+6*alpha*H*s.diff(R,t)
expectedii = -(2*s.diff(H,t)+3*H**2)+alpha*(2*R*(s.diff(H,t)+3*H**2)-
    R**2/2-2*s.diff(R,t,2)-4*H*s.diff(R,t))
exact('FLRW_E00_original',E[0,0]-expected00)
for i in range(1,4):
    exact(f'FLRW_E{i}{i}_original',E[i,i]/b**2-expectedii)
for i in range(4):
    for j in range(4):
        if i!=j:
            exact(f'FLRW_offdiagonal_{i}{j}',E[i,j])
exact('FLRW_shape',E[0,0]+E[1,1]/b**2+2*F*s.diff(H,t)-
    2*alpha*(H*s.diff(R,t)-s.diff(R,t,2)))
exact('FLRW_trace',sum(gi[i,j]*E[i,j] for i in range(4) for j in range(4))+R-6*alpha*box)
# Covector time divergence, from the generic metric connection itself.
div0 = sum(gi[i,j]*(s.diff(E[j,0],coords[i])-
    sum(Gamma[k][i][j]*E[k,0]+Gamma[k][i][0]*E[j,k] for k in range(4)))
    for i in range(4) for j in range(4))
exact('FLRW_offshell_divergence',div0)

# Static linearized vacuum tensor checked through radial/tangential Hessian eigenvalues.
r,m,A,M = s.symbols('r m A M', positive=True)
al = 1/(6*m*m)
U = A*s.exp(-m*r)/r
phi = -M/r-al*U
psi = -M/r+al*U
lap = lambda f:s.diff(f,r,2)+2*s.diff(f,r)/r
exact('static_scalar_definition',2*(2*lap(psi)-lap(phi))-U)
exact('static_E00',2*lap(psi)-2*al*lap(U))
d = psi-phi
exact('static_Err',s.diff(d,r,2)-lap(d)+2*al*(lap(U)-s.diff(U,r,2)))
exact('static_Etangent',s.diff(d,r)/r-lap(d)+2*al*(lap(U)-s.diff(U,r)/r))
Na,Nb = s.symbols('Na Nb',positive=True)
exact('static_echo_product',(Nb/Na)*(Na/Nb)-1)
# Catch controls: wrong potential sign and omitted Hessian are actually detected.
checks['catch_wrong_psi'] = {'pass': s.simplify(2*lap(phi)-2*al*lap(U))!=0}
checks['catch_omitted_hessian'] = {'pass': s.simplify(s.diff(d,r,2)-lap(d)+2*al*lap(U))!=0}

# Actual affine null geodesics in supplied b(t)=1+t^2 (a protocol control, not a B solution).
start = 0.1
L = 0.2
tb = np.tan(np.arctan(start)+L)
tf = np.tan(np.arctan(start)+2*L)
aa = lambda tt:1+tt*tt
pred_p = aa(tb)/aa(start)
pred_q = aa(tf)/aa(tb)

def affine_leg(t0,x0,direction,target,rtol,atol):
    def rhs(lam,state):
        tt,xx,kt,kx = state
        av = aa(tt)
        return [kt,kx,-av*2*tt*kx*kx,-4*tt/av*kt*kx]
    def event(lam,state):return state[1]-target
    event.terminal = True
    event.direction = direction
    out=solve_ivp(rhs,(0,3),[t0,x0,1.,direction/aa(t0)],events=event,
        rtol=rtol,atol=atol,method='DOP853')
    if len(out.t_events[0])!=1:raise AssertionError('missing_control_arrival')
    final=out.y_events[0][0]
    null_max=float(np.max(np.abs(-out.y[2]**2+aa(out.y[0])**2*out.y[3]**2)))
    return final,1/final[2],null_max

clock_results=[]
for rtol,atol,gate in [(1e-8,1e-10,1e-7),(1e-11,1e-13,1e-9)]:
    fwd,p,nf=affine_leg(start,0,1,L,rtol,atol)
    ret,q,nr=affine_leg(fwd[0],L,-1,0,rtol,atol)
    errors={'arrival':abs(float(fwd[0])-tb),'echo':abs(float(ret[0])-tf),
        'p':abs(float(p)-pred_p),'q':abs(float(q)-pred_q),
        'product':abs(float(p*q)-aa(tf)/aa(start)),'null':max(nf,nr)}
    passed=max(errors.values())<gate
    clock_results.append(dict(rtol=rtol,atol=atol,gate=gate,errors=errors,
        arrival=float(fwd[0]),echo=float(ret[0]),p=float(p),q=float(q),passed=passed))
    if not passed:raise AssertionError(clock_results[-1])

result={'status':'PASS','versions':{'python':platform.python_version(),'sympy':s.__version__,
    'numpy':np.__version__,'scipy':scipy.__version__},'exact_and_catch_checks':checks,
    'actual_affine_null_controls':clock_results,
    'scope':'source-first conditional algebra and supplied clock protocol; no physical adoption'}
assert all(v['pass'] for v in checks.values())
print(json.dumps(result,indent=2))
