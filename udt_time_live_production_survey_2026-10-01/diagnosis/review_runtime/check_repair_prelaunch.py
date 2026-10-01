"""Operational prelaunch check of the one frozen 26-case numerical repair."""
import hashlib, importlib.util, json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent
def read(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 path=B/'diagnosis/repair_runtime/campaign.json';m=read(path);old=read(B/'production_runtime/campaign.json');oldrows={x['id']:x for x in old['cases']}
 assert len(m['cases'])==26 and m['wall_seconds'] is None and m['output_bytes']==64*1024**3
 roots=[Path(p).resolve() for p in m['storage_roots']]
 assert len(roots)==len(set(roots))
 assert all(not a.is_relative_to(b) for a in roots for b in roots if a!=b)
 assert all(p.is_relative_to(B) for p in roots)
 for p,h in m['source_sha256'].items():assert sha(p)==h,p
 s=importlib.util.spec_from_file_location('unchanged_worker',B/'production_worker.py');worker=importlib.util.module_from_spec(s);s.loader.exec_module(worker)
 results=[];reserves=0
 for row in m['cases']:
  original_id=row['id'].replace('_n24_quarter','_n24_half').replace('_n32_half','_n32');oldrow=oldrows[original_id]
  spec=read(row['spec']);original=read(oldrow['spec'])
  assert sha(row['spec'])==row['spec_sha256']
  assert {k for k in spec if spec[k]!=original[k]}=={'cfl','max_step_ticks'}
  assert spec['cfl']==original['cfl']/2 and spec['max_step_ticks']==original['max_step_ticks']//2
  saves,checks,initial=worker.validate(spec)
  assert len(saves)==32 and spec['output_bytes']==256*1024**2
  assert sha(initial)==m['source_sha256'][str(initial)]
  folder=next((B/'production_runtime/attempts').glob('*_'+original_id))
  logs=[json.loads(l) for l in (folder/'stdout').read_text().splitlines()]
  omega=max(x['stage_omega'] for x in logs if x['status']=='ACCEPTED_STEP')
  floor_margin=spec['cfl']/(omega*spec['dt_min']);assert floor_margin>1
  reserve=sum(w['count']*2*spec['n']**3*16*8+1024**2 for w in spec['windows'])+1024**2
  reserves+=reserve
  results.append(dict(case=row['id'],spec_sha256=row['spec_sha256'],initial_sha256=sha(initial),n=spec['n'],cfl=spec['cfl'],max_step_ticks=spec['max_step_ticks'],past_stage_floor_tick_margin=floor_margin,window_assembly_reserve_bytes=reserve))
 assert [x['case'] for x in results[:2]]==['oblique_a5_p0_r0_n24_quarter','oblique_a5_p0_r0_n32_half']
 mapping=read(B/'diagnosis/REPAIR_CASES.json');assert mapping['repair_manifest_sha256']==sha(path)
 used=sum(p.stat().st_size for root in roots for p in root.rglob('*') if p.is_file())
 capsum=26*256*1024**2;diagnosis_reserve=1024**3
 assert used+capsum+reserves+diagnosis_reserve<m['output_bytes']
 result=dict(status='FIRST_PAIR_OPERATIONAL_GATE_CLEARED',repair_manifest_sha256=sha(path),repair_dispatch_sha256=sha(B/'diagnosis/REPAIR_DISPATCH.md'),checker_sha256=sha(__file__),results=results,current_root_bytes=used,run_cap_sum_bytes=capsum,window_assembly_reserve_bytes=reserves,diagnosis_reserve_bytes=diagnosis_reserve,forecast_ceiling_bytes=used+capsum+reserves+diagnosis_reserve,total_output_bytes=m['output_bytes'],scope='Prelaunch source/schema/budget and past-geometry floor checks only. Actual new geometry, original equations, schedules, outputs and two-case firstgate must pass before remaining24; existing interrupt/restart tests attributed to byte-identical worker/supervisor/checkpoint path.',first_pair_command=['python3',str(B/'supervise.py'),str(path),str(path.parent),'--stop-after','2'],omissions=['No new GPU run or forecast of new outcomes','No independent general-data evolution','No repeated actual pause/restart control; unchanged executable source established by hashes','Parent host GPU/device freshness evidence attributed separately'])
 with (HERE/'REPAIR_PRELAUNCH_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
if __name__=='__main__':main()
