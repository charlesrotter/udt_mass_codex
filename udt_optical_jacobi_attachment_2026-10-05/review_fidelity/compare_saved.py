"""Compare already saved independent values; launches no finite cases."""
import json, hashlib
from pathlib import Path
import mpmath as mp
mp.mp.dps=70
p=Path(__file__).resolve().parent.parent
q=p/'review_fidelity'
ours=json.loads((q/'REPLAY_RESULT.json').read_text())
parent=json.loads((p/'CONSTRUCTION_RESULT.json').read_text())
comparisons=[]
for row in ours['records']:
    for prec in parent['precisions']:
        if row['label'].startswith('actual_'):
            ref=next(r for r in prec['actual_incidences'] if mp.mpf(r['E'])==mp.mpf(row['E']) and mp.mpf(r['R'])==mp.mpf(row['R']))
            keys=['b','P','I','B_parallel','B_perp','j_parallel','j_perp','D_A','D_o','Z','t_e']
        else:
            ref=next(r for r in prec['neighbor_controls'] if mp.mpf(r['R'])==mp.mpf(row['R']))
            keys=['b','B_parallel','B_perp']
        errors={key:abs(mp.mpf(row[key])-mp.mpf(ref[key]))/(1+abs(mp.mpf(ref[key]))) for key in keys}
        comparisons.append(dict(case=row['label'],parent_dps=prec['dps'],
            max_scaled_difference=mp.nstr(max(errors.values()),30),
            differences={k:mp.nstr(v,30) for k,v in errors.items()},passed=max(errors.values())<mp.mpf('1e-24')))
result=dict(status='PASS' if all(r['passed'] for r in comparisons) else 'FAIL',
    comparisons=comparisons,
    maximum_scaled_difference=mp.nstr(max(mp.mpf(r['max_scaled_difference']) for r in comparisons),30),
    source_hashes={str(x.relative_to(p.parent)):hashlib.sha256(x.read_bytes()).hexdigest()
        for x in [p/'CONSTRUCTION_RESULT.json',q/'REPLAY_RESULT.json',p/'CLARIFICATIONS.md']},
    unique_finite_cases_replayed=7,cumulative_case_count=23)
(q/'SAVED_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],result['maximum_scaled_difference'],'comparisons',len(comparisons))
