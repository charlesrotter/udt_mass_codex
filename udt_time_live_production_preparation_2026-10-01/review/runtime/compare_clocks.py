"""Compare independently completed Hamilton and producer Christoffel readouts."""
import hashlib,json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
independent=HERE/'late_clock.stdout';own=json.loads(independent.read_text());rows=[]
for name,file in [('kasner_n16_half','clock_kasner'),('axial1_n24_half','clock_axial_half')]:
    path=BASE/'checks'/(file+'.stdout');producer=json.loads(path.read_text())
    assert producer['history_sha256']==own['history_sha256'][producer['history']]
    diffs=[];position=[]
    for a,b in zip(own['readouts'][name],producer['readouts'],strict=True):
        assert a['emission']==b['te'] and a['reception']==b['to']
        assert np.array_equal(a['initial_coordinate_direction'],b['initial_coordinate_direction'])
        diffs.append(abs(a['logZ']-b['logZ']))
        position.append(float(np.max(abs(np.array(a['receiver_position'])-b['receiver_position']))))
    assert max(diffs)<2e-7
    rows.append(dict(name=name,max_logZ_difference=max(diffs),max_endpoint_position_difference=max(position),
        producer_output_sha256=sha(path),history_sha256=producer['history_sha256']))
print(json.dumps(dict(status='INDEPENDENT_CLOCK_AGREEMENT_PASS',rows=rows,
    independent_output_sha256=sha(independent),
    scope='Separate ray equations and integrators, same supplied saved geometry and Fourier/Hermite methods. Not an independent metric evolution.'),indent=2))
