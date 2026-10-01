"""Finite conditional algebra controls; no solver or physical-law selection."""
import json
import resource
import sys
import sympy as s

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
t, x, y, z = s.symbols('t x y z', real=True)
kap = s.symbols('kappa_x kappa_y kappa_z', real=True)
coords = (t, x, y, z)
a = [1 + q*t*t for q in kap]
g = s.diag(-1, *(ai*ai for ai in a))
gi = g.inv()
checks = []

def zero(name, value):
    result = s.simplify(value)
    if result != 0:
        raise AssertionError((name, result))
    checks.append(name)

# Direct connection/Ricci construction uses no H or clock identity.
Gamma = [[[s.simplify(sum(gi[i,d]*(s.diff(g[d,k],coords[j])
             + s.diff(g[d,j],coords[k])-s.diff(g[j,k],coords[d]))
             for d in range(4))/2) for k in range(4)]
             for j in range(4)] for i in range(4)]
R00 = sum(s.diff(Gamma[c][0][0],coords[c])
        - s.diff(Gamma[c][0][c],t)
        + sum(Gamma[c][c][d]*Gamma[d][0][0]
              - Gamma[c][0][d]*Gamma[d][0][c] for d in range(4))
        for c in range(4))
zero('direct_Ric00',R00+sum(s.diff(ai,t,2)/ai for ai in a))
zero('initial_Ric00',R00.subs(t,0)+2*sum(kap))
for j in range(4):
    zero('clock_geodesic_'+str(j),Gamma[j][0][0])
H = [s.diff(ai,t)/ai for ai in a]
zero('shear_difference',H[0]-H[1]
     - 2*t*(kap[0]-kap[1])/((1+kap[0]*t*t)*(1+kap[1]*t*t)))

k,L=s.symbols('k L',positive=True)
out_plus=s.tan(k*L)/k
ret_plus=s.tan(2*k*L)/k
out_minus=s.tanh(k*L)/k
ret_minus=s.tanh(2*k*L)/k
zero('positive_out_null',s.diff(out_plus,L)-(1+k*k*out_plus*out_plus))
zero('positive_return_null',s.diff(ret_plus,L)-2*(1+k*k*ret_plus*ret_plus))
zero('negative_out_null',s.diff(out_minus,L)-(1-k*k*out_minus*out_minus))
zero('negative_return_null',s.diff(ret_minus,L)-2*(1-k*k*ret_minus*ret_minus))
zero('positive_tick_ratio',1+k*k*out_plus*out_plus-1/s.cos(k*L)**2)
zero('negative_tick_ratio',1-k*k*out_minus*out_minus-1/s.cosh(k*L)**2)
zero('positive_two_way_ratio',1+k*k*ret_plus*ret_plus-1/s.cos(2*k*L)**2)
zero('negative_two_way_ratio',1-k*k*ret_minus*ret_minus-1/s.cosh(2*k*L)**2)
zero('positive_log_leading',s.limit(s.log(1+k*k*out_plus*out_plus)/L**2,L,0)-k*k)
zero('negative_log_leading',s.limit(s.log(1-k*k*out_minus*out_minus)/L**2,L,0)+k*k)

# Direct CK equation for the isotropic multiplier xi=a(t) U.
q=s.symbols('q',real=True)
isub={ki:q for ki in kap}
ai=1+q*t*t
xi_cov=s.Matrix([-ai,0,0,0])
nabla=s.Matrix(4,4,lambda i,j:s.diff(xi_cov[j],coords[i])
    -sum(Gamma[c][i][j].subs(isub)*xi_cov[c] for c in range(4)))
ck=(nabla+nabla.T)/2-s.diff(ai,t)*g.subs(isub)
for i in range(4):
    for j in range(4):
        zero('isotropic_CK_'+str(i)+str(j),ck[i,j])

print(json.dumps({'status':'PASS','check_count':len(checks),'checks':checks,
    'python':sys.version,'sympy':s.__version__,
    'scope':'Exact algebra on supplied finite controls, not native geometry or adoption.',
    'address_space_limit_bytes':2*1024**3,
    'wall_timeout_seconds':None,'cpu_timeout_seconds':None},indent=2))
