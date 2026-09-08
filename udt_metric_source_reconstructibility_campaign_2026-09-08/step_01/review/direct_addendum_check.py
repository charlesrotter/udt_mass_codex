"""Post-exposure independent addendum; imports only this reviewer's engine.

The author quartic example adds nonclosed-canonical-root coverage not present
in the first independent run. This file does NOT claim target-blind design.
"""

import contextlib
import io
import json
import runpy

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    owned = runpy.run_path(
        'udt_metric_source_reconstructibility_campaign_2026-09-08/'
        'step_01/review/independent_reconstruction_check.py')
s = owned['s']
u, r, x, y = owned['coords']
q = s.Matrix([1, 0, 0, 0])
geometry = owned['geometry']
zero = owned['zero']
divergence = owned['divergence']
catch = owned['catch']
require_equal = owned['require_equal']
prior_check_count = len(owned['records'])
prior_red_count = len(owned['red'])

metric = s.Matrix([[-x**4 / 6, 1, 0, 0], [1, 0, 0, 0],
                   [0, 0, 1, 0], [0, 0, 0, 1]])
inverse, connection, ricci, scalar, tracefree = geometry(metric)
root = x * q  # supplied local branch x>0, partial_r future, beta=1.
exterior_root = s.Matrix(4, 4, lambda i, j:
    s.diff(root[j], owned['coords'][i]) - s.diff(root[i], owned['coords'][j]))
zero('quartic actual full Ricci', ricci - x**2 * q * q.T)
zero('quartic actual scalar', scalar)
zero('quartic canonical root full square', tracefree - root * root.T)
zero('quartic root is integrable', s.Matrix(list(owned['wedge_da'](root).values())))
zero('quartic root exterior explicit', exterior_root - s.Matrix([
    [0, 0, -1, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]))
zero('quartic integrating factor gives exact phase', root / x - q)
zero('quartic reconstructed current conserved', divergence(x**2 * inverse * q, connection))
catch('canonical root falsely treated as exact phase',
      lambda: require_equal(exterior_root, s.zeros(4)))

# The algebraic curvature realization asserted in the candidate is an exact
# contraction identity; this diagnostic does not claim a neighborhood solution.
flat = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
T = owned['ranktwo']
riemann = lambda a, b, c, d: (flat[a, c] * T[b, d] + flat[b, d] * T[a, c]
                             - flat[a, d] * T[b, c] - flat[b, c] * T[a, d]) / 2
contracted = s.Matrix(4, 4, lambda b, d: sum(flat.inv()[a, c] * riemann(a, b, c, d)
                      for a in range(4) for c in range(4)))
zero('candidate pointwise algebraic Ricci contraction', contracted - T)
zero('candidate pointwise algebraic first Bianchi', s.Matrix([
    s.simplify(riemann(a, b, c, d) + riemann(a, c, d, b) + riemann(a, d, b, c))
    for a in range(4) for b in range(4) for c in range(4) for d in range(4)]))

print(json.dumps({
    'status': 'PASS',
    'exposure': 'Post-candidate; reviewer own engine, no author code import.',
    'base_exact_diagnostic_groups_replayed': prior_check_count,
    'new_exact_diagnostic_groups': len(owned['records']) - prior_check_count,
    'new_checks': owned['records'][prior_check_count:],
    'new_actual_red_controls': owned['red'][prior_red_count:],
    'actual_quartic_Ricci': str(ricci), 'actual_quartic_R': str(scalar),
    'actual_quartic_root_exterior': str(exterior_root),
    'scope': 'Exact local diagnostics; not genericity or physical adoption.'
}, indent=2, sort_keys=True))
