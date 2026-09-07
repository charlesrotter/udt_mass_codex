"""Exposed comparison: reuse the sealed independent all-covector differentiator."""
import contextlib
import io
import json
import pathlib
import runpy
import sympy as s

ROOT=pathlib.Path('/home/udt-admin/udt_mass_codex')
STEP=ROOT/'udt_phase_current_product_persistence_campaign_2026-09-07/step_02'
buffer=io.StringIO()
with contextlib.redirect_stdout(buffer):
    independent=runpy.run_path(str(STEP/'review/source_first_check.py'))
prior=json.loads(buffer.getvalue())
checks=[]
def check(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    if not ok:
        print(json.dumps(dict(status='FAIL',checks=checks),default=str))
        raise SystemExit(1)

t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z)
saved=json.loads((STEP/'author_commutator_active.stdout').read_text())
V=s.Matrix([s.sympify(a,locals=dict(zip(('t','x','y','z'),coords))) for a in saved['V']])
g=s.diag(-1,1,1,1)*(t*t+2)**2
result=independent['commutator_control']('exposed_author_metric',coords,g,list(g*V),False)
def tensor(name):
    return {str((b,a)):s.cancel(g.inv()[b,b]*s.sympify(result[name].get(str((a,b)),0)))
            for a in range(4) for b in range(4)}
F=tensor('curvature_term')
Div=tensor('differentiated_curvature_term')
left=tensor('direct_minus_gradwave')
Ric={k:s.cancel(left[k]-F[k]-Div[k]) for k in left}
counts=dict(two_curvature_gradient=sum(v!=0 for v in F.values()),
            div_curvature_vector=sum(v!=0 for v in Div.values()),
            Ricci_gradient=sum(v!=0 for v in Ric.values()))
check('all_saved_nonzero_term_counts',counts==saved['nonzero_term_counts'])
check('saved_baseline_and_independent_identity',saved['status']=='PASS' and saved['residuals']=={})
residual_data={}
for mode,expected in [('omit_div_curvature',Div),('omit_Ricci',Ric),
                      ('half_curvature',{k:v/2 for k,v in F.items()})]:
    payload=json.loads((STEP/('mutant_'+mode+'.stdout')).read_text())
    residual_data[mode]={k:str(v) for k,v in expected.items() if v!=0}
    check(mode+'_saved_is_failure',payload['status']=='FAIL')
    check(mode+'_all_saved_residuals',all(s.cancel(v-s.sympify(payload['residuals'].get(k,0),
          locals=dict(zip(('t','x','y','z'),coords))))==0 for k,v in expected.items())
          and set(payload['residuals'])=={k for k,v in expected.items() if v!=0})

# Check the saved general-b initial scalar independently from the ambient inverse
# metric, then from the full graph normal decomposition; no author imports.
u,v,x,y=s.symbols('u v x y',real=True)
b=s.Function('b')(u,x,y)
H=s.Function('H')(u,x,y)
c=s.symbols('c',real=True)
g2=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
alpha=s.Matrix([s.diff(b,w)/b for w in (u,v,x,y)])
q=s.cancel((alpha.T*g2.inv()*alpha)[0])
L=H+2*c
normal=(alpha[0]+(H+c)*alpha[1])/s.sqrt(L)
intrinsic=s.cancel((alpha[0]-c*alpha[1])**2/L+alpha[2]**2+alpha[3]**2-normal**2)
recipe=json.loads((STEP/'author_recipe_data.stdout').read_text())
qsaved=s.sympify(recipe['initial_scalar'],locals={'u':u,'v':v,'x':x,'y':y,'b':s.Function('b')})
check('saved_initial_scalar_recomputed',s.cancel(q-qsaved)==0)
check('independent_graph_normal_subtraction',s.cancel(q-intrinsic)==0)
check('author_recipe_guard_report',recipe['status']=='PASS' and recipe['guard_count']==len(recipe['guards'])==11)

print(json.dumps(dict(status='PASS',checks=checks,source_first_recheck=prior,
 compared_term_counts=counts,compared_mutant_residuals=residual_data,
 independently_recomputed_initial_scalar=str(q),
 scope='Exposed independent lower-covector coordinate differentiation compared to saved upper-vector quantities; no author code imports.'),
 indent=2,default=str))
