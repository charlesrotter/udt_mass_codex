"""Independent generic-bivector first-jet review; no author scientific imports."""
import itertools
import json
import sys
import sympy as s

eta = [-1, 1, 1, 1]
pairs = list(itertools.combinations(range(4), 2))
upper = list(itertools.combinations_with_replacement(range(6), 2))
symbols = s.symbols('z:21')
bil = s.zeros(6)
for (i, j), z in zip(upper, symbols):
    bil[i, j] = bil[j, i] = z

def q(a, b, c, d):
    if a == b or c == d:
        return s.Integer(0)
    i = pairs.index(tuple(sorted((a, b))))
    j = pairs.index(tuple(sorted((c, d))))
    return (1 if a < b else -1) * (1 if c < d else -1) * bil[i, j]

ric = s.Matrix(4, 4, lambda b, c: sum(eta[a]*q(a, b, c, a) for a in range(4)))
scalar = sum(eta[a]*ric[a, a] for a in range(4))
conditions = [q(a,b,c,d)+q(b,c,a,d)+q(c,a,b,d)
              for a,b,c,d in itertools.product(range(4), repeat=4)]
conditions += [ric[a,b] - (eta[a]*scalar/4 if a == b else 0)
               for a,b in itertools.combinations_with_replacement(range(4), 2)]
alg = s.linear_eq_to_matrix(conditions, symbols)[0]
basis = s.Matrix.hstack(*alg.nullspace())
assert basis.shape == (21, 11)

def row(a,b,c,d):
    return s.linear_eq_to_matrix([q(a,b,c,d)], symbols)[0] * basis

rows = {(a,b,c,d): row(a,b,c,d) for a,b,c,d in itertools.product(range(4), repeat=4)}
def derivative_row(m,a,b,c,d):
    r = s.zeros(1,44)
    r[:,11*m:11*(m+1)] = rows[a,b,c,d]
    return r

bianchi = s.Matrix.vstack(*[
    derivative_row(m,a,b,c,d)+derivative_row(a,b,m,c,d)+derivative_row(b,m,a,c,d)
    for m,a,b in itertools.combinations(range(4),3)
    for c,d in pairs
])
lam = -sum((rows[i,0,0,i] for i in range(1,4)), s.zeros(1,11))
dlam = s.zeros(4,44)
for m in range(4):
    dlam[m,11*m:11*(m+1)] = lam
assert bianchi.rank() == 20
assert s.Matrix.vstack(bianchi,dlam).rank() == 20
fixed_scalar_basis = s.Matrix.hstack(*dlam.nullspace())
assert (bianchi*fixed_scalar_basis).rank() == 16
assert len(bianchi.nullspace()) == 24

electric_slots = list(itertools.combinations_with_replacement(range(1,4),2))
fit = s.Matrix.vstack(*[rows[i,0,0,j] for i,j in electric_slots],
                      *[rows[i,0,j,k] for i in range(1,4)
                        for j,k in itertools.combinations(range(1,4),2)])
def from_electric(diagonal):
    target=s.Matrix([diagonal[i-1] if i==j else 0 for i,j in electric_slots]+[0]*9)
    answer,free=fit.gauss_jordan_solve(target)
    assert free.rows == 0 and fit*answer==target
    return answer

v = from_electric([1,-1,0])
bad = s.zeros(44,1)
bad[11:22,0] = v
bad_residual = bianchi*bad
assert any(bad_residual)
assert dlam*bad == s.zeros(4,1)
div_e = [sum((rows[i,0,0,j]*bad[11*i:11*(i+1),0])[0] for i in range(1,4))
         for j in range(1,4)]
assert div_e == [1,0,0]

record_rows=[rows[i,0,0,j] for i,j in electric_slots]
for i,j,k in [(1,2,3),(2,3,1),(3,1,2)]:
    for sign in [1,-1]:
        for a,b in [(j,j),(j,k),(k,k)]:
            record_rows.append(rows[a,0,0,b]+sign*rows[a,i,0,b]+
                               sign*rows[a,0,i,b]+rows[a,i,i,b])
record=s.Matrix.vstack(*record_rows)
annihilator=s.Matrix.vstack(*(n.T for n in record.T.nullspace()))
assert record.rank()==11 and annihilator.rank()==13
assert annihilator*record*v == s.zeros(13,1)

def tensor(coef):
    return {key:(r*coef)[0] for key,r in rows.items()}

def frame_action(tensor_value, omega):
    result={}
    for key in rows:
        total=0
        for slot in range(4):
            for r in range(4):
                replaced=list(key)
                replaced[slot]=r
                total += omega[key[slot],r]*tensor_value[tuple(replaced)]
        result[key]=s.expand(total)
    return result

generators=[]
for a,b in pairs:
    omega=s.zeros(4)
    omega[a,b]=1
    omega[b,a]=-s.Rational(eta[b],eta[a])
    assert s.diag(*eta)*omega.T+omega*s.diag(*eta)==s.zeros(4)
    generators.append(omega)
zero=tensor(s.zeros(11,1))
scalar_tensor=tensor(from_electric([-1,-1,-1]))
for omega in generators:
    assert not any(frame_action(zero,omega).values())
    assert not any(frame_action(scalar_tensor,omega).values())

# A changing frame creates raw slopes even when the corrected derivative is zero.
# This is a tensor gauge control, not an Einstein-development existence argument.
omega=generators[pairs.index((1,2))]
action=frame_action(tensor(v),omega)
action_vector=s.Matrix([action[pairs[i]+pairs[j]] for i,j in upper])
coef,free=basis.gauss_jordan_solve(action_vector)
assert free.rows==0
raw=s.zeros(44,1)
raw[11:22,0]=coef
assert any(bianchi*raw)
assert bianchi*(raw-raw)==s.zeros(24,1)

# An intentionally omitted final slot cannot masquerade as the full action.
partial={}
for key in rows:
    partial[key]=action[key]-sum(omega[key[3],r]*tensor(v)[key[:3]+(r,)] for r in range(4))
assert partial != action

result=dict(status='SOURCE_FIRST_CHECKS_PASS_NOT_CANDIDATE_VERDICT',
    python=sys.version,sympy=s.__version__,algebraic_constraint_rank=alg.rank(),
    einstein_dimension=basis.cols,record_rank=record.rank(),record_annihilator_rank=annihilator.rank(),
    differential_bianchi_shape=list(bianchi.shape),differential_bianchi_rank=bianchi.rank(),
    fixed_scalar_derivative_dimension=fixed_scalar_basis.cols,
    fixed_scalar_bianchi_rank=(bianchi*fixed_scalar_basis).rank(),
    formal_einstein_curvature_derivative_dimension=len(bianchi.nullspace()),
    bad_jet_electric_divergence=div_e,bad_jet_bianchi_residual=list(bad_residual),
    bad_jet_record_derivative=list(record*v),
    all_frame_actions_zero_at_zero_and_scalar_curvature=True,
    changing_frame_raw_bianchi_residual=list(bianchi*raw),
    limitations=['finite exact algebra, not PDE existence',
                'raw-minus-identical-correction guard is regression/tautological and excluded as independent evidence',
                'no author candidate/code/results exposed'])
print(json.dumps(result,default=str,indent=2))
