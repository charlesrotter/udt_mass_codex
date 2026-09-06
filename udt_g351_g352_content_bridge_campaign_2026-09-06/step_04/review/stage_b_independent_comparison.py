"""Portable stdout-only comparison; imports only sealed reviewer Stage A code."""
import argparse
import contextlib
import io
import json
import pathlib
import runpy
import sys
sys.dont_write_bytecode = True
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=pathlib.Path, required=True)
args = parser.parse_args()
with contextlib.redirect_stdout(io.StringIO()):
    independent = runpy.run_path(str(pathlib.Path(__file__).with_name('stage_a_checks.py')))
source = args.repo/'udt_g351_g352_content_bridge_campaign_2026-09-06/step_04/AUTHOR_RESULT.json'
saved = json.loads(source.read_text())
u,x,y = [independent[name] for name in ('u','x','y')]
rad, angle = S.symbols('rad angle', positive=True)
delta, kap = map(S.sympify, (saved['witness']['Delta'], saved['witness']['kappa']))
qrad = S.simplify(independent['q'].subs({x:rad,y:0}))
brad = S.root(independent['n'].subs({x:rad,y:0}),4)
wrad = S.simplify(qrad*brad)
matches = []

def check(name, actual, expected):
    if isinstance(actual,S.MatrixBase):
        assert all(S.simplify(e)==0 for e in actual-expected), name
    else:
        assert S.simplify(actual-S.sympify(expected))==0, (name,actual,expected)
    matches.append(name)

# Differentiate the actual Cartesian-to-polar full map, including graph slopes.
vv = S.symbols('vv',real=True)
old_map = S.Matrix([u,vv,rad*S.cos(angle),rad*S.sin(angle)])
P = old_map.jacobian([u,vv,rad,angle])
gcart = independent['g'].subs(independent['H'], independent['cubic'])
gpolar = S.trigsimp(P.T*gcart.subs({x:old_map[2],y:old_map[3]})*P)
check('full_polar_pullback',gpolar,S.Matrix([[rad**3*S.cos(3*angle),-1,0,0],
                                          [-1,0,0,0],[0,0,1,0],[0,0,0,rad**2]]))
fx, fy = S.symbols('fx fy',real=True)
cut = S.Matrix([[0,0],[fx,fy],[1,0],[0,1]])
gram = S.simplify(cut.T*gpolar*cut)
jacobian = S.sqrt(gram.det())
check('full_polar_graph_area',jacobian,rad)
sigma = S.simplify(delta/kap*wrad*jacobian)
rlo,rhi = map(S.sympify,saved['witness']['polar_patch']['r'])
alo,ahi = map(S.sympify,saved['witness']['polar_patch']['angle'])
ulo,uhi = map(S.sympify,saved['witness']['u_interval'])
mu = S.integrate(sigma,(rad,rlo,rhi),(angle,alo,ahi))
xi = S.integrate(wrad*jacobian,(rad,rlo,rhi),(angle,alo,ahi),(u,ulo,uhi))
check('saved_mu_total',mu,saved['witness']['mu_total'])
check('saved_Xi_total',xi,saved['witness']['Xi_total'])
rates = []
for i,asu in enumerate(saved['witness']['observer_Uu']):
    tangent = S.sympify(asu)
    rate = S.simplify(tangent*wrad.subs(rad,S.sympify(saved['witness']['point_r'])))
    check('saved_rate_'+str(i),rate,saved['witness']['rates'][i])
    rates.append(str(rate))
check('saved_negative_mixed_derivative',S.diff(independent['log_u'],x).subs({u:0,x:1,y:0}),
      saved['negative']['mixed_log_derivative'])
fourth = independent['wm4']
def value(ui,xi):
    return fourth.subs({u:ui,x:xi,y:0})
cross = S.factor(value(S.Rational(1,10),2)*value(0,1)/(value(S.Rational(1,10),1)*value(0,2)))
check('saved_negative_fourth_cross_ratio',cross,saved['negative']['positive_cross_ratio_fourth_power'])
assert cross>0 and cross!=1

# New exposed witness, independently derived through the already sealed source method.
with contextlib.redirect_stdout(io.StringIO()):
    nv,qv,wv4 = independent['profile_data'](S.exp(2*u)*independent['cubic'])
check('variable_profile_N',nv,S.exp(4*u)*independent['n'])
check('variable_profile_q',qv,independent['q'])
check('variable_profile_w_fourth',wv4,S.exp(4*u)*independent['w4'])
check('variable_phase_primitive',S.diff(-kap*S.exp(u),u),-kap*S.exp(u))
# Positive N,q and exp(u) determine the positive fourth root uniquely.
print(json.dumps(dict(matches=matches,comparison_count=len(matches),
                     mu_total=str(mu),Xi_total=str(xi),rates=rates,
                     positive_cross_ratio_fourth_power=str(cross),
                     independent_stage_a_guards=independent['checks'][:33],
                     proof_status='exact checks; analytic quantifiers reviewed separately'),
                 indent=2,sort_keys=True))
