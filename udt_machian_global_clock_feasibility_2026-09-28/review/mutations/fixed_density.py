"""Exact MGC1 diagnostic checks; no native matter law or numerical certification.

Reuse only the pinned geometry method via AST, never its source-model body.
All metric/matter equations below are EXTERNAL GR COMPARISON or declared FREE
controls. c,G are accepted calibration symbols; no numerical constants fitted.
"""
from pathlib import Path
import ast,hashlib,json,platform
import sympy as S
ROOT=Path(__file__).resolve().parent.parent
method=ROOT/'udt_source_metric_connection_campaign_2026-09-08/step_03/check_interface.py'
assert hashlib.sha256(method.read_bytes()).hexdigest()=='8a34a9e57a2b5fab7f67586e6bff6398f76effe4b8f68407fa43f124ca40a416'
nodes=[n for n in ast.parse(method.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='geometry']
assert len(nodes)==1
ns={'S':S};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(method),'exec'),ns)
geometry=ns['geometry'];checks={};catches={};values={}
def residual(a,b=0):
    if isinstance(a,S.MatrixBase) or isinstance(b,S.MatrixBase):
        a,b=S.Matrix(a),S.Matrix(b);assert a.shape==b.shape
        return list((a-b).applyfunc(S.simplify))
    return [S.simplify(a-b)]
def eq(name,a,b=0):
    rr=residual(a,b);assert all(x==0 for x in rr),(name,rr);checks[name]=True
def reject(name,a,b=0):
    rr=residual(a,b);assert any(x!=0 and x.is_zero is False for x in rr),(name,rr);catches[name]=True
