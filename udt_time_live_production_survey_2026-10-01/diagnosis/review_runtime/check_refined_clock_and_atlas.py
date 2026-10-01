"""Actual refined-clock capture/provenance and atlas packaging review."""
import collections, csv, hashlib, json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];D=B/'diagnosis';ROOT=B.parent
def read(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def capture(prefix):
 receipt=read(prefix.with_suffix('.json'))
 assert receipt['returncode']==0 and receipt['wall_timeout_seconds'] is None and receipt['cpu_timeout_seconds'] is None
 assert receipt['address_space_bytes']==2*1024**3 and receipt['forwarded_signals']==[] and receipt['capture_sha256']==sha(B/'capture.py')
 for stream in ['stdout','stderr']:assert sha(prefix.with_suffix('.'+stream))==receipt[stream+'_sha256']
 return receipt
def main():
 fp=HERE/'REFINED_CLOCK_FREEZE.json';freeze=read(fp);review_path=HERE/'REFINED_CLOCK_REVIEW.json';review=read(review_path)
 assert review['freeze_sha256']==sha(fp)
 for group in [freeze['source_sha256'],review['field_evidence_sha256'],review['source_review_sha256']]:
  for p,h in group.items():assert sha(ROOT/p)==h,p
 assert all(review[k]=='CLEARED' for k in ['parent_source_review','math_source_review','field_diagnostic_readouts'])
 clock_capture=capture(D/'checks/refined_clocks');atlas_capture=capture(D/'checks/build_atlas')
 assert (ROOT/clock_capture['command'][1]).resolve()==HERE/'refined_clock_completion.py'
 assert (ROOT/atlas_capture['command'][1]).resolve()==D/'build_atlas.py'
 directory=D/'refined_clock_completion';result=read(directory/'COMPLETION_RESULT.json');candidate=read(directory/'REFINED_CLOCK_CANDIDATE.json')
 assert read(D/'checks/refined_clocks.stdout')==result
 assert result['status']=='REFINED_CLOCK_CHARACTERIZATION_COMPLETE_PENDING_REVIEW' and result['machine_diagnostic']=='PASS' and result['manual_signal'] is None
 assert result['freeze_sha256']==sha(fp) and result['review_sha256']==sha(review_path)
 manifest_path=D/'repair_runtime/campaign.json';manifest=read(manifest_path);mh=sha(manifest_path);mapping=read(D/'REPAIR_CASES.json');math_result=read(D/'review_math/REPAIR_MATH.json')
 assert len(result['stages'])==26 and [r['case'] for r in result['stages']]==[r['id'] for r in manifest['cases']]
 assert math_result['selected_cases']==26 and math_result['original_equations_pass'] is True
 assert len(candidate['datasets'])==13 and len(candidate['refined_output_sha256'])==26 and len(candidate['all_supplied_signs'])==39
 records={};hashes={};nulls=[];raw_bytes=0;maxrss=0
 dispatch=read(B/'CLOCK_DISPATCH.json')
 for row,stage in zip(manifest['cases'],result['stages'],strict=True):
  name=row['id'];output=directory/name/'clock.json';value=read(output);receipt=capture(directory/name/'capture');maxrss=max(maxrss,receipt['maxrss_kib'])
  assert stage['returncode']==0 and stage['command']==receipt['command'] and read(directory/name/'capture.stdout')==value
  history=D/'repair_analysis'/name/'histories'/(name+'_window2.npz');history_hash=sha(history);raw_bytes+=history.stat().st_size
  expected=[str(ROOT/'udt_time_live_production_preparation_2026-10-01/clock_checks.py'),str(history),str(output)]
  assert receipt['command'][1:]==expected and value['history_sha256']==history_hash and value['status']=='FINITE_CLOCK_CHECK_PASS'
  report_path=D/'review_math/repair_cases'/(name+'.json');field=read(report_path)
  assert sha(report_path)==math_result['case_report_sha256'][str(report_path.relative_to(ROOT))]
  assert field['case']==name and field['status']=='PASS' and field['manifest_sha256']==mh
  binding=field['windows'][2]['binding'];assembly=D/'repair_analysis'/name/'ASSEMBLY.json'
  assert (ROOT/binding['path']).resolve()==history and binding['sha256']==history_hash and binding['assembly_sha256']==sha(assembly)==candidate['refined_assembly_sha256'][name]
  assert len(value['readouts'])==4
  for ray,vec in zip(value['readouts'],dispatch['directions'],strict=True):
   norm=math.sqrt(sum(x*x for x in vec))
   assert ray['initial_coordinate_direction']==[x/norm for x in vec] and ray['emitter_position']==dispatch['origin'] and [ray['te'],ray['to']]==dispatch['query_times']
   assert all(math.isfinite(ray[k]) for k in ['Z','logZ','max_sampled_abs_null_norm']) and ray['Z']>0 and ray['max_sampled_abs_null_norm']<2e-7
   nulls.append(ray['max_sampled_abs_null_norm'])
  records[name]=value;hashes[name]=sha(output);assert hashes[name]==candidate['refined_output_sha256'][name]
 for name,h in candidate['original_anchor_sha256'].items():
  path=B/'production_analysis'/name/'clock.json';assert sha(path)==h;records[name]=read(path)
 assert set(records)==set(candidate['all_supplied_signs'])
 for name,value in records.items():
  expected=[dict(Z=x['Z'],logZ=x['logZ'],sign='positive' if x['logZ']>0 else 'negative' if x['logZ']<0 else 'zero') for x in value['readouts']]
  assert candidate['all_supplied_signs'][name]==expected
 for row in candidate['datasets']:
  assert row['original_field_qualification']=='UNQUALIFIED' and row['repaired_field_qualification']=='NOT_DETERMINED_BY_CLOCK_COMPARISON'
  assert row['field_evidence_sha256']==review['field_evidence_sha256']
  for pair in row['matched']:
   delta=max(abs(x['logZ']-y['logZ']) for x,y in zip(records[pair['reference']]['readouts'],records[pair['other']]['readouts'],strict=True))
   assert delta==pair['max_logZ_difference'] and pair['diagnostic']==('PASS' if delta<2e-7 else 'FAIL')
 atlas_path=D/'atlas/ATLAS.json';atlas=read(atlas_path)
 for p,h in atlas['source_sha256'].items():assert sha(ROOT/p)==h,p
 for name,h in atlas['artifacts_sha256'].items():assert sha(D/'atlas'/name)==h,name
 assert read(D/'checks/build_atlas.stdout')=={'status':atlas['status'],'statistics':atlas['statistics']}
 with (D/'atlas/clock_atlas.csv').open(newline='') as f:rows=list(csv.DictReader(f))
 assert len(rows)==atlas['rows']==364
 counts=collections.Counter(r['edition'] for r in rows);assert counts=={'original':312,'refined':52}
 assert len({(r['edition'],r['dataset'],r['direction']) for r in rows})==364
 old={r['dataset']:r for r in read(B/'production_analysis/postprocess/MATH_CANDIDATE.json')['datasets']};new={r['dataset']:r for r in math_result['datasets']}
 for row in rows:
  assert row['original_field_status']==old[row['dataset']]['status']
  status=old[row['dataset']]['status'] if row['edition']=='original' else new[row['dataset']]['repaired_status']
  assert row['field_status_this_edition']==status and row['clock_comparison']=='PASS'
 assert sum(r['edition']=='original' and r['field_status_this_edition']!='PASS' for r in rows)==52
 assert sum(r['edition']=='refined' and r['field_status_this_edition']=='PASS' for r in rows)==52
 summary=dict(status='ACTUAL_REFINED_CLOCK_AND_ATLAS_OPERATIONAL_REVIEW_PASS',reviewer_context='/root/survey_completion_runtime',checker_sha256=sha(__file__),refined_freeze_sha256=sha(fp),refined_candidate_sha256=sha(directory/'REFINED_CLOCK_CANDIDATE.json'),atlas_sha256=sha(atlas_path),atlas_builder_sha256=sha(D/'build_atlas.py'),refined_cases=26,refined_rays=104,old_anchors=13,actual_late_payload_bytes_hashed=raw_bytes,max_refined_sampled_null=max(nulls),max_refined_pair_logZ_difference=max(p['max_logZ_difference'] for r in candidate['datasets'] for p in r['matched']),clock_stage_seconds=clock_capture['duration_seconds'],clock_stage_maxrss_kib=clock_capture['maxrss_kib'],max_case_clock_rss_kib=maxrss,atlas_seconds=atlas_capture['duration_seconds'],atlas_maxrss_kib=atlas_capture['maxrss_kib'],atlas_rows=364,original_rows=312,refined_rows=52,original_unqualified_rows_retained=52,refined_field_pass_rows=52,refined_output_sha256=hashes,scope='Actual captures, hashes, fixed coverage, qualification joins and matched scalar differences checked. Mathematical reviewer separately owns complete scalar/table/visual assessment. No new ray or field solve; all original13 failures remain visible and repaired qualification comes from field evidence, not clock agreement.',independence='Runtime reviewer authored the adapters; parent separately reviewed their source. Actual receipt/report checks are independent of parent execution, not a new independent clock method or general-data evolution. Same inherited model; fields and interpolation mathematics shared.',visual_status='PNG/PDF hashes authenticated; visual inspection is separate from this script.')
 with (HERE/'ACTUAL_REFINED_CLOCK_AND_ATLAS_REVIEW.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='refined_output_sha256'},indent=2))
if __name__=='__main__':main()
