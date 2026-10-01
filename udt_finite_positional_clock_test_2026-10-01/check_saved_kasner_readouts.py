"""Exposed parent recomputation from saved arrival/momentum series, not ray independence."""
import hashlib
import json
from pathlib import Path
import sympy as s

B = Path(__file__).resolve().parent
source = B / 'math/kasner_higher.stdout'
data = json.loads(source.read_text())
L = s.Symbol('L', real=True)
rows = []
for row in data['controls']:
    r = s.Rational(row['p'])
    parse = lambda name: s.sympify(row[name], locals={'L': L})
    tb, ta, C = 1 + parse('tb_minus_one'), 1 + parse('ta_minus_one'), parse('C')
    # Future ray k^t=t^-r, k^x=+/-t^-2r has conserved k_x=+/-1.
    # Receiver four-velocity V^t=sqrt(1+C²/t^(2r)), V^x=C/t^(2r).
    # Contractions -g(k,V) give both frequencies before forming their ratios.
    w = s.series(C * tb**(-r), L, 0, 5).removeO()
    gamma = s.series(s.sqrt(1+w*w), L, 0, 5).removeO()
    outgoing_receive = s.series(tb**(-r)*(gamma-w), L, 0, 5).removeO()
    return_emit = s.series(tb**(-r)*(gamma+w), L, 0, 5).removeO()
    return_receive = s.series(ta**(-r), L, 0, 5).removeO()
    lp = s.series(-s.log(outgoing_receive), L, 0, 5).removeO().expand()
    lq = s.series(s.log(return_emit)-s.log(return_receive), L, 0, 5).removeO().expand()
    assert s.expand(lp-parse('log_outgoing')) == 0
    assert s.expand(lq-parse('log_return')) == 0
    rows.append((lp, lq))
meanp, meanq = [s.expand((rows[0][i]+2*rows[1][i])/3) for i in (0, 1)]
assert meanp == -s.Rational(7, 243)*L**4
assert meanq == s.Rational(5, 81)*L**4
print(json.dumps({'status': 'PASS', 'saved_series_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'readouts': [[str(x) for x in row] for row in rows], 'principal_axis_mean_log_outgoing': str(meanp),
    'principal_axis_mean_log_return': str(meanq), 'scope': 'Parent endpoint-frequency recomputation using saved arrival/momentum series. Separate code, shared saved inputs and SymPy; not independent geodesic integration or independent confirmation of truncation/remainder.'}, indent=2))
