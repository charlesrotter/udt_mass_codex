#!/usr/bin/env python3
"""Independent exact spot checks; analytic quantifiers are in SOURCE_FIRST.md.
No imports from parent or construction-worker code. No numerical approximation.
"""
import json
import platform
import sympy as s

checks = {}
a, b, A, B, C = s.symbols('a b A B C')
eta = s.diag(-1, 1, 1, 1)
k = s.Matrix([1, 2, 0, 0])
kup = eta*k
k2 = (k.T*kup)[0]
uv = s.symbols('u0:10')
vv = s.symbols('v0:10')
pairs4 = [(i,j) for i in range(4) for j in range(i,4)]
def symmetric(values, pairs, n):
    m = s.zeros(n)
    for value, (i,j) in zip(values,pairs):
        m[i,j] = m[j,i] = value
    return m
u, v = symmetric(uv,pairs4,4), symmetric(vv,pairs4,4)
def tr4(q):
    return s.trace(eta*q)
def kk(q):
    return (kup.T*q*kup)[0]
def linear_ricci(q):
    return (k*(q*kup).T+(q*kup)*k.T-k2*q-tr4(q)*k*k.T)/2
def response(q):
    return a*linear_ricci(q)+b*(kk(q)-k2*tr4(q))*eta
def pair(q,r):
    return s.trace(eta*q*eta*r)
antisym = s.expand(pair(u,response(v))-pair(v,response(u)))
factor = (a/2+b)*(tr4(u)*kk(v)-tr4(v)*kk(u))
checks['flat_full_symmetric_helmholtz_identity'] = s.expand(antisym-factor) == 0
checks['helmholtz_nonvacuous'] = antisym != 0
checks['helmholtz_einstein_relation'] = s.expand(antisym.subs(b,-a/2)) == 0
checks['helmholtz_tracefree_response_fails'] = s.expand(antisym.subs(b,-a/4)) != 0

# A nonconstant, nondiagonal positive metric, det(base)=1. All six momenta
# are independent nonconstant components; their tensor density weight is +1.
x,y,z = s.symbols('x y z')
coords = [x,y,z]
scale = 1+x
L = s.Matrix([[1,0,0],[1,1,0],[0,1,1]])
h = scale**2*(L*L.T)
hi = h.inv()
root_h = scale**3   # fixture domain x > -1
P = s.Matrix([[x+y*z, x*y+z, z*x+y],
              [x*y+z, y*y+x, y*z+x*x],
              [z*x+y, y*z+x*x, z*z+y]])
pi = root_h*P
pi_lower = h*pi*h
trace_pi = s.trace(h*pi)
gamma = [[[s.simplify(sum(hi[i,l]*(s.diff(h[l,j],coords[k_])+s.diff(h[l,k_],coords[j])-s.diff(h[j,k_],coords[l])) for l in range(3))/2)
            for k_ in range(3)] for j in range(3)] for i in range(3)]
def hessian(f):
    return s.Matrix(3,3,lambda i,j:s.diff(f,coords[i],coords[j])-sum(gamma[k_][i][j]*s.diff(f,coords[k_]) for k_ in range(3)))
def potential_derivative(f):
    hs=hessian(f)
    return C*root_h*(hi*hs*hi-hi*s.trace(hi*hs))
def kinetic_derivative(f):
    return 2*f/root_h*(A*pi_lower+B*trace_pi*h)
N=x*x*y+z+x
M=x*y*y+z*z+y
contract=lambda q,r:sum(q[i,j]*r[i,j] for i in range(3) for j in range(3))
direct=contract(potential_derivative(N),kinetic_derivative(M))-contract(kinetic_derivative(N),potential_derivative(M))
w=s.Matrix([N*s.diff(M,c)-M*s.diff(N,c) for c in coords])
div_pi=s.Matrix([sum(s.diff(pi[j,i],coords[j])+sum(gamma[i][j][k_]*pi[j,k_] for k_ in range(3)) for j in range(3)) for i in range(3)])
grad_trace=s.Matrix([s.diff(trace_pi,c)-sum(gamma[j][j][i] for j in range(3))*trace_pi for i,c in enumerate(coords)])
predicted=2*C*(A*(div_pi.T*w)[0]-(A+2*B)*(grad_trace.T*hi*w)[0])
Q=A*pi-(A+2*B)*trace_pi*hi
flux=Q*w
div_flux=sum(s.diff(flux[i],coords[i]) for i in range(3))
checks['curved_nondiagonal_density_bracket_mod_divergence']=s.simplify(direct-predicted+2*C*div_flux)==0
# Omitting scalar-density connection is a real defect, not an equivalent notation.
wrong_grad=s.Matrix([s.diff(trace_pi,c) for c in coords])
wrong=2*C*(A*(div_pi.T*w)[0]-(A+2*B)*(wrong_grad.T*hi*w)[0])
checks['omitted_density_connection_detected']=s.simplify(direct-wrong+2*C*div_flux)!=0
checks['strong_lorentzian_coefficients']=s.solve([A*C+1,C*(A+2*B)],[B,C],dict=True)==[{B:-A/2,C:-1/A}]
checks['C_zero_cannot_close_strongly']=s.simplify((A*C+1).subs(C,0))==1
checks['A_zero_cannot_close_strongly']=s.simplify((A*C+1).subs(A,0))==1
checks['kinetic_trace_degeneracy_not_selected']=s.simplify((A+3*B).subs(B,-A/2))==-A/2
out={
  'python':platform.python_version(),'sympy':s.__version__,
  'arithmetic':'exact symbolic; no floating point',
  'checks':checks, 'passed':sum(checks.values()), 'total':len(checks),
  'helmholtz_obstruction':'(a/2+b)*(tr(u)*k.v.k-tr(v)*k.u.k)',
  'canonical_bracket':'-A*C*D[w]-2*C*(A+2*B)*integral(w^i*nabla_i(pi))',
  'scope':'Independent finite exact checks support, but do not replace, analytic derivations.'
}
print(json.dumps(out,indent=2,sort_keys=True))
assert all(checks.values()), out
