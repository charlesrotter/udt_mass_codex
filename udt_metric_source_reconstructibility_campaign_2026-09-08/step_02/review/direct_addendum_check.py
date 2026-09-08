"""Post-target RT2 formula/ambient-closure audit using reviewer geometry only."""
import contextlib
import io
import json
from pathlib import Path
import runpy

captured = io.StringIO()
with contextlib.redirect_stdout(captured):
    d = runpy.run_path(str(Path(__file__).with_name('independent_product_check.py')))
s=d['s']; u,r,x,y=d['coords']; coords=d['coords']
geometry=d['geometry']; zero=d['zero']; q=d['q']
groups={}
reds={}


def check(name, value):
    groups[name]=zero(value)
    assert groups[name], (name,value)


def exterior(v):
    return s.Matrix(4,4,lambda i,j:s.diff(v[j],coords[i])-s.diff(v[i],coords[j]))


def red(name, value):
    try:
        assert zero(value), name
    except AssertionError:
        reds[name]=str(value)
    else:
        raise AssertionError(('false pass',name))


a=1+u*u
B=2+y
sigma=a*a*B
for sign in (1,-1):
    beta=3*sign  # FREE optional comparison sign/amplitude; not a physical constant.
    g, inv, C, Ric, scalar=geometry(-sign*sigma*x*x)
    b=a*s.sqrt(B)*q
    nmatch=B
    qmatch=b/s.sqrt(3*B)
    jmatch=s.sqrt(B/3)*inv*b
    check(f'actual_full_curvature_sign_{sign}',Ric-sign*b*b.T)
    check(f'actual_scalar_sign_{sign}',scalar)
    check(f'fixed_data_full_tensor_beta_{beta}',beta*nmatch*qmatch*qmatch.T-Ric)
    check(f'fixed_data_current_beta_{beta}',jmatch-nmatch*inv*qmatch)
    check(f'fixed_data_ambient_closure_beta_{beta}',exterior(qmatch))
    U=s.Matrix([-1,(g[0,0]+1)/2,0,0])
    check(f'fixed_observer_formula_beta_{beta}',-(U.T*g*jmatch)[0]
          -s.sqrt(B/3)*(-(b.T*U)[0]))
    bad=b/s.sqrt(3)  # s_fixed=1; full pointwise tensor still matches.
    dbad=exterior(bad)
    check(f'wrong_measure_cut_restriction_vacuous_{sign}',dbad.extract([1,2,3],[1,2,3]))
    check(f'wrong_measure_full_derivative_{sign}',dbad[3,0]-a/(2*s.sqrt(3)*s.sqrt(B)))
    red(f'cut_only_closure_false_pass_{sign}',dbad.subs({u:0,y:0}))

gn, inn, cn, Ricn, Rn=geometry(-x*x*(1+u*y))
check('author_nonseparable_actual_full_curvature',Ricn-(1+u*y)*q*q.T)
check('author_nonseparable_actual_scalar',Rn)
check('author_nonseparable_exact_mixed_derivative',s.diff(s.log(Ricn[0,0]),u,y)-1/(1+u*y)**2)

print(json.dumps(dict(stage='POST_TARGET_EXPOSURE_ADDENDUM',
    source_first_checker_replayed=json.loads(captured.getvalue())['groups'],
    additional_groups=len(groups),checks=groups,actual_red_controls=reds,
    limitation='General closure equivalence is analytic; finite diagnostics do not establish global or physical claims.'
),indent=2,sort_keys=True))
