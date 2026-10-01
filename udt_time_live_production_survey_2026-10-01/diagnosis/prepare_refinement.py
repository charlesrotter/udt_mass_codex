"""Emit one outcome-disclosed resolution repair; no equation or threshold change."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1];ROOT=B.parent;D=B/'diagnosis'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,d):
 with Path(p).open('x') as f:json.dump(d,f,indent=2,sort_keys=True);f.write('\n')
def main():
 original=B/'production_runtime/campaign.json';aggregate=B/'production_analysis/postprocess/MATH_CANDIDATE.json'
 freeze=read(D/'INITIAL_FREEZE.json')
 for p in [original,aggregate]:
  assert sha(p)==freeze['sha256'][str(p.relative_to(ROOT))]
 m=read(original);rows=read(aggregate)['datasets'];failed=[r['dataset'] for r in rows if r['status']=='DIAGNOSTIC_NOT_QUALIFIED']
 expected=['axial_a5']+[f'oblique_a5_p{p}_r{r}' for p in range(4) for r in range(3)]
 assert failed==expected
 specs=D/'repair_specs';runtime=D/'repair_runtime';runs=B/'runs/refinement';analysis=D/'repair_analysis'
 for p in [specs,runtime,runs,analysis]:
  if p.exists():raise ValueError('REFUSE_EXISTING_REPAIR_AREA: '+str(p))
 for p in [specs,runtime,runs,analysis]:p.mkdir(parents=True)
 old={r['id']:r for r in m['cases']};cases=[];mapping=[]
 # First dataset has both original time and spatial diagnostic flags.
 ordering=['oblique_a5_p0_r0']+[x for x in failed if x!='oblique_a5_p0_r0']
 for dataset in ordering:
  rowmap={'dataset':dataset,'original_status':'DIAGNOSTIC_NOT_QUALIFIED','base_case':dataset+'_n24_half','quarter_case':dataset+'_n24_quarter','fine32_case':dataset+'_n32_half'}
  for old_suffix,new_suffix in [('n24_half','n24_quarter'),('n32','n32_half')]:
   original_row=old[dataset+'_'+old_suffix];assert sha(original_row['spec'])==original_row['spec_sha256'];spec=read(original_row['spec']);oldspec=dict(spec)
   spec['cfl']/=2;spec['max_step_ticks']//=2
   assert {k for k in spec if spec[k]!=oldspec[k]}=={'cfl','max_step_ticks'}
   cid=dataset+'_'+new_suffix;path=specs/(cid+'.json');write(path,spec)
   cases.append(dict(id=cid,spec=str(path),spec_sha256=sha(path),run=str(runs/cid)))
  mapping.append(rowmap)
 roots=[*m['storage_roots'],str(B/'review/math/cases'),str(B/'review/math/captures'),str(runs),str(D)]
 for a in roots:
  for b in roots:
   if a!=b and Path(a).resolve().is_relative_to(Path(b).resolve()):raise ValueError('OVERLAPPING_STORAGE_ROOTS')
 sources=dict(m['source_sha256'])
 for p in [Path(__file__),D/'WORK_ORDER.md',D/'REPAIR_DISPATCH.md',D/'INITIAL_FREEZE.json']:sources[str(p)]=sha(p)
 result=dict(wall_seconds=None,output_bytes=m['output_bytes'],storage_roots=roots,source_sha256=sources,cases=cases)
 write(runtime/'campaign.json',result)
 write(D/'REPAIR_CASES.json',dict(original_manifest_sha256=sha(original),original_failed_aggregate_sha256=sha(aggregate),case_count=len(cases),datasets=mapping,repair_manifest_sha256=sha(runtime/'campaign.json'),scope='Old24half,new24quarter,new32half; unchangedinputs/equations/windows/thresholds. Original65/13table remains fixed.'))
 print(json.dumps(dict(status='REPAIR_SPECS_FROZEN',cases=len(cases),manifest=str(runtime/'campaign.json'))))
if __name__=='__main__':main()
