"""CPU-only preview-grid and polarization controls; never emit a campaign."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
sys.path.insert(0,str(BASE))
from prepare_campaign import families

data=families();assert len(data)==78
assert sum(k.startswith('axial') for k in data)==6
assert sum(k.startswith('oblique') for k in data)==72
original=json.loads((BASE/'families/oblique1.json').read_text())['modes']
amplitudes=[.25,.5,1.,1.5,2.,3.]
records=[]
for name,modes in data.items():
    for index,mode in enumerate(modes):
        n=np.array(mode['k'],float);matrix=np.array(mode['matrix'],float)
        assert np.max(abs(n))<12
        if name.startswith('oblique'):
            a,p,r=(int(part[1:]) for part in name.split('_')[1:])
            unit=n/np.linalg.norm(n)
            # Independent SVD tensor construction from the baseline matrix.
            _,_,vh=np.linalg.svd(n.reshape(1,3),full_matrices=True);x,y=vh[1:]
            s=np.array(original[index]['matrix'],float)
            baseline=.5*(x@s@x-y@s@y)*(np.outer(x,x)-np.outer(y,y))+(x@s@y)*(np.outer(x,y)+np.outer(y,x))
            baseline*=np.sqrt(2)/np.linalg.norm(baseline)
            theta=[0.,np.pi/12,np.pi/6][r]
            J=np.array([[0.,-unit[2],unit[1]],[unit[2],0.,-unit[0]],[-unit[1],unit[0],0.]])
            rotation=np.eye(3)+np.sin(theta)*J+(1-np.cos(theta))*(J@J)
            expected=rotation@baseline@rotation.T
            error=float(abs(expected-matrix).max())
            trace=float(abs(np.trace(matrix)));trans=float(abs(n@matrix).max());sym=float(abs(matrix-matrix.T).max())
            norm=float(np.sum(matrix*matrix))
            assert max(error,trace,trans,sym,abs(norm-2))<5e-14
            assert mode['amplitude']==original[index]['amplitude']*amplitudes[a]
            assert mode['phase']==original[index]['phase']+([0.,.5,1.,1.5][p] if index==3 else 0.)
            records.append(dict(name=name,mode=index,rotation_error=error,trace=trace,transversality=trans,symmetry=sym,norm2=norm))
result=dict(status='PASS',datasets=len(data),planned_runs=3*len(data),checked_oblique_modes=len(records),
    maximum_rotation_error=max(r['rotation_error'] for r in records),
    maximum_tt_defect=max(max(r['trace'],r['transversality'],r['symmetry']) for r in records),
    maximum_norm2_error=max(abs(r['norm2']-2) for r in records),
    producer_code_imported_for_recipe=True,independent_method='SVD baseline plus Rodrigues rotation; no producer TT projector imported directly',
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    recipe_sha256=hashlib.sha256((BASE/'prepare_campaign.py').read_bytes()).hexdigest(),
    scope='Pure-data preview only. No initial conformal solve or evolution for the78 proposed data sets; future original constraints and history checks remain mandatory. No inequivalence, genericity or native-law claim.')
print(json.dumps(result,indent=2,sort_keys=True))
