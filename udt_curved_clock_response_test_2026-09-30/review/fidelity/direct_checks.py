"""Direct review controls written independently after candidate exposure."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as S

root=Path.cwd()
p=root/'udt_curved_clock_response_test_2026-09-30'
pin_checks=[]
for name,key in [('CHECK_FREEZE.json','sha256'),('CANDIDATE_FREEZE.json','sha256'),('review/fidelity/SOURCE_FIRST_SEAL.json','files')]:
    freeze=json.loads((p/name).read_text())
    for path,wanted in freeze[key].items():
        actual=hashlib.sha256((root/path).read_bytes()).hexdigest()
        assert actual==wanted,(name,path,actual,wanted)
        pin_checks.append({'freeze':name,'path':path,'sha256':actual})

checks=[]
rejections=[]
def eq(name,expr):
    value=S.simplify(expr)
    assert value==0,(name,value)
    checks.append(name)
def wrong(name,expr):
    value=S.simplify(expr)
    assert value!=0,(name,value)
    rejections.append({'name':name,'nonzero_difference':str(value)})

s,t,z,eps=S.symbols('s t z epsilon',real=True)
B=s**2
alpha=S.exp(-B)*S.Integral(S.exp(z**2),(z,0,s))
eq('integrating factor original ODE',S.diff(alpha,s)+2*s*alpha-1)
M=2+s*s
J=2*s*M
eq('strict mean sign derivative',M*S.diff(alpha,s)+J*alpha-M)
bad_alpha=S.exp(B)*S.Integral(S.exp(z**2),(z,0,s))
wrong('wrong integrating factor sign',(S.diff(bad_alpha,s)+2*s*bad_alpha-1).subs(s,1))

H,L=S.symbols('H L',positive=True)
Q=S.Function('Q')(eps)
arrival=s*S.exp(H*Q)
ratio=S.diff(arrival,s)
eq('conformal proper arrival baseline',arrival.subs(eps,0).subs(Q.subs(eps,0),L)-s*S.exp(H*L))
replacement={Q:L,S.diff(Q,eps):1/H}
variation=S.diff(arrival,eps).subs(replacement)
eq('conformal moving arrival',variation-s*S.exp(H*L))
qD=S.diff(S.log(ratio),eps).subs(replacement)
eq('conformal curved clock contrast derivative',qD-1)
wrong('freezing curved receiver event',qD)
# Independent connection-product derivation: Gamma^x_xt=Gamma^t_yy=H.
# All derivative terms and the other connection product vanish for R^x_yxy.
Rxyxy=S.exp(2*H*t)*H*H
wrong('curved diagnostic is flat',Rxyxy)
eq('cosmic time curvature crosscheck',Rxyxy.subs(t,S.log(H*S.exp(z))/H)-H**4*S.exp(2*z))

producer=json.loads((p/'checks/curved_result.json').read_text())
receipt=json.loads((p/'checks/curved.json').read_text())
assert producer['status']=='PASS'
assert all(v=='0' for v in producer['identities'].values())
assert len(producer['identities'])==14 and len(producer['wrong_nonidentities_rejected'])==6
assert receipt['returncode']==0 and receipt['timeout'] is False
assert (p/'checks/curved.stderr').read_bytes()==b''
print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':S.__version__,
 'identities':checks,'wrong_formulas_rejected':rejections,'pin_checks':pin_checks,
 'producer_saved_record_verified':{'identities':14,'rejected_nonidentities':6,'returncode':0},
 'scope':'Post-exposure independent algebra; source-first review is separately sealed. Curved auxiliary clocks are not CES1 or a selected UDT solution.'},indent=2))
