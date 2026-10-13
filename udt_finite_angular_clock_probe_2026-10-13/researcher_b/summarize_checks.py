"""Frozen-artifact summary; numerical convergence is not interval certification."""
import json
from pathlib import Path

base=Path(__file__).resolve().parent
def read(name): return json.loads((base/name).read_text())

deformation=[]
for tag in ['neg4','neg5','pos5','pos4']:
    fine=read(f'deform_{tag}_data.json')
    baseline=read(f'deform_{tag}_baseline_data.json') if tag.startswith('neg') else None
    for i,row in enumerate(fine['results']):
        delta=None
        if baseline:
            delta=max(abs(row[k]-baseline['results'][i][k]) for k in ['M_plus','M_minus'])
            assert min(abs(row[k]) for k in ['M_plus','M_minus'])>50*delta
        deformation.append(dict(epsilon=fine['arguments']['epsilon'],L=row['L'],
                                M_plus=row['M_plus'],M_minus=row['M_minus'],
                                combined_mean=(row['M_plus']+row['M_minus'])/2,
                                baseline_fine_max_difference=delta))
arrival=json.loads((base/'arrival_derivatives.stdout').read_text())
cap=[]
for path in sorted(base.glob('*.json')):
    d=read(path.name)
    if 'returncode' in d and 'command' in d:
        cap.append(dict(file=path.name,returncode=d['returncode'],seconds=d['duration_seconds'],
                        maxrss_kib=d['maxrss_kib']))
assert all(x['returncode']==0 for x in cap)
print(json.dumps(dict(status='SAVED_ARTIFACT_SUMMARY',deformation=deformation,
                      arrival_comparisons=len(arrival['results']),
                      max_arrival_frequency_difference=max(x['absolute_difference'] for x in arrival['results']),
                      max_arrival_incidence_residual=max(x['max_incidence_residual'] for x in arrival['results']),
                      captures=cap,captured_wall_seconds=sum(x['seconds'] for x in cap),
                      note='CPU seconds not separately recorded by existing capture utility; this is summed wall time.'),indent=2))
