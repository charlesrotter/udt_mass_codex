"""Independent arithmetic from existing saved observations; no fit/download."""
import hashlib,json,math,sys
from pathlib import Path
import sympy as s
x=s.symbols('x',real=True)
F=s.exp(x)-1
assert s.simplify(s.exp(x)*F/s.diff(F,x)-(s.exp(x)-1))==0
source=Path('udt_observation_guided_function_search_2026-09-28/observations/comparison_checked/RESULT.json')
d=json.loads(source.read_text())
rows=[]
for i,z in enumerate(d['z']):
    if not d['within_sne_domain'][i]:continue
    observed=d['ratios'][i];sigma=math.sqrt(d['ratio_covariance'][i][i])
    if not all(math.isfinite(v) for v in [z,observed,sigma]) or sigma<=0:raise ValueError('invalid saved input')
    rows.append(dict(z=z,observed=observed,sigma=sigma,predicted=z,difference=z-observed))
assert len(rows)==5
author=json.loads(Path('udt_common_geometry_whiteboard_2026-09-28/parent/CONSTANT_H_INTERFACE_CHECK.json').read_text())
for r,a in zip(rows,author['rows']):
    for independent,saved in [('z','z'),('observed','observed_ratio'),('sigma','inherited_linear_sigma'),('predicted','constant_H_prediction'),('difference','prediction_minus_observed')]:
        if r[independent]!=a[saved]:raise ValueError((independent,r[independent],a[saved]))
print(json.dumps(dict(method='Independent exp(x)F/Fprime derivation and saved-source binary64 arithmetic; no significance',python=sys.version,sympy=s.__version__,source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),rows=rows,max_arithmetic_difference=0,shape=[6,6],selected_bins=5),indent=2))
