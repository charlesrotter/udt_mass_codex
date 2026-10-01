"""Operation-only synthetic tests of the 26-readout adapter; no geodesic solves."""
import hashlib, importlib.util, json, math, types
from pathlib import Path
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];ADAPTER=HERE/'refined_clock_completion.py'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
def load():
 s=importlib.util.spec_from_file_location('refined_clock_control',ADAPTER);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def clock_value(history,delta=0):
 directions=[[1,0,0],[0,1,0],[0,0,1],[1,1,1]];rays=[]
 for d in directions:
  norm=math.sqrt(sum(x*x for x in d));rays.append(dict(te=2.484,to=2.496,emitter_position=[.31,.47,.19],receiver_position=[.32,.48,.2],initial_coordinate_direction=[x/norm for x in d],Z=math.exp(delta),logZ=delta,max_sampled_abs_null_norm=1e-12))
 return dict(status='FINITE_CLOCK_CHECK_PASS',history_sha256=sha(history),readouts=rays)
def main():
 base=HERE/'refined_clock_binding_fixtures';base.mkdir(exist_ok=False);checks=[]
 realmanifest=read(B/'diagnosis/repair_runtime/campaign.json');realmap=read(B/'diagnosis/REPAIR_CASES.json');original=read(B/'production_analysis/postprocess/MATH_CANDIDATE.json')
 for mode in ['complete','stage_failure','comparison_failure','null_failure','query_failure','history_binding_failure','joined_history_mutation','old_anchor_join_mutation','incomplete_math_coverage']:
  m=load();fixture=base/mode;fixture.mkdir();m.B=fixture;m.ROOT=fixture;m.OUT=fixture/'output';m.FREEZE=fixture/'freeze.json';m.REVIEW=fixture/'review.json';m.helper.B=fixture;m.helper.ROOT=fixture
  write(fixture/'CLOCK_DISPATCH.json',read(B/'CLOCK_DISPATCH.json'))
  mp=fixture/'diagnosis/repair_runtime/campaign.json';write(mp,realmanifest)
  mapping=json.loads(json.dumps(realmap));mapping['repair_manifest_sha256']=sha(mp);write(fixture/'diagnosis/REPAIR_CASES.json',mapping)
  original_fixture=json.loads(json.dumps(original));original_fixture['result_sha256']={};case_hashes={}
  def field_report(name,history,assembly,manifest_hash,mutated=False):
   binding=dict(path=str(history.relative_to(fixture)),sha256=hashlib.sha256(b'synthetic fixture only').hexdigest() if mutated else sha(history),assembly_sha256='0'*64 if mutated else sha(assembly))
   return dict(case=name,status='PASS',manifest_sha256=manifest_hash,windows=[dict(index=i,binding=binding) for i in range(3)])
  for item in mapping['datasets']:
   name=item['base_case'];directory=fixture/'production_analysis'/name;history=directory/'histories'/(name+'_window2.npz');history.parent.mkdir(parents=True);history.write_bytes(b'mutated fixture' if mode=='old_anchor_join_mutation' else b'synthetic fixture only')
   write(directory/'clock.json',clock_value(history))
   assembly=directory/'ASSEMBLY.json';write(assembly,dict(output_sha256={str(history):sha(history)}))
   report_path=fixture/'review/math/cases'/(name+'.json');write(report_path,field_report(name,history,assembly,mapping['original_manifest_sha256'],mode=='old_anchor_join_mutation'));original_fixture['result_sha256'][str(report_path)]=sha(report_path)
  write(fixture/'production_analysis/postprocess/MATH_CANDIDATE.json',original_fixture)
  for row in realmanifest['cases']:
   name=row['id'];directory=fixture/'diagnosis/repair_analysis'/name;history=directory/'histories'/(name+'_window2.npz');history.parent.mkdir(parents=True);history.write_bytes(b'mutated fixture' if mode=='joined_history_mutation' else b'synthetic fixture only')
   assembly=directory/'ASSEMBLY.json';write(assembly,dict(input_sha256={str(mp):sha(mp)},output_sha256={str(history):sha(history) if mode!='history_binding_failure' else '0'*64}))
   report_path=fixture/'diagnosis/review_math/repair_cases'/(name+'.json');write(report_path,field_report(name,history,assembly,sha(mp),mode=='joined_history_mutation'));case_hashes[str(report_path.relative_to(fixture))]=sha(report_path)
  math_path=fixture/'diagnosis/review_math/REPAIR_MATH.json';write(math_path,dict(status='PASS',selected_cases=25 if mode=='incomplete_math_coverage' else 26,original_equations_pass=True,case_report_sha256=case_hashes,repair_specs_review={'manifest_sha256':sha(mp)}))
  write(m.FREEZE,dict(source_sha256={str(ADAPTER):sha(ADAPTER)},reserve_bytes=1024,total_output_bytes=2**30))
  write(m.REVIEW,dict(freeze_sha256=sha(m.FREEZE),parent_source_review='CLEARED',math_source_review='CLEARED',field_diagnostic_readouts='CLEARED',field_evidence_sha256={str(math_path.relative_to(fixture)):sha(math_path)}))
  # Real original capture authentication was separately exercised on first3.
  # Here histories are deliberately synthetic; no numerical claim is tested.
  m.helper.authenticated_producer_receipts=lambda value:None
  class Process:
   def __init__(self,call,**kwargs):
    prefix=Path(call[2]);command=call[3:];history=Path(command[2]);output=Path(command[3]);self.code=2 if mode=='stage_failure' else 0
    value=clock_value(history,1e-3 if mode=='comparison_failure' else 0)
    if mode=='null_failure':value['readouts'][0]['max_sampled_abs_null_norm']=3e-7
    if mode=='query_failure':value['readouts'][0]['te']=2.485
    write(output,value);write(prefix.with_suffix('.stdout'),value);prefix.with_suffix('.stderr').write_text('')
    write(prefix.with_suffix('.json'),dict(command=command,returncode=self.code,wall_timeout_seconds=None,cpu_timeout_seconds=None,address_space_bytes=2*1024**3,stdout_sha256=sha(prefix.with_suffix('.stdout')),stderr_sha256=sha(prefix.with_suffix('.stderr'))))
   def poll(self):return self.code
   def wait(self):return self.code
  m.subprocess=types.SimpleNamespace(Popen=Process)
  if mode in ['history_binding_failure','joined_history_mutation','old_anchor_join_mutation','incomplete_math_coverage']:
   try:m.main()
   except ValueError as error:
    expected='REFINED_HISTORY_ASSEMBLY_BINDING' if mode=='history_binding_failure' else 'REFINED_FIELD_MATH_COVERAGE' if mode=='incomplete_math_coverage' else 'CLOCK_FIELD_REVIEW_HISTORY_JOIN'
    assert str(error)==expected and not m.OUT.exists(),str(error)
   else:raise AssertionError('history mismatch passed')
  else:
   code=m.main();result=read(m.OUT/'COMPLETION_RESULT.json')
   if mode in ['complete','comparison_failure']:
    candidate=read(m.OUT/'REFINED_CLOCK_CANDIDATE.json');assert len(candidate['datasets'])==13 and len(candidate['refined_output_sha256'])==26 and len(candidate['all_supplied_signs'])==39
    assert all(x['original_field_qualification']=='UNQUALIFIED' and x['repaired_field_qualification']=='NOT_DETERMINED_BY_CLOCK_COMPARISON' and len(x['matched'])==2 for x in candidate['datasets'])
    assert code==(0 if mode=='complete' else 2) and candidate['machine_diagnostic']==('PASS' if mode=='complete' else 'FAIL')
   elif mode=='stage_failure':assert code==2 and result['status']=='REFINED_CLOCK_DIAGNOSTIC_STOP' and len(result['stages'])==1
   else:assert code==2 and result['status']=='UNRESOLVED_OPERATIONAL_ERROR' and len(result['stages'])==1
  checks.append(mode+'_expected_behavior')
 report=dict(status='REFINED_CLOCK_OPERATIONAL_CONTROLS_PASS',adapter_sha256=sha(ADAPTER),checker_sha256=sha(__file__),checks=checks,scope='Author-side mocked orchestration/query/null/binding/qualification checks only. No scientific arrays or geodesic execution. Same capture/signal forwarding primitive as original adapter, whose actual manual-signal test is separately recorded; not repeated with a new actual child here.')
 write(HERE/'REFINED_CLOCK_BINDING_CONTROLS.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
