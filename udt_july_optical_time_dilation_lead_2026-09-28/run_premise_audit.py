from pathlib import Path
import datetime,hashlib,json,platform,subprocess,time
p=Path(__file__).resolve().parent/'premise_audit'
command=['python3','verify_current_scientific_premises.py']
tracked=['CURRENT_SCIENTIFIC_PREMISES.tsv','CURRENT_SCIENTIFIC_PREMISES.md','verify_current_scientific_premises.py','AGENTS.md','CLAUDE.md','CANON.md','LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md']
def hashes(): return {n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in tracked}
r={'command':command,'cwd':str(Path.cwd()),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'timeout_seconds':900,'before':hashes()}
t=time.monotonic()
try:
 with (p/'stdout.txt').open('w') as out,(p/'stderr.txt').open('w') as err:
  c=subprocess.run(command,stdout=out,stderr=err,timeout=900)
 r['exit_code']=c.returncode
except subprocess.TimeoutExpired:r['timeout']=True
r.update(elapsed_seconds=time.monotonic()-t,after=hashes());r['inputs_unchanged']=r['before']==r['after']
(p/'RUN_RECORD.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['before','after']},indent=2))
raise SystemExit(0 if r.get('exit_code')==0 and r['inputs_unchanged'] else 1)
