"""Exposed independent comparison against saved PC1 quantities; stdout only."""
import ast
import contextlib
import io
import itertools
import json
import pathlib
import runpy
import sympy as s

review = pathlib.Path(__file__).resolve().parent
step = review.parent
with contextlib.redirect_stdout(io.StringIO()):
    own = runpy.run_path(str(review/'source_first_check.py'))
saved = json.loads((step/'diagnose_weyl_corrected.stdout').read_text())
old_c,old_i,old_j = s.symbols('c i j')
conversion = {old_c:-own['lam'],old_i:own['var'][19],old_j:-own['var'][20]}
compared = 0
for key,value in saved['B_full'].items():
    idx = ast.literal_eval(key)
    right = s.sympify(value).subs(conversion, simultaneous=True)
    assert s.expand(own['B'][idx]-right) == 0, (idx,own['B'][idx],right)
    compared += 1
assert compared == 256
assert own['B'][1,0,0,0] == own['B'][2,0,0,0] == 0
assert s.expand(own['B'][1,1,1,1]-2*own['lam']**2/3) == 0
for key,value in saved['ambient_nonzero'].items():
    a,b,d=ast.literal_eval(key)
    assert s.expand(own['qs'][a,b,0,d]+own['qs'][a,b,3,d]-
                    s.sympify(value).subs(conversion,simultaneous=True)) == 0

# Independently differentiated general graph, using the mixed-index momentum
# divergence rather than the author's lower-index contraction implementation.
u,x,y,c = s.symbols('u x y c',real=True)
coord=[u,x,y]
H=s.Function('H')(u,x,y)
F=H+2*c
gam=s.diag(F,1,1)
inv=gam.inv()
C={}
for a,b,d in itertools.product(range(3),repeat=3):
    C[a,b,d]=s.simplify(sum(inv[a,k]*(s.diff(gam[k,b],coord[d])+
         s.diff(gam[k,d],coord[b])-s.diff(gam[b,d],coord[k])) for k in range(3))/2)
ric=s.zeros(3)
for i,j in itertools.product(range(3),repeat=2):
    ric[i,j]=s.simplify(sum(s.diff(C[k,i,j],coord[k])-s.diff(C[k,i,k],coord[j])+
       sum(C[k,k,m]*C[m,i,j]-C[k,j,m]*C[m,i,k] for m in range(3)) for k in range(3)))
# K from Hess(v+c*u)/sqrt(F) under the independently reconstructed ambient connection.
K=s.zeros(3)
for i in range(3):
    K[0,i]=K[i,0]=s.diff(H,coord[i])/(2*s.sqrt(F))
scalar=s.simplify(s.trace(inv*ric))
tr=s.trace(inv*K)
ham=s.simplify(scalar+tr**2-s.trace(inv*K*inv*K))
stress=K*inv-tr*s.eye(3)
mom=[s.simplify(sum(s.diff(stress[i,j],coord[j])+
     sum(C[j,j,k]*stress[i,k]-C[k,j,i]*stress[k,j] for k in range(3))
     for j in range(3))) for i in range(3)]
data=json.loads((step/'author_exact.stdout').read_text())
locals_map=dict(H=s.Function('H'),u=u,x=x,y=y,c=c)
parse=lambda text:s.sympify(text,locals=locals_map)
checks={
  'gamma':all(s.simplify(z)==0 for z in gam-parse(data['gamma'])),
  'K':all(s.simplify(z)==0 for z in K-parse(data['K'])),
  'scalar_three':s.simplify(scalar-parse(data['scalar_three']))==0,
  'hamiltonian':s.simplify(ham-parse(data['hamiltonian']))==0,
  'momentum':all(s.simplify(a-parse(b))==0 for a,b in zip(mom,data['momentum'])),
  'f':s.simplify(1/s.sqrt(F)-parse(data['f']))==0,
  'Y':all(s.simplify(a-parse(b))==0 for a,b in zip([-1/F,0,0],data['Y'])),
  'full_root_obstruction':own['B'][1,0,0,0]==0 and own['B'][2,0,0,0]==0,
}
assert all(checks.values()),checks
print(json.dumps(dict(status='PASS',B_components_compared=compared,
  parameter_translation='author(c,i,j)=(-Lambda,z19,-z20)',
  checks=checks,hamiltonian=str(ham),momentum=list(map(str,mom)),
  implementation='independent reviewer tensor code plus exposed general-graph comparison; no author imports',
  exposure='candidate, author code and saved results exposed before this comparator was written'),indent=2))
