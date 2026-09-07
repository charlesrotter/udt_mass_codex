"""R1 preservation, unchanged-analysis membership and quadratic-root semantics."""
import ast
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy import fft

root = Path(__file__).resolve().parent.parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
ready = json.loads((root/'AUTHOR_REPAIR_READY.json').read_text())
initial = json.loads((root/'AUTHOR_CANDIDATE_READY.json').read_text())
assert sha(root/'AUTHOR_CANDIDATE_READY.json') == ready['initial_ready_sha256']
preserved = {}
for key,row in ready['initial_preservation'].items():
    assert sha(root/row['path']) == row['sha256'] == initial[key+'_sha256']
    preserved[key] = row['sha256']
for key,path in ready['artifact_paths'].items():
    assert sha(root/path) == ready[key+'_sha256']
assert sha(root.parent/'step_01/FREEZE.json') == ready['freeze_unchanged_sha256'] == 'fa0506eaea5ef20dcd92aabf3b2d1a0efc7fb75ef6c7272c00e5e6764c591324'
def functions(path):
    return {n.name:ast.dump(n) for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef)}
old,new = functions(root/'initial/screen.py'),functions(root/'screen.py')
assert old.keys() == new.keys()
changed = [key for key in old if old[key] != new[key]]
assert set(changed) == {'synthetic','evaluate'}
# Independently compare old and new core membership; no import of screen.
freq = fft.rfftfreq(90*4096,1/4096)
bins = np.arange(len(freq))
assert np.array_equal((freq>=30)&(freq<=500),(bins>=2700)&(bins<=45000))
evaluation = json.loads((root/ready['artifact_paths']['evaluation']).read_text())
with np.load(root/ready['artifact_paths']['coefficients'],allow_pickle=False) as data:
    q,c,u,T = data['reference_Q'],data['cross_terms'],data['signal_Q'],float(data['threshold'])
    roots = []
    maximum_equality_error = 0.
    for family in range(3):
        cs = c[family]
        us = u[family][:,None]
        distance = T-q[None,:]
        discriminant = np.sqrt(cs**2+us*distance)
        denominator = discriminant+cs
        stable = np.divide(distance,denominator,out=np.zeros_like(cs),where=denominator!=0)
        critical = np.where(cs>=0,stable,(discriminant-cs)/us)
        equality = q[None,:]+2*cs*critical+us*critical**2
        maximum_equality_error = max(maximum_equality_error,float(np.max(abs(equality-T))/T))
        hrss = float(np.sort(critical.ravel())[151]/1e21)
        roots.append(hrss)
        assert abs(hrss/evaluation['families'][family]['finite_90percent_crossing_hrss']-1)<1e-12
    assert maximum_equality_error < 1e-12
candidate = (root/'CANDIDATE.md').read_text()
assert 'strict-crossing infimum' in candidate and 'equality itself does not pass' in candidate
print(json.dumps({'all_original_pins_preserved':True,'preserved_hashes':preserved,
                  'freeze_unchanged':True,'changed_function_definitions':changed,
                  'core_band_membership_unchanged':True,'root_semantics':'threshold-equality roots; strict-crossing infima, not directly injected beyond-grid trials',
                  'stable_90percent_root_hrss':roots,'root_equality_max_relative_error':maximum_equality_error,
                  'ready_sha256':sha(root/'AUTHOR_REPAIR_READY.json')},indent=2))
