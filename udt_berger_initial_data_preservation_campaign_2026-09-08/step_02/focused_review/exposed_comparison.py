"""Post-seal comparison of saved tensors; no author/prior executable reruns."""
import hashlib
import json
from pathlib import Path
import re
import sympy as S

base=Path(__file__).resolve().parent
step=base.parent
prior=step/'review'
own=json.loads((base/'source_first_check.stdout').read_text())
author=json.loads((step/'author_check_01.stdout').read_text())
old=json.loads((prior/'spacetime_independent_run.stdout').read_text())
old_comparison=json.loads((prior/'candidate_comparison_run.stdout').read_text())
mutants=json.loads((prior/'additional_mutations_run.stdout').read_text())
checks=[]
def check(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
def zero(name,value):
    vals=list(value) if isinstance(value,S.MatrixBase) else [value]
    residuals=[S.factor(v) for v in vals]
    checks.append(dict(name=name,passed=all(v==0 for v in residuals),residuals=list(map(str,residuals))))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
hashes={}
for digest,n in re.findall(r'^\s+([a-f0-9]{64})\s+(\S+)\s*$',(step/'CANDIDATE_FREEZE.md').read_text(),re.M):
    hashes[str(step/n)]=sha(step/n)
    check('frozen pin '+n,hashes[str(step/n)]==digest)
for n,digest in old_comparison['candidate_sha256'].items():
    check('original comparison candidate correspondence '+n,sha(step/n)==digest)
    hashes[str(step/n)]=sha(step/n)
for n in ['REVIEW_REPORT.md','spacetime_independent.py','candidate_comparison.py','additional_mutations.py',
          'spacetime_independent_run.stdout','spacetime_independent_run.json','spacetime_independent_run.stderr',
          'candidate_comparison_run.stdout','candidate_comparison_run.json','candidate_comparison_run.stderr',
          'additional_mutations_run.stdout','additional_mutations_run.json','additional_mutations_run.stderr']:
    hashes[str(prior/n)]=sha(prior/n)
for n in ['spacetime_independent_run','candidate_comparison_run','additional_mutations_run']:
    receipt=json.loads((prior/(n+'.json')).read_text())
    check('prior successful receipt '+n,receipt['returncode']==0 and not receipt['timeout'])
    check('prior empty stderr '+n,(prior/(n+'.stderr')).read_bytes()==b'')
q=S.symbols('A B C3',positive=True)
v=S.symbols('u1 u2 u3',real=True)
w=S.symbols('w1 w2 w3',real=True)
k=S.symbols('k1 k2 k3',real=True)
acc=S.symbols('a1 a2 a3',real=True)
lam=S.Symbol('Lambda',real=True)
loc={str(t):t for t in [*q,*v,*w,*k,lam]}
myric=S.sympify(own['original_Ricci'],locals=loc)
myr=[S.sympify(t,locals=loc) for t in own['spatial_eigenvalues']]
myH=S.sympify(own['Hamiltonian'],locals=loc)
myLie=S.sympify(own['horizontal_Lie_derivative'],locals=loc)
oldloc=dict(zip(['x1','x2','x3'],q))
oldloc.update({str(t):t for t in [*k,*acc,lam]})
oldric=S.sympify(old['fixed_frame_Ricci4'],locals=oldloc)
rate_sub=dict(zip([*v,*w],[-2*q[i]*k[i] for i in range(3)]+
                 [4*q[i]*k[i]**2-2*q[i]*acc[i] for i in range(3)]))
zero('all 16 prior unspecialized spacetime entries',myric.subs(rate_sub,simultaneous=True)-oldric)
zero('prior Hamiltonian',myH-S.sympify(old['Hamiltonian'],locals=oldloc))
length=S.symbols('l1 l2 l3',positive=True)
authorloc={str(t):t for t in [*k,lam]}
authorloc.update({'n'+str(i+1):2*length[i]/(length[(i+1)%3]*length[(i+2)%3]) for i in range(3)})
authorric=S.sympify(author['full_Ricci4'],locals=authorloc)
evo={acc[i]:myr[i]+sum(k)*k[i]-lam for i in range(3)}
own_evolved=myric.subs(rate_sub,simultaneous=True).subs(evo)
length_sub={q[i]:length[i]**2 for i in range(3)}
T=S.diag(1,*[1/l for l in length])
zero('all 16 author moving-frame spacetime entries',T*own_evolved.subs(length_sub)*T-authorric)
controls=[]
for i,c in enumerate(author['controls']):
    sub=dict(zip(q,map(S.Rational,c['squared_sizes'])))
    r=[S.factor(e.subs(sub)) for e in myr]
    gaps=[S.factor(r[2]-r[j]) for j in range(2)]
    descended=myLie.subs(sub)==S.zeros(3)
    check('control Ricci '+str(i),list(map(str,r))==c['Ricci'])
    check('control gaps '+str(i),list(map(str,gaps))==c['gaps'])
    check('control direct descent '+str(i),descended==c['direct_descent'])
    controls.append(dict(squared_sizes=c['squared_sizes'],Ricci=list(map(str,r)),gaps=list(map(str,gaps)),direct_descent=descended))
# Authenticate prior actual mutants and compare their saved false outputs to
# this context's sealed geometry. This rechecks correspondence, not executions.
false_outputs=[]
for result in mutants['results']:
    p=prior/result['mutant_path']
    check('prior mutant source hash '+result['name'],sha(p)==result['mutant_sha256'])
    hashes[str(p)]=sha(p)
    if result['author_rejected']:
        check('prior mutant rejection receipt '+result['name'],result['author_failure']['type']=='AssertionError')
    else:
        saved=json.loads(result['stdout'])
        failures=[]
        for i,c in enumerate(saved['controls']):
            for field in ['Ricci','gaps','direct_descent']:
                if c[field]!=controls[i][field]:
                    failures.append(dict(control=i,field=field,reported=c[field],expected=controls[i][field]))
        check('source-first geometry rejects prior saved false output '+result['name'],bool(failures))
        false_outputs.append(dict(name=result['name'],source_sha256=result['mutant_sha256'],failures=failures))
check('retain exactly two BI2 reporting blind spots',len(false_outputs)==2)
(base/'EXPOSED_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
record=dict(all_pass=all(c['passed'] for c in checks),count=len(checks),checks=checks,
    exact_recomputed_controls=controls,prior_false_outputs_rechecked=false_outputs,
    evidence_type='Post-seal saved-tensor comparison against independently sealed source-first 4D calculation; prior checks/mutations authenticated and reused, not rerun',
    prior_counts=dict(spacetime=old['check_count'],comparison=old_comparison['check_count'],additional_mutants=mutants['count'],author_rejections=mutants['author_rejections'],false_outputs=mutants['author_false_passes_independently_detected']))
print(json.dumps(record,indent=2))
raise SystemExit(0 if record['all_pass'] else 1)
