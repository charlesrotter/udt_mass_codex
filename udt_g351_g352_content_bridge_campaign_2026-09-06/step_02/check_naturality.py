"""Exact metric/phase symmetry controls, not a physical-content selector.

Stdout only. The general naturality and measure arguments live in the candidate;
these full-matrix checks support algebra, not their physical adoption.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import json
import platform
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--mutation', choices=['v_shift_sign','wrong_y_ode','homothety_v_power',
                                         'density_scale','component_as_scalar'])
mutation = parser.parse_args().mutation
if not __debug__:
    raise RuntimeError('Assertions must remain enabled')
u,v,x,y,A = S.symbols('u v x y A', real=True)
p,q,dp,dq = S.symbols('p q dp dq', real=True)
h,a,b = S.symbols('h a b', positive=True)
def metric(X,Y,amp=A):
    return S.Matrix([[amp*(X**2-Y**2),-1,0,0],[-1,0,0,0],
                     [0,0,1,0],[0,0,0,1]])
g = metric(x,y)
beta = S.Matrix([-b,0,0,0])
passed=[]
def matrix_equal(name,left,right):
    residual=(left-right).applyfunc(S.simplify)
    assert residual == S.zeros(*residual.shape), name
    passed.append(name)
def equal(name,left,right):
    assert S.simplify(left-right)==0, name
    passed.append(name)

# Exact Jacobian of T=(u,v+p'x+q'y+(pp'+qq')/2,x+p,y+q).
# p''=Ap and q''=-Aq; values p,q,p',q' at a fixed u are arbitrary.
ddp=A*p
ddq=A*q if mutation=='wrong_y_ode' else -A*q
sign=-1 if mutation=='v_shift_sign' else 1
T=S.Matrix([[1,0,0,0],
 [sign*(ddp*x+ddq*y+(dp**2+p*ddp+dq**2+q*ddq)/2),1,sign*dp,sign*dq],
 [dp,0,1,0],[dq,0,0,1]])
matrix_equal('full_translation_isometry',T.T*metric(x+p,y+q)*T,g)
matrix_equal('full_covector_preserved',T.T*beta,beta)
equal('isometry_jacobian',T.det(),1)
matrix_equal('generator_preserved',T*S.Matrix([0,b,0,0]),S.Matrix([0,b,0,0]))

D=S.diag(1,h if mutation=='homothety_v_power' else h**2,h,h)
matrix_equal('full_proper_homothety',D.T*metric(h*x,h*y)*D,h**2*g)
matrix_equal('homothety_beta_fixed',D.T*beta,beta)
equal('homothety_volume',D.det(),h**4)
matrix_equal('homothety_current_weight',(h**2*g).inv()*beta,h**-2*g.inv()*beta)
# Quotient density |dtheta| dxdy has Jacobian h^2, not weight zero.
actual_density_scale=S.Integer(1) if mutation=='density_scale' else S.diag(1,h,h).det()
equal('quotient_amount_area_weight',actual_density_scale,h**2)

# A is a displayed component parameter, not a scalar under null coordinate boost.
new_amp=A if mutation=='component_as_scalar' else A/a**2
N=S.diag(a,1/a,1,1)
matrix_equal('passive_null_boost_metric',N.T*metric(x,y,new_amp)*N,g)
matrix_equal('passive_null_boost_covector',N.T*S.Matrix([-b/a,0,0,0]),beta)

# Finite exact anchors; they supplement, not replace, the general argument.
witnesses=[]
for amp in [S.Rational(2),S.Rational(-3)]:
    subs={A:amp,x:S.Rational(1,3),y:S.Rational(-2,5),p:S.Rational(2,3),
          q:S.Rational(3,7),dp:S.Rational(-1,2),dq:S.Rational(4,5),b:2}
    residual=(T.T*metric(x+p,y+q)*T-g).subs(subs)
    matrix_equal(f'rational_isometry_A_{amp}',residual,S.zeros(4))
    witnesses.append({'A':str(amp),'metric_pullback_residual':[[str(z) for z in row] for row in residual.tolist()]})
equal('nonconstant_profile_fails_translation',(1+x**2).subs(x,1)-(1+x**2).subs(x,0),1)
equal('fixed_point_weight_obstruction_coefficient',1-S.Rational(2)**-2,S.Rational(3,4))
equal('unit_square_countable_partition_first_N_mass',sum(S.Rational(3,2) for _ in range(7)),S.Rational(21,2))
print(json.dumps({'kind':'exact algebra/regression; analytic quantifiers require argument review',
 'python':platform.python_version(),'sympy':S.__version__,'mutation':mutation,
 'passed_groups':passed,'group_count':len(passed),'metric_shape':[4,4],
 'generic_residual':'zero using p_second=A*p, q_second=-A*q',
 'homothety':{'metric_weight':2,'beta_weight':0,'current_weight':-2,'amount_weight':2},
 'fixed_point_h_2_coefficient':'3/4','finite_witnesses':witnesses},indent=2))
