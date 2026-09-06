#!/usr/bin/env python3
"""Portable read-only comparison using the frozen source-first implementation."""
import argparse, contextlib, io, json, pathlib, runpy
import sympy as S

parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=pathlib.Path,required=True)
args=parser.parse_args()
here=pathlib.Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    d=runpy.run_path(str(here/'stage_a_checks.py'))
base=args.repo/'udt_g351_g352_content_bridge_campaign_2026-09-06/step_02'
saved=json.loads((base/'AUTHOR_RESULT.json').read_text())
A,u,x,y,b,h=[d[k] for k in ['A','u','x','y','b','h']]
aa,cc=d['a'],d['c']
comparison=[]
for row in saved['finite_witnesses']:
    amp=S.Rational(row['A'])
    subs={A:amp,x:S.Rational(1,3),y:S.Rational(-2,5),b:S.Integer(2),
          aa:S.Rational(2,3),cc:S.Rational(3,7),
          S.diff(aa,u):S.Rational(-1,2),S.diff(cc,u):S.Rational(4,5),
          S.diff(aa,u,2):amp*S.Rational(2,3),
          S.diff(cc,u,2):-amp*S.Rational(3,7)}
    J=d['JF'].subs(subs,simultaneous=True)
    source=d['g'].subs(subs,simultaneous=True)
    target=d['metric_at'](d['F']).subs(subs,simultaneous=True)
    # Calculate the full pullback afresh at each witness before comparison;
    # never use the author's zero residual as a computed quantity.
    pullback=(J.T*target*J).applyfunc(S.simplify)
    residual=(pullback-source).applyfunc(S.simplify)
    assert residual==S.Matrix([[S.Rational(z) for z in r]
                              for r in row['metric_pullback_residual']])
    assert residual==S.zeros(4)
    beta_w=d['beta'].subs(subs,simultaneous=True)
    assert J.T*beta_w==beta_w
    # Replace the rational witness's auxiliary b=2 by the actual recipe root.
    beta_recipe=S.Matrix([-S.sqrt(2*abs(amp)),0,0,0])
    assert (J.T*beta_recipe-beta_recipe).applyfunc(S.simplify)==S.zeros(4,1)
    comparison.append({'A':str(amp),'reconstructed_Jacobian':str(J),
                       'reconstructed_full_pullback':str(pullback),
                       'full_residual_matches_saved':True,
                       'recipe_beta_u':str(beta_recipe[0]),
                       'recipe_beta_preserved':True})

g,beta,JD=d['g'],d['beta'],d['JD']
C=g.inv()*beta
Cs=(h*h*g).inv()*beta
assert (Cs-h**-2*C).applyfunc(S.simplify)==S.zeros(4,1)
vol=S.sqrt(-g.det())
vols=S.sqrt(-(h*h*g).det())
volume_ratio=S.simplify(vols/vol)
current_ratio=S.simplify(Cs[1]/C[1])
amount_ratio=S.simplify(volume_ratio*current_ratio)
assert [volume_ratio,current_ratio,amount_ratio]==[h**4,h**-2,h**2]
computed={'metric_weight':2,'beta_weight':0,
          'current_weight':int(current_ratio.as_powers_dict()[h]),
          'amount_weight':int(amount_ratio.as_powers_dict()[h])}
assert computed==saved['homothety']
assert S.simplify(1-S.Rational(2)**-2)==S.Rational(saved['fixed_point_h_2_coefficient'])

print(json.dumps({'status':'PASS','basis':'frozen source-first coordinate maps differentiated independently',
 'saved_witnesses':comparison,'homothety_independent_contraction':{
  'volume_ratio':str(volume_ratio),'current_ratio':str(current_ratio),'amount_ratio':str(amount_ratio)},
 'author_code_imported':False,'author_results_exposed':True,
 'read_only':True,'finite_witnesses_are_not_theorem_proof':True},indent=2))
