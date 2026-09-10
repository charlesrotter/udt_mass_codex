#!/usr/bin/env python3
"""Small exact author checks. Not independent review or proof by sampling."""
import hashlib
import json
from pathlib import Path
import platform
import sympy as s

if not __debug__:
    raise RuntimeError("Exact evidence checks require normal Python; -O is forbidden")

records = []


def check(name, condition, detail):
    if condition is not True:
        raise AssertionError(name)
    records.append({"name": name, "passed": True, "detail": detail})


def simp(x):
    return s.simplify(s.trigsimp(x))


def zero(x):
    return all(simp(v) == 0 for v in x) if isinstance(x, s.MatrixBase) else simp(x) == 0


def geometry(g, u, coords):
    """Direct coordinate definitions, full four-dimensional Christoffel contraction."""
    gi = g.inv()
    d = len(coords)
    G = [[[simp(sum(gi[a, q] * (s.diff(g[q, b], coords[c])
                  + s.diff(g[q, c], coords[b]) - s.diff(g[b, c], coords[q]))
                  for q in range(d)) / 2) for c in range(d)]
                  for b in range(d)] for a in range(d)]
    ul = g * u
    nab = s.Matrix(d, d, lambda a, b: simp(s.diff(ul[b], coords[a])
                   - sum(G[c][a][b] * ul[c] for c in range(d))))
    h = g + ul * ul.T
    proj = s.eye(d) + ul * u.T
    theta = simp(sum(gi[a, b] * nab[a, b] for a in range(d) for b in range(d)))
    H = theta / 3
    acceleration = s.Matrix(d, 1, lambda b, _: simp(sum(u[a] * nab[a, b] for a in range(d))))
    sigma = (proj * ((nab + nab.T)/2) * proj.T - H*h).applyfunc(simp)
    alpha = (acceleration-H*ul).applyfunc(simp)
    da = s.Matrix(d, d, lambda a, b: simp(s.diff(alpha[b], coords[a])-s.diff(alpha[a], coords[b])))
    return {"g": g, "gi": gi, "u": u, "ul": ul, "G": G, "nab": nab,
            "H": H, "a": acceleration, "sigma": sigma, "alpha": alpha,
            "dalpha": da, "coords": coords}


def ck_residual(data, f):
    x = data["coords"]
    xi = f * data["u"]
    g = data["g"]
    lie = s.Matrix(4, 4, lambda a, b: simp(sum(
        xi[c]*s.diff(g[a, b], x[c]) + g[c, b]*s.diff(xi[c], x[a])
        + g[a, c]*s.diff(xi[c], x[b]) for c in range(4))))
    return (lie - 2*f*data["H"]*g).applyfunc(simp)


t, x, y, z = s.symbols("t x y z", real=True)
r = s.symbols("r", positive=True)
th, ph = s.symbols("theta varphi", real=True)
eta = s.diag(-1, 1, 1, 1)

# Algebraic null-quadratic kernel: exact rank, not a random-direction count.
entries = s.symbols("S00 S01 S02 S03 S11 S12 S13 S22 S23 S33")
S = s.Matrix([[entries[0], entries[1], entries[2], entries[3]],
              [entries[1], entries[4], entries[5], entries[6]],
              [entries[2], entries[5], entries[7], entries[8]],
              [entries[3], entries[6], entries[8], entries[9]]])
directions = []
for i in range(3):
    for sign in (-1, 1):
        n = [s.Integer(0)]*3
        n[i] = s.Integer(sign)
        directions.append(s.Matrix([1]+n))
for i, j in ((0, 1), (0, 2), (1, 2)):
    n = [s.Integer(0)]*3
    n[i] = n[j] = 1/s.sqrt(2)
    directions.append(s.Matrix([1]+n))
M = s.Matrix([[(k.T*S*k)[0].diff(v) for v in entries] for k in directions])
check("null_directions", all(zero((k.T*eta*k)[0]) for k in directions), "9 exact future-null directions")
check("null_quadratic_rank", M.rank() == 9, "rank9 in Sym2 dimension10; one-dimensional metric kernel")
metric_vector = s.Matrix([-1, 0, 0, 0, 1, 0, 0, 1, 0, 1])
check("null_quadratic_kernel", zero(M*metric_vector), "eta lies in the one-dimensional kernel")

# Full original static spherical family; no field equation/profile imposed.
p = s.Function("phi")(r)
gs = s.diag(-s.exp(-2*p), s.exp(2*p), r**2, r**2*s.sin(th)**2)
static = geometry(gs, s.Matrix([s.exp(p), 0, 0, 0]), (t, r, th, ph))
check("static_unit", zero((static["u"].T*gs*static["u"])[0]+1), "g(U,U)=-1")
check("static_shear_expansion", zero(static["sigma"]) and zero(static["H"]), "sigma=H=0")
check("static_alpha", zero(static["alpha"]-s.Matrix([0, -s.diff(p,r), 0, 0])), "alpha=-phi'(r) dr")
check("static_ck", zero(ck_residual(static, s.exp(-p))), "xi=partial_t; conformal-Killing residual zero")

