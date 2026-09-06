"""Symbolic reconstruction and exact controls for the frozen curvature recipe.

General conclusions require the accompanying analytic argument and review.
All constants/patches are free-and-explored mathematical witness data, not UDT
physical inputs. No files are written. --mutation deliberately damages a branch.
"""
import sys
sys.dont_write_bytecode = True
import argparse
from itertools import product
import json
from pathlib import Path
import platform
import sympy as S
from curvature_recipe import (geometry, quadratic, real_future_root, exterior_one,
    covariant_one, divergence, raised_current, sheet_area, product_readout, tidy)

parser = argparse.ArgumentParser()
parser.add_argument('--mutation', choices=['omit_dual','omit_dual_half','euclidean_contraction',
    'wrong_root_degree','past_root','differentials_zero','homothety_inverse_frozen',
    'euclidean_cut_area','phase_gauge_recreates_mu'])
mutation = parser.parse_args().mutation
if not __debug__:
    raise RuntimeError('Checks require non-optimized Python')
checks = []


def zero_on_nonzero_A(value):
    """Exact branch coverage of the declared real A!=0 extraction domain.

    No tolerance or numerical sampling: A=t and A=-t with symbolic t>0.
    Expressions with no A, including separately recomputed A=0 controls,
    still require ordinary exact equality.
    """
    value = S.simplify(value)
    if value == 0:
        return True
    if value.has(A):
        positive_A = S.Dummy('positive_A', positive=True)
        return all(S.simplify(value.subs(A,sign*positive_A)) == 0 for sign in [1,-1])
    return False


def eq(name, actual, expected=0):
    assert zero_on_nonzero_A(actual-expected), name
    checks.append(name)


def matrix_eq(name, actual, expected):
    assert actual.shape == expected.shape, name+'_shape'
    assert all(zero_on_nonzero_A(a-b) for a,b in zip(actual,expected)), name
    checks.append(name)


def tensor_eq(name, actual, expected):
    assert all(zero_on_nonzero_A(actual.get(key,0)-expected.get(key,0))
               for key in product(range(4),repeat=4)), name
    checks.append(name)


def power4(beta):
    return {key: S.simplify(S.prod(beta[a] for a in key))
            for key in product(range(4),repeat=4)}


def observer(g, alpha, px, py):
    H = g[0,0]
    return S.Matrix([alpha,(1+H*alpha**2+px**2+py**2)/(2*alpha),px,py])


u,v,x,y,A = S.symbols('u v x y A', real=True)
coordinates = [u,v,x,y]
H = A*(x*x-y*y)
g = S.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
gi,connection,R,Ric,scalar,W = geometry(g,coordinates)
eq('metric_determinant',g.det(),-1)
matrix_eq('ricci_flat_full',Ric,S.zeros(4))
eq('scalar_zero',scalar)
eq('tidal_x_sign',R.get((0,2,0,2),0),-A)
eq('tidal_y_sign',R.get((0,3,0,3),0),A)
tensor_eq('weyl_equals_riemann',W,R)
dual,B = quadratic(g,gi,W,mutation=mutation)
tensor_eq('full_quadratic_tensor',B,{(0,0,0,0):4*A*A})
dual_reversed,B_reversed = quadratic(g,gi,W,orientation=-1)
tensor_eq('orientation_independent_B',B_reversed,B)
_,B_opposite_curvature = quadratic(g,gi,{key:-value for key,value in W.items()})
tensor_eq('curvature_sign_independent_B',B_opposite_curvature,B)

# Root extraction uses a removable auxiliary, not a supplied physical observer.
U = observer(g,S.Integer(1),S.Integer(0),S.Integer(0))
matrix_eq('auxiliary_unit',U.T*g*U,S.Matrix([[-1]]))
beta = real_future_root(B,U,mutation)
raw_beta = beta
b = S.sqrt(2*S.Abs(A))
tensor_eq('root_full_fourth_power',power4(beta),B)
eq('future_sign_positive_A',(-(beta.T*U)[0]).subs(A,2),2)
matrix_eq('root_covector',beta,S.Matrix([-b,0,0,0]))
# Use the readable representative only after exact equivalence on BOTH signs.
beta = S.Matrix([-b,0,0,0])
eq('root_null',(beta.T*gi*beta)[0])
matrix_eq('root_closed',exterior_one(beta,coordinates,mutation),S.zeros(4))
matrix_eq('root_parallel',covariant_one(beta,connection,coordinates),S.zeros(4))
C = raised_current(gi,beta)
matrix_eq('root_raised_vector',C,S.Matrix([0,b,0,0]))
eq('root_current_conserved',divergence(g,C,coordinates,mutation))
control = S.Matrix([-(1+v),0,0,0])
eq('nonclosed_control',exterior_one(control,coordinates,mutation)[1,0],-1)
eq('nonconserved_control',divergence(g,gi*control,coordinates,mutation),1)
U2 = observer(g,S.Rational(3,2),S.Rational(1,3),-S.Rational(2,5))
matrix_eq('second_auxiliary_unit',U2.T*g*U2,S.Matrix([[-1]]))
matrix_eq('root_auxiliary_independent',real_future_root(B,U2),beta)

