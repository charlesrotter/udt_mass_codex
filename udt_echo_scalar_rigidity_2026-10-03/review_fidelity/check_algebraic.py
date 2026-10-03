"""Finite exact source-first curvature check; no ESR/IEC code is imported."""
from pathlib import Path
import hashlib
import json
import os
import platform
import sympy as s

root = Path(__file__).resolve().parent
eta = s.diag(-1, 1, 1, 1)
pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
symbols = s.symbols('b0:21')
B = s.zeros(6)
k = 0
for i in range(6):
    for j in range(i, 6):
        B[i, j] = B[j, i] = symbols[k]
        k += 1

def wedge(x, y):
    return s.Matrix([x[i]*y[j]-x[j]*y[i] for i, j in pairs])

def tensor(x, y, z, w):
    return (wedge(x, y).T*B*wedge(z, w))[0]

def electric(frame):
    u = frame[:, 0]
    return s.Matrix(3, 3, lambda i, j:
                    s.expand(tensor(frame[:, i+1], u, u, frame[:, j+1])))

def boost(direction):
    d = s.Matrix(direction)
    assert (d.T*d)[0] == 1
    gamma, speed = s.Rational(5, 4), s.Rational(3, 4)
    m = s.eye(4)
    m[0, 0] = gamma
    for i in range(3):
        m[0, i+1] = m[i+1, 0] = speed*d[i]
        for j in range(3):
            m[i+1, j+1] += (gamma-1)*d[i]*d[j]
    assert m.T*eta*m == eta
    assert m[0, 0] > 0
    return m

directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1),
              (0,0,-1), (s.Rational(3,5), s.Rational(4,5), 0),
              (-s.Rational(3,5), -s.Rational(4,5), 0)]
frames = [s.eye(4)] + [boost(d) for d in directions]
bianchi = B[0,5]-B[1,4]+B[2,3]
isotropy, zero = [bianchi], [bianchi]
electric_matrices = [electric(f) for f in frames]
for e in electric_matrices:
    isotropy.extend([e[0,1], e[0,2], e[1,2], e[0,0]-e[1,1], e[1,1]-e[2,2]])
    zero.extend([e[0,0], e[1,1], e[2,2], e[0,1], e[0,2], e[1,2]])

Miso, _ = s.linear_eq_to_matrix(isotropy, symbols)
Mzero, _ = s.linear_eq_to_matrix(zero, symbols)
rank_iso, rank_zero = Miso.rank(), Mzero.rank()
assert rank_iso == 20, rank_iso
assert rank_zero == 21, rank_zero
spaceform_B = s.diag(*[-eta[i,i]*eta[j,j] for i,j in pairs])
spatial_B = s.diag(*[-int(i>0 and j>0) for i,j in pairs])

def flatten(m):
    return s.Matrix([m[i,j] for i in range(6) for j in range(i,6)])

constant_vector = flatten(spaceform_B)
assert Miso*constant_vector == s.zeros(Miso.rows, 1)
ns = Miso.nullspace()
assert len(ns) == 1 and s.Matrix.hstack(ns[0], constant_vector).rank() == 1
assert s.Matrix(Miso[:6, :]).rank() == 6  # one frame leaves 15 of 21 raw variables

sub = dict(zip(symbols, flatten(spatial_B)))
spatial_e = [e.subs(sub) for e in electric_matrices]
assert spatial_e[0] == s.zeros(3)
assert any(e != s.zeros(3) for e in spatial_e[1:])
assert any(e != s.eye(3)*e[0,0] for e in spatial_e[1:])
assert bianchi.subs(sub) == 0
assert spatial_B != s.zeros(6)
constraints = len(isotropy)+len(zero)+6*len(spatial_e)
assert constraints <= 500
result = {
    'status': 'PASS', 'families': 3, 'scalar_constraint_evaluations': constraints,
    'frames': [[str(v) for v in f] for f in frames],
    'isotropy_matrix_shape': list(Miso.shape), 'isotropy_rank': rank_iso,
    'zero_electric_matrix_shape': list(Mzero.shape), 'zero_electric_rank': rank_zero,
    'single_frame_isotropy_rank': 6,
    'spaceform_kernel_vector': [str(x) for x in constant_vector],
    'ultrastatic_electric_rest': [[str(x) for x in row] for row in spatial_e[0].tolist()],
    'ultrastatic_electric_first_boost': [[str(x) for x in row] for row in spatial_e[1].tolist()],
    'python': platform.python_version(), 'sympy': s.__version__,
    'thread_environment': {k: os.environ.get(k) for k in
                           ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']},
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'limits': 'Exact rational finite 55x21 maximum; no numerical tolerance or metric census',
}
output = root/'CHECK_RESULT.json'
with output.open('x') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
print(json.dumps(result, indent=2))
