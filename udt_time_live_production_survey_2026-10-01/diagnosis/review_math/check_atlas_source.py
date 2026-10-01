"""Pre-output synthetic joins/labels controls; does not build the real atlas."""
import copy,hashlib,importlib.util,json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];B=ROOT/'udt_time_live_production_survey_2026-10-01';D=B/'diagnosis';HERE=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
source=D/'build_atlas.py';s=importlib.util.spec_from_file_location('atlas_under_review',source);atlas=importlib.util.module_from_spec(s);s.loader.exec_module(atlas)
original=read(B/'production_analysis/postprocess/MATH_CANDIDATE.json');mapping=read(D/'REPAIR_CASES.json');grid=read(B/'production_runtime/case_grid.json');dispatch=read(B/'CLOCK_DISPATCH.json');subset=read(B/'review/runtime/SUBSET_CLOCK_QUERIES.json')
fixture={};records={};digest='mock-bound-by-fixture-not-a-real-artifact-sha'
def fixture_put(path,value):fixture[str(path)]=value
def rays(values):
    return [dict(te=dispatch['query_times'][0],to=dispatch['query_times'][1],emitter_position=dispatch['origin'].copy(),initial_coordinate_direction=[x/math.sqrt(sum(y*y for y in direction)) for x in direction],logZ=value,Z=math.exp(value)) for value,direction in zip(values,dispatch['directions'])]
for j,item in enumerate(original['datasets']):
    base=[.001+j*1e-8,-.002+j*1e-8,.003+j*1e-8,-.004+j*1e-8]
    for suffix,delta in [('_n24',0),('_n24_half',1e-9),('_n32',-2e-9)]:
        name=item['dataset']+suffix;records[name]=dict(readouts=rays([v+delta for v in base]))
        fixture_put(B/'production_analysis'/name/'clock.json',records[name])
for item in mapping['datasets']:
    base=[r['logZ'] for r in records[item['base_case']]['readouts']]
    for key,delta in [('quarter_case',.25e-9),('fine32_case',-.5e-9)]:
        name=item[key];records[name]=dict(readouts=rays([v+delta for v in base]));fixture_put(D/'refined_clock_completion'/name/'clock.json',records[name])
def comparison(a,b):
    delta=max(abs(x['logZ']-y['logZ']) for x,y in zip(records[a]['readouts'],records[b]['readouts']))
    return dict(reference=a,other=b,max_logZ_difference=delta,diagnostic='PASS')
clocks=dict(cases=234,independent_cases=30,source_sha256={str((B/'production_analysis'/name/'clock.json').relative_to(ROOT)):digest for name in records if name.endswith(('_n24','_n24_half','_n32'))},matched=[comparison(r['dataset']+'_n24',r['dataset']+suffix) for r in original['datasets'] for suffix in ['_n24_half','_n32']],independent_comparisons=[dict(case=r['name'],max_logZ_difference=1e-12,max_endpoint_difference=2e-12) for r in subset['cases']])
repaired=dict(selected_cases=26,datasets=[dict(**mp,repaired_status='DIAGNOSTIC_NOT_QUALIFIED' if j==0 else 'PASS') for j,mp in enumerate(mapping['datasets'])])
newclocks=dict(datasets=[dict(dataset=mp['dataset'],matched=[comparison(mp['base_case'],mp[k]) for k in ['quarter_case','fine32_case']]) for mp in mapping['datasets']],refined_output_sha256={mp[k]:digest for mp in mapping['datasets'] for k in ['quarter_case','fine32_case']},original_anchor_sha256={mp['base_case']:digest for mp in mapping['datasets']})
paths=[B/'production_analysis/postprocess/MATH_CANDIDATE.json',D/'clock_completion/CLOCK_CANDIDATE.json',D/'review_math/REPAIR_MATH.json',D/'refined_clock_completion/REFINED_CLOCK_CANDIDATE.json',B/'production_runtime/case_grid.json',D/'REPAIR_CASES.json',B/'CLOCK_DISPATCH.json',B/'launch_evidence/case_grid.json',B/'review/runtime/SUBSET_CLOCK_QUERIES.json']
for p,value in zip(paths,[original,clocks,repaired,newclocks,grid,mapping,dispatch,grid,subset]):fixture_put(p,value)
baseline=copy.deepcopy(fixture)
atlas.sha=lambda p:digest
atlas.read=lambda p:copy.deepcopy(fixture[str(Path(p))])
rows,bindings,stats=atlas.build_rows()
assert len(rows)==364 and stats['original']['datasets']==78 and stats['refined']['datasets']==13
assert stats['original']['qualified_datasets']==65 and stats['refined']['qualified_datasets']==12
for edition,count in [('original',78),('refined',13)]:
    assert stats[edition]['directions']['x']['signs']['redshift']==count
    assert stats[edition]['directions']['y']['signs']['blueshift']==count
