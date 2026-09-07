"""One bounded, fresh existing-CLI review; no configuration or infrastructure edits."""
import datetime,json,os,resource,signal,subprocess,time
from pathlib import Path
root=Path(__file__).resolve().parents[2]
here=Path(__file__).resolve().parent
prefix=here/'fresh_review'
cmd=['codex','exec','--ephemeral','--sandbox','workspace-write','--json',
     '-C',str(root),'-o',str(here/'review'/'CLI_FINAL_MESSAGE.md'),
     'Read and faithfully execute only '+str(here/'REVIEW_DISPATCH.md')+'. This is an authorized fresh separate-context scientific review; no resume or fork.']
started=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
 resource.setrlimit(resource.RLIMIT_CPU,(900,900))
env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
with (prefix.with_suffix('.stdout')).open('xb') as out, (prefix.with_suffix('.stderr')).open('xb') as err:
 p=subprocess.Popen(cmd,cwd=root,env=env,stdout=out,stderr=err,start_new_session=True,preexec_fn=limits)
 try: rc=p.wait(timeout=4200); timed=False
 except subprocess.TimeoutExpired:
  os.killpg(p.pid,signal.SIGTERM)
  try: rc=p.wait(timeout=10)
  except subprocess.TimeoutExpired: os.killpg(p.pid,signal.SIGKILL);rc=p.wait()
  timed=True
result=dict(command=cmd,started_utc=started,duration_seconds=time.monotonic()-t,
 returncode=rc,timeout=timed,address_space_bytes=2*1024**3,cpu_seconds=900,
 scope='fresh existing Codex review, no resume/fork/config modification')
with prefix.with_suffix('.json').open('x') as f:json.dump(result,f,indent=2)
print(json.dumps(result))
raise SystemExit(0 if rc==0 and not timed else 1)
