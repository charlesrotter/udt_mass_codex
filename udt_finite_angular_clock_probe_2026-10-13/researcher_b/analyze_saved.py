"""Read saved independent integrations; compare convergence and exposed series."""
import json
from pathlib import Path
import numpy as np

base = Path(__file__).resolve().parent
def read(name):
    return json.loads((base/name).read_text())

b = read('vacuum_baseline_data.json')
f = read('vacuum_fine_data.json')
flat = read('flat_fine_data.json')
floor = max(abs(row[k]) for row in flat['results'] for k in ('M_plus','M_minus'))
rows = []
for rb, rf in zip(b['results'], f['results']):
    L = rf['L']
    err = max(abs(rb[k]-rf[k]) for k in ('M_plus','M_minus'))
    accepted = min(rf[k] for k in ('M_plus','M_minus')) > 50*max(err, floor)
    assert accepted, ('NUMERIC_SIGN_NOT_SEPARATED', L)
    max_directional = 0.
    for row in rf['angular_records']:
        z = row['mu']**2
        # This series was exposed by researcher A after both numerical runs.
        approx = (3*z-1)*L**2/9-2*(3*z-1)*L**3/27-(117*z*z-204*z+43)*L**4/486
        max_directional = max(max_directional, abs(row['log_plus']-approx))
    axes = rf['axes']
    # Previously published FPC1 axis formulas, inspected before implementation.
    old0 = -L*L/9+2*L**3/27-43*L**4/486
    old1 = 2*L*L/9-4*L**3/27+22*L**4/243
    axis_remainders = [axes[0]['log_plus']-old0, axes[1]['log_plus']-old1]
    rows.append(dict(L=L,M_plus=rf['M_plus'],M_minus=rf['M_minus'],
                     baseline_fine_abs_difference=err, flat_mean_floor=floor,
                     numerical_sign_separated=accepted,
                     plus_over_L4=rf['M_plus']/L**4, minus_over_L4=rf['M_minus']/L**4,
                     exact_A_coefficient_exposed=4/1215,
                     max_exposed_forward_series_remainder=max_directional,
                     remainder_over_L5=max_directional/L**5,
                     published_axis_remainders=axis_remainders))
print(json.dumps(dict(status='NUMERICAL_CORROBORATION_NOT_CERTIFIED_ENCLOSURE',results=rows),indent=2))
