"""Independent exact-rational check of conservative analytic inequalities."""
from fractions import Fraction as Q
import hashlib,json,platform
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def q(x): return Q(str(x))
checks={}
values={}
def le(name,left,right,strict=False):
    ok=left<right if strict else left<=right
    checks[name]=bool(ok)
    values[name]={'left':str(left),'right':str(right),'left_float':float(left),'right_float':float(right)}
    assert ok, name

mu=q('.01');Amin=q('.05');Amax=q('.1');B=q('.0001');y=q('.00002')
slo=q('.999');shi=q('1.001');O=q('9');I=(1/Amax-y)/shi**3
le('ray_lower_squared',slo**2,1-B**2/Amin**2,True)
le('ray_upper_squared',1+B**2*(1+2*mu/Amin**3),shi**2,True)
le('h_lower',q('.4'),1-3*mu/Amin)
le('f_lower',q('.59'),1-2*mu/Amin-Amax**2)
le('omega_lower_squared',q('4'),q('.005')/Amax**3-1)
le('omega_upper_squared',mu/Amin**3-1,O**2,True)
root_lhs=B*(1/Amax-y)/shi*(1-O*B/(1+slo))
root_rhs=O*y
le('root_bracket',root_rhs,root_lhs,True)
W=q('1.00000002');Wp=q('.002');D=10*y+W;Dp=10+Wp
le('W_upper_squared',1+99*y*y+2*mu*y**3,W*W)
le('Wprime_upper',99*y+3*mu*y*y,Wp,True)
alpha=1+W*B*B/(1+slo)
le('alpha_upper',alpha,q('1.000000006'),True)
Bp=(B/slo+O*alpha/(1-O*B))/I
le('Bprime_upper',Bp,q('1'),True)
Sp=(B*(1+2*mu*y**3)+B*B*(y+3*mu*y*y))/slo
le('sprime_upper',Sp,q('.000101'),True)
jp=(Wp*D+W*Dp)*B*B/(1+slo)+W*D*(2*B/(1+slo)+B*B*q('.000101')/(1+slo)**2)
le('jprime_upper',jp,q('.000101'),True)
logF=O/(1-O*B)+Dp+jp
le('logF_upper',logF,q('20'),True)
eta_bound=W-1+W*y*q('20')
le('eta_upper',eta_bound,q('.0005'),True)
checks['countercheck_overstrong_eta_rejected']=eta_bound>q('.000001')
checks['countercheck_expanded_tail_not_certified']=(W-1+W*q('.002')*20)>q('.0005')
assert all(checks.values())
out={'status':'PASS','evidence':'exact rational checks of analytic bounds; no incidence cases',
     'python':platform.python_version(),'cases_consumed':0,'checks':checks,'values':values,
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
target=ROOT/'BOUND_RESULT.json'
with target.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
