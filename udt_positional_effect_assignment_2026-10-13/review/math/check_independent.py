"""Exposed independent algebra for PEA1; no author implementation imported."""
import hashlib
import json
import os
import platform
from pathlib import Path

import sympy as s

here = Path(__file__).resolve().parent
root = here.parents[2]
checks = {}


def zero(name, expressions):
    residues = [s.factor(s.cancel(e)) for e in expressions]
    assert all(e == 0 for e in residues), (name, residues)
    checks[name] = {"status": "EXACT_ZERO", "scalar_count": len(residues)}


def nonzero(name, expressions):
    residues = [s.factor(s.cancel(e)) for e in expressions]
    assert any(e != 0 for e in residues), name
    checks[name] = {"status": "DEFECT_CAUGHT", "nonzero_residuals":
                    [str(e) for e in residues if e != 0]}


# Abstract symbols are X.X, b.X, b.Y, X.Y, b.b, Y.Y. No sampled coordinates.
xx, bx, by, xy, bb, yy = s.symbols("xx bx by xy bb yy")
den = 1 - 2*bx + bb*xx
d_den = -2*by + 2*bb*xy
n_sq = xx - 2*xx*bx + bb*xx**2
a_sq = yy - 4*by*xy + 4*bb*xy**2
a_dot_n = xy - xx*by - 2*xy*bx + 2*bb*xx*xy
direction_square_numerator = den**2*a_sq - 2*den*d_den*a_dot_n + d_den**2*n_sq
zero("bilinear_all_direction_pullback", [direction_square_numerator-den**2*yy])
nonzero("wrong_pullback_weight_caught", [direction_square_numerator-den**4*yy])

t, x, y, z = coords = s.symbols("t x y z", real=True)
a, ell = s.symbols("a ell", positive=True)
eta_signs = [-1, 1, 1, 1]
norm_x = -t*t+x*x+y*y+z*z
v = 1+2*a*t-a*a*norm_x


def special(point, parameter):
    tt, xx_, yy_, zz = point
    norm = -tt*tt+xx_*xx_+yy_*yy_+zz*zz
    denominator = 1+2*parameter*tt-parameter**2*norm
    return [(tt-parameter*norm)/denominator, xx_/denominator,
            yy_/denominator, zz/denominator]


f = special(coords, a)
zero("inverse_map", [q-p for q, p in zip(special(f, -a), coords)])
origin = dict.fromkeys(coords, 0)
zero("origin_normalization", [v.subs(origin)-1]+[q.subs(origin) for q in f])
zero("identity_first_order", [s.diff(f[i], coords[j]).subs(origin)-(1 if i == j else 0)
                               for i in range(4) for j in range(4)])
grad = [s.diff(v, q) for q in coords]
norm_grad = sum(sign*d*d for sign, d in zip(eta_signs, grad))
box = sum(sign*s.diff(v, q, q) for sign, q in zip(eta_signs, coords))
zero("gradient_norm", [norm_grad+4*a*a*v])
zero("hessian", [s.diff(v, coords[i], coords[j])+2*a*a*(eta_signs[i] if i == j else 0)
                  for i in range(4) for j in range(4)])
ricci = []
wrong_ricci = []
for i in range(4):
    for j in range(4):
        eta_ij = eta_signs[i] if i == j else 0
        value = 2*s.diff(v, coords[i], coords[j])/v+(box/v-3*norm_grad/v**2)*eta_ij
        ricci.append(value)
        wrong_ricci.append(value+3*norm_grad/v**2*eta_ij)
zero("limiting_reference_full_flat_conformal_ricci", ricci)
nonzero("omitted_gradient_norm_caught", wrong_ricci)

# Actual limiting incidence, then proper-clock derivative. Both endpoints
# are coordinate-static physical Minkowski clocks, so the physical lapse is1.
emit, receive = s.symbols("emit receive", real=True)
world_function = (-(receive-emit)**2+ell**2)/2
arrival = emit+ell
arrival_derivative = -s.diff(world_function, emit)/s.diff(world_function, receive)
zero("actual_flat_incidence", [world_function.subs(receive, arrival)])
zero("actual_flat_net_ratio", [arrival_derivative.subs(receive, arrival)-1])
v_emit = v.subs({t: 0, x: 0, y: 0, z: 0})
v_receive = v.subs({t: ell, x: ell, y: 0, z: 0})
zero("second_assigned_limit", [v_receive/v_emit-(1+2*a*ell)])
zero("second_reference_clock_limit", [v_emit/v_receive-1/(1+2*a*ell)])
nonzero("two_assigned_limits_differ", [v_receive/v_emit-1])

inputs = [Path(__file__), here/"CHECK_PLAN.md", here/"SOURCE_FIRST.md",
          root/"udt_positional_effect_assignment_2026-10-13/INITIAL_CANDIDATE.md",
          root/"udt_positional_effect_assignment_2026-10-13/researcher_b/CANDIDATE.md"]
result = {
    "status": "PASS", "method": "abstract bilinear directional polynomial and independent flat conformal Ricci",
    "versions": {"python": platform.python_version(), "sympy": s.__version__},
    "threads": {key: os.environ.get(key) for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]},
    "checks": checks,
    "limits": {"physical_net_both": "1", "assigned_first": "1", "assigned_second": "1+2*a*ell"},
    "input_sha256": {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
    "omissions": ["No sampled rank inference", "No numerical geodesic solver", "Family continuity and rank proved analytically", "No physical adoption"],
}
with (here/"CHECK_RESULT.json").open("x") as stream:
    json.dump(result, stream, indent=2)
    stream.write("\n")
print(json.dumps(result, indent=2), flush=True)
