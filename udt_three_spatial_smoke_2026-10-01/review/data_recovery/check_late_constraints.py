"""Original metric constraints with K independently reconstructed via Lie_beta gamma."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
sys.path.insert(0,str(BASE/'review/data'))
from check_constraints import derivative, constraints
from check_harmonic import contracted

def extrinsic_lie(g,v,periods):
    gamma=g[...,1:,1:]
    inverse=np.linalg.inv(gamma)
    spacetime_inverse=np.linalg.inv(g)
    alpha=1/np.sqrt(-spacetime_inverse[...,0,0])
    beta=np.einsum('...ij,...j->...i',inverse,g[...,0,1:])
    dgamma=[derivative(gamma,k,periods) for k in range(3)]
    dbeta=[derivative(beta,k,periods) for k in range(3)]
    lie=np.zeros_like(gamma)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                lie[...,i,j]+=beta[...,k]*dgamma[k][...,i,j]
                lie[...,i,j]+=gamma[...,k,j]*dbeta[i][...,k]+gamma[...,i,k]*dbeta[j][...,k]
    K=(lie-v[...,1:,1:])/(2*alpha[...,None,None])
    return gamma,K,alpha,beta

records=[]
for name in ('n8_repaired','n12','n16','n16_half','kasner','kasner_half'):
    path=BASE/'histories'/f'{name}.npz'
    with np.load(path,allow_pickle=False) as history:
        periods=np.broadcast_to(history['period'],(3,))
        # The final slice plus a separated interior slice avoid an initial-only test.
        for index in sorted(set([len(history['times'])//2,len(history['times'])-1])):
            g=history['g'][index];v=history['v'][index]
            gamma,K,alpha,beta=extrinsic_lie(g,v,periods)
            result,_=constraints(gamma,K,periods)
            h_cov=contracted(g,v,periods)
            h_contra=np.einsum('...ab,...b->...a',np.linalg.inv(g),h_cov)
            result.update(name=name,index=index,t=float(history['times'][index]),
                harmonic_covector_abs_max=float(np.max(np.abs(h_cov))),
                harmonic_vector_abs_max=float(np.max(np.abs(h_contra))),
                lapse_minmax=[float(alpha.min()),float(alpha.max())],
                shift_abs_max=float(np.max(np.abs(beta))),
                source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            assert max(result['hamiltonian_abs_max'],*result['momentum_abs_max_by_component'],
                       result['harmonic_vector_abs_max'])<2e-5
            records.append(result)
late={r['name']:r for r in records if r['index']==max(x['index'] for x in records if x['name']==r['name'])}
for previous,later in [('n8_repaired','n12'),('n12','n16')]:
    assert late[later]['hamiltonian_abs_max']<late[previous]['hamiltonian_abs_max']
    assert max(late[later]['momentum_abs_max_by_component'])<max(late[previous]['momentum_abs_max_by_component'])
print(json.dumps(dict(status='LATE_ORIGINAL_CONSTRAINTS_PASS',records=records,
    code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    scope='Original constraints at saved interior/final times, Lie-shift K reconstruction. Same Fourier method as producer; not continuum or long-time certification.'),indent=2,sort_keys=True))
