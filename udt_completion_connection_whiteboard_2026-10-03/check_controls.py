"""CCW1 finite exact diagnostics; supplied metrics, not native selection."""
import json, platform
import sympy as S

x=S.symbols('x', positive=True)
y,z,w=S.symbols('y z w', real=True)
coords=(x,y,z,w)
P=S.symbols('P', real=True)
results={}

def geometry(g):
    inv=g.inv()
    G=[[[S.simplify(sum(inv[a,d]*(S.diff(g[d,c],coords[b])
          +S.diff(g[d,b],coords[c])-S.diff(g[b,c],coords[d]))
          for d in range(4))/2) for c in range(4)]
          for b in range(4)] for a in range(4)]
    ric=S.zeros(4)
    for a in range(4):
        for b in range(4):
            ric[a,b]=S.simplify(sum(S.diff(G[c][a][b],coords[c])
                -S.diff(G[c][a][c],coords[b])
                +sum(G[c][a][b]*G[d][c][d]-G[d][a][c]*G[c][b][d]
                     for d in range(4)) for c in range(4)))
    scalar=S.simplify(sum(inv[a,b]*ric[a,b] for a in range(4) for b in range(4)))
    return G,ric,scalar

def zero(q):
    r=S.simplify(q)
    assert r==0,r
    return str(r)

def acceleration(G,u):
    return [S.simplify(sum(u[b]*S.diff(u[a],coords[b]) for b in range(4))
            +sum(G[a][b][c]*u[b]*u[c] for b in range(4) for c in range(4)))
            for a in range(4)]

# FREE: nonuniform regular conformal metric diagnostic, no field equation.
N=1+y*y
gn=S.diag(-N*N,1,1,1)/x**2
Gn,Rn,rn=geometry(gn)
expected=12/N**2-4*x**2/N
results['nonuniform_curvature']={
    'direct_scalar':str(rn),'identity_residual':zero(rn-expected),
    'boundary_scalar':str(S.limit(rn,x,0,dir='+')),
    'boundary_residual':zero(S.limit(rn,x,0,dir='+')-12/N**2),
    'direct_ricci':[[str(Rn[a,b]) for b in range(4)] for a in range(4)]}
# Omitting the leading term must fail at a definite regular point.
wrong=-4*x*x/N
assert S.simplify((rn-wrong).subs({x:S.Rational(1,2),y:S.Rational(1,3)}))!=0
results['nonuniform_curvature']['omitted_leading_term_detected']=True

# FREE: beta2 control, conformal factor x^2 has zero endpoint gradient.
eta=S.diag(-1,1,1,1)
Gb,Rb,rb=geometry(eta/x**4)
results['beta2']={'direct_scalar':str(rb),'residual':zero(rb-36*x*x),
                  'boundary_scalar':str(S.limit(rb,x,0,dir='+'))}
assert S.limit(rb,x,0,dir='+')==0

# FREE: actual clocks and a null correspondence in a supplied beta1 metric.
g=eta/x**2
G,R,scalar=geometry(g)
zero(scalar-12)
s=-S.log(1+x);tau=-S.log(x);Z=(1+x)/x
results['proper_clock_map']={
    'derivative_residual':zero(S.diff(tau,x)/S.diff(s,x)-Z),
    'gap_residue':str(S.limit(-s*Z,x,0,dir='+')),
    'log_rate':str(S.limit(S.log(Z)/tau,x,0,dir='+')),
    'curvature':str(scalar)}
assert S.limit(-s*Z,x,0,dir='+')==1
assert S.limit(S.log(Z)/tau,x,0,dir='+')==1

# Verify with P held constant BEFORE forming an event-indexed population.
u=S.Matrix([-x*S.sqrt(1+P*P*x*x),P*x*x,0,0])
k=S.Matrix([-x*x,x*x,0,0])
unit=zero((u.T*g*u)[0]+1)
geodesic=[zero(q) for q in acceleration(G,u)]
ray_null=zero((k.T*g*k)[0])
ray_affine=[zero(q) for q in acceleration(G,k)]
Pq=(1-x**-2)/2
gammaq=(x+x**-1)/2  # positive for x>0; squared identity checked below
zero(gammaq**2-(1+Pq**2*x*x))
omega=x*(gammaq-Pq*x)
zero(omega-1)
cases=[]
for q in [S.Rational(1,2),S.Rational(1,4),S.Rational(1,8)]:
    cases.append({'x':str(q),'constant_P_for_this_receiver':str(Pq.subs(x,q)),
                  'received_frequency':str(S.simplify(omega.subs(x,q)))})
results['fixed_emission_population']={
    'unit_residual':unit,'geodesic_residuals_constant_P':geodesic,
    'null_residual':ray_null,'affine_residuals':ray_affine,
    'population_received_frequency':str(S.simplify(omega)),
    'P_limit':str(S.limit(Pq,x,0,dir='+')),'cases':cases,
    'scope':'Different free receivers through (x,1-x); emission (1,0), omega_e=1. Unbounded preparation momentum; not a single accelerated curve or a bounded-population counterexample.'}
assert S.limit(Pq,x,0,dir='+')==-S.oo
print(json.dumps({'status':'PASS','python':platform.python_version(),
    'sympy':S.__version__,'families':4,'cases':7,
    'limits':'Exact supplied controls; general analytic proofs and physical attribution separate.',
    'results':results},indent=2))
