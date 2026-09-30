"""Bounded exact diagnostics of supplied comparison formulas; no QFT derivation."""
import json
import platform
import sympy as s

eta = s.diag(-1, 1, 1, 1)
H, b, hbar, c, kappa, rho, q = s.symbols('H b hbar c kappa rho q', nonzero=True)
T = 6*b*hbar*c*H**4*eta
G = -3*H**2*eta
tf = lambda A: s.simplify(A - s.trace(eta.inv()*A)*eta/4)
assert tf(G-kappa*T) == s.zeros(4)

# This algebraic stress is a supplied diagnostic, not a computed quantum state.
Trad = s.diag(rho, rho/3, rho/3, rho/3)
assert tf(Trad) == Trad
assert tf(-kappa*Trad) != s.zeros(4)

# HSS curvature convention: screen Ricci trace = Ric(k,k).
r, w, v = s.symbols('r w v')
screen = s.Matrix([[r/2+w, v], [v, r/2-w]])
correction = 13*r*s.eye(2)-4*screen
assert s.trace(correction) == 22*r
ricci_flat = correction.subs({r: 0, w: q, v: 0})
assert ricci_flat == s.diag(-4*q, 4*q)
assert ricci_flat != s.zeros(2)

print(json.dumps({
    'scope': 'exact algebra on imported/supplied formulas, not QFT or geometry selection',
    'python': platform.python_version(), 'sympy': s.__version__,
    'checks': {
        'de_sitter_shape_response_vanishes_for_free_H': True,
        'supplied_radiation_stress_changes_shape_response_at_fixed_metric': True,
        'spinor_qed_screen_trace_coefficient': '22*R_kk',
        'ricci_flat_tide_correction_bracket': str(ricci_flat),
    },
    'omitted': ['state-prescription construction', 'QFT loop recomputation',
                'all-metric classification', 'physical clock propagation',
                'empirical validation', 'native premises or scale selection'],
}, indent=2))
