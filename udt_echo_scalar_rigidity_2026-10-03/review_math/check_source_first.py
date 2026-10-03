"""Independent exact algebra anchors; no ESR1 candidate or code is loaded."""
import json
import platform
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
checks = []

def check(label, condition):
    checks.append({"label": label, "pass": bool(condition)})
    if not condition:
        raise AssertionError(label)

# Family 1: Taylor coefficient recomputed directly from reviewed IEC hand audit.
e, T, aa, ab, bb, c = s.symbols("e T aa ab bb c")
p = 1-T*e/2+(T*T/6-ab/6-bb/24)*e**2
q = 1-3*T*e/2+(T*T/4+2*aa+ab/2-bb/8)*e**2
residual = s.expand(q-(1+3*(p-1)+c*(p-1)**2)).coeff(e, 2)
check("arbitrary_Q_quartic", s.expand(residual-(2*aa+ab-(c+1)*T*T/4)) == 0)
check("eigendirection_fixes_c7", s.expand(residual.subs({aa:T*T, ab:0})-(7-c)*T*T/4) == 0)
z = s.symbols("z")
q0 = (1+z)/(2-(1+z)**2)
check("rational_Q_first_jet", s.diff(q0, z).subs(z, 0) == 3)
check("rational_Q_second_jet", s.diff(q0, z, 2).subs(z, 0) == 14)

# Family 2: independent 21-variable curvature tensor linear system.
# R_abcd=g(R(e_a,e_b)e_c,e_d), paired bivector symmetric matrix; Bianchi added.
g = s.diag(-1, 1, 1, 1)
base = [s.eye(4)[:, i] for i in range(4)]
pairs = [(i,j) for i in range(4) for j in range(i+1,4)]
where = {pair:i for i,pair in enumerate(pairs)}
variables = s.symbols("r0:21")
matrix = s.zeros(6)
cursor = 0
for i in range(6):
    for j in range(i,6):
        matrix[i,j] = matrix[j,i] = variables[cursor]
        cursor += 1

def comp(a,b,c,d):
    if a == b or c == d:
        return s.S.Zero
    sign = (1 if a<b else -1)*(1 if c<d else -1)
    return sign*matrix[where[tuple(sorted((a,b)))], where[tuple(sorted((c,d)))]]

def curvature(x,y,z,w):
    xv = [(i,x[i]) for i in range(4) if x[i]]
    yv = [(i,y[i]) for i in range(4) if y[i]]
    zv = [(i,z[i]) for i in range(4) if z[i]]
    wv = [(i,w[i]) for i in range(4) if w[i]]
    return s.expand(sum(vx*vy*vz*vw*comp(a,b,c,d)
        for a,vx in xv for b,vy in yv for c,vz in zv for d,vw in wv))

equations = [comp(0,1,2,3)+comp(1,2,0,3)+comp(2,0,1,3)]
frames = [(base[0], base[1:])]
for axis in range(1,4):
    for sign in [-1,1]:
        ch,sh=s.Rational(5,3),sign*s.Rational(4,3)
        U=ch*base[0]+sh*base[axis]
        spatial=[sh*base[0]+ch*base[axis]]+[base[j] for j in range(1,4) if j!=axis]
        frames.append((U,spatial))

for k,(U,spatial) in enumerate(frames):
    frame=s.Matrix.hstack(U,*spatial)
    check(f"frame_{k}_orthonormal", frame.T*g*frame == g)
    electric=s.Matrix(3,3,lambda i,j:curvature(spatial[i],U,U,spatial[j]))
    equations.extend([electric[0,1],electric[0,2],electric[1,2],
                      electric[0,0]-electric[1,1],electric[0,0]-electric[2,2]])

A,b=s.linear_eq_to_matrix(equations,variables)
check("curvature_system_shape", A.shape == (36,21))
check("curvature_system_homogeneous", b == s.zeros(36,1))
rank=A.rank()
null=A.nullspace()
check("curvature_system_rank20", rank == 20)
check("curvature_system_nullity1", len(null) == 1)
model=s.Matrix([g[b,c]*g[a,d]-g[a,c]*g[b,d]
    for i,(a,b) in enumerate(pairs) for c,d in pairs[i:]])
check("constant_K_tensor_in_nullspace", A*model == s.zeros(36,1))
factor=next(null[0][i]/model[i] for i in range(21) if model[i])
check("only_constant_K_tensor_survives", null[0] == factor*model)
check("no_vacuous_zero_constraint_matrix", any(A))
# Negative control: a Lorentz2 x flat2 product has only the 01 curvature block.
product=s.zeros(21,1)
product[0]=1
check("product_has_explicit_violated_constraint", A*product != s.zeros(36,1))

result={"status":"PASS", "python":platform.python_version(), "sympy":s.__version__,
    "families":2,"scalar_assertions":len(checks),"frames":len(frames),
    "matrix_shape":list(A.shape),"matrix_rank":rank,"matrix_nullity":len(null),
    "exact_quartic_residual":str(residual),"checks":checks,
    "limits":"Finite exact anchors; proof and reviewed IEC hypotheses own the universal claim."}
destination=HERE/"SOURCE_FIRST_CHECK_RESULT.json"
with destination.open("x") as f:
    json.dump(result,f,indent=2)
    f.write("\n")
print(json.dumps(result,sort_keys=True),flush=True)
