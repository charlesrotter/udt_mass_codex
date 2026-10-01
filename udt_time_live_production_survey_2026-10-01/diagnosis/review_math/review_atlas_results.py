"""Independent actual CSV/statistics replay; figure inspection recorded separately."""
import csv,json,math,re
from pathlib import Path
from review_original_clock_results import ROOT,B,D,HERE,read,sha

out=D/'atlas';report=read(out/'ATLAS.json');original=read(B/'production_analysis/postprocess/MATH_CANDIDATE.json');refined=read(HERE/'REPAIR_MATH.json');grid=read(B/'production_runtime/case_grid.json');dispatch=read(B/'CLOCK_DISPATCH.json')
for p,h in report['source_sha256'].items():assert sha(ROOT/p)==h
for name,h in report['artifacts_sha256'].items():assert sha(out/name)==h
with (out/'clock_atlas.csv').open(newline='') as f:rows=list(csv.DictReader(f))
old={r['dataset']:r for r in original['datasets']};new={r['dataset']:r for r in refined['datasets']};directions=['x','y','z','diagonal'];records={}
assert len(rows)==report['rows']==364
expected={(edition,name,direction) for edition,names in [('original',old),('refined',new)] for name in names for direction in directions}
assert {(r['edition'],r['dataset'],r['direction']) for r in rows}==expected
for row in rows:
    edition,name,direction=row['edition'],row['dataset'],row['direction'];di=directions.index(direction)
    match=re.fullmatch(r'(axial|oblique)_a([0-5])(?:_p([0-3])_r([0-2]))?',name);assert match
    family,ai,pi,ri=match.groups();assert row['family']==family and float(row['amplitude_multiplier'])==grid['amplitudes'][int(ai)]
    assert row['phase_offset']==('' if pi is None else str(grid['fourth_oblique_phase_offsets'][int(pi)]))
    assert row['polarization_degrees']==('' if ri is None else str(grid['polarization_angles_degrees'][int(ri)]))
    suffixes=['_n24','_n24_half','_n32'] if edition=='original' else ['_n24_half','_n24_quarter','_n32_half'];names=[name+s for s in suffixes]
    assert [row[k] for k in ['baseline_case','temporal_case','spatial_case']]==names
    rays=[]
    for case in names:
        if case not in records:
            directory=D/'refined_clock_completion' if case.endswith(('_quarter','_n32_half')) else B/'production_analysis';records[case]=read(directory/case/'clock.json')
        rays.append(records[case]['readouts'][di])
    logs=[r['logZ'] for r in rays]
    assert [float(row[k]) for k in ['baseline_logZ','temporal_logZ','spatial_logZ']]==logs
    delta=max(abs(logs[0]-v) for v in logs[1:]);assert float(row['max_logZ_difference'])==delta and row['clock_comparison']==('PASS' if delta<2e-7 else 'FAIL')
    assert float(row['spatial_Z'])==rays[2]['Z'] and row['original_field_status']==old[name]['status']
    assert row['field_status_this_edition']==(old[name]['status'] if edition=='original' else new[name]['repaired_status'])
    signs=['redshift' if x>0 else 'blueshift' if x<0 else 'zero' for x in logs]
    assert row['spatial_sign']==signs[2] and row['all_three_signs_agree']==str(len(set(signs))==1)
stats={}
for edition in ['original','refined']:
    selected=[r for r in rows if r['edition']==edition]
    stats[edition]=dict(datasets=len(selected)//4,qualified_datasets=len({r['dataset'] for r in selected if r['field_status_this_edition']=='PASS'}),maximum_matched_logZ_difference=max(float(r['max_logZ_difference']) for r in selected),directions={})
    for direction in directions:
        subset=[r for r in selected if r['direction']==direction];values=[float(r['spatial_logZ']) for r in subset]
        stats[edition]['directions'][direction]=dict(min_logZ=min(values),max_logZ=max(values),signs={s:sum(r['spatial_sign']==s for r in subset) for s in ['redshift','blueshift','zero']})
    assert stats[edition]==report['statistics'][edition]
independent=read(D/'clock_completion/CLOCK_CANDIDATE.json')['independent_comparisons']
stats['independent_original_subset']=dict(cases=len(independent),maximum_logZ_difference=max(r['max_logZ_difference'] for r in independent),maximum_endpoint_difference=max(r['max_endpoint_difference'] for r in independent));assert stats['independent_original_subset']==report['statistics']['independent_original_subset']
result=dict(status='ACTUAL_ATLAS_TABLE_AND_STATISTICS_PASS',reviewer_context='/root/survey_completion_math',atlas_sha256=sha(out/'ATLAS.json'),builder_sha256=sha(D/'build_atlas.py'),CSV_sha256=sha(out/'clock_atlas.csv'),review_code_sha256=sha(__file__),actual_rows=len(rows),actual_clock_histories=len(records),statistics=stats,original_unqualified_dataset_count=len({r['dataset'] for r in rows if r['edition']=='original' and r['field_status_this_edition']!='PASS'}),refined_unqualified_dataset_count=len({r['dataset'] for r in rows if r['edition']=='refined' and r['field_status_this_edition']!='PASS'}),scope='Actual364row table independently joined to260original/refined clock reports and exact field grades; all source/artifact hashes checked, every float/sign/amplitude and full statistics recomputed. No ray or field recomputation, no fit, distribution or continuum claim. Figure visual review and common integration attestation remain separate.')
with (HERE/'ATLAS_RESULT_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ['status','actual_rows','actual_clock_histories','original_unqualified_dataset_count','refined_unqualified_dataset_count']}))
