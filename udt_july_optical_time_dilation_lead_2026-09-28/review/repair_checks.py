#!/usr/bin/env python3
"""Focused precision repair and already supplied time-live sign controls."""
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import sympy as s

here=Path(__file__).resolve().parent
package=here.parent
T,x=s.symbols("T x",real=True)
b=s.symbols("b",positive=True)
checks=[]
for sign in (-1,1):
    for velocity in (s.Integer(0),2*b,-2*b):
        f=1-velocity*T-b*x
        # The generic expression was independently derived from the connection
        # in direct_checks.py, before the author's follow-up was exposed.
        rate=-s.diff(f,T)/(2*f)+sign*s.diff(f,x)/2
        origin=s.simplify(rate.subs({T:0,x:0}))
        expected=(velocity-sign*b)/2
        if s.simplify(origin-expected)!=0:
            raise RuntimeError("sign-control mismatch")
        checks.append({"direction":sign,"v":str(velocity),"origin_rate":str(origin),"passed":True})

# On |b T|,|b x|<1/16 the v=+/-2b controls have 13/16<f<19/16.
# This bound is a local mathematical control, not a physical cutoff.
rate_margin=s.Rational(16,19)-s.Rational(1,2)
if rate_margin<=0:
    raise RuntimeError("no strict neighborhood sign margin")

pins={}
for name in ("INITIAL_CANDIDATE.md","REPAIR.md","TIME_DEPENDENT_FOLLOWUP.md","DECISION_BRIEF.md","OWNER_DIRECTION.md","check_time_dependent_followup.py","TIME_DEPENDENT_CHECK_RESULT.json"):
    pins[name]=hashlib.sha256((package/name).read_bytes()).hexdigest()
initial=json.loads((package/"INITIAL_REVIEW_FREEZE.json").read_text())
if pins["INITIAL_CANDIDATE.md"]!=initial["CANDIDATE.md"]:
    raise RuntimeError("initial candidate changed")

# Same-code replay kept distinct from the independent connection and sign checks.
replay=here/"followup_author_replay"
replay.mkdir(exist_ok=True)
script=replay/"check_time_dependent_followup.py"
script.write_bytes((package/script.name).read_bytes())
env=os.environ.copy()
env.update({"OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1","MKL_NUM_THREADS":"1"})
run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,env=env,timeout=60)
(replay/"stdout.txt").write_text(run.stdout)
(replay/"stderr.txt").write_text(run.stderr)
if run.returncode!=0:
    raise RuntimeError(f"follow-up replay exit {run.returncode}")
result=json.loads((replay/"TIME_DEPENDENT_CHECK_RESULT.json").read_text())
frozen=json.loads((package/"TIME_DEPENDENT_CHECK_RESULT.json").read_text())
if result!=frozen:
    raise RuntimeError("follow-up replay differs")
print(json.dumps({"utc":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),"sympy":s.__version__,"independent_sign_checks":checks,"local_neighborhood_margin_in_units_b":str(rate_margin),"review_target_pins":pins,"author_replay":{"label":"same-code regression","exit_code":run.returncode,"output_equals_saved":result==frozen,"exact_checks":len(result["checks"]),"wrong_endpoint_depth_rejected":result["wrong_endpoint_depth_rejected"],"mutant_difference":result["mutant_difference"]},"scope":"Conditional unadopted controls only; no physical time dependence selected."},indent=2))
