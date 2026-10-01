"""Finite candidate-check companion; waits for one bound controller, never a timer.

Reuses frozen assemblers, mathematical checkers and both ray implementations.
All resulting flags are machine diagnostics pending actual adversarial review.
"""
import argparse,datetime,fcntl,hashlib,json,math,os,signal,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent
TPP=ROOT/'udt_time_live_production_preparation_2026-10-01'

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def read(path):return json.loads(Path(path).read_text())
def write(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def process_alive(record):
    stat=Path('/proc')/str(record['pid'])/'stat'
    try:parts=stat.read_text().rsplit(')',1)[1].split()
    except FileNotFoundError:return False
    return parts[19]==record['proc_start_ticks'] and parts[0]!='Z'
def bytes_used(roots):
    files={p.resolve() for root in roots if root.exists() for p in root.rglob('*') if p.is_file()}
    return sum(p.stat().st_size for p in files)
def verify_sources(dispatch):
    for path,value in dispatch['source_sha256'].items():
        if sha(ROOT/path)!=value:raise ValueError('POSTPROCESS_SOURCE_CHANGED: '+path)
def successful_queue(manifest,runtime):
    known={row['id'] for row in manifest['cases']};complete=set();attempts=[]
    if len(known)!=234 or len(manifest['cases'])!=234:raise ValueError('EXPECTED_234_CASES')
    for folder in sorted((runtime/'attempts').iterdir()):
        if not folder.is_dir():continue
        receipt=read(folder/'receipt.json');launch=read(folder/'launch.json')
        if receipt['case'] not in known or receipt['case']!=launch['case'] or launch['manifest_sha256']!=manifest['_sha256']:raise ValueError('ATTEMPT_BINDING')
        for stream in ['stdout','stderr']:
            if sha(folder/stream)!=receipt[stream+'_sha256']:raise ValueError('ATTEMPT_STREAM_CHANGED')
        if receipt['returncode']==0:
            if receipt['case'] in complete or receipt['worker_status']!='TPS1_RUN_COMPLETE':raise ValueError('COMPLETION_CLAIM')
            complete.add(receipt['case'])
        elif receipt['returncode']!=75 or receipt.get('worker_stop_reason') not in ['SIGNAL','REQUESTED_PAUSE']:raise ValueError('DIAGNOSTIC_ATTEMPT')
        attempts.append(dict(case=receipt['case'],returncode=receipt['returncode'],receipt_sha256=sha(folder/'receipt.json')))
    if complete!=known:raise ValueError('INCOMPLETE_QUEUE')
    return attempts

def compare_clocks(manifest,analysis,independent_path,output):
    independent=read(independent_path);dispatch=read(B/'CLOCK_DISPATCH.json');query=read(B/'review/runtime/SUBSET_CLOCK_QUERIES.json')
    if independent.get('status')!='HAMILTON_CLOCK_REVIEW_PASS':raise ValueError('INDEPENDENT_CHECK_NOT_PASSED')
    limit=dispatch['matched_logZ_threshold'];null_limit=dispatch['null_threshold'];records={};hashes={}
    for row in manifest['cases']:
        path=analysis/row['id']/'clock.json';value=read(path);history=analysis/row['id']/'histories'/(row['id']+'_window2.npz')
        if value['status']!='FINITE_CLOCK_CHECK_PASS' or value['history_sha256']!=sha(history) or len(value['readouts'])!=4:raise ValueError('PRODUCER_CLOCK_BINDING')
        for ray in value['readouts']:
            if [ray['te'],ray['to']]!=dispatch['query_times'] or not all(math.isfinite(ray[k]) for k in ['Z','logZ','max_sampled_abs_null_norm']):raise ValueError('CLOCK_QUERY_OR_FINITE')
            if ray['Z']<=0 or ray['max_sampled_abs_null_norm']>=null_limit:raise ValueError('CLOCK_NULL_OR_FREQUENCY')
        records[row['id']]=value;hashes[str(path.relative_to(ROOT))]=sha(path)
    matched=[]
    for i in range(0,len(manifest['cases']),3):
        a,b,c=[row['id'] for row in manifest['cases'][i:i+3]]
        for other in [b,c]:
            diffs=[]
            for x,y in zip(records[a]['readouts'],records[other]['readouts'],strict=True):
                if x['initial_coordinate_direction']!=y['initial_coordinate_direction'] or x['emitter_position']!=y['emitter_position']:raise ValueError('UNMATCHED_CLOCK_QUERY')
                diffs.append(abs(x['logZ']-y['logZ']))
            matched.append(dict(reference=a,other=other,max_logZ_difference=max(diffs),diagnostic='PASS' if max(diffs)<limit else 'FAIL'))
    required={row['name'] for row in query['cases']}
    if set(independent['readouts'])!=required or len(required)!=30:raise ValueError('INDEPENDENT_SUBSET_COVERAGE')
    comparisons=[]
    for row in query['cases']:
        name=row['name'];own=independent['readouts'][name];producer=records[name]
        if len(own)!=4 or independent['history_sha256'][row['history']]!=producer['history_sha256']:raise ValueError('INDEPENDENT_HISTORY_BINDING')
        diffs=[];positions=[]
        for x,y in zip(own,producer['readouts'],strict=True):
            if x['emission']!=y['te'] or x['reception']!=y['to'] or x['initial_coordinate_direction']!=y['initial_coordinate_direction']:raise ValueError('INDEPENDENT_QUERY_MISMATCH')
            if not math.isfinite(x['logZ']) or x['max_sampled_abs_null_norm']>=null_limit:raise ValueError('INDEPENDENT_CLOCK_VALIDITY')
            diffs.append(abs(x['logZ']-y['logZ']));positions.append(max(abs(u-v) for u,v in zip(x['receiver_position'],y['receiver_position'],strict=True)))
        comparisons.append(dict(case=name,max_logZ_difference=max(diffs),max_endpoint_difference=max(positions),diagnostic='PASS' if max(diffs)<limit else 'FAIL'))
    signs={name:[dict(logZ=r['logZ'],Z=r['Z'],sign='positive' if r['logZ']>0 else 'negative' if r['logZ']<0 else 'zero') for r in value['readouts']] for name,value in records.items()}
    passed=all(row['diagnostic']=='PASS' for row in matched+comparisons)
    result=dict(status='CANDIDATE_PENDING_ADVERSARIAL_REVIEW',machine_diagnostic='PASS' if passed else 'FAIL',cases=len(records),independent_cases=len(comparisons),matched=matched,independent_comparisons=comparisons,all_supplied_signs=signs,source_sha256=hashes,independent_output_sha256=sha(independent_path),scope='Supplied finite late-window clocks; all signs retained. Shared fields/Fourier mathematics; no physical population, gap-spanning or native-law claim.')
    write(output,result);return passed

def main():
    ap=argparse.ArgumentParser();ap.add_argument('controller_launch');args=ap.parse_args()
    runtime=B/'production_runtime';analysis=B/'production_analysis';manifest_path=runtime/'campaign.json';dispatch=read(B/'POSTPROCESS_DISPATCH.json')
    verify_sources(dispatch);manifest=read(manifest_path);manifest['_sha256']=sha(manifest_path)
    if manifest['_sha256']!=dispatch['manifest_sha256'] or manifest['wall_seconds'] is not None:raise ValueError('POSTPROCESS_MANIFEST_BINDING')
    launch_path=Path(args.controller_launch).resolve()
    if launch_path.parent!=runtime.resolve():raise ValueError('CONTROLLER_PATH_SCOPE')
    launch=read(launch_path);receipt_path=Path(launch['result_receipt']).resolve()
    if receipt_path.parent!=runtime.resolve() or launch['manifest_sha256']!=manifest['_sha256']:raise ValueError('CONTROLLER_BINDING')
    directory=analysis/'postprocess';directory.mkdir(exist_ok=False);results=[];requested={'signal':None};active={'process':None}
    def stop(signum,frame):
        requested['signal']=signum;p=active['process']
        if p is not None and p.poll() is None:
            try:os.killpg(p.pid,signum)
            except ProcessLookupError:pass
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    roots=[Path(q) for q in manifest['storage_roots']]+[B/'review/math/cases',B/'review/math/captures']
    def finish(reason,code,**extra):
        record=dict(status='CANDIDATE_PENDING_ADVERSARIAL_REVIEW',phase=reason,manifest_sha256=manifest['_sha256'],controller_launch_sha256=sha(launch_path),manual_signal=requested['signal'],stages=results,used_bytes=bytes_used(roots),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**extra)
        write(directory/'POSTPROCESS_RESULT.json',record);print(json.dumps(record),flush=True);return code
    try:
        with (directory/'companion.lock').open('a+') as lock:
            fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            print(json.dumps(dict(status='WAITING_FOR_CONTROLLER',pid=launch['pid'],wall_timeout_seconds=None)),flush=True)
            while process_alive(launch):
                if requested['signal']:return finish('MANUAL_PAUSE',75)
                time.sleep(5)
            if requested['signal']:return finish('MANUAL_PAUSE',75)
            if not receipt_path.exists():return finish('CONTROLLER_RECEIPT_MISSING',2)
            controller=read(receipt_path)
            if controller['returncode']!=0:return finish('CONTROLLER_STOPPED_OR_DIAGNOSTIC',75 if controller['returncode']==75 else 2,controller_returncode=controller['returncode'])
            if controller['wall_timeout_seconds'] is not None or controller['cpu_timeout_seconds'] is not None:raise ValueError('CONTROLLER_TIME_LIMIT')
            for stream in ['stdout','stderr']:
                if sha(runtime/(receipt_path.stem+'.'+stream))!=controller[stream+'_sha256']:raise ValueError('CONTROLLER_STREAM_BINDING')
            attempts=successful_queue(manifest,runtime);write(directory/'QUEUE_COMPLETION.json',dict(status='EXECUTION_COMPLETE_PENDING_SCIENTIFIC_CHECKS',attempts=attempts))
            commands=[
                ('assembly',[sys.executable,str(B/'assemble_campaign.py'),str(manifest_path),str(runtime)]),
                ('case_checks',[sys.executable,str(B/'review/math/run_case_checks.py')]),
                ('math_aggregate',[sys.executable,str(B/'review/math/check_survey.py'),'aggregate','--output',str(directory/'MATH_CANDIDATE.json')]),
                ('producer_clocks',[sys.executable,str(B/'clock_batch.py')]),
                ('independent_clocks',[sys.executable,str(TPP/'review/runtime/check_clock_hamilton.py'),str(B/'review/runtime/SUBSET_CLOCK_QUERIES.json')]),
            ]
            for name,command in commands:
                if requested['signal']:return finish('MANUAL_PAUSE',75)
                verify_sources(dispatch)
                if bytes_used(roots)+512*1024**2>manifest['output_bytes']:return finish('OUTPUT_RESERVE_STOP',2)
                prefix=directory/name;call=[sys.executable,str(B/'capture.py'),str(prefix),*command]
                with (directory/(name+'.controller.stdout')).open('x') as out,(directory/(name+'.controller.stderr')).open('x') as err:
                    active['process']=subprocess.Popen(call,stdout=out,stderr=err,start_new_session=True)
                    code=active['process'].wait();active['process']=None
                stage=dict(name=name,command=call,returncode=code,receipt=str(prefix)+'.json');results.append(stage)
                print(json.dumps(dict(status='STAGE_RETURNED',**stage)),flush=True)
                if code:return finish('MANUAL_PAUSE' if requested['signal'] else 'CHECK_STOPPED_OR_DIAGNOSTIC',75 if requested['signal'] else 2)
                if bytes_used(roots)>manifest['output_bytes']:return finish('OUTPUT_LIMIT',2)
            if requested['signal']:return finish('MANUAL_PAUSE',75)
            verify_sources(dispatch)
            if not compare_clocks(manifest,analysis,directory/'independent_clocks.stdout',directory/'CLOCK_CANDIDATE.json'):return finish('CLOCK_COMPARISON_DIAGNOSTIC',2)
            if requested['signal']:return finish('MANUAL_PAUSE',75)
            return finish('FINITE_CHECK_PIPELINE_COMPLETE',0,note='Machine checks complete. No adversarial review, central integration, scientific promotion or banking is performed by this companion. Fixed checker reviewer_context fields identify method authorship, not a live review of these automatic outputs.')
    except Exception as exc:return finish('UNRESOLVED_ERROR',2,error_type=type(exc).__name__,error=str(exc))
if __name__=='__main__':raise SystemExit(main())