# Time-dependent positive conformal control, using exp(q) to keep positivity explicit.
q = s.Function("q")(t)
gc = s.exp(2*q)*eta
conformal = geometry(gc, s.Matrix([s.exp(-q), 0, 0, 0]), (t,x,y,z))
check("conformal_shear", zero(conformal["sigma"]), "no shear despite time dependence")
check("conformal_alpha", zero(conformal["alpha"]-s.Matrix([s.diff(q,t), 0, 0, 0])), "alpha=dq; Psi=-q")
check("conformal_ck", zero(ck_residual(conformal, s.exp(q))), "xi=partial_t; CK but not generally Killing")

# Flat shear control, compute at x=0 after taking all derivatives.
kap = s.symbols("kappa", nonzero=True, real=True)
shear = geometry(eta, s.Matrix([s.cosh(kap*x), s.sinh(kap*x), 0, 0]), (t,x,y,z))
at_origin = lambda mat: mat.subs(x, 0).applyfunc(simp)
check("flat_shear_unit", zero((shear["u"].T*eta*shear["u"])[0]+1), "smooth future unit congruence")
check("flat_shear_H", zero(shear["H"].subs(x,0)-kap/3), "H=kappa/3 at x=0")
check("flat_shear_tensor", zero(at_origin(shear["sigma"])-s.diag(0,2*kap/3,-kap/3,-kap/3)), "nonzero sigma at x=0")
rates = [simp(-(k.T*at_origin(shear["nab"])*k)[0]) for k in directions[:6]]
check("flat_direction_rates", rates == [-kap, -kap, 0, 0, 0, 0], "d log omega/dlambda for +/-x,+/-y,+/-z")
b0,b1,b2,b3 = s.symbols("b0 b1 b2 b3")
gradient = s.Matrix([b0,b1,b2,b3])
coeff = s.Matrix([list(k) for k in directions[:6]])
check("no_scalar_gradient", coeff.rank() < coeff.row_join(s.Matrix(rates)).rank(), "inconsistent linear system for one scalar gradient")

# Nonintegrable, shear-free acceleration in a flat positive-lapse patch.
N = 1+t*x
gf = s.diag(-N**2,1,1,1)
acc = geometry(gf, s.Matrix([1/N,0,0,0]), (t,x,y,z))
check("acceleration_shear_expansion", zero(acc["sigma"]) and zero(acc["H"]), "sigma=H=0 on N>0")
check("acceleration_alpha", zero(acc["alpha"]-s.Matrix([0,t/N,0,0])), "alpha=t/(1+tx) dx")
expected_da = s.zeros(4)
expected_da[0,1], expected_da[1,0] = 1/N**2, -1/N**2
check("acceleration_nonclosure", zero(acc["dalpha"]-expected_da), "dalpha=dt wedge dx/(1+tx)^2; nonzero on N>0")
G = acc["G"]
coords = acc["coords"]
riemann = [simp(s.diff(G[a][b][d],coords[c])-s.diff(G[a][b][c],coords[d])
    + sum(G[a][c][e]*G[e][b][d]-G[a][d][e]*G[e][b][c] for e in range(4)))
    for a in range(4) for b in range(4) for c in range(4) for d in range(4)]
check("acceleration_flat", all(v == 0 for v in riemann), "all256 coordinate Riemann components exactly zero")

# Arbitrary diagonal homogeneous scale factors; no dynamics or time profile imposed.
qs = [s.Function("q"+str(i))(t) for i in range(1,4)]
gb = s.diag(-1,*(s.exp(2*v) for v in qs))
hom = geometry(gb,s.Matrix([1,0,0,0]),(t,x,y,z))
mean = sum(s.diff(v,t) for v in qs)/3
expected_sigma = s.diag(0,*(s.exp(2*v)*(s.diff(v,t)-mean) for v in qs))
check("homogeneous_shear", zero(hom["sigma"]-expected_sigma), "orthonormal diagonal Hi-H")
check("homogeneous_alpha", zero(hom["alpha"]-s.Matrix([mean,0,0,0])) and zero(hom["dalpha"]), "alpha=H dt, locally exact")

# Actual mutant conditions are evaluated against nontrivial controls.
correct_static = static["alpha"]-s.Matrix([0,-s.diff(p,r),0,0])
wrong_static = static["alpha"]-s.Matrix([0,s.diff(p,r),0,0])
check("catch_wrong_potential_sign", zero(correct_static) and not zero(wrong_static), "Psi=-phi mutant violates dPsi=-alpha for arbitrary nonconstant phi")
correct_acc_gate = zero(acc["sigma"]) and zero(acc["dalpha"])
mutant_acc_gate = zero(acc["sigma"])
check("catch_shear_only_gate", correct_acc_gate is False and mutant_acc_gate is True, "dropping closure falsely admits accelerating flat congruence")
correct_shear_gate = zero(at_origin(shear["sigma"])) and zero(at_origin(shear["dalpha"]))
check("catch_flatness_implies_potential", correct_shear_gate is False, "Minkowski metric does not imply P for arbitrary supplied U")

here = Path(__file__).resolve().parent
result = {
    "status": "PASS", "evidence_type": "author exact symbolic regression and controls; not independent review",
    "checks": records, "check_count": len(records),
    "versions": {"python": platform.python_version(), "sympy": s.__version__},
    "candidate_sha256": hashlib.sha256((here/"INITIAL_CANDIDATE.md").read_bytes()).hexdigest(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "omitted": ["all source package replays", "physical instrument/transfer test", "metric field equation", "global topology example", "empirical observations"]
}
print(json.dumps(result, indent=2, sort_keys=True))
