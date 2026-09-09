"""Expose the off-constraint map difference; not a new science result."""
import json
import platform
import sympy as s
e,a,x,y,z=s.symbols('e a x y z', real=True)
coords=(x,y,z)
gamma=s.diag(1+e,1,1)
gi=gamma.inv()
K=s.diag(a,-2*a+x,-2*a)
# All spatial metric derivatives vanish for this explicit off-constraint probe.
tau=s.trace(gi*K)
mixed=gi*K
M=s.Matrix([sum(s.diff(mixed[j,i],coords[j]) for j in range(3))-s.diff(tau,coords[i]) for i in range(3)])
J=-2*M
raised=gi*J
assert J==s.Matrix([2,0,0])
assert J.diff(e)==s.zeros(3,1)
discrepancy=s.simplify((raised-J).diff(e).subs(e,0))
assert discrepancy==s.Matrix([-2,0,0])
assert discrepancy!=s.zeros(3,1)  # reject same-zero-set => same-linearization shortcut
for signs in ((-1,1,1),(1,-1,1),(1,1,-1)):
    S=s.diag(*signs)
    assert S.T*s.eye(3)*S==s.eye(3)  # fixed-base vector/covector pairing invariant
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
 'status':'PASS','covector_J':str(J),'wrong_map_derivative_difference':str(discrepancy),
 'evidence_kind':'explicit off-constraint false-interface witness; not PDE theorem',
 'scientific_scope_changed':False},indent=2))
