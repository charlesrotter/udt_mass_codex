"""CPU test of producer bound against independent ADM reconstruction."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np
import torch

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
sys.path.insert(0,str(BASE))
from production_worker import geometry_bound

torch.set_num_threads(1)
rng=np.random.default_rng(83921)
rows=[]
for trial in range(20):
    matrix=rng.normal(size=(3,3))
    gamma=matrix.T@matrix+.2*np.eye(3)
    alpha=float(np.exp(rng.normal()))
    beta=rng.normal(size=3)
    g=np.zeros((4,4));g[1:,1:]=gamma;g[0,1:]=g[1:,0]=gamma@beta
    g[0,0]=-alpha**2+beta@gamma@beta
    actual,_=geometry_bound(torch,torch.tensor(g),16,2*np.pi)
    expected=8*(np.abs(beta).sum()+alpha*np.sqrt(3*np.linalg.eigvalsh(np.linalg.inv(gamma)).max()))
    modes=np.array(list(itertools.product(range(-8,9),repeat=3)),float)
    frequencies=np.abs(modes@beta)+alpha*np.sqrt(np.einsum('ni,ij,nj->n',modes,np.linalg.inv(gamma),modes))
    relative_error=float(abs(actual-expected)/expected)
    assert relative_error<2e-13
    assert frequencies.max()<=actual*(1+2e-13)
    rows.append(dict(trial=trial,bound=actual,independent_bound=expected,relative_error=relative_error,
        largest_principal_frequency=float(frequencies.max())))
caught=[]
for label,g in [('spatial_indefinite',np.diag([-1.,-1.,1.,1.])),
                ('euclidean',np.eye(4)),('nan',np.full((4,4),np.nan))]:
    try:
        geometry_bound(torch,torch.tensor(g),16,2*np.pi)
    except RuntimeError as exc:
        caught.append(dict(label=label,error=str(exc)))
assert len(caught)==3
print(json.dumps(dict(status='PASS',rows=rows,invalid_geometry_caught=caught,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    producer_sha256=hashlib.sha256((BASE/'production_worker.py').read_bytes()).hexdigest(),
    numpy=np.__version__,torch=torch.__version__,device='cpu',
    scope='Tests producer bound only; independent frequency reconstruction, no numerical-stability or native-law conclusion.'),indent=2,sort_keys=True))
