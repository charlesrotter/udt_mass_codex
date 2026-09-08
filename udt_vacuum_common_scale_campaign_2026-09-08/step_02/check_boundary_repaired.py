"""One normalizer-only same-premise repair; initial code/output preserved.

Execute the SHA-frozen original tests, changing only exact symbolic residual
normalization to expand trig identities before simplify. No tolerance, sample,
expected expression, rejected control or scientific condition is changed.
"""
import hashlib
from pathlib import Path

source = Path(__file__).with_name('check_boundary.py')
payload = source.read_bytes()
assert hashlib.sha256(payload).hexdigest() == 'b5d2bf791b4eae5ef83c0f4e85a6181436293e188c98215c1ba313044a51dae6'
before = 'residual = (S.Matrix(actual)-S.Matrix(expected)).applyfunc(S.simplify)'
after = 'residual = (S.Matrix(actual)-S.Matrix(expected)).applyfunc(lambda e: S.simplify(S.expand_trig(e)))'
text = payload.decode()
assert text.count(before) == 1
namespace = {'__name__': '__main__', '__file__': str(source)}
exec(compile(text.replace(before,after),str(source)+' [exact-trig-normalizer repair]','exec'),namespace)
