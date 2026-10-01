"""Actual refined clock input/scalar/qualification review without ray reruns."""
import json,math,sys,time
from pathlib import Path
from review_original_clock_results import ROOT,B,D,HERE,read,sha,captured,sign

def main():
    started=time.monotonic();out=D/'refined_clock_completion';candidate_path=out/'REFINED_CLOCK_CANDIDATE.json';candidate=read(candidate_path);completion=read(out/'COMPLETION_RESULT.json')
    capture_hash=captured(D/'checks/refined_clocks',['python3','udt_time_live_production_survey_2026-10-01/diagnosis/review_runtime/refined_clock_completion.py'])
    freeze_path=D/'review_runtime/REFINED_CLOCK_FREEZE.json';review_path=D/'review_runtime/REFINED_CLOCK_REVIEW.json';freeze=read(freeze_path);review=read(review_path)
    assert completion['freeze_sha256']==review['freeze_sha256']==sha(freeze_path) and completion['review_sha256']==sha(review_path)
    for p,h in freeze['source_sha256'].items():assert sha(ROOT/p)==h
    for p,h in review['field_evidence_sha256'].items():assert sha(ROOT/p)==h
    fields_path=HERE/'REPAIR_MATH.json';fields=read(fields_path);mapping=read(D/'REPAIR_CASES.json');original=read(B/'production_analysis/postprocess/MATH_CANDIDATE.json');old={r['dataset']:r for r in original['datasets']}
    assert completion['cases']==26 and completion['datasets']==13 and len(completion['stages'])==26 and all(r['returncode']==0 for r in completion['stages'])
    assert fields['selected_cases']==26 and fields['original_equations_pass'] is True
    records={};bindings=[];counts={'positive':0,'negative':0,'zero':0};new_counts=dict(counts);nullmax=0.;dispatch=read(B/'CLOCK_DISPATCH.json')
    for mp in mapping['datasets']:
        for key in ['base_case','quarter_case','fine32_case']:
            name=mp[key];base=key=='base_case'
            report_path=(B/'review/math/cases' if base else HERE/'repair_cases')/(name+'.json');expected=original['result_sha256'][str(report_path)] if base else fields['case_report_sha256'][str(report_path.relative_to(ROOT))]
            assert sha(report_path)==expected;report=read(report_path);assert report['case']==name and report['status']=='PASS';binding=report['windows'][2]['binding']
            analysis=(B/'production_analysis' if base else D/'repair_analysis')/name;history=analysis/'histories'/(name+'_window2.npz');assembly=analysis/'ASSEMBLY.json'
            assert sha(history)==binding['sha256'] and sha(assembly)==binding['assembly_sha256'] and (ROOT/binding['path']).resolve()==history
            path=(B/'production_analysis'/name if base else out/name)/'clock.json';value=read(path)
            assert sha(path)==(candidate['original_anchor_sha256'][name] if base else candidate['refined_output_sha256'][name])
            assert value['status']=='FINITE_CLOCK_CHECK_PASS' and value['history_sha256']==binding['sha256'] and len(value['readouts'])==4
            if not base:
                prefix=out/name/'capture';captured(prefix,[sys.executable,str(ROOT/'udt_time_live_production_preparation_2026-10-01/clock_checks.py'),str(history),str(path)])
                assert value==read(prefix.with_suffix('.stdout')) and candidate['refined_assembly_sha256'][name]==sha(assembly)
            for ray,vector in zip(value['readouts'],dispatch['directions'],strict=True):
                expected_direction=[x/math.sqrt(sum(y*y for y in vector)) for x in vector]
                assert ray['initial_coordinate_direction']==expected_direction and ray['emitter_position']==dispatch['origin'] and [ray['te'],ray['to']]==dispatch['query_times']
                assert ray['Z']>0 and all(math.isfinite(ray[k]) for k in ['Z','logZ','max_sampled_abs_null_norm']) and abs(math.log(ray['Z'])-ray['logZ'])<5e-15 and ray['max_sampled_abs_null_norm']<2e-7
                assert all(math.isfinite(x) for x in ray['receiver_position'])
                counts[sign(ray['logZ'])]+=1
                if not base:new_counts[sign(ray['logZ'])]+=1
                nullmax=max(nullmax,ray['max_sampled_abs_null_norm'])
            assert candidate['all_supplied_signs'][name]==[dict(Z=r['Z'],logZ=r['logZ'],sign=sign(r['logZ'])) for r in value['readouts']]
            records[name]=value;bindings.append(dict(case=name,reviewed_field_report_sha256=expected,history_sha256=binding['sha256'],assembly_sha256=sha(assembly),clock_sha256=sha(path)))
    assert len(records)==39 and len(candidate['all_supplied_signs'])==39 and len(candidate['refined_output_sha256'])==26
    rows=[]
    for mp,record in zip(mapping['datasets'],candidate['datasets'],strict=True):
        assert record['dataset']==mp['dataset'] and record['original_field_qualification']=='UNQUALIFIED' and record['original_numerical_gate']==old[mp['dataset']]
        assert record['repaired_field_qualification']=='NOT_DETERMINED_BY_CLOCK_COMPARISON' and record['field_evidence_sha256']==review['field_evidence_sha256']
        assert old[mp['dataset']]['status']=='DIAGNOSTIC_NOT_QUALIFIED'
        for other,reported in zip([mp['quarter_case'],mp['fine32_case']],record['matched'],strict=True):
            value=max(abs(a['logZ']-b['logZ']) for a,b in zip(records[mp['base_case']]['readouts'],records[other]['readouts'],strict=True))
            expected=dict(reference=mp['base_case'],other=other,max_logZ_difference=value,diagnostic='PASS' if value<2e-7 else 'FAIL');assert expected==reported;rows.append(expected)
    passed=all(r['diagnostic']=='PASS' for r in rows);assert candidate['machine_diagnostic']==completion['machine_diagnostic']==('PASS' if passed else 'FAIL')
    result=dict(status='REFINED_CLOCK_RESULTS_VERIFIED_WITH_CAVEATS',reviewer_context='/root/survey_completion_math',clock_machine_diagnostic=candidate['machine_diagnostic'],candidate_sha256=sha(candidate_path),field_math_sha256=sha(fields_path),capture_sha256=capture_hash,review_script_sha256=sha(__file__),reused_capture_helper_sha256=sha(HERE/'review_original_clock_results.py'),history_count=39,new_histories=26,anchor_histories=13,pair_comparisons=len(rows),all39_sign_counts=counts,new26_sign_counts=new_counts,maximum_temporal_logZ_difference=max(r['max_logZ_difference'] for r in rows if r['other'].endswith('_quarter')),maximum_spatial_logZ_difference=max(r['max_logZ_difference'] for r in rows if r['other'].endswith('_n32_half')),maximum_sampled_null=nullmax,actual_field_and_clock_bindings=bindings,original_unqualified_preserved=13,refined_qualification_owned_by='Separate REPAIR_MATH.json, not these clock comparisons',seconds=time.monotonic()-started,scope='Actual fixed late-window output and input/scalar replay, no geodesic recomputation. Original30Hamiltonian subset remains on original anchors; new26queries are producer readouts, not a new independent clock method. Shared saved fields/Fourier/Hermite mathematics, no population, gap or continuum claim.')
    with (HERE/'REFINED_CLOCK_RESULT_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='actual_field_and_clock_bindings'}))
if __name__=='__main__':main()
