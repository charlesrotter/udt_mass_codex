import hashlib,json,platform
from pathlib import Path
import sympy as s
base=Path('development_reconstruction_2026-09-29')
out=base/'review/math'
freeze=json.loads((base/'PILOT_FREEZE.json').read_text())
pilot=base/'PILOT_CANDIDATE.md'
digest=hashlib.sha256(pilot.read_bytes()).hexdigest()
assert digest==freeze['sha256'][str(pilot)]
seal=json.loads((out/'SOURCE_FIRST_SEAL.json').read_text())
for p,h in seal['artifacts'].items():
    assert hashlib.sha256((out/p).read_bytes()).hexdigest()==h,p
x=s.symbols('x',real=True)
D=s.diag(s.exp(-x),s.exp(x))
J=s.simplify(D.inv()*D.diff(x))
assert s.trace(J)**2/2==0
assert s.trace(J*J)/2==1
# Recompute the parent's displayed regular witness without its functions.
E=s.Matrix([[4,1,0,0],[1,2,1,0],[0,1,2,1],[1,0,1,2]])
F=s.Matrix([[2,0],[0,1],[0,1],[0,0]])
H=F.T*E.T*s.diag(-1,1,1,1)*E*F
assert H[0,1]==0 and H[0,0]<0 and H.det()<0
ours=json.loads((out/'core_results.json').read_text())
assert ours['checks']['G179_full_witness'] and ours['checks']['completed_shift']
record={'pilot_sha256':digest,'source_first_seal_unchanged':True,
 'literal_squared_trace':str(s.trace(J)**2/2),
 'trace_of_matrix_square_on_unit_parameter_tangent':str(s.trace(J*J)/2),
 'parent_regular_witness':str(H),'parent_regular_witness_nonzero_shift':False,
 'reviewer_generic_and_nonzero_shift_checks':True,
 'python':platform.python_version(),'sympy':s.__version__}
with (out/'pilot_direct_results.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record,sort_keys=True))
