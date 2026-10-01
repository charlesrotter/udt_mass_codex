"""Actual original 234-clock capture/source/qualification review, no ray rerun."""
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
 freeze_path=HERE/'CLOCK_COMPLETION_FREEZE.json';freeze=read(freeze_path)
 for path,value in freeze['source_sha256'].items():assert sha(ROOT/path)==value,path
 review_path=HERE/'CLOCK_COMPLETION_REVIEW.json';review=read(review_path)
 assert review['freeze_sha256']==sha(freeze_path)
 assert all(review[k]=='CLEARED' for k in ['parent_source_review','math_source_review','scientific_diagnostic_readouts'])
 for p,h in review['references'].items():assert sha(ROOT/p)==h
 directory=B/'diagnosis/clock_completion';result=read(directory/'COMPLETION_RESULT.json')
 assert result['status']=='CLOCK_CHARACTERIZATION_COMPLETE_PENDING_REVIEW' and result['clock_machine_diagnostic']=='PASS' and result['manual_signal'] is None
 assert result['freeze_sha256']==sha(freeze_path) and result['review_sha256']==sha(review_path)
 assert [r['name'] for r in result['stages']]==['producer_clocks','independent_clocks']
 captures=[]
 for stage in result['stages']:
  prefix=directory/stage['name'];receipt=read(prefix.with_suffix('.json'))
  assert stage['returncode']==receipt['returncode']==0 and stage['command'][3:]==receipt['command']
  assert receipt['wall_timeout_seconds'] is None and receipt['cpu_timeout_seconds'] is None and receipt['address_space_bytes']==2*1024**3 and receipt['forwarded_signals']==[]
  assert receipt['capture_sha256']==sha(B/'capture.py')
  for stream in ['stdout','stderr']:assert sha(prefix.with_suffix('.'+stream))==receipt[stream+'_sha256']
  captures.append(dict(stage=stage['name'],receipt_sha256=sha(prefix.with_suffix('.json')),seconds=receipt['duration_seconds'],maxrss_kib=receipt['maxrss_kib']))
 manifest=read(B/'production_runtime/campaign.json')
 spec=importlib.util.spec_from_file_location('reviewed_clock_adapter',HERE/'clock_completion.py');adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
 adapter.authenticated_producer_receipts(manifest)
 candidate=read(directory/'CLOCK_CANDIDATE.json');qualifications=read(directory/'ORIGINAL_FIELD_QUALIFICATIONS.json');original_path=B/'production_analysis/postprocess/MATH_CANDIDATE.json';original=read(original_path)
 assert candidate['cases']==234 and candidate['independent_cases']==30 and candidate['machine_diagnostic']=='PASS'
 assert qualifications['original_aggregate_sha256']==sha(original_path) and qualifications['clock_candidate_sha256']==sha(directory/'CLOCK_CANDIDATE.json')
 assert len(qualifications['datasets'])==78 and [r['original_numerical_gate'] for r in qualifications['datasets']]==original['datasets']
 qualified=[r for r in qualifications['datasets'] if r['original_field_qualification']=='PASS'];unqualified=[r for r in qualifications['datasets'] if r['original_field_qualification']=='UNQUALIFIED']
 assert len(qualified)==65 and len(unqualified)==13
 for index,row in enumerate(qualifications['datasets']):
  assert row['cases']==[r['id'] for r in manifest['cases'][index*3:index*3+3]]
  assert row['original_field_qualification']==('PASS' if row['original_numerical_gate']['status']=='PASS' else 'UNQUALIFIED')
 producer_hashes={};producer_captures={};nulls=[];readouts=0
 for row in manifest['cases']:
  casepath=B/'production_analysis'/row['id']/'clock.json';case=read(casepath);capturepath=casepath.parent/'clock_capture.json';receipt=read(capturepath)
  assert candidate['source_sha256'][str(casepath.relative_to(ROOT))]==sha(casepath)
  assert len(case['readouts'])==4 and receipt['forwarded_signals']==[] and receipt['capture_sha256']==sha(B/'capture.py')
  for ray in case['readouts']:
   assert math.isfinite(ray['logZ']) and ray['Z']>0 and ray['max_sampled_abs_null_norm']<2e-7
   nulls.append(ray['max_sampled_abs_null_norm']);readouts+=1
  producer_hashes[row['id']]=sha(casepath);producer_captures[row['id']]=sha(capturepath)
 independent_path=directory/'independent_clocks.stdout';independent=read(independent_path);queries_path=B/'review/runtime/SUBSET_CLOCK_QUERIES.json';queries=read(queries_path);subset=read(B/'review/runtime/CLOCK_SUBSET_FREEZE.json')
 expected={r['name'] for r in queries['cases']};assert len(expected)==subset['selected_dataset_count']==30
 assert set(independent['readouts'])==expected and {r['case'] for r in candidate['independent_comparisons']}==expected
 assert independent['status']=='HAMILTON_CLOCK_REVIEW_PASS' and independent['queries_sha256']==sha(queries_path)
 assert independent['checker_sha256']==sha(ROOT/'udt_time_live_production_preparation_2026-10-01/review/runtime/check_clock_hamilton.py')
 assert candidate['independent_output_sha256']==sha(independent_path)
 for row in queries['cases']:
  producer=read(B/'production_analysis'/row['name']/'clock.json')
  assert independent['history_sha256'][row['history']]==producer['history_sha256']
  assert len(independent['readouts'][row['name']])==4
 assert len(candidate['matched'])==156 and all(r['diagnostic']=='PASS' for r in candidate['matched']+candidate['independent_comparisons'])
 output=dict(status='ACTUAL_ORIGINAL_CLOCK_OPERATIONAL_REVIEW_PASS',reviewer_context='/root/survey_completion_runtime',checker_sha256=sha(__file__),source_freeze_sha256=sha(freeze_path),completion_result_sha256=sha(directory/'COMPLETION_RESULT.json'),candidate_sha256=sha(directory/'CLOCK_CANDIDATE.json'),qualification_sha256=sha(directory/'ORIGINAL_FIELD_QUALIFICATIONS.json'),producer_cases=234,producer_rays=readouts,independent_cases=30,independent_rays=120,original_fields_pass=65,original_fields_unqualified=13,max_producer_sampled_null=max(nulls),max_matched_logZ_difference=max(r['max_logZ_difference'] for r in candidate['matched']),max_independent_logZ_difference=max(r['max_logZ_difference'] for r in candidate['independent_comparisons']),captures=captures,producer_output_sha256=producer_hashes,producer_capture_sha256=producer_captures,scope='Fresh runtime-context actual artifact audit. Reuses reviewed authentication helper; no new geodesic or original-equation recomputation. Parent/math own full scalar and reviewed-field joins. All original13field failures remain explicit despite clock agreement.',independence='Fresh context, same inherited model. Hamilton/RK45 implementation separate from producer Christoffel/DOP853; saved fields and Fourier/Hermite mathematics shared. No independent general-data time integrator, physical population, sign selection, or continuum claim.')
 with (HERE/'ACTUAL_ORIGINAL_CLOCK_REVIEW.json').open('x') as f:json.dump(output,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in output.items() if k not in ['producer_output_sha256','producer_capture_sha256']},indent=2))
if __name__=='__main__':main()
