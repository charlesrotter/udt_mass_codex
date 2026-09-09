"""Focused direct-review scope checks, preserving pre-candidate scripts unchanged."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sympy as s

with contextlib.redirect_stdout(io.StringIO()):
    import independent_coordinate_check as data
    import independent_evolution_interface as ev

checks=[]
def check(name,ok):
    passed=bool(ok);checks.append({'name':name,'pass':passed});assert passed,name
def zero(z):return s.simplify(z)==0

# This is an independent generic-jet recomputation of the candidate's freely
# variable connected scalar, beyond the pre-exposure Lambda=0 evolution check.
Lam=s.symbols('Lambda',real=True)
g,dg,ddg=ev.fourmetric(-2*(ev.Ktime-Lam*ev.gamma))
RR,_=ev.tensor(g,dg,ddg)
check('all_spatial_Ricci_equal_Lambda_gamma',all(zero(z)for z in RR[1:4,1:4]-Lam*ev.gamma))
check('full_Ricci_time_residual_equals_H_minus_2Lambda',zero(RR[0,0]+Lam-(ev.H-2*Lam)))
check('full_Ricci_mixed_residual_equals_negative_M',all(zero(RR[0,i+1]+ev.M[i])for i in range(3)))

# General higher-order analytic scalar/mean functions have unchanged first jets.
e=data.eps
lambda_tail=s.Function('lambda_tail')(e)
mean_tail=s.Function('mean_tail')(e)
subdata={**data.cotangent,data.q:data.q0+e*e*(data.q2+mean_tail)}
ldata=data.ell_completion.subs(data.Lam,e*e*lambda_tail).subs(subdata).doit()
kdata=data.K.subs(subdata).subs(data.ell,ldata).doit()
check('arbitrary_analytic_higher_order_scalar_and_mean_preserve_complete_K_tangent',
      all(zero(z)for z in kdata.diff(e).subs(e,0)-data.expected_k))
check('higher_order_scalar_changes_admitted_data',not zero(s.diff(ldata,lambda_tail)))
check('higher_order_mean_changes_admitted_data',not zero(s.diff(ldata,mean_tail)))

root=Path(__file__).resolve().parents[3]
step=Path(__file__).resolve().parents[1]
frozen=(step/'check_nr2.py').read_text()
start=frozen.index('# Contract Bianchi at an arbitrary slice-normal spatial-coordinate anchor.')
end=frozen.index('print(json.dumps(',start)
reconstructed=frozen[:start]+frozen[end:]
check('reconstructed_prior_source_matches_disclosed_removal',reconstructed==(step/'pre_bianchi_check.py').read_text())
check('candidate_replay_scientific_stdout_byte_equal',
      (step/'frozen_checks.stdout').read_bytes()==(step/'review/candidate_replay.stdout').read_bytes())
record={
    'checks':checks,
    'candidate_sha256':hashlib.sha256((step/'INITIAL_CANDIDATE.md').read_bytes()).hexdigest(),
    'code_sha256':hashlib.sha256((step/'check_nr2.py').read_bytes()).hexdigest(),
    'scope':'Higher-order analytic freedom and full constant-Lambda geometric interface; no theorem/source replay or physical adoption',
}
print(json.dumps(record,indent=2))
