"""Exact finite algebraic anchors for GRC1 B2; no floating-point survey."""
import itertools
import json
import platform
import sympy as s

eta = s.diag(-1, 1, 1, 1)
basis = [s.eye(4)[:, i] for i in range(4)]
pairs = list(itertools.combinations(range(4), 2))
variables = s.symbols('r0:21')
pair_matrix = s.zeros(6)
cursor = 0
for i in range(6):
    for j in range(i, 6):
        pair_matrix[i, j] = pair_matrix[j, i] = variables[cursor]
        cursor += 1

def wedge(x, y):
    return s.Matrix([x[i]*y[j]-x[j]*y[i] for i, j in pairs])

def D(x, y, z, w):
    return s.expand((wedge(x, y).T*pair_matrix*wedge(z, w))[0])

def B(x, y, z, w):
    dot = lambda a, b: (a.T*eta*b)[0]
    return s.expand(dot(y,z)*dot(x,w)-dot(x,z)*dot(y,w))

# Pair antisymmetry and pair exchange are built in; impose algebraic Bianchi.
equations = []
for i,j,k,l in itertools.product(range(4), repeat=4):
    q = D(basis[i],basis[j],basis[k],basis[l])
    q += D(basis[j],basis[k],basis[i],basis[l])
    q += D(basis[k],basis[i],basis[j],basis[l])
    if q != 0:
        equations.append(q)
bianchi_rank = s.linear_eq_to_matrix(equations, variables)[0].rank()

# Exact null directions, with complete symmetric screen tests per chosen ray.
# These finite constraints are independently checked to leave only space-form
# algebra, rather than being treated as an assumed sample of all directions.
spatial_directions = []
for i in range(3):
    v = s.zeros(3, 1); v[i] = 1
    spatial_directions += [v, -v]
for i,j in itertools.combinations(range(3), 2):
    for si,sj in itertools.product([-1,1], repeat=2):
        v = s.zeros(3,1); v[i] = s.Rational(3,5)*si
        v[j] = s.Rational(4,5)*sj
        spatial_directions.append(v)
null_count = 0
for v in spatial_directions:
    k = s.Matrix([1, *v])
    assert (k.T*eta*k)[0] == 0
    screen = s.Matrix([list(v)]).nullspace()
    for n in [screen[0], screen[1], screen[0]+screen[1]]:
        nn = s.Matrix([0, *n])
        assert (nn.T*eta*k)[0] == 0
        equations.append(D(nn,k,k,nn)); null_count += 1
matrix = s.linear_eq_to_matrix(equations, variables)[0]
nullspace = matrix.nullspace()
constant_vector = s.Matrix([B(basis[i],basis[j],basis[k],basis[l])
                           for p,(i,j) in enumerate(pairs)
                           for k,l in pairs[p:]])
assert matrix.rank() == 20
assert len(nullspace) == 1
assert matrix*constant_vector == s.zeros(matrix.rows,1)
assert s.Matrix.hstack(nullspace[0], constant_vector).rank() == 1

# Exact Kottler-type algebraic control: positive clock coefficients in one
# frame, zero null Ricci, but a rational boost yields a negative coefficient.
kappa,w = s.symbols('kappa w', real=True)
diagonal = [-2*w-kappa, w-kappa, w-kappa, -w+kappa, -w+kappa, 2*w+kappa]
control = s.zeros(6)
for i,(a,b) in enumerate(pairs):
    # Input diagonal is A_abba; our bivector matrix stores A_abab.
    control[i,i] = -diagonal[i]
def contract_control(x,y,z,v):
    return s.expand((wedge(x,y).T*control*wedge(z,v))[0])
ric = s.Matrix(4,4,lambda i,j: sum(eta[a,a]*contract_control(basis[a],basis[i],basis[j],basis[a]) for a in range(4)))
assert ric == 3*kappa*eta
boosted = s.Matrix([s.Rational(5,4),0,0,s.Rational(3,4)])
n = basis[2]
assert (boosted.T*eta*boosted)[0] == -1
coefficient = -contract_control(n,boosted,boosted,n)
bad_value = coefficient.subs({kappa:2,w:1})
assert bad_value == -s.Rational(11,16)
base_coefficients = [-contract_control(basis[i],basis[0],basis[0],basis[i]).subs({kappa:2,w:1}) for i in range(1,4)]
assert base_coefficients == [4,1,1]

# Direct coordinate curvature for the non-space-form sign-only survivor.
# Exact symbolic metric: -dt^2+cosh(t)^2(dx^2+dy^2+dz^2), no field equation.
t = s.symbols('t', real=True)
coords = [t,*s.symbols('x y z', real=True)]
a = s.cosh(t)
g = s.diag(-1,a*a,a*a,a*a)
ginv = g.inv()
Gamma = [[[s.simplify(sum(ginv[i,l]*(s.diff(g[l,k],coords[j])+s.diff(g[l,j],coords[k])-s.diff(g[j,k],coords[l])) for l in range(4))/2)
          for k in range(4)] for j in range(4)] for i in range(4)]
def curvature_cov(i,j,k,l):
    # A(i,j,k,l)=g(R(partial_i,partial_j)partial_k,partial_l).
    return s.simplify(sum(g[l,m]*(s.diff(Gamma[m][j][k],coords[i])-s.diff(Gamma[m][i][k],coords[j])
        +sum(Gamma[m][i][q]*Gamma[q][j][k]-Gamma[m][j][q]*Gamma[q][i][k] for q in range(4))) for m in range(4)))
electric = s.simplify(curvature_cov(1,0,0,1)/a**2)
spatial = s.simplify(curvature_cov(1,2,2,1)/a**4)
assert electric == -1
assert s.simplify(spatial-s.tanh(t)**2) == 0
null_trace = s.simplify(2*(electric+spatial))
assert s.simplify(null_trace+2/s.cosh(t)**2) == 0

# Vertex Jacobi area Taylor coefficient, from B''+T B=0, B(0)=0,B'(0)=I.
lam = s.symbols('lam')
q11,q12,q22 = s.symbols('q11 q12 q22')
tidal = s.Matrix([[q11,q12],[q12,q22]])
vertex = lam*s.eye(2)-lam**3*tidal/6
area_quadratic = s.expand(vertex.det()/lam**2).coeff(lam,2)
assert area_quadratic == -(q11+q22)/6

print(json.dumps({
    'kind':'exact rational/symbolic finite anchors; analytic quantifiers remain in proof',
    'python':platform.python_version(), 'sympy':s.__version__,
    'algebraic_curvature_variables':21, 'bianchi_rank':bianchi_rank,
    'null_ray_count':len(spatial_directions),'screen_equations':null_count,
    'combined_rank':matrix.rank(),'nullspace_dimension':len(nullspace),
    'nullspace_is_spaceform':True,
    'weyl_control':{'ricci':str(ric),'unboosted_clock_coefficients':list(map(str,base_coefficients)),
                    'boost':[str(x) for x in boosted], 'boosted_coefficient':str(bad_value)},
    'cosh_metric':{'electric':str(electric),'spatial':str(spatial),'null_ricci_unit_k':str(null_trace)},
    'vertex_area_quadratic':str(area_quadratic),
    'all_assertions_passed':True
},indent=2))
