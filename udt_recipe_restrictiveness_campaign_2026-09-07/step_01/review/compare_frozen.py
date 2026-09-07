"""Exposed comparison against sealed reviewer calculations, no author imports."""
import ast
import contextlib
import io
import itertools
import json
from pathlib import Path
import runpy
here=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    d=runpy.run_path(str(here/'source_first.py'))
    initial=runpy.run_path(str(here/'initial_data_check.py'))
s=d['s']; u,v,x,y,k=[d[z] for z in ('u','v','x','y','k')]
e=s.Symbol('epsilon',real=True); I=range(4); coords=(u,v,x,y)
saved=json.loads((here.parent/'author_exact.stdout').read_text())
syms={str(z):z for z in (u,v,x,y,k,e)}
def parse(z): return s.sympify(z,locals=syms)
def equal(a,b):
    if isinstance(a,s.MatrixBase): return (a-b).applyfunc(s.simplify)==s.zeros(*a.shape)
    return s.simplify(a-b)==0
checks={}
def check(name,truth):
    checks[name]=bool(truth)
    assert truth,name
for name,ref in [('gamma0',initial['ga']),('delta_gamma',initial['ha']),('K0',initial['K']),('delta_K',initial['dK'])]:
    check('saved_'+name,equal(parse(saved[name]),ref))
savedB={ast.literal_eval(key):parse(val) for key,val in saved['delta_B_nonzero'].items()}
check('all256_saved_B1',all(equal(d['dB'][ix],savedB.get(ix,0)) for ix in itertools.product(I,repeat=4)))
check('saved_root_tangent',all(equal(parse(val),d['root_ratios'][i]) for i,val in enumerate(saved['relative_root_tangent'])))
check('saved_root_direction',equal(parse(saved['root_direction_variation']),s.Matrix([0,0,-d['root_ratios'][2],-d['root_ratios'][3]])))
check('saved_differential_obstruction',equal(parse(saved['seed_derivative_obstruction']),-s.diff(d['root_ratios'][3],x)))

# Independently recompute exact finite metric Ricci as an explicit connection
# divergence, not by importing the author's four-tensor implementation.
finite=d['g']+e*d['h'].subs(k,-2); inv=finite.inv()
Gamma={}
for a,b,c in itertools.product(I,repeat=3):
    Gamma[a,b,c]=s.expand(sum(inv[a,z]*(s.diff(finite[z,c],coords[b])+s.diff(finite[z,b],coords[c])-s.diff(finite[b,c],coords[z])) for z in I)/2)
Ric=s.Matrix(4,4,lambda a,b:s.simplify(sum(s.diff(Gamma[c,a,b],coords[c])-s.diff(Gamma[c,c,a],coords[b])+sum(Gamma[c,c,z]*Gamma[z,a,b]-Gamma[c,b,z]*Gamma[z,c,a] for z in I) for c in I)))
check('finite_saved_Ricci',equal(Ric,parse(saved['Ricci'])))
check('finite_scalar_zero',s.simplify(s.trace(inv*Ric))==0)
dt=s.Matrix([2,1,0,0]); S=s.simplify(-(dt.T*inv*dt)[0])
check('finite_saved_S',equal(S,parse(saved['S'])))
n=-inv*dt/s.sqrt(S); T=d['Tang']
ham=(2*(n.T*Ric*n)[0]).subs(v,-2*u)
mom=(-T.T*Ric*n).subs(v,-2*u)
check('saved_Hamiltonian_projection',equal(ham,parse(saved['Hamiltonian_projection'])))
check('saved_momentum_projection',equal(mom,parse(saved['momentum_projection'])))
check('independent_intrinsic_linear_constraints',initial['dham']==0 and initial['dmomentum']==[0,0,0])

# Spatial integrability alone, retaining every seed component (not imposing
# nullness or using full ambient annihilation), reconstructed from reviewer Q.
a=s.symbols('a0:4')
eq=[s.simplify(sum(T[A,i]*T[B,j]*(d['dQ'][A,B,1,D]+sum(d['Q'][A,B,c,D]*a[c] for c in I)) for A,B in itertools.product(I,repeat=2))) for i,j,D in itertools.product(range(3),range(3),I)]
solution=s.linsolve(eq,a)
expected=s.FiniteSet((0,a[1],-y/(3*(x*x+y*y)),-x/(3*(x*x+y*y))))
check('spatial_only_integrability_converse',solution==expected)
check('full_spatial_substitution',all(s.simplify(q.subs(dict(zip(a,next(iter(expected))))))==0 for q in eq))
# False-pass counterchecks change actual substantive values; no FAIL toggles.
check('omitted_vterm_activity',d['dric'].subs(k,0)[0,3]==-1)
check('omitted_transverse_root_activity',d['dB'][0,0,0,3].subs({x:1,y:0})==12)
check('wrong_K_variation_detected',not equal(parse(saved['delta_K']),-initial['dK']))
print(json.dumps(dict(status='PASS',checks=checks,exact_Ricci=Ric.tolist(),spatial_solution=str(solution),independence='reviewer implementation only; saved author strings used solely as comparison targets'),indent=2,default=str))
