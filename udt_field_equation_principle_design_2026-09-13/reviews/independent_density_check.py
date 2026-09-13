"""One exact metric-density/Christoffel witness, not a physical-law test."""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import datetime
import hashlib
import json
import platform
import resource
import time

resource.setrlimit(resource.RLIMIT_AS, (2048 * 1024**2, 2048 * 1024**2))
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
wall_start = time.monotonic()
eta = [[Q((-1, 1, 1, 1)[a]) if a == b else Q(0) for b in range(4)] for a in range(4)]


def antisymmetric(entries):
    f = [[Q(0) for _ in range(4)] for _ in range(4)]
    for a, b, value in entries:
        f[a][b], f[b][a] = Q(value), -Q(value)
    assert all(f[a][b] == -f[b][a] for a in range(4) for b in range(4))
    return f


def mul_poly(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def det_poly(matrix):
    out = [Q(0)] * 9
    for perm in permutations(range(4)):
        inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i + 1, 4))
        term = [Q((-1) ** inversions)]
        for a in range(4):
            term = mul_poly(term, matrix[a][perm[a]])
        for degree, coefficient in enumerate(term):
            out[degree] += coefficient
    return out


def density_data(terms, w):
    # Actual g(q*w) entries, not a curvature expansion.
    h = [[Q(0) for _ in range(4)] for _ in range(4)]
    for coefficient, f in terms:
        fw = [sum(f[a][b] * w[b] for b in range(4)) for a in range(4)]
        for a in range(4):
            for b in range(4):
                h[a][b] += coefficient * fw[a] * fw[b]
    determinant = det_poly([[[eta[a][b], Q(0), h[a][b]] for b in range(4)] for a in range(4)])
    ratio = [-entry for entry in determinant]  # det(eta)=-1
    assert ratio[0] == 1
    assert all(ratio[d] == 0 for d in (1, 3, 5, 7))
    # log D(q*w)=1/2 log(ratio); second q derivative equals ratio[2].
    return ratio[2], ratio


def ricci_from_connection(terms):
    # Metric second partials are differentiated from the explicit polynomial.
    def metric_second(a, b, c, d):
        return sum(coefficient * (f[a][c] * f[b][d] + f[a][d] * f[b][c]) for coefficient, f in terms)

    def connection_derivative(k, a, b, c):
        return sum(eta[k][l] * (metric_second(l, b, a, c) + metric_second(l, a, b, c) - metric_second(a, b, l, c)) for l in range(4)) / 2

    # All first metric derivatives and connection values vanish at the origin.
    return [[sum(connection_derivative(k, a, b, k) - connection_derivative(k, a, k, b) for k in range(4)) for b in range(4)] for a in range(4)]


f1 = antisymmetric([(0, 1, 1), (0, 2, 2), (0, 3, -1), (1, 2, 3), (1, 3, 2), (2, 3, 1)])
f2 = antisymmetric([(0, 1, 2), (0, 2, -1), (0, 3, 3), (1, 2, 1), (1, 3, -2), (2, 3, 4)])
fixtures = {"flat": [], "mixed_full_metric": [(Q(2, 3), f1), (Q(-3, 5), f2)]}
results = {}
for name, terms in fixtures.items():
    basis = [[Q(int(a == b)) for a in range(4)] for b in range(4)]
    hessian = [[Q(0) for _ in range(4)] for _ in range(4)]
    for a in range(4):
        hessian[a][a] = density_data(terms, basis[a])[0]
    for a in range(4):
        for b in range(a + 1, 4):
            w = [basis[a][j] + basis[b][j] for j in range(4)]
            value = (density_data(terms, w)[0] - hessian[a][a] - hessian[b][b]) / 2
            hessian[a][b] = hessian[b][a] = value
    e_density = [[-3 * hessian[a][b] for b in range(4)] for a in range(4)]
    ricci = ricci_from_connection(terms)
    assert all(e_density[a][b] == ricci[a][b] for a in range(4) for b in range(4)), name
    scalar = sum(eta[a][b] * ricci[a][b] for a in range(4) for b in range(4))
    shape = [[ricci[a][b] - scalar * eta[a][b] / 4 for b in range(4)] for a in range(4)]
    _, det_ratio = density_data(terms, [Q(1), Q(2), Q(3), Q(4)])
    log_density_q4 = (det_ratio[4] - det_ratio[2] ** 2 / 2) / 2
    if name == "mixed_full_metric":
        assert any(shape[a][b] != 0 for a in range(4) for b in range(4))
        assert any(ricci[a][b] != 0 for a in range(4) for b in range(a + 1, 4))
        assert det_ratio[4] != 0
        assert log_density_q4 != 0
    else:
        assert not any(ricci[a][b] for a in range(4) for b in range(4))
    results[name] = {
        "all_16_components_equal": True,
        "density_separation_hessian": hessian,
        "ricci_from_christoffel_derivatives": ricci,
        "scalar_curvature": scalar,
        "tracefree_ricci": shape,
        "determinant_ratio_along_1_2_3_4": det_ratio,
        "log_density_quartic_coefficient_along_1_2_3_4": log_density_q4,
    }

record = {
    "status": "PASS",
    "scope": "Two exact diagnostic metrics; no physical response adoption or original-theorem reproof",
    "started_utc": started,
    "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "wall_seconds": time.monotonic() - wall_start,
    "python": platform.python_version(),
    "arithmetic": "fractions.Fraction exact rational",
    "cpu_seconds_limit": 120,
    "address_space_mib_limit": 2048,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "fixtures": results,
    "skipped": ["historical source suites", "physical motivation certification", "Cauchy/stability/empirical tests", "GPU", "author code"],
}
output = Path(__file__).with_name("INDEPENDENT_DENSITY_CHECK.json")
output.write_text(json.dumps(record, indent=2, default=str) + "\n")
print(json.dumps({"status": "PASS", "fixtures": len(results), "tensor_components_compared": 32, "output": str(output), "wall_seconds": record["wall_seconds"]}))