c,G,L,M,rho,C,q,lam,T,D=S.symbols('c G L M rho C q lam T D',positive=True)
w=S.symbols('w',real=True);t,chi,theta,phi=S.symbols('t chi theta phi',real=True)
Q=G*M/(c**2*L)
# Independent unit-exponent matrix, columns c,G,M,L in L,T,M order.
dim=S.Matrix([[1,3,0,1],[-1,-2,0,0],[0,-1,1,0]])
eq('compactness_dimensions',dim*S.Matrix([-2,1,1,-1]),S.zeros(3,1))
eq('fixed_mass_scale',Q.subs(L,G*M/(q*c**2)),q)
eq('density_scale', (C*G*rho*L**2/c**2).subs(L,2*c*S.sqrt(q/(C*G*rho))),q)
eq('defined_mass_identity',Q.subs(M,q*c**2*L/G),q)
eq('general_homogeneity',Q.subs({M:lam**w*M,L:lam*L},simultaneous=True),lam**(w-1)*Q)
eq('geometric_mass_weight_one',Q.subs({M:lam*M,L:lam*L},simultaneous=True),Q)
eq('fixed_mass_nonzero_scale_slope',S.diff(Q.subs(L,lam*L),lam).subs(lam,1),-Q)
eq('fixed_density_scale_slope',S.diff(C*G*rho*(lam*L)**2/c**2,lam).subs(lam,1),2*C*G*rho*L**2/c**2)
reject('wrong_fixed_mass_invariance',Q/2,Q)
reject('wrong_fixed_density_invariance',4*C*G*rho*L**2/c**2,C*G*rho*L**2/c**2)
f=lambda s:3*s+s*s/T+D
s=S.symbols('s',nonnegative=True)
fl=lam*f(t/lam)
eq('rescaled_arrival_map',fl.subs(t,lam*s),lam*f(s))
eq('proper_clock_derivative_invariant',S.diff(fl,t).subs(t,lam*s),S.diff(f(t),t).subs(t,s))
eq('echo_length_scaling',c*(fl.subs(t,lam*s)-lam*s)/2,lam*c*(f(s)-s)/2)
reject('wrong_elapsed_time_invariance',(lam*f(s)-lam*s).subs(lam,2),f(s)-s)
mu1,mu2=S.Rational(2),S.Rational(5);J1,J2=S.Rational(3),S.Rational(7)
eq('measure_normalization_transfer_ratio',(lam*(mu1+mu2)/J2)/(lam*(mu1+mu2)/J1),J1/J2)
reject('wrong_absolute_density_invariance',2*(mu1+mu2)/J1,(mu1+mu2)/J1)
H=S.symbols('H',positive=True);RH=c/H;rhoc=3*H**2/(8*S.pi*G)
MH=4*S.pi*rhoc*RH**3/3
qh=S.simplify(G*MH/(c**2*RH))
eq('flat_friedmann_compactness_identity',qh,S.Rational(1,2))
eq('flat_friedmann_no_H_selection',S.diff(qh,H))
reject('wrong_flat_friedmann_value',qh,S.Integer(1))
# Original external 4D metric, not a Friedmann shortcut for this tensor check.
a=S.symbols('a',positive=True);coords=[t,chi,theta,phi]
g=S.diag(-c*c,a*a,a*a*S.sin(chi)**2,a*a*S.sin(chi)**2*S.sin(theta)**2)
conn,ric,scal=geometry(g,coords)
expected=S.diag(0,2,2*S.sin(chi)**2,2*S.sin(chi)**2*S.sin(theta)**2)
eq('static_original_metric_Ricci',ric,expected)
eq('static_original_metric_scalar',scal,6/a**2)
E=ric-scal*g/2;Lambda=1/a**2;rhoE=c*c/(4*S.pi*G*a*a)
U=S.Matrix([1,0,0,0]);Uflat=g*U;stress=rhoE*Uflat*Uflat.T
rhs=8*S.pi*G/c**4*stress
eq('static_original_Einstein_equation',E+Lambda*g,rhs)
reject('wrong_static_density', (E+Lambda*g-2*rhs)[0,0])
reject('wrong_static_Lambda', (E+2*Lambda*g-rhs)[0,0])
eq('ordinary_local_clock',(U.T*g*U)[0],-c*c)
eq('parallel_timelike_direction',S.Matrix(4,4,lambda i,j:conn[i][j][0]),S.zeros(4,4))
k=S.Matrix([a/c,1,0,0])
eq('radial_tangent_null',(k.T*g*k)[0])
eq('radial_tangent_affine_geodesic',S.Matrix([sum(conn[i][j][l]*k[j]*k[l] for j in range(4) for l in range(4)) for i in range(4)]),S.zeros(4,1))
# Spatial volume on the declared S^3 (positive chart density).
vol=S.integrate(a**3*S.sin(chi)**2*S.sin(theta),(phi,0,2*S.pi),(theta,0,S.pi),(chi,0,S.pi))
eq('S3_volume',vol,2*S.pi**2*a**3)
ME=S.simplify(rhoE*vol);QE=S.simplify(G*ME/(c*c*a))
eq('proper_dust_mass',ME,S.pi*c*c*a/(2*G))
eq('static_compactness',QE,S.pi/2)
eq('independent_mass_fixes_radius',ME.subs(a,2*G*M/(S.pi*c*c)),M)
eq('static_family_mass_scales',ME.subs(a,lam*a),lam*ME)
reject('wrong_euclidean_global_volume',S.simplify(vol/(S.pi*a**3)),S.Rational(4,3))
alpha=S.symbols('alpha',positive=True);arrival=t+a*alpha/c
Z=S.diff(arrival,t)
eq('static_tick_ratio',Z,1)
eq('antipodal_delay_limit',S.limit(arrival-t,alpha,S.pi,dir='-'),S.pi*a/c)
eq('antipodal_no_redshift_limit',S.limit(Z,alpha,S.pi,dir='-'),1)
reject('wrong_static_clock_slowing',Z,S.Integer(2))
values={'external_static_rho':str(rhoE),'external_static_Lambda':str(Lambda),'proper_dust_mass':str(ME),'Q_static_curvature_radius':str(QE),'Q_flat_Friedmann_defined_ball':str(qh),'static_clock_Z':str(Z)}
print(json.dumps({'status':'PASS','checks':checks,'rejected_wrong_rules':catches,'values':values,'versions':{'python':platform.python_version(),'sympy':S.__version__},'limits':'Exact symbolic supporting controls, not independent proof; imported GR never native; no empirical/stability claim'},indent=2))
