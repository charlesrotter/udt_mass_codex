"""Reuse reviewer's pre-exposure implementation; compare complete frozen saved artifacts."""
import contextlib
import datetime
import io
import itertools
import json
import pathlib
import runpy
import sympy as s

scratch=pathlib.Path('/tmp/udt-curvature-review-qassiP')
pkg=pathlib.Path('/home/udt-admin/udt_mass_codex/udt_g313_curvature_phase_current_candidate_2026-09-06')
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with contextlib.redirect_stdout(io.StringIO()):
    independent=runpy.run_path(str(scratch/'stage_a_tensor.py'))
A=independent['A']; u,v,x,y=independent['coords']; g=independent['g']; gi=independent['gi']
saved=json.loads((pkg/'AUTHOR_RESULT.json').read_text())
inputs=json.loads((pkg/'WITNESS_INPUTS.json').read_text())
locals_={str(z):z for z in (u,v,x,y,A)}
checks=[]
for key,ours,rank in [('connection','Gamma',3),('Riemann','R',4),('Weyl','W',4),
                       ('dual_Weyl','star',4),('B','B',4)]:
    data={tuple(row['indices']):s.sympify(row['value'],locals=locals_) for row in saved['symbolic'][key]}
    assert len(data)==len(saved['symbolic'][key]),'duplicate sparse indices'
    for t in itertools.product(range(4),repeat=rank):
        assert s.simplify(data.get(t,0)-independent[ours][t])==0,(key,t)
    checks.append(f'complete saved {key} compared with pre-exposure coordinate reconstruction')

# Both metric inverse contractions receive separate deliberately wrong identity substitutions.
def altered(g1,g2):
    out={}
    terms1=[(e,f,g1[e,f]) for e in range(4) for f in range(4) if g1[e,f]!=0]
    terms2=[(h,i,g2[h,i]) for h in range(4) for i in range(4) if g2[h,i]!=0]
    for a,b,c,d in itertools.product(range(4),repeat=4):
        out[a,b,c,d]=s.simplify(sum(c1*c2*T[a,e,c,h]*T[b,f,d,i]
            for T in (independent['W'],independent['star'])
            for e,f,c1 in terms1 for h,i,c2 in terms2))
    return out
mutants={}
for label,g1,g2 in [('first_inverse_identity',s.eye(4),gi),
                    ('second_inverse_identity',gi,s.eye(4)),
                    ('both_inverse_identity',s.eye(4),s.eye(4))]:
    bad=altered(g1,g2)
    defects={str(t):str(s.simplify(bad[t]-independent['B'][t]))
             for t in bad if s.simplify(bad[t]-independent['B'][t])!=0}
    assert defects,label
    mutants[label]=defects
checks.append('each metric inverse separately load-bearing; deliberate substitutions fail full tensor')

# Recompute all saved finite witness observer/rate data from independent g and B.
rows=[]
point={z:s.Rational(value) for z,value in zip((u,v,x,y),inputs['point'])}
for av,record in zip(inputs['A_values'],saved['witnesses'],strict=True):
    aval=s.Rational(av)
    metric=g.subs({A:aval,**point})
    b=s.real_root(independent['B'][0,0,0,0].subs(A,aval),4)
    current=s.Matrix([0,b,0,0])
    alpha,px,py=map(s.Rational,[inputs['observer_u_component'],
                               inputs['observer_x_component'],inputs['observer_y_component']])
    uv=s.solve((s.Matrix([alpha,s.Symbol('uv'),px,py]).T*metric*
                s.Matrix([alpha,s.Symbol('uv'),px,py]))[0]+1,s.Symbol('uv'))[0]
    observer=s.Matrix([alpha,uv,px,py])
    assert (observer.T*metric*observer)[0]==-1
    rate=s.simplify(-(observer.T*metric*current)[0])
    row={'A':str(aval),'B_uuuu':str(b**4),'beta_u':str(-b),
         'C_v_component':str(b),'observer':list(map(str,observer)),'J':'1','Gamma':str(rate)}
    assert row==record,(row,record)
    rows.append(row)
checks.append('four saved witness rows independently reconstructed from metric and computed B')

# Verify the direct metric-isometry counterexample to canonical cross-phase labels.
bfun=s.Function('b')(u)
mapping=s.Matrix([u,v+s.diff(bfun,u)*x+s.diff(bfun,u)*bfun/2,x+bfun,y])
jac=mapping.jacobian((u,v,x,y))
pulled=jac.T*g.subs({x:x+bfun})*jac
residual=(pulled-g).applyfunc(lambda z:s.simplify(z.subs(s.diff(bfun,u,2),A*bfun)))
assert residual==s.zeros(4)
checks.append('phase-dependent translation with b second derivative=A b preserves complete metric')

# Check author extraction on both exact nonzero branches, with flat separately excluded.
raw=s.sympify(saved['symbolic']['raw_beta'][0],locals=locals_)
t=s.symbols('t',positive=True)
assert all(s.simplify((raw+s.sqrt(2*s.Abs(A))).subs(A,sign*t))==0 for sign in (-1,1))
assert raw.subs(A,0) is s.nan
checks.append('pre-freeze domain correction verified on both symbolic signs; division invalid at zero')

print(json.dumps({'start_utc':start,'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'checks':checks,'metric_inverse_mutant_differences':mutants,'saved_witnesses':rows,
 'all_passed':True,'implementation':'pre-exposure independent coordinate implementation reused; no author module imported'},
 indent=2,sort_keys=True))
