"""Small capture wrapper, confined to this review directory."""
import datetime
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

base=Path(__file__).resolve().parent
name=sys.argv[1]
command=[sys.executable,'-B',str(base/(name+'.py'))]
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
def limits():
    resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
    resource.setrlimit(resource.RLIMIT_CPU,(60,60))
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
t=time.monotonic()
try:
    p=subprocess.run(command,capture_output=True,timeout=60,env=env,preexec_fn=limits)
    rc,out,err,timed=p.returncode,p.stdout,p.stderr,False
except subprocess.TimeoutExpired as e:
    rc,out,err,timed=None,e.stdout or b'',e.stderr or b'',True
(base/(name+'.stdout')).write_bytes(out)
(base/(name+'.stderr')).write_bytes(err)
record=dict(command=command,cwd=os.getcwd(),started_utc=start,duration_seconds=time.monotonic()-t,
    returncode=rc,timeout=timed,address_space_bytes=536870912,cpu_seconds=60,wall_seconds=60,
    maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    thread_environment={key:env[key] for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']})
(base/(name+'.receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
sys.exit(0 if rc==0 else 1)
