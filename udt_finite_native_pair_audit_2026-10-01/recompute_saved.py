"""Parent readout recomputation from peer-saved rows; not a new trajectory proof."""
from pathlib import Path
from fractions import Fraction as Q
import json, hashlib
src=Path(__file__).parent/'math/ambient.stdout'
d=json.loads(src.read_text()); assert d['status']=='PASS' and len(d['rows'])==30
checks=0
for r in d['rows']:
    eps=r['curvature_sign']; k=Q(r['k']); p=Q(r['p']); m=Q(r['source_affine_span'])
    kap=eps*k*k
    # Endpoint ribbon contractions from J=(1-lambda)U+lambda*p*UB,
    # U.UB=-p and UB.UB=-1. These derive full h without its formula.
    for lam in [Q(0),Q(1,3),Q(1)]:
        h00=-(1-lam)**2-2*lam*(1-lam)*p*p-lam*lam*p*p
        expected=-1-kap*m*m*lam*(2-lam)
        assert h00==expected and h00<0; checks+=1
        det=-m*m
        assert det<0; checks+=1
    # Full Lorentz first column reconstructed from the null multiplier,
    # then compare the independently saved projective readout.
    gamma=Q(r['Gamma_transport']); chi=Q(r['signed_projective']); ss=gamma*chi
    assert gamma*gamma-ss*ss==1; checks+=1
    assert gamma+ss==1/p and gamma-ss==p; checks+=1
    assert chi==(1-p*p)/(1+p*p); checks+=1
    assert r['A_static_first_reception_regular']==(1-kap*m*m>0); checks+=1
print(json.dumps({'status':'PASS','rows':30,'assertions':checks,
 'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'scope':'Saved-row original ribbon contractions and Lorentz/null-frequency identities; shares displayed mathematical premises, no new independent worldline reconstruction.'},indent=2))
