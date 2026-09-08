#!/usr/bin/env python3
"""Capture one bounded independent check without using author implementations."""
import datetime
import json
import os
from pathlib import Path
import resource
import subprocess
import sys

here=Path(__file__).resolve().parent
env=dict(os.environ)
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    env[key]="1"
env["PYTHONDONTWRITEBYTECODE"]="1"


def limit():
    resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
    resource.setrlimit(resource.RLIMIT_CPU,(60,60))


command=[sys.executable,"-B",str(here/"independent_check.py")]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(command,capture_output=True,text=True,env=env,preexec_fn=limit,timeout=60)
(here/"independent_check.stdout").write_text(p.stdout)
(here/"independent_check.stderr").write_text(p.stderr)
record={"command":command,"cwd":os.getcwd(),"started_utc":started,
        "finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "returncode":p.returncode,"address_space_bytes":536870912,
        "cpu_seconds":60,"wall_timeout_seconds":60,"library_threads":1}
(here/"independent_check.run.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record,indent=2))
print(p.stdout)
print(p.stderr,file=sys.stderr)
raise SystemExit(p.returncode)
