"""Fixed 26 repair-history clocks against the unchanged old N24half anchors.

Only the supplied late-window query is reused. Clock agreement is separate from
field qualification; the frozen original 30-dataset Hamiltonian subset stays on
its original histories and is not replaced by these producer readouts.
"""
import importlib.util
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys

HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ROOT=B.parent
TPP=ROOT/'udt_time_live_production_preparation_2026-10-01'
s=importlib.util.spec_from_file_location('clock_operation_helpers',HERE/'clock_completion.py')
helper=importlib.util.module_from_spec(s);s.loader.exec_module(helper)
read,sha,write=helper.read,helper.sha,helper.write
FREEZE=HERE/'REFINED_CLOCK_FREEZE.json';REVIEW=HERE/'REFINED_CLOCK_REVIEW.json'
OUT=B/'diagnosis/refined_clock_completion'

def validate_readout(value,history):
    dispatch=read(B/'CLOCK_DISPATCH.json')
    if value['status']!='FINITE_CLOCK_CHECK_PASS' or value['history_sha256']!=sha(history) or len(value['readouts'])!=4:
        raise ValueError('REFINED_CLOCK_OUTPUT_BINDING')
    for ray,direction in zip(value['readouts'],dispatch['directions'],strict=True):
        norm=math.sqrt(sum(x*x for x in direction));expected=[x/norm for x in direction]
        if [ray['te'],ray['to']]!=dispatch['query_times'] or ray['emitter_position']!=dispatch['origin'] or ray['initial_coordinate_direction']!=expected:
            raise ValueError('REFINED_CLOCK_QUERY_CHANGED')
        if not all(math.isfinite(ray[k]) for k in ['Z','logZ','max_sampled_abs_null_norm']) or not all(math.isfinite(x) for x in ray['receiver_position']):
            raise ValueError('REFINED_CLOCK_NONFINITE')
        if ray['Z']<=0 or ray['max_sampled_abs_null_norm']>=dispatch['null_threshold']:
            raise ValueError('REFINED_CLOCK_NULL_OR_FREQUENCY')

