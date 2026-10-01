"""Original-coordinate Kasner polynomial/clock control, after candidate exposure."""
import json
import sys
import sympy as S

t=S.symbols('t',positive=True)
x,y,z=S.symbols('x y z',real=True)
L,ell=S.symbols('L ell',real=True)
p=S.symbols('p',real=True)
coord=(t,x,y,z)
ps=(S.Rational(-1,3),S.Rational(2,3),S.Rational(2,3))
g=S.diag(-1,*(t**(2*v) for v in ps));gi=g.inv()
checks=[]
def equal(name,actual,expected=0):
    residue=S.simplify(actual-expected)
    if residue!=0:raise AssertionError((name,residue))
    checks.append(name)
def trunc(expr,var=L,degree=3):
    return S.series(expr,var,0,degree).removeO().expand()

Gamma=[[[S.simplify(sum(gi[a,d]*(S.diff(g[d,c],coord[b])
        +S.diff(g[d,b],coord[c])-S.diff(g[b,c],coord[d]))
        for d in range(4))/2) for c in range(4)]for b in range(4)]for a in range(4)]
def R(a,b,c,d):
    return S.simplify(S.diff(Gamma[a][d][b],coord[c])-S.diff(Gamma[a][c][b],coord[d])
        +sum(Gamma[a][c][e]*Gamma[e][d][b]-Gamma[a][d][e]*Gamma[e][c][b] for e in range(4)))
for b in range(4):
    for d in range(4):
        equal('Ric_'+str(b)+str(d),sum(R(a,b,a,d) for a in range(4)))
tidal=[R(i,0,i,0).subs(t,1) for i in range(1,4)]
equal('tidal_trace',sum(tidal))
if all(v==0 for v in tidal):raise AssertionError('FLAT_CONTROL_NOT_ALLOWED')

# Derive/check the preparation jets in the original synchronous chart.
# They are a spacetime spacelike geodesic, not the t=1 spatial coordinate line.
tp=1-p*ell**2/2
xp=ell+p**2*ell**3/3
Vt=1+p**2*ell**2/2
Vx=-p*ell
equal('spacelike_t_jet',trunc(S.diff(tp,ell,2)+p*tp**(2*p-1)*S.diff(xp,ell)**2,ell,1))
equal('spacelike_x_jet',trunc(S.diff(xp,ell,2)+2*p/tp*S.diff(tp,ell)*S.diff(xp,ell),ell,2))
equal('parallel_time_jet',trunc(S.diff(Vt,ell)+p*tp**(2*p-1)*S.diff(xp,ell)*Vx,ell,2))
equal('parallel_space_jet',trunc(S.diff(Vx,ell)+p/tp*(S.diff(tp,ell)*Vx+S.diff(xp,ell)*Vt),ell,1))
equal('initial_unit_clock',trunc(-Vt**2+tp**(2*p)*Vx**2,ell,3),-1)

# Exact spatial momentum is conserved on each receiver geodesic.
# The displayed preparation gives C=-p L+O(L^3), enough for quadratic ratios.
C=-p*L
equal('prepared_momentum_jet',trunc((tp**(2*p)*Vx).subs(ell,L),L,3),C)
tb=1+L-p*L**2/2
ta=1+2*L
xb=L-p*L*(tb-1)
eta=lambda delta:delta-p*delta**2/2
equal('outgoing_null_incidence_jet',trunc(eta(tb-1)-xb))
equal('return_null_incidence_jet',trunc(eta(ta-1)-eta(tb-1)-xb))

ab=trunc(tb**p);aa=trunc(ta**p)
w=trunc(C/ab)
gamma=trunc(S.sqrt(1+w*w))
# Frequency contraction and implicit neighboring-arrival differentiation give
# these expressions while C and prepared worldlines remain fixed with emission.
out=trunc(ab/(gamma-w))
ret=trunc(aa/ab*(gamma+w))
equal('outgoing_original_coordinate_coefficient',out,1+p*(p-1)*L**2/2)
equal('return_original_coordinate_coefficient',ret,1+3*p*(p-1)*L**2/2)
for i,exponent in enumerate(ps):
    equal('out_vs_direct_tidal_'+str(i),out.subs(p,exponent),1-tidal[i]*L**2/2)
    equal('return_vs_direct_tidal_'+str(i),ret.subs(p,exponent),1-3*tidal[i]*L**2/2)
equal('outgoing_triad_mean',sum(out.subs(p,v)-1 for v in ps))
equal('return_triad_mean',sum(ret.subs(p,v)-1 for v in ps))

print(json.dumps({'status':'PASS','checks':checks,'check_count':len(checks),
    'kasner_exponents':[str(v) for v in ps],
    'direct_tidal_at_t1':[str(v) for v in tidal],
    'outgoing_L2_coefficients':[str(v*(v-1)/2)for v in ps],
    'return_L2_coefficients':[str(3*v*(v-1)/2)for v in ps],
    'scope':'Finite symbolic Taylor check in supplied nonflat Ricci-flat Kasner; not a ray/field solve, native UDT countermodel, or generic 4D proof.',
    'python':sys.version,'sympy':S.__version__},indent=2))
