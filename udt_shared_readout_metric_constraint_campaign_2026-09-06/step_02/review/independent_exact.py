"""Independent Step02 exact reconstruction; no author imports or outputs."""
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
import pathlib
import platform
import subprocess
import sys

ROOT = pathlib.Path('/home/udt-admin/udt_mass_codex')
PIN = '70034a6faa9264bf054eb473d5eb7a0889f3d2de'
checks = []

def require(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def lorentz(a, b):
    return -a[0]*b[0] + dot(a[1:], b[1:])

def times(a, x):
    return [dot(row, x) for row in a]

def solve_unique(a, b):
    """Exact augmented elimination, rectangular allowed; None for nonunique/inconsistent."""
    cols = len(a[0]) if a else 0
    aug = [[F(t) for t in row] + [F(y)] for row, y in zip(a, b)]
    pivots = []
    r = 0
    for c in range(cols):
        chosen = next((i for i in range(r, len(aug)) if aug[i][c]), None)
        if chosen is None:
            continue
        aug[r], aug[chosen] = aug[chosen], aug[r]
        denom = aug[r][c]
        aug[r] = [v/denom for v in aug[r]]
        for i in range(len(aug)):
            if i != r:
                coef = aug[i][c]
                aug[i] = [v-coef*w for v, w in zip(aug[i], aug[r])]
        pivots.append(c)
        r += 1
    if any(not any(row[:cols]) and row[-1] for row in aug):
        return None
    if len(pivots) != cols:
        return None
    result = [F(0)] * cols
    for i, c in enumerate(pivots):
        result[c] = aug[i][-1]
    return result

def conic_witness(a, y):
    """Enumerate independent supports, solving full original equations exactly."""
    m = len(a)
    n = len(a[0]) if m else 0
    if not any(y):
        return [F(0)] * n
    for count in range(1, min(m, n)+1):
        for support in combinations(range(n), count):
            selected = [[row[j] for j in support] for row in a]
            weights = solve_unique(selected, y)
            if weights is not None and all(w >= 0 for w in weights):
                full = [F(0)] * n
                for j, w in zip(support, weights):
                    full[j] = w
                if times(a, full) != list(y):
                    raise AssertionError('original residual')
                return full
    return None

alpha, spacing = F(2), F(3)
ds = [F(1), F(2), F(3)]
cut_times = [F(-2), F(0), F(5)]
k_cov = [-alpha, F(0), F(0), alpha]
k_vec = [alpha, F(0), F(0), alpha]
ex, ey = [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)]
require('raised phase is null future nonzero', lorentz(k_vec, k_vec) == 0 and k_vec[0] > 0)
require('screen Gram is Euclidean', [lorentz(ex, ex), lorentz(ex, ey), lorentz(ey, ey)] == [1, 0, 1])

def cut(i, label):
    x, y = label
    return [cut_times[i], x, y, cut_times[i]]

def in_image_window(i, point):
    t, x, y, z = point
    if t != cut_times[i] or z != cut_times[i] or not 0 <= x <= 3 or not 0 <= y <= 1:
        return False
    return [x < 2, x >= 1, x < 1 or x >= 2][i]

observers, rates = [], []
for i, d in enumerate(ds):
    # Reconstruct components from u^t-u^z=d and the unit hyperbola.
    u_plus, u_minus = 1/d, d
    u = [(u_plus+u_minus)/2, F(0), F(0), (u_plus-u_minus)/2]
    omega = -dot(k_cov, u)
    require(f'observer {i} full norm/time/frequency', lorentz(u, u) == -1 and u[0] > 0 and omega == alpha*d)
    require(f'observer {i} screen orthogonality', lorentz(ex, u) == lorentz(ey, u) == 0)
    tau = F(7, 11)
    base = cut(i, [F(1, 2), F(1, 3)])
    endpoint = [v+tau*w for v, w in zip(base, u)]
    require(f'observer {i} continuous phase slope', alpha*(endpoint[3]-endpoint[0]) == -tau*omega)
    observers.append(u)
    rates.append(omega/spacing)

for theta, t in product([F(-5, 3), F(0), F(8, 7)], [F(-2), F(0), F(9)]):
    point = [t, F(1, 2), F(3, 4), t+theta/alpha]
    require(f'phase product extension {theta} {t}', dot(k_cov, point) == theta)

for x, y in product([F(0), F(1, 2), F(1), F(3, 2), F(2), F(5, 2), F(3)], [F(0), F(1, 3), F(1)]):
    j = 0 if x < 1 else 1 if x < 2 else 2
    incidence = [[True, True, False], [False, True, True], [True, False, True]]
    for i in range(3):
        require(f'cut/window boundary {i} {x} {y}', in_image_window(i, cut(i, [x, y])) == incidence[i][j])

representatives = [(F(1, 2), F(1, 3)), (F(3, 2), F(1, 3)), (F(5, 2), F(1, 3))]
A = [[rates[i] * int(in_image_window(i, cut(i, point))) for point in representatives] for i in range(3)]
known_mass = [F(1), F(2), F(3)]
good_record = times(A, known_mass)
bad_record = [F(2, 3), F(4, 3), F(6)]
good_solution = solve_unique(A, good_record)
bad_solution = solve_unique(A, bad_record)
require('geometry-derived compatible record', good_record == [F(2), F(20, 3), F(8)] and good_solution == known_mass)
require('geometry-derived incompatible masses', bad_solution == [F(3, 2), F(-1, 2), F(3, 2)])
inverse_rows = []
for i in range(3):
    basis = [F(int(i == j)) for j in range(3)]
    inverse_rows.append(solve_unique(A, basis))
