"""Bounded adaptation of the prior first-three operational receipt checker.

Same runtime checks, parameterized for the repaired first pair/full 26. No
original-equation reconstruction or new independent evolution implementation.
"""
import argparse, collections, hashlib, json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent
def read(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--count',type=int,choices=[2,26],required=True);ap.add_argument('--controller',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
 path=B/'diagnosis/repair_runtime/campaign.json';m=read(path);runtime=path.parent;mh=sha(path)
 assert len(m['cases'])==26 and m['wall_seconds'] is None
 assert (runtime/'manifest.sha256').read_text().strip()==mh
 for p,h in m['source_sha256'].items():assert sha(p)==h,p
 folders=sorted(p for p in (runtime/'attempts').iterdir() if p.is_dir());assert len(folders)==args.count
 reports=[]
 for row,folder in zip(m['cases'][:args.count],folders,strict=True):
  spec=read(row['spec']);receipt=read(folder/'receipt.json');launch=read(folder/'launch.json');run=Path(row['run'])
  assert row['spec_sha256']==sha(row['spec'])==sha(run/'spec.json')
  assert receipt['case']==launch['case']==row['id'] and launch['manifest_sha256']==mh
  assert receipt['returncode']==0 and receipt['worker_status']=='TPS1_RUN_COMPLETE'
  assert not any(receipt[x] for x in ['resume','sigint_sent','sigterm_sent','sigkill_sent','forwarded_signal'])
  assert launch['wall_seconds_limit'] is None and spec['wall_seconds'] is None
  assert receipt['command']==launch['command'] and receipt['command'][1:]==[str(B/'production_worker.py'),row['spec'],row['run']]
  for stream in ['stdout','stderr']:assert sha(folder/stream)==receipt[stream+'_sha256']
  logs=[json.loads(x) for x in (folder/'stdout').read_text().splitlines()]
  accepted=[x for x in logs if x['status']=='ACCEPTED_STEP'];checked=[x for x in logs if x['status']=='CHECKED_STATE'];tick=0
  saves={0,spec['end_tick'],*range(spec['checkpoint_ticks'],spec['end_tick'],spec['checkpoint_ticks'])}
  for window in spec['windows']:saves.update(window['center']+(i-window['count']//2)*window['stride'] for i in range(window['count']))
  checks=saves|set(range(spec['check_ticks'],spec['end_tick'],spec['check_ticks']))
  assert {x['tick'] for x in checked}==checks
  for step in accepted:
   jump=step['jump_ticks'];assert jump>0 and jump&(jump-1)==0 and jump<=spec['max_step_ticks']
   assert not any(tick<event<tick+jump for event in checks);tick+=jump
   assert step['tick']==tick and step['t']==1+tick*spec['dt_min']
   assert math.isclose(step['stage_cfl'],jump*spec['dt_min']*step['stage_omega'],rel_tol=1e-13)
   assert step['stage_cfl']<=spec['cfl']*(1+1e-12)
  assert tick==spec['end_tick']==4800 and logs[-1]['status']=='TPS1_RUN_COMPLETE' and logs[-1]['steps']==len(accepted)
  assert logs[-1]['retries']==sum(x['status']=='REJECTED_TRIAL_STEP' for x in logs)
  peak=max(x['gpu_allocated_peak'] for x in checked);constraint=max(x['metrics'][k] for x in checked for k in ['hamiltonian','momentum','harmonic'])
  assert peak<=spec['gpu_bytes']==8*1024**3 and constraint<=spec['constraint_limit']==2e-5
  ticks=set();payload_bytes=0
  for marker in run.glob('checkpoints/*/COMMITTED'):
   checkpoint=marker.parent;meta=read(checkpoint/'metadata.json');ticks.add(meta['step'])
   assert marker.read_text().strip()==sha(checkpoint/'metadata.json')
   assert meta['eligible_for_resume'] and meta['diagnostic'] is None and meta['t']==1+meta['step']*spec['dt_min']
   assert meta['signature']['spec']==row['spec_sha256'] and meta['signature']['initial']==m['source_sha256'][str(ROOT/spec['initial'])]
   for p,h in meta['signature']['code'].items():assert h==m['source_sha256'][str(ROOT/p)]
   assert meta['shape']==[2,spec['n'],spec['n'],spec['n'],4,4] and meta['dtype']=='float64'
   assert sha(checkpoint/'state.npz')==meta['payload_sha256'];payload_bytes+=(checkpoint/'state.npz').stat().st_size
  assert ticks==saves and len(ticks)==32
  size=sum(p.stat().st_size for p in run.rglob('*') if p.is_file());assert size<=spec['output_bytes']==256*1024**2
  oldid=row['id'].replace('_n24_quarter','_n24_half').replace('_n32_half','_n32');oldfolder=next((B/'production_runtime/attempts').glob('*_'+oldid));oldlogs=[json.loads(x) for x in (oldfolder/'stdout').read_text().splitlines()];oldsteps=sum(x['status']=='ACCEPTED_STEP' for x in oldlogs);assert len(accepted)>oldsteps
  reports.append(dict(case=row['id'],steps=len(accepted),old_reference_case=oldid,old_steps=oldsteps,step_histogram=dict(collections.Counter(x['jump_ticks'] for x in accepted)),max_stage_cfl=max(x['stage_cfl'] for x in accepted),max_stage_omega=max(x['stage_omega'] for x in accepted),gpu_peak_bytes=peak,maximum_logged_original_constraint=constraint,authenticated_checkpoints=len(ticks),payload_bytes_hashed=payload_bytes,case_bytes=size,receipt_sha256=sha(folder/'receipt.json')))
 controller=Path(args.controller);capture=read(controller)
 assert capture['returncode']==(75 if args.count==2 else 0) and capture['wall_timeout_seconds'] is None and capture['cpu_timeout_seconds'] is None
 assert capture['command'][1:4]==[str(B/'supervise.py'),str(path),str(runtime)]
 if args.count==2:assert capture['command'][4:]==['--stop-after','2']
 for stream in ['stdout','stderr']:assert sha(controller.with_suffix('.'+stream))==capture[stream+'_sha256']
 last=json.loads(controller.with_suffix('.stdout').read_text().splitlines()[-1]);assert last['status']==('QUEUE_CHECKPOINT' if args.count==2 else 'QUEUE_COMPLETE')
 if args.count==2:assert last['newly_completed']==2
 roots=[Path(p) for p in m['storage_roots']];files={p.resolve() for root in roots for p in root.rglob('*') if p.is_file()};size=sum(p.stat().st_size for p in files);assert size<=m['output_bytes']
 result=dict(status='REPAIR_OPERATIONS_PASS',cases=args.count,manifest_sha256=mh,controller_sha256=sha(controller),checker_sha256=sha(__file__),adapted_prior_checker_sha256=sha(B/'review/runtime/check_first_three_operations.py'),reports=reports,used_budgeted_bytes=size,scope='Actual receipt/log/step/CFL/checkpoint/resource review. All repair payload hashes authenticated; producer-reported constraints are attributed, original equation recomputation owned by separate mathematics review. Existing interrupt/restart evidence remains attributed; no new interruption was performed on repair fields.')
 with Path(args.output).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
