"""Finite exact anchors for ECS1; analytic domains/proofs live in INITIAL_DERIVATION."""
import json
import platform
import sympy as S

checks = []


def zero(label, expression):
    value = S.factor(S.simplify(expression))
    assert value == 0, (label, value)
    checks.append(label)


k, x, c, s = S.symbols('k x c s', positive=True)
for eps in [1, -1]:
    # c^2 + eps*s^2=1; no numerical curvature or distance is selected.
    reduce_c = lambda e: S.factor(S.together(e)).subs(c**2, 1-eps*s**2)
    r = s/(k*S.sqrt(1-eps*x*x))
    dx = k*(1-eps*x*x)
    v = eps*s*x/S.sqrt(1-eps*x*x)
    dt = c*(1-eps*x*x)/(c*c-eps*x*x)
    f = 1-eps*k*k*r*r
    zero(f'{eps}:radial_velocity', S.diff(r, x)*dx-v)
    zero(f'{eps}:geodesic_acceleration', S.diff(v, x)*dx-eps*k*k*r)
    zero(f'{eps}:Killing_energy', reduce_c(f*dt-c))
    zero(f'{eps}:proper_normalization', reduce_c(-f*dt*dt+v*v/f+1))
    zero(f'{eps}:retarded_derivative', reduce_c(dt-v/f-1/(c+v)))
    zero(f'{eps}:advanced_derivative', reduce_c(dt+v/f-1/(c-v)))
    zero(f'{eps}:incidence_polynomial',
         (x*x*(1-eps*x*x)-c*c*s*s).subs(c*c,1-eps*s*s)
         +eps*(x*x-s*s)*(x*x-eps*c*c).subs(c*c,1-eps*s*s))
    vb=eps*s*s/c
    zero(f'{eps}:outgoing_clock', reduce_c(c+vb-1/c))
    zero(f'{eps}:return_clock', reduce_c(1/(c-vb)-c/(2*c*c-1)))
    zero(f'{eps}:relay_norm', reduce_c(c*c-vb*vb-(2*c*c-1)/(c*c)))

f,v=S.symbols('f v', real=True)
zero('outgoing_endpoint_frequency', (f/(c-v)-(c+v)).subs(f,c*c-v*v))
zero('incoming_endpoint_frequency', ((c+v)/f-1/(c-v)).subs(f,c*c-v*v))
p=S.symbols('p',positive=True)
q=p/(2-p*p)
zero('scale_elimination', (c/(2*c*c-1)).subs(c,1/p)-q)
zero('total_echo', p*q-p*p/(2-p*p))
# The general static relation uses p + 1/q = 2c; only at incidence is c=1/p.
zero('static_energy_at_incidence', p+1/q-2/p)
assert q.subs(p,1)==1
checks.append('flat_limit')
assert q.subs(p,S.Rational(4,5))==S.Rational(10,17)
assert q.subs(p,S.Rational(6,5))==S.Rational(15,7)
checks.append('two_rational_sign_controls')

P,L=S.symbols('P L',real=True)
prediction=P-S.log(2-S.exp(2*P))
zero('log_relation_jet', S.series(prediction,P,0,3).removeO()-3*P-4*P*P)
kasner=[]
for exponent,a2,a3,b3,want in [
    (S.Rational(-1,3),S.Rational(2,9),S.Rational(-4,27),S.Rational(-28,27),S.Rational(-16,27)),
    (S.Rational(2,3),S.Rational(-1,9),S.Rational(2,27),S.Rational(14,27),S.Rational(8,27))]:
    Pjet=a2*L**2+a3*L**3
    Qjet=3*a2*L**2+b3*L**3
    residual=S.expand(Qjet-3*Pjet-4*Pjet**2)
    zero(f'Kasner_cubic_{exponent}',residual.coeff(L,3)-want)
    kasner.append({'exponent':str(exponent),'cubic_log_residual':str(want)})

t,r,y,z,K=S.symbols('t r y z K',real=True)
coords=(t,r,y,z)
F=1-K*r*r
g=S.diag(-F,1/F,1,1)
gi=g.inv()
Gamma=[[[S.simplify(sum(gi[a,d]*(S.diff(g[d,b],coords[c0])+S.diff(g[d,c0],coords[b])-S.diff(g[b,c0],coords[d])) for d in range(4))/2) for c0 in range(4)] for b in range(4)] for a in range(4)]
Ric=S.zeros(4)
for a in range(4):
    for b in range(4):
        Ric[a,b]=S.simplify(sum(S.diff(Gamma[d][a][b],coords[d])-S.diff(Gamma[d][a][d],coords[b])+sum(Gamma[d][d][e]*Gamma[e][a][b]-Gamma[d][b][e]*Gamma[e][a][d] for e in range(4)) for d in range(4)))
for a in range(4):
    for b in range(4):
        zero(f'product_Ric_{a}{b}',Ric[a,b]-(K*g[a,b] if a<2 and b<2 else 0))
R=S.simplify(S.trace(gi*Ric))
zero('product_scalar',R-2*K)
zero('product_tracefree_nonzero_component',Ric[2,2]-R*g[2,2]/4+K/2)

# A base-dependent positive transverse warp tests the mixed connection rather
# than only a constant block. General H proof is analytic, not sampled here.
w=S.Function('w')(t,r)
gw=S.diag(-F,1/F,w*w,w*w)
gwi=gw.inv()
for a in [2,3]:
    for b in [0,1]:
        for c0 in [0,1]:
            gabc=sum(gwi[a,d]*(S.diff(gw[d,b],coords[c0])+S.diff(gw[d,c0],coords[b])-S.diff(gw[b,c0],coords[d])) for d in range(4))/2
            zero(f'warp_sheet_geodesic_{a}{b}{c0}',gabc)

print(json.dumps({'status':'PASS','checks':len(checks),'check_labels':checks,
 'versions':{'python':platform.python_version(),'sympy':S.__version__},
 'saved_values':{'q':'p/(2-p^2)','total_echo':'p^2/(2-p^2)','product_Ric':[[str(Ric[i,j]) for j in range(4)] for i in range(4)],'product_scalar':str(R),'kasner':kasner},
 'limits':'Finite exact anchors, not domain/continuum/uniqueness or physical certification. Kasner coefficients copied from reviewed source; independent saved-artifact reconstruction belongs to fidelity check. General transverse-H argument is analytic.'},indent=2))
