"""Independent scalar/coverage replay from completed saved clock reports."""
import hashlib,json,math,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];B=ROOT/'udt_time_live_production_survey_2026-10-01';D=B/'diagnosis';HERE=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text())
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def captured(prefix,command):
    receipt=read(prefix.with_suffix('.json'))
    assert receipt['command']==command and receipt['returncode']==0
    assert receipt['wall_timeout_seconds'] is None and receipt['cpu_timeout_seconds'] is None and receipt['address_space_bytes']==2*1024**3
    for suffix in ['stdout','stderr']:assert sha(prefix.with_suffix('.'+suffix))==receipt[suffix+'_sha256']
    return sha(prefix.with_suffix('.json'))
def sign(value):return 'positive' if value>0 else 'negative' if value<0 else 'zero'

def main():
    started=time.monotonic();out=D/'clock_completion';manifest=read(B/'production_runtime/campaign.json');original_path=B/'production_analysis/postprocess/MATH_CANDIDATE.json';original=read(original_path);dispatch=read(B/'CLOCK_DISPATCH.json')
    assert sha(original_path)==read(D/'INITIAL_FREEZE.json')['sha256'][str(original_path.relative_to(ROOT))]
    candidate_path=out/'CLOCK_CANDIDATE.json';candidate=read(candidate_path);qual_path=out/'ORIGINAL_FIELD_QUALIFICATIONS.json';qual=read(qual_path)
    inputs=read(HERE/'ORIGINAL_CLOCK_COMPLETE_BINDINGS.json');assert inputs['joined_field_cases']==inputs['available_clock_outputs']==234 and not inputs['pending_clock_outputs']
    fields={r['case']:r for r in inputs['rows']}
    query_path=B/'review/runtime/SUBSET_CLOCK_QUERIES.json';query=read(query_path)
    hamilton_path=out/'independent_clocks.stdout';independent=read(hamilton_path)
    captures=dict(producer=captured(out/'producer_clocks',[sys.executable,str(B/'clock_batch.py')]),independent=captured(out/'independent_clocks',[sys.executable,str(ROOT/'udt_time_live_production_preparation_2026-10-01/review/runtime/check_clock_hamilton.py'),str(query_path)]))
    assert independent['status']=='HAMILTON_CLOCK_REVIEW_PASS' and independent['queries_sha256']==sha(query_path)
    assert independent['checker_sha256']==sha(ROOT/'udt_time_live_production_preparation_2026-10-01/review/runtime/check_clock_hamilton.py')
    assert candidate['independent_output_sha256']==sha(hamilton_path)
    assert candidate['cases']==234 and candidate['independent_cases']==30
    assert qual['original_aggregate_sha256']==sha(original_path) and qual['clock_candidate_sha256']==sha(candidate_path)
    records={};nullmax=0.;counts={'positive':0,'negative':0,'zero':0};case_captures={}
    for case in manifest['cases']:
        name=case['id'];directory=B/'production_analysis'/name;path=directory/'clock.json';history=directory/'histories'/(name+'_window2.npz');value=read(path)
        assert sha(path)==candidate['source_sha256'][str(path.relative_to(ROOT))]==fields[name]['available_clock_sha256']
        assert value['history_sha256']==fields[name]['history_sha256']==sha(history)
        case_captures[name]=captured(directory/'clock_capture',[sys.executable,str(ROOT/'udt_time_live_production_preparation_2026-10-01/clock_checks.py'),str(history),str(path)])
        assert value==read(directory/'clock_capture.stdout') and value['status']=='FINITE_CLOCK_CHECK_PASS' and len(value['readouts'])==4
        for ray,vector in zip(value['readouts'],dispatch['directions'],strict=True):
            expected=[x/math.sqrt(sum(y*y for y in vector)) for x in vector]
            assert ray['initial_coordinate_direction']==expected and ray['emitter_position']==dispatch['origin'] and [ray['te'],ray['to']]==dispatch['query_times']
            assert all(math.isfinite(ray[k]) for k in ['Z','logZ','max_sampled_abs_null_norm']) and all(math.isfinite(x) for x in ray['receiver_position'])
            assert ray['Z']>0 and abs(math.log(ray['Z'])-ray['logZ'])<5e-15 and ray['max_sampled_abs_null_norm']<2e-7
            counts[sign(ray['logZ'])]+=1;nullmax=max(nullmax,ray['max_sampled_abs_null_norm'])
        expected_signs=[dict(logZ=r['logZ'],Z=r['Z'],sign=sign(r['logZ'])) for r in value['readouts']]
        assert candidate['all_supplied_signs'][name]==expected_signs
        records[name]=value
    assert len(records)==len(candidate['source_sha256'])==len(candidate['all_supplied_signs'])==234
    pair_rows=[];qualification_counts={'PASS':0,'UNQUALIFIED':0}
    assert len(qual['datasets'])==78
    for j,dataset in enumerate(original['datasets']):
        name=dataset['dataset'];cases=[name+s for s in ['_n24','_n24_half','_n32']]
        assert cases==[r['id'] for r in manifest['cases'][3*j:3*j+3]]
        expected='PASS' if dataset['status']=='PASS' else 'UNQUALIFIED';qualification_counts[expected]+=1
        q=qual['datasets'][j];assert q['dataset']==name and q['cases']==cases and q['original_field_qualification']==expected and q['original_numerical_gate']==dataset
        own=[]
        for other in cases[1:]:
            delta=max(abs(x['logZ']-y['logZ']) for x,y in zip(records[cases[0]]['readouts'],records[other]['readouts'],strict=True))
            row=dict(reference=cases[0],other=other,max_logZ_difference=delta,diagnostic='PASS' if delta<2e-7 else 'FAIL');pair_rows.append(row);own.append(row)
        assert q['matched_clock_diagnostics']==own
    assert pair_rows==candidate['matched'] and qualification_counts=={'PASS':65,'UNQUALIFIED':13}
    required={r['name'] for r in query['cases']};assert len(required)==30 and set(independent['readouts'])==required
    independent_rows=[];independent_null=0.
    for row in query['cases']:
        name=row['name'];rays=independent['readouts'][name];producer=records[name]['readouts'];assert len(rays)==4 and independent['history_sha256'][row['history']]==records[name]['history_sha256']
        changes=[];positions=[]
        for x,y in zip(rays,producer,strict=True):
            assert x['emission']==y['te'] and x['reception']==y['to'] and x['initial_coordinate_direction']==y['initial_coordinate_direction']
            assert all(math.isfinite(x[k]) for k in ['Z','logZ','max_sampled_abs_null_norm']) and all(math.isfinite(v) for v in x['receiver_position'])
            assert x['Z']>0 and abs(math.log(x['Z'])-x['logZ'])<5e-15 and x['max_sampled_abs_null_norm']<2e-7
            changes.append(abs(x['logZ']-y['logZ']));positions.append(max(abs(a-b) for a,b in zip(x['receiver_position'],y['receiver_position'],strict=True)));independent_null=max(independent_null,x['max_sampled_abs_null_norm'])
        independent_rows.append(dict(case=name,max_logZ_difference=max(changes),max_endpoint_difference=max(positions),diagnostic='PASS' if max(changes)<2e-7 else 'FAIL'))
    assert independent_rows==candidate['independent_comparisons']
    passed=all(r['diagnostic']=='PASS' for r in pair_rows+independent_rows);assert candidate['machine_diagnostic']==('PASS' if passed else 'FAIL')
    result=dict(status='ORIGINAL_CLOCK_RESULT_REPLAY_PASS',clock_machine_diagnostic=candidate['machine_diagnostic'],reviewer_context='/root/survey_completion_math',source_sha256=sha(__file__),candidate_sha256=sha(candidate_path),qualification_table_sha256=sha(qual_path),complete_input_bindings_sha256=sha(HERE/'ORIGINAL_CLOCK_COMPLETE_BINDINGS.json'),capture_sha256=captures,per_case_capture_sha256=case_captures,cases=234,rays=936,matched_pairs=len(pair_rows),independent_cases=len(independent_rows),original_field_qualification_counts=qualification_counts,all_original_ray_sign_counts=counts,maximum_time_logZ_difference=max(r['max_logZ_difference'] for r in pair_rows if r['other'].endswith('_n24_half')),maximum_mesh_logZ_difference=max(r['max_logZ_difference'] for r in pair_rows if r['other'].endswith('_n32')),maximum_independent_logZ_difference=max(r['max_logZ_difference'] for r in independent_rows),maximum_independent_endpoint_difference=max(r['max_endpoint_difference'] for r in independent_rows),maximum_producer_sampled_null=nullmax,maximum_independent_sampled_null=independent_null,seconds=time.monotonic()-started,scope='Independently reconstituted scalar comparisons/signs/qualifications from all completed reports and actual input hashes. No geodesic rerun. Source-independent Hamilton/RK45 and Christoffel/DOP853 outputs share saved fields and Fourier/Hermite interpolation. Original65PASS/13UNQUALIFIED preserved, no physicalpopulation or continuum claims.')
    with (HERE/'ORIGINAL_CLOCK_RESULT_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['per_case_capture_sha256']}))
if __name__=='__main__':main()
