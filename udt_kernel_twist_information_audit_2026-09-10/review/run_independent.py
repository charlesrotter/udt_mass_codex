#!/usr/bin/env python3
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time

p=pathlib.Path(__file__).resolve().parent
cmd=[sys.executable,str(p/'independent_geometry.py')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
t0=time.monotonic()
try:
    result=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
    out,err,code=result.stdout,result.stderr,result.returncode
    timed_out=False
except subprocess.TimeoutExpired as exc:
    out=exc.stdout or b''; err=exc.stderr or b''
    out=out.decode() if isinstance(out,bytes) else out
    err=err.decode() if isinstance(err,bytes) else err
    code=None; timed_out=True
(p/'independent.stdout.json').write_text(out)
(p/'independent.stderr.txt').write_text(err)
record={'command':cmd,'cwd':str(pathlib.Path.cwd()),'start_utc':start,
 'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t0,
 'timeout_seconds':120,'timed_out':timed_out,'exit_code':code,'device':'CPU',
 'code_sha256':hashlib.sha256((p/'independent_geometry.py').read_bytes()).hexdigest()}
(p/'independent.run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
if code==0:
    data=json.loads(out)
    print(json.dumps({k:data[k] for k in ['status','positive_count','negative_count','derived']},indent=2))
else:
    print(err)
sys.exit(code if code is not None else 124)
