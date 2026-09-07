"""Exposed independent comparison, importing only sealed reviewer science."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import sympy as s

here=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    env=runpy.run_path(str(here/'source_first.py'))
u,v,x,y=(env[n] for n in ('u','v','x','y'))
P,Q=(env[n] for n in ('P','Qpoly'))
psi=s.Function('psi')(u)
profile=s.cos(psi)*P+s.sin(psi)*Q
kappa0=s.symbols('kappa0',positive=True)
loc={'u':u,'v':v,'x':x,'y':y,'psi':s.Function('psi'),'kappa0':kappa0}
saved=json.loads((here.parent/'serial_author.stdout').read_text())
checks=[]
def simp(z):
    return s.factor(s.trigsimp(s.simplify(z)))
def check(name,values):
    residuals=[simp(z) for z in values]
    assert all(z==0 for z in residuals),(name,residuals)
    checks.append(name)
def read(name):return s.sympify(saved[name],locals=loc)
check('saved_polynomial_and_profile',[read('P')-P,read('Q')-Q,read('H')-profile])
substitute=lambda expr:expr.subs(env['H'],profile).doit()
check('saved_full_Ricci',list(substitute(env['Ric'])-read('Ricci')))
N=env['N0'];qq=env['q0'];ww=qq*N**s.Rational(1,4)
check('saved_N_q_w',[read('N0')-N,read('q0')-qq,read('w0')-ww])
alpha=s.Matrix([s.diff(N,z)/(4*N) for z in (u,v,x,y)])
check('saved_all_recurrence_covector_slots',list(alpha-s.Matrix([s.sympify(z,locals=loc) for z in saved['alpha']])))
check('saved_anchor_values',[read('N_at_point')-N.subs({x:1,y:0}),read('q_at_point')-qq.subs({x:1,y:0})])
TT=substitute(env['T'])
check('saved_all_tidal_entries',list(read('tidal_matrix')-TT))
check('saved_registered_tide_anchor',list(read('tidal_at_point')-TT.subs({x:1,y:0})))
check('saved_wrong_phase_density',[read('wrong_phase_product_residual')+ww/(2*kappa0)])
eps=s.symbols('eps',real=True)
bad=s.cos(eps*x)*P+s.sin(eps*x)*Q
badRic=simp(-s.diff(s.diff(bad,x,2)+s.diff(bad,y,2),eps).subs(eps,0)/2)
check('saved_off_equation_control',[read('transverse_angle_linear_Ricci')-badRic,badRic+s.diff(Q,x)])
# Do not rely on the isolated anchor where this diagnostic vanishes.
eta=s.symbols('eta',real=True)
near=badRic.subs({x:1,y:eta})
check('adverse_control_active_arbitrarily_near_anchor',[near-(4*eta**3-18*eta)])
assert badRic.subs({x:1,y:s.Rational(1,10)})!=0
L=env['L'];gi=env['gi'];ci=env['ci'];KK=env['K'];X=env['X'];rr=range(3)
Y=s.Matrix([-1/L,0,0]);f=1/s.sqrt(L)
check('full_spatial_seed_scalar',(s.diff(f,X[i])-sum(KK[i,j]*Y[j] for j in rr) for i in rr))
check('full_spatial_seed_vector',(s.diff(Y[j],X[i])+sum(ci[j][i][k]*Y[k] for k in rr)-
  f*sum(gi[j,k]*KK[i,k] for k in rr) for i in rr for j in rr))
check('full_seed_norm_and_decomposition',[ (Y.T*env['gamma']*Y)[0]-f*f]+list(env['embed']*Y+f*env['n']-env['V']))
# Same registration, not arbitrary isometry classification.
ff=s.Function('f')(u,x,y);H1=s.Function('H1')(u,x,y);H2=s.Function('H2')(u,x,y)
trans=s.Matrix([u,v+ff,x,y]);J=trans.jacobian((u,v,x,y))
target=s.Matrix([[H2,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
source=target.subs(H2,H1)
pull=s.simplify(J.T*target*J-source)
expected=s.zeros(4);expected[0,0]=H2-H1-2*s.diff(ff,u)
expected[0,2]=expected[2,0]=-s.diff(ff,x)
expected[0,3]=expected[3,0]=-s.diff(ff,y)
check('full_registered_isometry_pullback',list(pull-expected))
# Supplied null pair vs separately supplied unit-timelike affine normalization.
Knull=env['Knull'];VV=env['V'];gg=env['g'];U=(VV+Knull)/s.sqrt(2)
check('timelike_normalization_translation',[(U.T*gg*U)[0]+1,
      -(U.T*gg*Knull)[0]-1/s.sqrt(2),-(U.T*gg*(s.sqrt(2)*Knull))[0]-1])
# Profile-derivative freedom actually appears in the full induced K.
aa=s.symbols('a',real=True)
angle=s.pi/2+aa*u
Kangle=substitute(KK).subs(psi,angle).doit()
Kanchor=simp(Kangle[0,0].subs({u:0,x:1,y:0}))
check('derivative_freedom_in_complete_K',[Kanchor+aa/2])
print(json.dumps({'status':'PASS','checks':checks,'all_saved_scientific_expressions':'EXACT_MATCH',
  'general_registered_pullback_difference':str(pull),'original_control_at_1_1_tenth':str(badRic.subs({x:1,y:s.Rational(1,10)})),
  'near_anchor_control':str(near),'K_uu_for_angle_pi_over2_plus_a_u_at_anchor':str(Kanchor),
  'independence':'Imports only sealed reviewer scientific implementation; saved author strings are comparison targets.'},indent=2))
