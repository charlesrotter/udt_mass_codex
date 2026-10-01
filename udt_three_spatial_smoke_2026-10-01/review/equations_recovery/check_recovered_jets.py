#!/usr/bin/env python3
"""Recovery consistency check against attributed prior reviewer code, not a new independent argument."""
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np
from history_ricci import original_ricci

HERE=Path(__file__).resolve().parent
prior=HERE.parent/'equations'/'independent_jets.py'
spec=importlib.util.spec_from_file_location('prior_equation_reviewer',prior)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
previous=json.loads((prior.parent/'INDEPENDENT_JETS_RESULT.json').read_text())
assert previous['reviewer_source_sha256']==hashlib.sha256(prior.read_bytes()).hexdigest()
rng=np.random.default_rng(978671)
errors=[];identity=[]
for _ in range(12):
    a=rng.normal(size=(4,4))*.03;g=np.diag([-1.,1.,1.,1.])+a+a.T
    d=rng.normal(size=(4,4,4))*.12;d=(d+d.transpose(0,2,1))/2
    dd=rng.normal(size=(4,4,4,4))*.12;dd=(dd+dd.transpose(1,0,2,3))/2;dd=(dd+dd.transpose(0,1,3,2))/2
    actual=original_ricci(g,d,dd)[0];reference=old.geometry(g,d,dd)
    errors.append(float(abs(actual-reference['ric']).max()))
    identity.append(float(abs(reference['identity_error']).max()))
assert max(errors)<1e-13 and max(identity)<1e-13
result={'status':'RECOVERY_CONSISTENCY_PASS','old_source_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),
        'history_checker_sha256':hashlib.sha256((HERE/'history_ricci.py').read_bytes()).hexdigest(),
        'max_ricci_implementation_difference':max(errors),'max_replayed_old_identity_error':max(identity),
        'random_jet_count':len(errors),'numpy':np.__version__,
        'scope':'Old separate-context implementation replay plus recovery NumPy Ricci consistency; explicit prior-source exposure, not a wholly new independent reviewer argument.'}
with (HERE/'RECOVERED_JETS_RESULT.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(result,sort_keys=True))