def main():
    freeze=read(FREEZE);review=read(REVIEW)
    if review.get('freeze_sha256')!=sha(FREEZE) or any(review.get(k)!='CLEARED' for k in ['parent_source_review','math_source_review','field_diagnostic_readouts']):
        raise ValueError('REFINED_CLOCK_REVIEW_REQUIRED')
    if not review.get('field_evidence_sha256'):
        raise ValueError('REFINED_FIELD_EVIDENCE_REQUIRED')
    for path,value in review['field_evidence_sha256'].items():
        if sha(ROOT/path)!=value:raise ValueError('REFINED_FIELD_EVIDENCE_CHANGED')
    helper.guard(freeze)
    manifest_path=B/'diagnosis/repair_runtime/campaign.json';manifest=read(manifest_path);mh=sha(manifest_path)
    mapping=read(B/'diagnosis/REPAIR_CASES.json');original=read(B/'production_analysis/postprocess/MATH_CANDIDATE.json')
    if len(manifest['cases'])!=26 or mapping['repair_manifest_sha256']!=mh or len(mapping['datasets'])!=13:
        raise ValueError('REFINED_CLOCK_COVERAGE')
    original_datasets={row['dataset']:row for row in original['datasets']}
    histories={};records={};field_records={};old_anchor_hashes={}
    for item in mapping['datasets']:
        name=item['base_case'];path=B/'production_analysis'/name/'clock.json'
        history=B/'production_analysis'/name/'histories'/(name+'_window2.npz')
        helper.authenticated_producer_receipts({'cases':[{'id':name}]})
        records[name]=read(path);validate_readout(records[name],history)
        old_anchor_hashes[name]=sha(path)
        if original_datasets[item['dataset']]['status']=='PASS':raise ValueError('EXPECTED_ORIGINAL_UNQUALIFIED_DATASET')
    for row in manifest['cases']:
        name=row['id'];directory=B/'diagnosis/repair_analysis'/name;assembly=read(directory/'ASSEMBLY.json')
        history=directory/'histories'/(name+'_window2.npz')
        if assembly['input_sha256'].get(str(manifest_path))!=mh or assembly['output_sha256'].get(str(history))!=sha(history):
            raise ValueError('REFINED_HISTORY_ASSEMBLY_BINDING')
        histories[name]=history;field_records[name]=sha(directory/'ASSEMBLY.json')
    OUT.mkdir(exist_ok=False)
    stopped={'signal':None};active={'process':None};stages=[]
    def stop(signum,frame):
        stopped['signal']=signum;process=active['process']
        if process is not None and process.poll() is None:
            try:os.killpg(process.pid,signum)
            except ProcessLookupError:pass
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    def finish(status,code,**extra):
        result=dict(status=status,freeze_sha256=sha(FREEZE),review_sha256=sha(REVIEW),manual_signal=stopped['signal'],stages=stages,**extra)
        write(OUT/'COMPLETION_RESULT.json',result);print(json.dumps(result),flush=True);return code
    try:
        for row in manifest['cases']:
            if stopped['signal']:return finish('MANUAL_INTERRUPTION',75)
            helper.guard(freeze);name=row['id'];history=histories[name]
            directory=OUT/name;directory.mkdir();prefix=directory/'capture';output=directory/'clock.json'
            command=[sys.executable,str(TPP/'clock_checks.py'),str(history),str(output)]
            with (directory/'controller.stdout').open('x') as out,(directory/'controller.stderr').open('x') as err:
                active['process']=subprocess.Popen([sys.executable,str(B/'capture.py'),str(prefix),*command],stdout=out,stderr=err,start_new_session=True)
                if stopped['signal']:stop(stopped['signal'],None)
                code=active['process'].wait();active['process']=None
            stages.append(dict(case=name,command=command,returncode=code))
            if code:return finish('MANUAL_INTERRUPTION' if stopped['signal'] else 'REFINED_CLOCK_DIAGNOSTIC_STOP',75 if stopped['signal'] else 2)
            receipt=read(prefix.with_suffix('.json'))
            if receipt['returncode']!=0 or receipt['command']!=command or receipt['wall_timeout_seconds'] is not None or receipt['cpu_timeout_seconds'] is not None or receipt['address_space_bytes']!=2*1024**3:
                raise ValueError('REFINED_CLOCK_CAPTURE')
            for stream in ['stdout','stderr']:
                if sha(prefix.with_suffix('.'+stream))!=receipt[stream+'_sha256']:raise ValueError('REFINED_CLOCK_STREAM')
            value=read(output)
            if value!=read(prefix.with_suffix('.stdout')):raise ValueError('REFINED_CLOCK_CAPTURE_OUTPUT_MISMATCH')
            validate_readout(value,history);records[name]=value;helper.guard(freeze)
        limit=read(B/'CLOCK_DISPATCH.json')['matched_logZ_threshold'];comparisons=[]
        for item in mapping['datasets']:
            base=item['base_case'];matched=[]
            for other in [item['quarter_case'],item['fine32_case']]:
                diffs=[abs(x['logZ']-y['logZ']) for x,y in zip(records[base]['readouts'],records[other]['readouts'],strict=True)]
                matched.append(dict(reference=base,other=other,max_logZ_difference=max(diffs),diagnostic='PASS' if max(diffs)<limit else 'FAIL'))
            comparisons.append(dict(dataset=item['dataset'],original_field_qualification='UNQUALIFIED',original_numerical_gate=original_datasets[item['dataset']],repaired_field_qualification='NOT_DETERMINED_BY_CLOCK_COMPARISON',field_evidence_sha256=review['field_evidence_sha256'],matched=matched))
        passed=all(x['diagnostic']=='PASS' for row in comparisons for x in row['matched'])
        signs={name:[dict(Z=x['Z'],logZ=x['logZ'],sign='positive' if x['logZ']>0 else 'negative' if x['logZ']<0 else 'zero') for x in value['readouts']] for name,value in records.items()}
        write(OUT/'REFINED_CLOCK_CANDIDATE.json',dict(status='DIAGNOSTIC_CHARACTERIZATION_PENDING_ACTUAL_REVIEW',machine_diagnostic='PASS' if passed else 'FAIL',datasets=comparisons,all_supplied_signs=signs,original_anchor_sha256=old_anchor_hashes,refined_assembly_sha256=field_records,refined_output_sha256={row['id']:sha(OUT/row['id']/'clock.json') for row in manifest['cases']},scope='26 refined producer queries compared against unchanged oldN24half anchors. Original30 Hamiltonian subset remains separate on original histories. All original13 field qualification failures retained; clock agreement cannot qualify fields. Same fields/interpolation mathematics, supplied clocks, no selected signs or gap-spanning rays.'))
        if stopped['signal']:return finish('MANUAL_INTERRUPTION',75)
        return finish('REFINED_CLOCK_CHARACTERIZATION_COMPLETE_PENDING_REVIEW' if passed else 'REFINED_CLOCK_COMPARISON_DIAGNOSTIC',0 if passed else 2,cases=26,datasets=13,machine_diagnostic='PASS' if passed else 'FAIL')
    except Exception as error:
        return finish('UNRESOLVED_OPERATIONAL_ERROR',2,error_type=type(error).__name__,error=str(error))

if __name__=='__main__':raise SystemExit(main())
