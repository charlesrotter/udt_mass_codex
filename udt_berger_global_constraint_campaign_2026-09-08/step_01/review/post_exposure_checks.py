#!/usr/bin/env python3
"""Frozen-author replay and separately assembled post-exposure exact checks."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
import sympy as s

here=Path(__file__).resolve().parent
step=here.parent
root=here.parents[2]
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save_outputs="--verify-only" not in sys.argv


def verify_manifest(manifest,base):
    rows=[]
    for line in manifest.read_text().splitlines():
        expected,name=line.split("  ",1)
        actual=digest(base/name)
        assert actual==expected,(name,actual,expected)
        rows.append({"file":name,"sha256":actual})
    return rows


source_seal=verify_manifest(here/"SOURCE_FIRST_SHA256SUMS",here)
source_inputs=verify_manifest(here/"SOURCE_INPUT_SHA256SUMS",root)
frozen=[]
for expected,name in re.findall(r"^([a-f0-9]{64})  (.+)$",(step/"CANDIDATE_FREEZE.md").read_text(),re.M):
    actual=digest(step/name)
    assert actual==expected,(name,actual,expected)
    frozen.append({"file":name,"sha256":actual})
assert len(frozen)==3
env=dict(os.environ)
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    env[key]="1"
env["PYTHONDONTWRITEBYTECODE"]="1"


def limits():
    resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
    resource.setrlimit(resource.RLIMIT_CPU,(60,60))


replays=[]
mutants=["none","cotton_half","positive_h_only","hamiltonian_denominator","momentum_one","L_trace_one","P_sign"]
for mutant in mutants:
    command=[sys.executable,"-B",str(step/"check_bg1.py")]
    if mutant!="none":
        command += ["--mutant",mutant]
    p=subprocess.run(command,capture_output=True,text=True,env=env,preexec_fn=limits,timeout=60,cwd=root)
    label="baseline" if mutant=="none" else mutant
    if save_outputs:
        (here/f"author_replay_{label}.stdout").write_text(p.stdout)
        (here/f"author_replay_{label}.stderr").write_text(p.stderr)
    output=json.loads(p.stdout)
    original_label="check_baseline" if mutant=="none" else f"mutation_{mutant}"
    byte_match=p.stdout==(step/f"{original_label}.stdout").read_text()
    stderr_match=p.stderr==(step/f"{original_label}.stderr").read_text()
    assert byte_match and stderr_match,label
    expected_rc=0 if mutant=="none" else 1
    assert p.returncode==expected_rc,(label,p.returncode)
    original_record=json.loads((step/f"{original_label}.json").read_text())
    assert original_record["returncode"]==expected_rc and not original_record["timeout"]
    failed=[check for check in output["checks"] if not check["pass"]]
    assert bool(failed)==(mutant!="none")
    replays.append({"mutant":mutant,"command":command,"returncode":p.returncode,
                    "stdout_byte_match":byte_match,"stderr_byte_match":stderr_match,
                    "check_count":output["count"],"failed_checks":failed,
                    "address_space_bytes":536870912,"cpu_seconds":60,"wall_seconds":60})

# Independent symbolic construction of P's principal action, with no author import.
xi=s.Matrix(s.symbols("z1:4",real=True))
v=s.Matrix(s.symbols("v1:4",real=True))
J=s.I*xi*v.T
L=J+J.T-s.Rational(2,3)*s.trace(J)*s.eye(3)
P=s.I*L*xi
Pmatrix=P.jacobian(v)
assert s.simplify(Pmatrix+xi.dot(xi)*s.eye(3)+xi*xi.T/3)==s.zeros(3)
det=s.factor(Pmatrix.det())
assert s.simplify(det+s.Rational(4,3)*xi.dot(xi)**3)==0

# Norm contraction checks the rank bookkeeping while conformal invariance
# itself remains an externally sourced analytical identity.
f=s.symbols("f",real=True)
C=s.MutableDenseNDimArray(s.symbols("c0:27"),(3,3,3))
inverse=s.exp(-2*f)*s.eye(3)
norm=sum(C[i,j,k]**2*inverse[i,i]*inverse[j,j]*inverse[k,k]
         for i in range(3) for j in range(3) for k in range(3))
weight=s.simplify(s.diff(norm,f)+6*norm)
assert weight==0

report={"recorded_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "exposure_stage":"After sealed source-first reconstruction and explicit author permission",
        "source_first_seal_payloads":source_seal,
        "source_input_payloads":source_inputs,
        "author_freeze_payloads":frozen,
        "candidate_freeze_sha256":digest(step/"CANDIDATE_FREEZE.md"),
        "method_sources_sha256":digest(step.parent/"METHOD_SOURCES.md"),
        "replays":replays,
        "independent_symbol_determinant":str(det),
        "three_inverse_metric_weight_residual":str(weight),
        "limits":["Author replays are regression, not independent implementations.",
                  "Post-exposure symbol code was written after reading author code.",
                  "Cotton conformal invariance and Fredholm/IFT are analytical methods, not numerical certifications."]}
if save_outputs:
    (here/"POST_EXPOSURE_CHECKS.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"author_freeze_authenticated":len(frozen),
                  "source_first_seal_authenticated":len(source_seal),
                  "baseline_pass":True,
                  "actual_mutations_caught":len(replays)-1,
                  "all_stdout_stderr_byte_identical":True,
                  "symbol_determinant":str(det),"norm_weight_residual":str(weight)},indent=2))
