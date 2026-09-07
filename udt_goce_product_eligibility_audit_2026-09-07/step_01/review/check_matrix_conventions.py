"""Exact source-equation review; no observation or flight-processor code."""
import json
import sys
import sympy as s

vx, vy, vz, vxy, vxz, vyz = s.symbols('vx vy vz vxy vxz vyz')
wx, wy, wz = s.symbols('wx wy wz')
hx, hy, hz = s.symbols('hx hy hz', positive=True)
V = s.Matrix([[vx, vxy, vxz], [vxy, vy, vyz], [vxz, vyz, vz]])
O = s.Matrix([[0, -wz, wy], [wz, 0, -wx], [-wy, wx, 0]])
Rhalf = s.diag(hx, hy, hz)
O2 = O * O
# Equation 6: no angular acceleration needed for this symmetric comparison.
A = -(V - O2) * Rhalf
# Equation 10, solved for V with equation 9's Rhalf convention.
scaled = A * Rhalf.inv()
intro = -(scaled + scaled.T) / 2 + O2

def algorithm16(lengths):
    B = A * s.diag(*lengths).inv()
    # Diagonal -2 a/L, off-diagonal -a/L-a/L, plus centrifugal term.
    return -(B + B.T) + O2

same_symbol = algorithm16((hx, hy, hz))
full_lengths = algorithm16((2 * hx, 2 * hy, 2 * hz))
zero = s.zeros(3)
assert s.simplify(intro - V) == zero, 'introductory matrix reconstruction'
assert s.simplify(same_symbol - (2 * V - O2)) == zero, 'same-symbol comparison'
assert s.simplify(full_lengths - V) == zero, 'full-separation reconstruction'
trace_written = -2 * (A[0, 0] / hx + A[1, 1] / hy + A[2, 2] / hz
                       + wx**2 + wy**2 + wz**2)
assert s.simplify(s.trace(same_symbol) - trace_written) == 0, 'written trace'

witness = {vx: 2, vy: 3, vz: 5, vxy: 1, vxz: -2, vyz: 4,
           wx: s.Rational(1, 7), wy: -s.Rational(2, 5),
           wz: s.Rational(3, 11), hx: 1, hy: 2, hz: 3}
print(json.dumps({
    'sympy_version': s.__version__,
    'identities': 4,
    'same_symbol_identity': '2*V - Omega^2',
    'full_separation_identity': 'V',
    'nonrotating_witness_diagonal_same': [str(same_symbol[i, i].subs(
        {**witness, wx: 0, wy: 0, wz: 0})) for i in range(3)],
    'rotating_witness_trace_expected': str(s.trace(V).subs(witness)),
    'rotating_witness_trace_same_symbol': str(s.trace(same_symbol).subs(witness)),
    'rotating_witness_trace_full_separation': str(s.trace(full_lengths).subs(witness)),
}, sort_keys=True), flush=True)

if '--wrong-length-convention' in sys.argv:
    assert s.simplify(same_symbol - V) == zero, 'mutant: half length treated as full'
print('PASS: exact symbolic document-convention identities; not flight validation')
