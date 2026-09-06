"""Exact positive product realization and fixed-label failure controls.

The phase is deliberately DIFFERENT from the original curvature root. Supplied
query units/patch/spacing and chosen recipes are not physical identification.
Stdout only; no imported author implementation from earlier steps.
"""
import sys
sys.dont_write_bytecode=True
import argparse,json,platform
import sympy as S
ap=argparse.ArgumentParser()
ap.add_argument('--mutation',choices=['old_root_as_phase','omit_polar_J','omit_conversion_q',
                                    'phase_measure_rebuild_gauge','phase_blind_product'])
mutation=ap.parse_args().mutation
if not __debug__: raise RuntimeError('Assertions must remain enabled')
u,v,x,y=S.symbols('u v x y',real=True)
r=S.symbols('r',positive=True);ang=S.symbols('angle',real=True)
kappa=S.Integer(2);Delta=S.Rational(3,2)
H=x**3-3*x*y*y
N=S.expand(S.diff(H,x,2)**2+S.diff(H,x,y)**2)
q=S.factor((S.diff(N,x)**2+S.diff(N,y)**2)/(16*N*N))
b=S.sqrt(6)*S.sqrt(r);qr=1/(4*r*r);w=qr*b
groups=[]
def eq(name,a,b=0):
    if isinstance(a,S.MatrixBase): assert (a-b).applyfunc(S.simplify)==S.zeros(*a.shape),name
    else: assert S.simplify(a-b)==0,name
    groups.append(name)
eq('harmonic_stationary_cubic',S.diff(H,x,2)+S.diff(H,y,2))
eq('intrinsic_recurrence_q_from_Hessian',q,1/(4*(x*x+y*y)))
g=S.Matrix([[r**3*S.cos(3*ang),-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,r*r]])
coords=[u,v,r,ang]
keff=b if mutation=='old_root_as_phase' else kappa
k=S.Matrix([-keff,0,0,0])
dk=S.Matrix(4,4,lambda i,j:S.diff(k[j],coords[i])-S.diff(k[i],coords[j]))
eq('new_full_phase_is_closed',dk,S.zeros(4))
eq('new_phase_null',(k.T*g.inv()*k)[0])
eq('new_phase_primitive',S.diff(-kappa*u,u),k[0])
# Nonzero graph gradients are included in the full intrinsic cut metric.
E=S.Matrix([[0,0],[S.Rational(2,5),S.Rational(-3,7)],[1,0],[0,1]])
Jactual=S.sqrt((E.T*g*E).det())
J=S.Integer(1) if mutation=='omit_polar_J' else Jactual
eq('intrinsic_polar_cut_area',J,r)
computed_w=b if mutation=='omit_conversion_q' else w
s=Delta/kappa*computed_w*r
total=S.integrate(s,(r,1,4),(ang,0,1))
eq('finite_dimensionless_label_amount',total,3*S.sqrt(6)/8)
Xi=S.integrate(computed_w*r,(r,1,4),(ang,0,1),(u,0,1))
eq('product_equals_original_geometric_amount',Xi,kappa/Delta*total)
eq('original_geometric_amount_value',Xi,S.sqrt(6)/2)
D=S.Matrix([0,w,0,0])
eq('converted_current_conservation',sum(S.diff(r*D[i],coords[i]) for i in range(4))/r)
rates=[]
for tangent_u in [S.Integer(1),S.Integer(3)]:
    U=S.Matrix([tangent_u,(1+g[0,0]*tangent_u**2)/(2*tangent_u),0,0])
    eq(f'full_unit_observer_{tangent_u}',(U.T*g*U)[0],-1)
    omega=-(k.T*U)[0]
    gamma=omega/Delta*s/J
    eq(f'fixed_current_readout_{tangent_u}',gamma,-(U.T*g*D)[0])
    rates.append(S.simplify(gamma.subs(r,2)))
eq('observer_rate_ratio',rates[1]/rates[0],3)
a=S.Rational(3,2)
new_s=a*s if mutation=='phase_measure_rebuild_gauge' else s
eq('fixed_measure_phase_spacing_gauge',(a*kappa)/(a*Delta)*new_s/J,kappa/Delta*s/J)
eq('fixed_D_changed_phase_only_measure_not_fixed',Delta/(a*kappa)*w*r,s/a)
h=S.symbols('h',positive=True)
eq('dimensionless_mu_homothety',(h**-2*qr)*b/kappa*Delta*(h**2*r),s)
eq('count_current_rate_homothety',h**2*h**-1*h**-4,h**-3)

# Positive variable-u cubic: factorization, not stationarity, is what is needed.
wv=S.exp(u)*w;kv=S.exp(u)*kappa
eq('variable_factorized_product',wv/kv,w/kappa)
eq('variable_aligned_phase_primitive',S.diff(-kappa*S.exp(u),u),-kv)

# Genuine fixed-label negative: harmonic cubic+u*quartic, positive near(0,1,0).
Hm=H+u*(x**4-6*x*x*y*y+y**4)
Nm=S.factor(S.diff(Hm,x,2)**2+S.diff(Hm,x,y)**2)
qm=S.factor((S.diff(Nm,x)**2+S.diff(Nm,y)**2)/(16*Nm*Nm))
eq('mixed_profile_harmonic',S.diff(Hm,x,2)+S.diff(Hm,y,2))
log_w_u=S.diff(qm,u)/qm+S.diff(Nm,u)/(4*Nm)
mixed=S.Integer(0) if mutation=='phase_blind_product' else S.diff(log_w_u,x).subs({u:0,x:1,y:0})
eq('nonseparable_product_discriminator',mixed,5)
eq('negative_control_positive_q',qm.subs({u:0,x:1,y:0}),S.Rational(1,4))
# Fourth powers eliminate radicals in the finite positive cross-ratio witness.
W4=S.factor(qm**4*Nm)
def value(U,X):return W4.subs({u:U,x:X,y:0})
cross4=S.factor(value(S.Rational(1,10),2)*value(0,1)/(value(S.Rational(1,10),1)*value(0,2)))
assert cross4>0 and cross4!=1,'finite_positive_cross_ratio_not_one'
groups.append('finite_positive_cross_ratio_not_one')
print(json.dumps({'kind':'conditional chosen-product compatibility, not physical content identity',
 'python':platform.python_version(),'sympy':S.__version__,'mutation':mutation,
 'passed_groups':groups,'group_count':len(groups),'metric_shape':[4,4],
 'witness':{'length_unit':'supplied L; printed coordinates in L units','kappa':'2','Delta':'3/2',
 'polar_patch':{'r':['1','4'],'angle':['0','1']},'u_interval':['0','1'],
 'mu_total':str(total),'Xi_total':str(Xi),'point_r':'2',
 'observer_Uu':['1','3'],'rates':[str(z) for z in rates],'phase':'-2*u'},
 'negative':{'H':str(Hm),'point':['0','1','0'],'mixed_log_derivative':str(mixed),
 'positive_cross_ratio_fourth_power':str(cross4)}},indent=2))
