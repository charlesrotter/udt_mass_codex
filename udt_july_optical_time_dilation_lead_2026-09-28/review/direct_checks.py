#!/usr/bin/env python3
"""Independent direct-review extensions; author replay is separately labeled."""
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as s

here = Path(__file__).resolve().parent
package = here.parent
checks = []


def zero(name, expr):
    residual = s.simplify(s.trigsimp(expr))
    passed = residual == 0
    checks.append({"name":name,"residual":str(residual),"passed":passed})
    if not passed:
        raise RuntimeError(f"{name}: {residual}")


def connection(g, coordinates):
    inv = g.inv()
    dim = len(coordinates)
    return [[[s.simplify(sum(inv[i,l]*(s.diff(g[l,j],coordinates[k])+s.diff(g[l,k],coordinates[j])-s.diff(g[j,k],coordinates[l]))/2 for l in range(dim))) for k in range(dim)] for j in range(dim)] for i in range(dim)]


# Full coordinate Riemann calculation for the areal alternative, not a borrowed
# closed-form spherical invariant. Work on 0<x<1/b, 0<theta<pi.
t,x,theta,varphi = s.symbols("t x theta varphi", real=True)
b = s.symbols("b", positive=True)
f = 1-b*x
g = s.diag(-f,1/f,x*x,x*x*s.sin(theta)**2)
ginv = g.inv()
coords = [t,x,theta,varphi]
Gamma = connection(g,coords)
Rm = {}
for i in range(4):
    for j in range(4):
        for k in range(4):
            for l in range(4):
                Rm[i,j,k,l]=s.trigsimp(s.simplify(s.diff(Gamma[i][l][j],coords[k])-s.diff(Gamma[i][k][j],coords[l])+sum(Gamma[i][k][m]*Gamma[m][l][j]-Gamma[i][l][m]*Gamma[m][k][j] for m in range(4))))
Ric = s.Matrix(4,4,lambda j,l:sum(Rm[i,j,i,l] for i in range(4)))
Rscalar = s.simplify(sum(ginv[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
Kscalar = s.trigsimp(s.simplify(sum(ginv[i,i]*ginv[j,j]*ginv[k,k]*ginv[l,l]*(g[i,i]*Rm[i,j,k,l])**2 for i in range(4) for j in range(4) for k in range(4) for l in range(4))))
zero("areal_scalar_curvature",Rscalar-6*b/x)
zero("areal_Kretschmann",Kscalar-8*b*b/x**2)

# A positive strictly decreasing profile can have a stationary point.
fc = s.exp(-x**3)
zero("strict_decrease_counterexample_zero_derivative",s.diff(fc,x).subs(x,0))
zero("variable_kappa_domain_pole",-2/s.diff(fc,x)-2*s.exp(x**3)/(3*x*x))

# Direct time-live connection reconstruction of the radial total clock rate.
F = s.Function("F")(t,x)
glive=s.diag(-F,1/F)
livecoords=[t,x]
Clive=connection(glive,livecoords)
U=s.Matrix([1/s.sqrt(F),0])
Ulower=glive*U
nablaU=s.Matrix(2,2,lambda i,j:s.simplify(s.diff(Ulower[j],livecoords[i])-sum(Clive[k][i][j]*Ulower[k] for k in range(2))))
for eps in (-1,1):
    v=U+s.Matrix([0,eps*s.sqrt(F)])
    rate_U=s.simplify((v.T*nablaU*v)[0])
    rate_O=s.simplify(s.sqrt(F)*rate_U)
    zero(f"time_live_total_optical_rate_eps_{eps}",rate_O-(-s.diff(F,t)/(2*F)+eps*s.diff(F,x)/2))

# Independently parameterize the homogeneous expanding null ray by reception
# time: L=(e^-h te-e^-h tr)/h. Its implicit slope is e^[h(tr-te)].
h,te,tr,L = s.symbols("h te tr L", real=True)
incidence=(s.exp(-h*te)-s.exp(-h*tr))/h-L
implicit_slope=-s.diff(incidence,te)/s.diff(incidence,tr)
zero("homogeneous_implicit_arrival_slope",implicit_slope-s.exp(h*(tr-te)))
zero("homogeneous_zero_h_limit",s.limit((s.exp(-h*te)-s.exp(-h*tr))/h,h,0)-(tr-te))

# Exact numeric counterexamples to the four declared wrong assertions. These
# are not claims of injected implementation-mutation coverage.
wrong_witnesses={
 "reciprocity_alone_implies_constant_Popt":s.Integer(2),
 "same_positive_shift_both_static_directions":s.Integer(2)-s.Rational(1,2),
 "same_coefficient_after_proper_clock_normalization":s.Rational(1,2)-1,
 "shear_can_be_isotropic":s.Integer(2)-(-1),
}
for name,residual in wrong_witnesses.items():
    if residual==0:
        raise RuntimeError(name)

# Pin both new-candidate versions and the frozen author artifacts before replay.
freeze=json.loads((package/"INITIAL_REVIEW_FREEZE.json").read_text())
pin_checks=[]
for name,expected in freeze.items():
    actual=hashlib.sha256((package/name).read_bytes()).hexdigest()
    pin_checks.append({"path":name,"sha256":actual,"matches_initial_freeze":actual==expected})
    if actual!=expected:
        raise RuntimeError(f"initial freeze changed: {name}")
if (package/"CANDIDATE.md").read_bytes()!=(package/"INITIAL_CANDIDATE.md").read_bytes():
    raise RuntimeError("initial candidate content differs before repair")

# Run exact preserved author bytes in review-owned paths to avoid rewriting the
# root frozen CHECK_RESULT.json. These runs are regression, not independence.
replays=[]
env=os.environ.copy()
env.update({"OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1","MKL_NUM_THREADS":"1"})
for origin,subdir,expected_return in [("INITIAL_check_lead.py","initial_author_replay",1),("check_lead.py","author_replay",0)]:
    replay=here/subdir
    replay.mkdir(exist_ok=True)
    script=replay/"check_lead.py"
    script.write_bytes((package/origin).read_bytes())
    result=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,env=env,timeout=60)
    (replay/"stdout.txt").write_text(result.stdout)
    (replay/"stderr.txt").write_text(result.stderr)
    if result.returncode!=expected_return:
        raise RuntimeError(f"author replay {origin}: exit {result.returncode}")
    row={"origin":origin,"script_sha256":hashlib.sha256(script.read_bytes()).hexdigest(),"returncode":result.returncode,"label":"same-code regression"}
    if expected_return==0:
        saved=json.loads((replay/"CHECK_RESULT.json").read_text())
        frozen=json.loads((package/"CHECK_RESULT.json").read_text())
        row.update({"output_equals_frozen":saved==frozen,"exact_check_count":len(saved["exact_checks"]),"wrong_assertions_rejected":len(saved["rejected_mutants"]),"finite_pulse_controls":len(saved["finite_pulse_controls"]),"max_pulse_error":saved["max_pulse_error"]})
        if saved!=frozen:
            raise RuntimeError("author replay output differs")
    else:
        row["same_failure_site"]="two_direction_clock_product" in result.stderr
        if not row["same_failure_site"]:
            raise RuntimeError("unexpected initial failure")
    replays.append(row)

print(json.dumps({"utc":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),"sympy":s.__version__,"exact_check_count":len(checks),"checks":checks,"wrong_assertion_counterexamples":{name:str(v) for name,v in wrong_witnesses.items()},"initial_freeze":pin_checks,"author_replays":replays,"interpretation":"Independent direct-stage exact checks, with separately labeled source-preserving same-code author replay; no physical adoption."},indent=2))
