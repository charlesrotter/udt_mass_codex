"""RCD1 exposed reconstruction from saved scale factor, without parent helpers."""
import hashlib,json
from pathlib import Path
import sympy as s

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
source=Path('udt_environment_response_candidates_2026-10-01/CUBIC_RECOMPUTATION.json')
saved=json.loads(source.read_text())
t,L=s.symbols('t L')
coeff=[s.Rational(q) for q in saved['a_coefficients'][:8]]
a=sum(q*t**n for n,q in enumerate(coeff))
eta=s.integrate(s.series(1/a,t,0,7).removeO(),(t,0,t))
inverse=L
reversion=[]
for n in range(2,8):
    cn=s.Symbol('c'+str(n))
    trial=inverse+cn*L**n
    residual=s.series(eta.subs(t,trial)-L,L,0,n+1).removeO().expand().coeff(L,n)
    value=s.solve(residual,cn)[0]
    inverse=trial.subs(cn,value)
    reversion.append(str(value))
lp=s.series(s.log(a.subs(t,inverse)),L,0,8).removeO().expand()
b3,b5=lp.coeff(L,3),lp.coeff(L,5)
alpha=s.factor(-b3/(120*b5))
assert b3==s.Rational(1,1200) and b5==-s.Rational(1,144000) and alpha==1
parent=json.loads((ROOT/'SAVED_SERIES_RESULT.json').read_text())
assert b3==s.Rational(parent['b3']) and b5==s.Rational(parent['b5']) and alpha==s.Rational(parent['reconstructed_alpha'])
for n in range(8):
    assert lp.coeff(L,n)==s.Rational(saved['logp_coefficients'][n])
H=s.diff(a,t)/a
R=6*(s.diff(H,t)+2*H**2)
P=s.diff(R,t)
C=3*(1+2*alpha*R)*H**2-alpha*R**2/2+6*alpha*H*P
K=s.diff(H,t)
J=2*R*K+s.diff(R,t,2)-H*P
cseries=s.series(C,t,0,7).removeO().expand()
shape=s.series(K+alpha*J,t,0,4).removeO().expand()
assert cseries==0 and shape==0

# Logical equivalence control only: no new response is proposed/adopted.
g=s.diag(-1,1,1,1)
values=s.symbols('e0:10');E=s.zeros(4);k=0
for i in range(4):
    for j in range(i,4):E[i,j]=E[j,i]=values[k];k+=1
f,q=s.symbols('f q',nonzero=True)
TF=lambda tensor:tensor-g*s.trace(g.inv()*tensor)/4
equivalence=TF(f*E+q*g)-f*TF(E)
assert all(s.expand(x)==0 for x in equivalence)
assert f*E+q*g!=E

bindings=[]
freeze=json.loads((ROOT/'CANDIDATE_FREEZE.json').read_text())
for name,wanted in freeze['sha256'].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==wanted,name
    bindings.append(name)
for stem in ['parent_symbolic','saved_series']:
    receipt=json.loads((ROOT/'checks'/f'{stem}.json').read_text())
    assert receipt['returncode']==0
    for kind in ['stdout','stderr']:
        assert hashlib.sha256((ROOT/'checks'/f'{stem}.{kind}').read_bytes()).hexdigest()==receipt[kind+'_sha256']
result={'pass':True,'exposure':'Actual new parent proof/code/results exposed; reused ERC1 context',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'b3':str(b3),'b5':str(b5),'alpha_reconstructed':str(alpha),
 'logp_coefficients_0_to_7':[str(lp.coeff(L,n)) for n in range(8)],
 'arrival_inverse_coefficients_2_to_7':reversion,
 'original00_coefficients_through_t6_zero':True,'direct_shape_coefficients_through_t3_zero':True,
 'response_rescaling_puretrace_identity':True,'candidate_binding_count':len(bindings),
 'parent_capture_bindings_verified':True,
 'scope':'Exact saved-artifact reconstruction and representation-equivalence control, not new physics, fresh context, empirical test or finite-interval certification.'}
with (OUT/'DIRECT_SAVED_RESULT.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps(result,indent=2))