# Nontrivial coordinate recomputation: old u=U+(2/3)X, old v=V, x=X, y=Y.
inputs = json.loads((Path(__file__).parent/'WITNESS_INPUTS.json').read_text())
mix = S.Rational(inputs['passive_u_x_mix'])
L = S.eye(4)
L[0,2] = mix
gmix = L.T*g*L
gimix,conmix,Rmix,Ricmix,smix,Wmix = geometry(gmix,coordinates)
_,Bmix = quadratic(gmix,gimix,Wmix)
Umix = L.inv()*U
beta_mix = real_future_root(Bmix,Umix)
matrix_eq('mixed_chart_observer_unit',Umix.T*gmix*Umix,S.Matrix([[-1]]))
matrix_eq('mixed_chart_root_covariance',beta_mix,L.T*beta)
tensor_eq('mixed_chart_full_fourth_power',Bmix,power4(L.T*beta))
matrix_eq('mixed_chart_root_parallel',covariant_one(beta_mix,conmix,coordinates),S.zeros(4))
matrix_eq('mixed_chart_current_covariance',gimix*beta_mix,L.inv()*C)

# A physical constant metric homothety is NOT the coordinate transform above.
hom = S.Rational(inputs['metric_homothety_factor'])
gs = hom**2*g
gis,cons,Rs,Rics,scalars,Ws = geometry(gs,coordinates)
_,Bs = quadratic(gs,gis,Ws)
tensor_eq('homothety_lower_W',Ws,{key:hom**2*value for key,value in W.items()})
tensor_eq('homothety_lower_B',Bs,B)
betas = real_future_root(Bs,U/hom)
matrix_eq('homothety_lower_beta',betas,beta)
Cs = raised_current(gis,betas,mutation,base_inverse=gi)
matrix_eq('homothety_raised_current',Cs,C/hom**2)
eq('homothety_volume_current',S.sqrt(-gs.det())*Cs[1],hom**2*C[1])
eq('homothety_normalized_observer_rate',-((U/hom).T*gs*Cs)[0],-(U.T*g*C)[0]/hom)

# Null-coordinate rescaling stays in the displayed family, with transformed A.
scale = S.Rational(inputs['null_coordinate_factor'])
eq('null_coordinate_root_component',b.subs(A,A/scale**2),b/scale)
eq('null_coordinate_phase',-b.subs(A,A/scale**2)*(scale*u),-b*u)

rows = []
point = dict(zip(coordinates,map(S.Rational,inputs['point'])))
alpha,px,py = map(S.Rational,[inputs['observer_u_component'],
                             inputs['observer_x_component'],inputs['observer_y_component']])
q1,q2 = map(S.Rational,inputs['cut_v_gradient'])
Delta = S.Rational(inputs['phase_spacing'])
E = S.Matrix([[0,0],[q1,q2],[1,0],[0,1]])
for av in map(S.Rational,inputs['A_values']):
    gv = g.subs(A,av)
    Uv = observer(gv,alpha,px,py)
    if av == 0:
        gif,conf,Rf,Ricf,scalarf,Wf = geometry(gv,coordinates)
        _,Bf = quadratic(gv,gif,Wf)
        tensor_eq('flat_recomputed_B',Bf,{})
        betav = real_future_root(Bf,Uv)
        Cv = gif*betav
    else:
        betav = beta.subs(A,av)
        Cv = C.subs(A,av)
    area = sheet_area(gv,E,mutation)
    eq(f'cut_area_A_{av}',area,1)
    matrix_eq(f'observer_unit_A_{av}',Uv.T*gv*Uv,S.Matrix([[-1]]))
    rate = S.simplify(-(Uv.T*gv*Cv)[0])
    if av != 0:
        eq(f'readout_A_{av}',product_readout(-(Uv.T*betav)[0],Delta,Delta,area),rate)
        phase_scale = S.Rational(inputs['phase_unit_factor'])
        eq(f'fixed_current_phase_gauge_A_{av}',
           product_readout(phase_scale*(-(Uv.T*betav)[0]),Delta,Delta,area,
                           mutation,new_spacing=phase_scale*Delta),rate)
    else:
        matrix_eq('flat_zero_root',betav,S.zeros(4,1))
        eq('flat_has_no_nonzero_recipe_phase',rate,0)
    rows.append({'A':str(av),'B_uuuu':str(B.get((0,0,0,0),0).subs(A,av)),
                 'beta_u':str(betav[0]),'C_v_component':str(Cv[1]),
                 'observer':list(map(str,Uv.subs(point))), 'J':str(area),
                 'Gamma':str(rate)})

rect = [[S.Rational(z) for z in side] for side in inputs['finite_label_rectangle']]
patch_area = S.prod(side[1]-side[0] for side in rect)
phase_width = S.Rational(inputs['phase_interval_width'])
eq('finite_patch_mu',Delta*patch_area,6)
eq('finite_patch_Xi',phase_width/Delta*(Delta*patch_area),5)
eq('homothety_geometric_mu',Delta*hom**2*patch_area,54)

def sparse(data):
    return [{'indices':list(key),'value':str(value)} for key,value in sorted(data.items())]

print(json.dumps({'kind':'symbolic tensor reconstruction and exact regression; not physical confirmation',
    'python':platform.python_version(),'sympy':S.__version__,'mutation':mutation,
    'checks_passed':len(checks),'checks':checks,'tensor_shapes':{'g':[4,4],'W':[4,4,4,4],'B':[4,4,4,4]},
    'symbolic':{'connection':sparse(connection),'Riemann':sparse(R),'Weyl':sparse(W),
                'dual_Weyl':sparse(dual),'B':sparse(B),'raw_beta':list(map(str,raw_beta)),
                'root_domain':'all real A!=0, exact positive and negative symbolic branches; flat recomputed separately',
                'beta':list(map(str,beta)),
                'current':list(map(str,C))},'witnesses':rows,
    'finite_patch':{'coordinate_area':str(patch_area),'mu':str(Delta*patch_area),
                    'Xi':str(phase_width*patch_area),'homothetic_mu':str(Delta*hom**2*patch_area)}},indent=2))
