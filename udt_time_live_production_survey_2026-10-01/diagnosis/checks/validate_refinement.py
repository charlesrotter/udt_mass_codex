from pathlib import Path
import hashlib,importlib.util,json
ROOT=Path.cwd();B=ROOT/'udt_time_live_production_survey_2026-10-01';D=B/'diagnosis'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
spec=importlib.util.spec_from_file_location('unchanged_worker',B/'production_worker.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
m=read(D/'repair_runtime/campaign.json');old=read(B/'production_runtime/campaign.json');oldrows={r['id']:r for r in old['cases']};rows=[]
for row in m['cases']:
 s=read(row['spec']);oldid=row['id'].replace('_n24_quarter','_n24_half').replace('_n32_half','_n32');before=read(oldrows[oldid]['spec'])
 assert {k for k in s if s[k]!=before[k]}=={'cfl','max_step_ticks'}
 assert s['cfl']==before['cfl']/2 and s['max_step_ticks']==before['max_step_ticks']//2
 assert sha(row['spec'])==row['spec_sha256'];ticks,checks,initial=module.validate(s)
 assert sha(initial)==old['source_sha256'][str(initial)]
 rows.append(dict(case=row['id'],checkpoints=len(ticks),check_events=len(checks),changed_keys=['cfl','max_step_ticks'],output_cap=s['output_bytes']))
for p,h in m['source_sha256'].items():assert sha(p)==h,p
result=dict(status='PASS_UNCHANGED_INPUTS_AND_ACTUAL_WORKER_SPEC_VALIDATION',rows=rows,manifest_sha256=sha(D/'repair_runtime/campaign.json'),scope='Configuration/source check only; does not certify new evolved fields or GPU behavior.')
with (D/'checks/REFINEMENT_SPECS.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(status=result['status'],cases=len(rows),sum_case_caps=sum(r['output_cap'] for r in rows))))
