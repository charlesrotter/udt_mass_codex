"""Actual bounded in-memory hostile mutations; no shared file changes.
Mutant self-reported code hashes refer to original __file__, not mutant identity.
The enclosing SHA256 and full mutant source are the actual identities.
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import traceback

path=Path(__file__).with_name('check_bi2.py')
original=path.read_text()
mutations=[
    ('wrong Lambda evolution sign','kd=[r[i]+tau*k[i]-lam for i in range(3)]','kd=[r[i]+tau*k[i]+lam for i in range(3)]'),
    ('wrong normal-frame motion','br[0][i+1][i+1]=k[i]\n    br[i+1][0][i+1]=-k[i]',
     'br[0][i+1][i+1]=-k[i]\n    br[i+1][0][i+1]=k[i]'),
    ('wrong spatial Ricci coefficient','r=[(n[i]**2-(n[(i+1)%3]-n[(i+2)%3])**2)/2 for i in range(3)]',
     'r=[(n[i]**2-(n[(i+1)%3]-n[(i+2)%3])**2)/4 for i in range(3)]'),
    ('omit additional spectral degeneracy factor','(x[2]+x[i]-x[1-i])','s.S.One'),
    ('erase quotient metric Lie obstruction','Lie=-ad.T*horizontal-horizontal*ad','Lie=s.zeros(3)'),
]
results=[]
for name,before,after in mutations:
    assert original.count(before)==1,(name,original.count(before))
    mutant=original.replace(before,after,1)
    out,err=io.StringIO(),io.StringIO()
    failure=None
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        try:
            exec(compile(mutant,'<BI2 '+name+'>','exec'),{'__name__':'__main__','__file__':str(path.resolve())})
        except Exception as exc:
            failure=dict(type=type(exc).__name__,message=str(exc))
            traceback.print_exc()
    results.append(dict(name=name,mutant_sha256=hashlib.sha256(mutant.encode()).hexdigest(),
        mutant_source=mutant,rejected=failure is not None,failure=failure,
        stdout=out.getvalue(),stderr=err.getvalue()))
passed=all(r['rejected'] for r in results)
print(json.dumps(dict(status='PASS' if passed else 'FAIL',original_sha256=hashlib.sha256(original.encode()).hexdigest(),
                     results=results,count=len(results),rejected=sum(r['rejected'] for r in results),
                     scope='five declared defects only; not proof of complete error coverage'),indent=2))
raise SystemExit(0 if passed else 1)