for row in rows:
    ai=int(row['dataset'].split('_a')[1][0]);assert row['amplitude_multiplier']==grid['amplitudes'][ai]
    assert row['clock_comparison']=='PASS'
    if row['edition']=='refined':assert row['original_field_status']=='DIAGNOSTIC_NOT_QUALIFIED'
assert all(r['field_status_this_edition']=='DIAGNOSTIC_NOT_QUALIFIED' for r in rows if r['edition']=='refined' and r['dataset']==mapping['datasets'][0]['dataset'])
controls=[]
def reject(label,mutate,expected):
    global fixture
    fixture=copy.deepcopy(baseline);mutate(fixture)
    try:atlas.build_rows()
    except ValueError as e:
        assert str(e)==expected,(label,str(e),expected);controls.append(dict(defect=label,rejection=str(e)))
    else:raise AssertionError('FALSE_PASS: '+label)
def permutation(data):
    for suffix in ['_n24','_n24_half','_n32']:
        rr=data[str(B/'production_analysis'/('axial_a0'+suffix)/'clock.json')]['readouts'];rr[0],rr[1]=rr[1],rr[0]
reject('consistent_xyz_permutation_inside_complete_triple',permutation,'FIXED_QUERY_LABEL')
reject('missing_original_pair',lambda x:x[str(paths[1])]['matched'].pop(),'EXACT_CLOCK_PAIR_COVERAGE')
reject('missing_refined_pair',lambda x:x[str(paths[3])]['datasets'][0]['matched'].pop(),'EXACT_CLOCK_PAIR_COVERAGE')
def duplicate_subset(data):data[str(paths[1])]['independent_comparisons'][1]=copy.deepcopy(data[str(paths[1])]['independent_comparisons'][0])
reject('duplicate_independent_case_with_count30',duplicate_subset,'EXACT_INDEPENDENT_SUBSET')
def movedorigin(data):
    for suffix in ['_n24','_n24_half','_n32']:
        for ray in data[str(B/'production_analysis'/('axial_a0'+suffix)/'clock.json')]['readouts']:ray['emitter_position']=[0,0,0]
reject('same_wrong_origin_in_complete_triple',movedorigin,'FIXED_QUERY_LABEL')
result=dict(status='ATLAS_SOURCE_CLEARED_WITH_ACTUAL_OUTPUT_REVIEW_PENDING',reviewer_context='/root/survey_completion_math',builder_sha256=sha(source),plan_sha256=sha(D/'ATLAS_PLAN.md'),checker_sha256=sha(__file__),source_repair_history_sha256=sha(D/'ATLAS_REVIEW_REPAIR.md'),synthetic_rows=len(rows),synthetic_qualifications=dict(original=65,refined=12),defect_controls=controls,scope='Pre-output synthetic joins, fixed-query direction labels, amplitude mapping, signs and field/clock separation. Hash function deliberately mocked in fixture; real artifact authentication is not claimed by synthetic tests.',source_review='Original78 and refined13 explicit triples retained. Original65/13grades remain fixed. Amplitude/phase/polarization parse matches supplied grid and construction source. Maximum resolution change means baseline-relative comparisons, not all pairwise spread or certified/statistical error. No fit, new query, sign selection or physical population inference. Larger outer rings and qualification caption address original-flag visibility.',omissions='Actual364CSV rows, statistics, raw-clock consistency, bindings and finalPNG/PDF visual review remain required after outputs exist. No actual atlas or geodesic was executed here.')
with (HERE/'ATLAS_SOURCE_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(status=result['status'],synthetic_rows=len(rows),rejected_defects=len(controls))))
