"""Compare completed separate Hamilton/RK45 and producer Christoffel/DOP853 rays."""
import hashlib,json,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
independent=HERE/'first_clock_hamilton.stdout';own=json.loads(independent.read_text());name='axial_a0_n24_half';producer_path=BASE/'production_analysis'/name/'clock.json';producer=json.loads(producer_path.read_text())
history=BASE/'production_analysis'/name/'histories'/(name+'_window2.npz');key=str(history.relative_to(ROOT))
assert producer['history_sha256']==own['history_sha256'][key]==sha(history)
rows=[]
for a,b in zip(own['readouts'][name],producer['readouts'],strict=True):
    assert a['emission']==b['te'] and a['reception']==b['to'] and np.array_equal(a['initial_coordinate_direction'],b['initial_coordinate_direction'])
    diff=abs(a['logZ']-b['logZ']);position=float(np.max(abs(np.array(a['receiver_position'])-b['receiver_position'])))
    assert diff<2e-7 and a['max_sampled_abs_null_norm']<2e-7
    rows.append(dict(direction=a['initial_coordinate_direction'],hamilton_Z=a['Z'],hamilton_logZ=a['logZ'],producer_logZ=b['logZ'],absolute_logZ_difference=diff,endpoint_position_difference=position,independent_sampled_null=a['max_sampled_abs_null_norm']))
# Temporal and spatial matched supplied queries across the exact first dataset.
all_producer={n:json.loads((BASE/'production_analysis'/n/'clock.json').read_text()) for n in ['axial_a0_n24','axial_a0_n24_half','axial_a0_n32']}
matched=[]
for other in ['axial_a0_n24_half','axial_a0_n32']:
    differences=[]
    for a,b in zip(all_producer['axial_a0_n24']['readouts'],all_producer[other]['readouts'],strict=True):
        assert a['te']==b['te'] and a['to']==b['to'] and np.array_equal(a['initial_coordinate_direction'],b['initial_coordinate_direction'])
        differences.append(abs(a['logZ']-b['logZ']))
    assert max(differences)<2e-7;matched.append(dict(reference='axial_a0_n24',other=other,maximum_logZ_difference=max(differences)))
result=dict(status='FIRST_CLOCK_INDEPENDENT_AGREEMENT_PASS',rows=rows,matched_refinement=matched,maximum_independent_logZ_difference=max(r['absolute_logZ_difference'] for r in rows),maximum_endpoint_position_difference=max(r['endpoint_position_difference'] for r in rows),source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [independent,producer_path,history,HERE/'CLOCK_SUBSET_FREEZE.json',Path(__file__)]},scope='Separate ray equations/integrators, same supplied geometry and Fourier/Hermite methods. First dataset late local windows only; no independent metric evolution, physical observer population or cosmological-distance claim.')
with (HERE/'FIRST_CLOCK_AGREEMENT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
