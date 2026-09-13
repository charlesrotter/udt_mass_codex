"""C1 repair-only exact controls, reusing reviewer tensor-engine definitions."""
from pathlib import Path
import hashlib
import json
import sys
import datetime

here=Path(__file__).resolve().parent
source=here/'independent_exact.py'
raw=source.read_text()
marker='# Metadata and source checks are saved with the same bounded capture.'
assert raw.count(marker)==1
ns={'__name__':'reviewer_tensor_definitions','__file__':str(source)}
exec(compile(raw.split(marker)[0],str(source),'exec'),ns)
Q=ns['Q'];coord=ns['coord'];J=ns['J'];diag=ns['diag'];tensors=ns['tensors'];equal=ns['equal'];zero=ns['zero'];nonzero=ns['nonzero']
u,v,x,y=coord([Q(1,2),Q(0),Q(2,3),Q(-1,4)])
g=diag(0,0,1,1);g[0][1]=g[1][0]=J(-1)
for name,K,target in [('affine',[0,x,1+u,0],Q(2)),('epsilon_zero',[0,0,1,0],Q(0))]:
    s=tensors(g,K)
    zero(name+'_Killing',s['Lie']);zero(name+'_Ricci',s['Ric'])
    equal(name+'_Fux',s['F'][0][2],target)
    zero(name+'_all_field_derivatives',[s['F'][a][b].d(c) for a in range(4) for b in range(4) for c in range(4)])
    zero(name+'_divergence',s['div'])
    zero(name+'_invariant',s['invariant'])
    if name=='affine':nonzero(name+'_nonzero_field',s['F'])
    else:zero(name+'_zero_field',s['F'])

pkg=here.parent
freeze=json.loads((pkg/'PROFILE_CLARIFICATION_FREEZE.json').read_text())
profile_hash=hashlib.sha256((pkg/freeze['file']).read_bytes()).hexdigest()
checks=ns['checks']
checks.append({'name':'C1_exact_frozen_clarification','pass':profile_hash==freeze['sha256']})
atlas=pkg.parent/'udt_native_radiative_current_energy_owner_audit_2026-08-15/CANDIDATE_OWNER_ATLAS.tsv'
checks.append({'name':'G95_addendum_exact_atlas_hash','pass':hashlib.sha256(atlas.read_bytes()).hexdigest()=='f2e4ba81d315d1ac77b5d60178c19e19683bcece1cfbd34c2cd32ebe052188f1'})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'C1 repair-only exact equation controls and source correspondence; reused reviewer engine, not new independent implementation','source_engine_sha256':hashlib.sha256(raw.encode()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'count':len(checks),'passed':sum(c['pass'] for c in checks),'all_pass':all(c['pass'] for c in checks)}
with Path(sys.argv[1]).open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'count':out['count'],'passed':out['passed'],'all_pass':out['all_pass']}))
sys.exit(0 if out['all_pass'] else 1)
