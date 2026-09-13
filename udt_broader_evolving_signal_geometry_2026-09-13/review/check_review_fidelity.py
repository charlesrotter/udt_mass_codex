"""Standard-library byte/receipt correspondence, not scientific proof."""
import json,hashlib,datetime
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B/'review';ROOT=B.parent
records=[]
for name,key in [('SOURCE_FIRST_SEAL.json','files'),('SOURCE_FIRST_INPUTS_AND_RUN_SEAL.json','files'),('DIRECT_INPUTS_AND_CHECKS.json','files'),('DIRECT_REVIEW_SEAL.json','files')]:
 data=json.loads((R/name).read_text())
 for path,h in data[key].items():
  p=ROOT/path;assert hashlib.sha256(p.read_bytes()).hexdigest()==h,(name,path)
 records.append({'seal':name,'verified_files':len(data[key])})
results=[]
for stem,expected in [('independent_metric_run',0),('independent_affine_run',0),('author_drop_cross_replay',1),('author_source_epoch_replay',1),('calibration_rank_replay',0)]:
 d=json.loads((R/(stem+'.json')).read_text());prov=json.loads((R/(stem+'.capture_provenance.json')).read_text())
 assert d['returncode']==expected and not d['timeout']
 assert d['duration_seconds']<=180 and d['address_space_bytes']==2048*1024**2 and d['cpu_seconds']==180
 assert set(prov['thread_environment'].values())=={'1'}
 results.append({'stem':stem,'returncode':d['returncode'],'duration_seconds':d['duration_seconds'],'maxrss_kib':d['maxrss_kib'],'started_utc':d['started_utc']})
for first,second in zip(results,results[1:]):
 end=datetime.datetime.fromisoformat(first['started_utc'])+datetime.timedelta(seconds=first['duration_seconds'])
 assert end<=datetime.datetime.fromisoformat(second['started_utc']),'reviewer scientific overlap'
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','scope':'Byte/receipt/resource/serial-capture correspondence only. No source grading, scientific proof, runtime model attestation or protected-payload access.','seals':records,'scientific_captures':results,'sum_scientific_duration_seconds':sum(d['duration_seconds'] for d in results),'maxrss_kib':max(d['maxrss_kib'] for d in results)},indent=2))
