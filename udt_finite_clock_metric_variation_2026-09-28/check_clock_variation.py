"""Exact first-variation/control checks. All metrics are supplied controls."""
import json
import platform
import sympy as S

t,x,y,z,s,L,eps,alpha=S.symbols('t x y z s L eps alpha', real=True)
Lpos=S.symbols('Lpos',positive=True)
checks=[]
catches=[]
values={}

def zero(name,v):
    entries=list(v) if isinstance(v,S.MatrixBase) else [v]
    assert all(S.simplify(a)==0 for a in entries),(name,v)
    checks.append(name)

def wrong(name,got,expected):
    assert S.simplify(got-expected)!=0,(name,got,expected)
    catches.append(name)

def geometry_check(name,g,k):
    coords=[t,x,y,z];gi=g.inv()
    Gamma=[[[S.simplify(sum(gi[a,d]*(S.diff(g[d,c],coords[b])+S.diff(g[d,b],coords[c])-S.diff(g[b,c],coords[d])) for d in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
    zero(name+'_null',(k.T*g*k)[0])
    acc=S.Matrix([sum(k[b]*S.diff(k[a],coords[b]) for b in range(4))+sum(Gamma[a][b][c]*k[b]*k[c] for b in range(4) for c in range(4)) for a in range(4)])
    zero(name+'_affine_geodesic',acc)

# Smooth polynomial control: NOT the compact-bump/all-endpoint-jets witness.
b=x*x*(1-x)**2
B0=S.integrate(b,(x,0,1));B1=S.integrate(x*b,(x,0,1))
g=S.diag(-S.exp(-2*eps*t*b),S.exp(2*eps*t*b),1,1)
h=g.diff(eps).subs(eps,0)
eta=S.diag(-1,1,1,1);ell=S.Matrix([1,1,0,0])
zero('reciprocal_exact_determinant',g.det()+1)
zero('reciprocal_tracefree_tangent',S.trace(eta*h))
zero('reciprocal_full_factor_two',h-2*t*b*S.diag(1,1,0,0))
zero('polynomial_source_clock_unchanged',g.subs(x,0)[0,0]+1)
zero('polynomial_target_clock_unchanged',g.subs(x,1)[0,0]+1)
I=S.integrate((ell.T*h*ell)[0].subs(t,s+x)/2,(x,0,1))
V=2*(s*B0+B1)
zero('world_function_vs_ray_ODE',I-V)
zero('variation_original_null_ODE',S.diff(S.exp(2*eps*t*b),eps).subs({eps:0,t:s+x})-2*(s+x)*b)
zero('arrival_shift_exact_value',V-(s/S.Integer(15)+S.Rational(1,30)))
Q=S.diff(V,s)
zero('clock_response_exact_value',Q-S.Rational(1,15))
wrong('endpoint_only_response_rejected',0,Q)
wrong('reciprocal_stationarity_rejected',0,Q)
wrong('drop_half_worldfunction_rejected',2*Q,Q)
values['polynomial_control']={'B0':str(B0),'B1':str(B1),'V':str(V),'Q':str(Q),'compact_support':False}

# Static curved lapse: direct incidence and proper clocks are independently known.
N=1+x*x;f=x
gs=S.diag(-N*N,1,1,1)
C=S.Rational(4,3) # integral_0^1 N dx fixes affine interval [0,1]
ks=S.Matrix([C/(N*N),C/N,0,0])
geometry_check('static_lapse',gs,ks)
hs=S.diag(-2*f*N*N,0,0,0)
Is=S.integrate((ks.T*hs*ks)[0]*N/C/2,(x,0,1))
Vs=S.simplify(Is/C)
direct_Vs=-S.integrate(f/N,(x,0,1))
zero('static_time_transfer_variation',Vs-direct_Vs)
zero('static_V_value',Vs+S.log(2)/2)
bs=-hs[0,0]/(2*N*N)
Qs=bs.subs(x,1)-bs.subs(x,0)
zero('static_clock_ratio_derivative',Qs-1)
wrong('static_normalization_sign_rejected',-Qs,Qs)
values['static']={'V':str(Vs),'Q':str(Qs),'baseline_Z':'2'}

# Curved conformal baseline, changed spatial ruler. Arrival shift term is essential.
a=1+t
gc=a*a*eta
Cf=((1+s+L)**3-(1+s)**3)/3
kc=S.Matrix([Cf/a**2,Cf/a**2,0,0])
geometry_check('conformal_baseline',gc,kc)
hc=S.diag(0,2*alpha*a*a,0,0)
Ic=S.integrate((kc.T*hc*kc)[0]*a*a/Cf/2,(t,s,s+L))
Vc=S.simplify(Ic/Cf)
zero('conformal_ruler_arrival',Vc-alpha*L)
Qc=Vc/(1+s+L)
Zeps=(1+s+(1+eps*alpha)*L)/(1+s)
direct_Qc=S.diff(Zeps,eps).subs(eps,0)/Zeps.subs(eps,0)
zero('conformal_arrival_normalization',Qc-direct_Qc)
wrong('omit_arrival_event_rejected',0,Qc)
zero('conformal_selected_value',Qc.subs({s:1,L:1,alpha:3})-1)
values['curved_ruler']={'V':str(Vc),'Q':str(Qc)}

# Conformal metric variation leaves unparametrized null curves unchanged.
hc2=2*t*t*gc
zero('conformal_hkk_zero',(kc.T*hc2*kc)[0])
bconf=t*t
Qconf=(s+L)**2-s*s
Nconf=(1+t)*S.exp(eps*t*t)
Zconf=Nconf.subs(t,s+L)/Nconf.subs(t,s)
zero('conformal_clock_normalization',S.diff(Zconf,eps).subs(eps,0)/Zconf.subs(eps,0)-Qconf)
Ds=S.diff(S.log((1+s+L)/(1+s)),s)
delta_s=-(s**3/S.Integer(3)+s**4/S.Integer(4))/(1+s)
Qtau=S.simplify(Qconf+Ds*delta_s)
zero('fixed_proper_source_example',Qtau.subs({s:1,L:1})-S.Rational(439,144))
wrong('fixed_label_equals_fixed_proper_rejected',Qconf,Qtau)

# Pure coordinate change with carried observers. xi=(tx,t^2+x^2,0,0).
xi=S.Matrix([t*x,t*t+x*x,0,0]);coords=[t,x,y,z]
Dxi=xi.jacobian(coords);hg=Dxi.T*eta+eta*Dxi
Ig=S.integrate((ell.T*hg*ell)[0].subs(t,s+x)/2,(x,0,1))
xi_e=xi.subs({t:s,x:0});xi_o=xi.subs({t:s+1,x:1})
Jg=Ig+(ell.T*eta*xi_e)[0]-(ell.T*eta*xi_o)[0]
zero('gauge_metric_integral_boundary',Ig-((ell.T*eta*xi_o)[0]-(ell.T*eta*xi_e)[0]))
zero('gauge_arrival_cancellation',Jg)
u=S.Matrix([1,0,0,0]);W=-xi
bg=-hg[0,0]/2-(u.T*eta*W.diff(t))[0]
zero('gauge_proper_clock_cancellation',bg)
Qfixed=-hg.subs({t:s+1,x:1})[0,0]/2+hg.subs({t:s,x:0})[0,0]/2+S.diff(Ig,s)
zero('uncarried_worldlines_are_different_protocol',Qfixed-2)
wrong('drop_worldline_terms_in_gauge_rejected',Qfixed,0)
values['gauge']={'I':str(Ig),'J_carried':str(S.simplify(Jg)),'Q_uncarried':str(Qfixed)}

# Nonconstant clock map: fixed inverse label has an extra chain term.
q=S.symbols('q',positive=True);v=S.symbols('v',positive=True)
AA=q*q+eps*q
BB=(-eps+S.sqrt(eps*eps+4*v))/2
zero('inverse_composition',S.simplify(AA.subs(q,BB))-v)
delta_A=q
Qforward=1/(2*q)
Dprime=1/q
pred_reverse=-Qforward+Dprime*delta_A/(2*q)
Qreverse=S.diff(S.diff(BB,v),eps).subs(eps,0)/S.diff(BB,v).subs(eps,0)
zero('fixed_inverse_chain_term',Qreverse-pred_reverse)
paired_inverse_slope=1/S.diff(AA,q)
zero('paired_inverse_response',S.diff(paired_inverse_slope,eps).subs(eps,0)/paired_inverse_slope.subs(eps,0)+Qforward)
wrong('drop_inverse_argument_shift_rejected',-Qforward,Qreverse)
values['inverse']={'Q_forward':str(Qforward),'Q_reverse_fixed_label':str(Qreverse),'Q_reverse_paired':str(-Qforward)}

print(json.dumps({'status':'PASS','evidence':'exact first-variation controls; general claims rest on proofs',
 'python':platform.python_version(),'sympy':S.__version__,'exact_check_count':len(checks),
 'rejected_wrong_rules':len(catches),'checks':checks,'catches':catches,'values':values},indent=2))
