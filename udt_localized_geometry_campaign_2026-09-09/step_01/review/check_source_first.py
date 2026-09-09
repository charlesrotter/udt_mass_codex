"""Exact local adjoint and nonlinear momentum-density checks, independently written.

No candidate import; no source equation or simulation. CPU-only symbolic
certificates supplement SOURCE_FIRST.md and do not prove gluing existence.
"""
import json
import platform
import sys

import sympy as s

T = s.symbols('T', positive=True)
N = s.symbols('N')
k = [1 / (3*T), -2 / (3*T), -2 / (3*T)]
tau = sum(k)
sq = sum(v*v for v in k)
assert s.simplify(tau*tau-sq) == 0
# Full first-adjoint equations give d_i Y_i=N k_i. Trace of the
# second adjoint then gives Delta N=N tau^2, and B_ii=0 gives N_ii=N tau k_i.
lap = N*tau*tau
diagonal_second = []
for i in range(3):
    ni = N*tau*k[i]
    Bii = N*tau*k[i] - 2*N*k[i]**2 + N*sq - lap + ni + 2*N*k[i]**2 - 2*N*tau*k[i]
    diagonal_second.append(s.simplify(Bii))
assert diagonal_second == [0, 0, 0]
compatibility_coefficient = s.simplify(k[1]*(tau*k[2]+tau*k[1]))
assert compatibility_coefficient == -8/(9*T**3)

o12, o13, o23 = s.symbols('o12 o13 o23')
omega = s.Matrix([[0,o12,o13],[-o12,0,o23],[-o13,-o23,0]])
K = s.diag(*k)
commutator = K*omega-omega*K
equations = [commutator[i,j] for i in range(3) for j in range(i+1,3)]
rotation_matrix, _ = s.linear_eq_to_matrix(equations, [o12,o13,o23])
assert rotation_matrix.rank() == 2
assert rotation_matrix.nullspace() == [s.Matrix([0,0,1])]
bad_rotation = commutator.subs({o12:1,o13:0,o23:0})
assert bad_rotation != s.zeros(3)

# Reconstruct the exact pointwise nonlinear momentum identity from arbitrary
# metric/density first jets. g is a supplied nonsingular SPD test value, while
# all independent derivative and density slots remain algebraically arbitrary.
g = s.Matrix([[2,1,0],[1,3,1],[0,1,2]])
assert all(g[:i,:i].det()>0 for i in (1,2,3))
ginv = g.inv()
def symmat(prefix):
    slots = {(i,j):s.Symbol(f'{prefix}_{i}{j}') for i in range(3) for j in range(i,3)}
    return s.Matrix(3,3,lambda i,j:slots[tuple(sorted((i,j)))])
dg = [symmat(f'dg{a}') for a in range(3)]
pi = symmat('pi')
dpi = [symmat(f'dpi{a}') for a in range(3)]
Y = s.Matrix(s.symbols('Y0:3'))
dY = s.Matrix(3,3,lambda a,i:s.Symbol(f'dY{a}_{i}'))
Gamma = [[[sum(ginv[i,l]*(dg[j][l,m]+dg[m][l,j]-dg[l][j,m])/2 for l in range(3))
           for m in range(3)] for j in range(3)] for i in range(3)]
divpi = [sum(dpi[j][i,j] for j in range(3))+
         sum(Gamma[i][j][m]*pi[j,m] for j in range(3) for m in range(3)) for i in range(3)]
lieg = s.Matrix(3,3,lambda i,j:sum(Y[a]*dg[a][i,j]+g[a,j]*dY[i,a]+g[i,a]*dY[j,a]
                                              for a in range(3)))
fluxdiv = sum(dpi[j][i,j]*g[i,a]*Y[a]+pi[i,j]*dg[j][i,a]*Y[a]+pi[i,j]*g[i,a]*dY[j,a]
              for i in range(3) for j in range(3) for a in range(3))
momentum = sum(g[i,a]*Y[a]*divpi[i] for i in range(3) for a in range(3))
strain = sum(pi[i,j]*lieg[i,j]/2 for i in range(3) for j in range(3))
identity_residual = s.expand(fluxdiv-momentum-strain)
assert identity_residual == 0
bare_momentum = sum(g[i,a]*Y[a]*dpi[j][i,j] for i in range(3) for a in range(3) for j in range(3))
connection_omission_residual = s.expand(fluxdiv-bare_momentum-strain)
assert connection_omission_residual != 0

# Full tensor Lie derivative must be retained for local rotation. A constant
# anisotropic h has zero directional derivative but nonzero tensor rotation.
h = s.diag(0,1,0)
rot = s.Matrix([[0,0,0],[0,0,-1],[0,1,0]])
full_rotation = rot.T*h+h*rot
assert full_rotation != s.zeros(3)
assert full_rotation[1,2] == -1

print(json.dumps({
    'status':'PASS_EXACT_SYMBOLIC_SCOPED',
    'python':sys.version,
    'sympy':s.__version__,
    'platform':platform.platform(),
    'no_lapse_coefficient':str(compatibility_coefficient),
    'rotation_constraint_rank':int(rotation_matrix.rank()),
    'local_kernel_dimension':4,
    'global_translation_quotient_kernel_dimension':3,
    'full_nonlinear_momentum_density_identity_residual':str(identity_residual),
    'catch_proofs':{
        'forbidden_x_y_rotation_rejected':bool(bad_rotation != s.zeros(3)),
        'missing_connection_term_rejected':bool(connection_omission_residual != 0),
        'componentwise_rotation_derivative_rejected':bool(full_rotation != s.zeros(3))},
    'limitations':['No nonlinear gluing existence','No general PDE surjectivity',
                   'Global kernel count uses the analytic full-rank-lattice proof',
                   'The exact identity is algebraic; integration/support is analytic'],
}, indent=2, sort_keys=True))
