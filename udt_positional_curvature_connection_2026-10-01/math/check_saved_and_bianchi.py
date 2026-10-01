"""Exposed mathematical review: compare saved independent outputs and PCC-c.

Shares SymPy with both calculations. Does not claim an independent library.
No parent implementation is imported or executed by this script.
"""
import hashlib
import itertools
import json
import platform
from pathlib import Path
import sympy as s

base = Path(__file__).resolve().parents[1]
own_path = base/'math/geometry_output.json'
parent_path = base/'checks/curvature_repaired.stdout'
own = json.loads(own_path.read_text())
parent = json.loads(parent_path.read_text())
checks = []


def eq(label, actual, expected=0):
    residual = s.simplify(s.expand_trig(actual-expected))
    checks.append({'label':label,'residual':str(residual),'pass':residual == 0})
    assert residual == 0,(label,residual)


# The two independently produced saved artifacts have different conventions:
# own sectionals are A(a,b,b,a)/(eta_aa eta_bb), parent stores A itself.
eta = [-1,1,1,1]
sections = {ij:s.sympify(own['static_sectionals'][str(ij)])
            for ij in itertools.combinations(range(4),2)}
sections = {ij:v.subs({s.Symbol('m'):s.Symbol('mu'),s.Symbol('k'):s.Symbol('kappa')})
            for ij,v in sections.items()}
for idx in itertools.product(range(4),repeat=4):
    a,b,c,d = idx
    expected = s.S.Zero
    if a != b:
        q = sections[tuple(sorted((a,b)))]*eta[a]*eta[b]
        if a == d and b == c:
            expected = q
        elif a == c and b == d:
            expected = -q
    actual = s.sympify(parent['orthonormal_curvature'].get(','.join(map(str,idx)),'0'))
    eq('saved independent full tensor '+str(idx),actual,expected)

# Direct covariant divergence under the physical connection in the variable-k
# example; reference Bianchi alone cannot set this residual to zero.
t,x,y,z,c = s.symbols('t x y z c',real=True)
coordinates = [t,x,y,z]
a = s.exp(t*t/2+c*t)
diag = [-s.S.One,a*a,a*a,a*a]
Gamma = {}
for i,j,k in itertools.product(range(4),repeat=3):
    Gamma[i,j,k] = s.simplify((
        (s.diff(diag[i],coordinates[j]) if i == k else 0)
        +(s.diff(diag[i],coordinates[k]) if i == j else 0)
        -(s.diff(diag[j],coordinates[i]) if j == k else 0))/(2*diag[i]))
Sdiag = [-3*(1+t*t),*(a*a*(1+3*t*t) for _ in range(3))]
S = lambda i,j:Sdiag[i] if i == j else s.S.Zero
divergence = []
for b in range(4):
    result = 0
    for j in range(4):
        derivative = s.diff(S(j,b),coordinates[j])
        derivative -= sum(Gamma[d,j,j]*S(d,b)+Gamma[d,j,b]*S(j,d)
                          for d in range(4))
        result += derivative/diag[j]
    divergence.append(s.simplify(result))
trace = s.simplify(sum(Sdiag[i]/diag[i] for i in range(4)))
kappa = 2*c*t+c*c
rhs = [s.simplify(divergence[i]-s.diff(trace,coordinates[i])/2) for i in range(4)]
for i in range(4):
    eq('PCC-c direct covariant component '+str(i),rhs[i],3*s.diff(kappa,coordinates[i]))
eq('nonzero generic time residual',rhs[0],6*c)
eq('reference pulled trace',trace,6+12*t*t)

result = {'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'source_hashes':{str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (own_path,parent_path)},
          'check_count':len(checks),'checks':checks,
          'reference_tensor_divergence_under_physical_connection':list(map(str,divergence)),
          'half_trace_corrected_divergence':list(map(str,rhs)),
          'kappa':str(kappa),
          'limits':'Saved independent symbolic tensor comparison and one direct covariant example; not a general regional existence theorem.'}
(base/'math/saved_and_bianchi_output.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'PCC-c_rhs':list(map(str,rhs))}))