inverse = list(map(list, zip(*inverse_rows)))
dual = [2*t for t in inverse[1]]
dual_columns = [dot(dual, col) for col in zip(*A)]
require('dual independently recovered by elimination', dual_columns == [0, 2, 0] and dot(dual, bad_record) == -1)

record_controls = 0
for normalized in product([F(-3, 2), F(-1, 3), F(0), F(1, 5), F(1), F(7, 3), F(4)], repeat=3):
    raw = [r*z for r, z in zip(rates, normalized)]
    witness = conic_witness(A, raw)
    triangle = all(normalized[i]+normalized[j] >= normalized[k] for i, j, k in [(0, 1, 2), (0, 2, 1), (1, 2, 0)])
    require(f'full-equation conic feasibility {record_controls}', (witness is not None) == triangle)
    if witness is None:
        solution = solve_unique(A, raw)
        negative = next(i for i, v in enumerate(solution) if v < 0)
        separating = inverse[negative]
        require(f'exact separating row {record_controls}', all(dot(separating, col) >= 0 for col in zip(*A)) and dot(separating, raw) < 0)
    record_controls += 1

# Rectangular/degenerate cone controls are not specific to the overlap inversion.
degenerate = [[F(1), F(0), F(1), F(0)], [F(0), F(1), F(1), F(0)], [F(0)]*4]
for x, y, z in product([F(-1), F(0), F(2)], repeat=3):
    require(f'zero row/column feasibility {x} {y} {z}', (conic_witness(degenerate, [x, y, z]) is not None) == (x >= 0 and y >= 0 and z == 0))
require('zero output permits zero measure', times(A, [F(0)]*3) == [0, 0, 0])
require('zero matrix is not positive-output feasible', conic_witness([[F(0), F(0)]], [F(1)]) is None)
require('zero columns permit unseen mass', times(degenerate, [F(0), F(0), F(0), F(17)]) == [0, 0, 0])

# A rank-deficient visible protocol can still have a unique boundary fibre.
boundary_a = [[F(1), F(0), F(1)], [F(0), F(1), F(1)]]
require('rank-deficient zero fibre unique by column positivity', all(sum(col) > 0 for col in zip(*boundary_a)))
require('rank-deficient positive fibre nonunique', times(boundary_a, [F(1), F(1), F(0)]) == times(boundary_a, [F(0), F(0), F(1)]))

# Compare two actual atomic measures through the endpoint windows.
atoms_a = list(zip(representatives, known_mass))
atoms_b = [((F(1, 4), F(3, 4)), F(1))] + atoms_a[1:]
def atom_readouts(atoms):
    return [rates[i]*sum((mass for point, mass in atoms if in_image_window(i, cut(i, point))), F(0)) for i in range(3)]
require('different singular label measures invisible', atoms_a != atoms_b and atom_readouts(atoms_a) == atom_readouts(atoms_b) == good_record)
require('different AC profiles same cell integral', F(1) == 2*(F(1)**2-F(0)**2)/2 and F(1, 2) != 2*(F(1, 2)**2-F(0)**2)/2)

disjoint = [[rates[i]*int(i == j) for j in range(3)] for i in range(3)]
require('disjoint control admits same formerly bad record', conic_witness(disjoint, bad_record) == [F(1), F(1), F(3)])
for b in [F(1, 11), F(5, 2), F(13)]:
    require(f'phase/spacing rescaling {b}', [(b*alpha)*d/(b*spacing) for d in ds] == rates)

# Direct independent sensitivity: each wrong scientific path disagrees with an
# independently computed original-equation reference, without changing a guard.
mutations = {
    'phase_sign': [-r for r in rates] != rates,
    'drop_observer_factor': [alpha/spacing]*3 != rates,
    'pretend_disjoint_windows': times(disjoint, known_mass) != good_record,
    'accept_signed_measure': (bad_solution is not None and any(v < 0 for v in bad_solution)),
    'drop_common_phase_spacing_rescale': [(F(2)*alpha)*d/spacing for d in ds] != rates,
}
require('independent changed-path sensitivity', all(mutations.values()))

source_hashes = {}
for path in ['udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md',
             'udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXACT_DERIVATION.md',
             'CURRENT_SCIENTIFIC_PREMISES.tsv']:
    blob = subprocess.check_output(['git', 'show', PIN+':'+path], cwd=ROOT)
    current = (ROOT/path).read_bytes()
    require('pinned source byte identity '+path, current == blob)
    source_hashes[path] = hashlib.sha256(blob).hexdigest()

def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    return value

print(json.dumps(serial(dict(
    verdict='INDEPENDENT_EXACT_CONTROLS_PASS',
    implementation='generic exact augmented elimination and sparse-support feasibility; geometry-derived matrix',
    caveat='finite controls are not the arbitrary-finite analytic proof',
    python=sys.version, platform=platform.platform(),
    matrix=A, rates=rates, observers=observers,
    compatible_record=good_record, compatible_mass=good_solution,
    incompatible_record=bad_record, signed_mass=bad_solution,
    inverse=inverse, dual=dual, dual_columns=dual_columns,
    dual_bad_value=dot(dual, bad_record),
    signed_rational_record_controls=record_controls,
    assertion_count=len(checks), sensitivity=mutations,
    pinned_source_hashes=source_hashes,
    passed_checks=checks,
)), indent=2, sort_keys=True))
