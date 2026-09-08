"""Post-seal end-to-end probes of the author's eight advertised omission contrasts.

No source file is changed. Exact original and mutant program texts/streams are
preserved in this capture. Mutants run in this same interpreter, not new agents.
Successful mutant self-hashes refer to its supplied __file__, so are explicitly
NOT mutation identity; the enclosing exact mutant SHA256 is controlling.
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import traceback
import sympy as S

step=Path('udt_berger_initial_data_preservation_campaign_2026-09-08/step_01')
path=step/'check_bi1.py'
original=path.read_text()
independent=json.loads((step/'review/source_first_run.stdout').read_text())
p,q=S.symbols('p q',positive=True)
x,y,z,u,v,w=S.symbols('x y z u v w',real=True)
own_symbols=dict(zip(['p','q','x','y','z','u','v','w'],[p,q,x,y,z,u,v,w]))
own_S=S.sympify(independent['homogeneous_Ricci_dot'],locals=own_symbols)
mutations=[
 ('omit raising term','Bdot=S+2*K*Ric','Bdot=S'),
 ('force symmetric projector','checks=[]','Pd=(Pd+Pd.T)/2\nchecks=[]'),
 ('omit momentum connection','M=s.Matrix([s.expand(sum(DK[i][i,j] for i in range(3))) for j in range(3)])','M=s.zeros(3,1)'),
 ('admit vertical shear in fixtures','z:s0,r:0,t:0','z:s0,r:1,t:1'),
 ('erase horizontal shear in block','block=s.Matrix([[C-V+d,ss,0],[ss,C-V-d,0],[0,0,V]])','block=s.Matrix([[C-V,0,0],[0,C-V,0],[0,0,V]])'),
 ('wrong norm sign Hamiltonian','s.trace(block)**2-s.trace(block*block)','s.trace(block)**2+s.trace(block*block)'),
 ('wrong negative K sign in covariant Ricci variation','M=s.Matrix([','S=-S\nM=s.Matrix(['),
 ('drop derivative-index connection','G[h][k][l]*DK[l][i,j]','s.S.Zero'),
]
results=[]
for name,before,after in mutations:
    assert original.count(before)==1,(name,original.count(before))
    mutant=original.replace(before,after,1)
    stdout,stderr=io.StringIO(),io.StringIO()
    namespace={'__name__':'__main__','__file__':str(path.resolve())}
    exception=None
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
        try:
            exec(compile(mutant,f'<BI1 mutant: {name}>','exec'),namespace)
        except Exception as exc:
            exception={'type':type(exc).__name__,'message':str(exc)}
            traceback.print_exc()
    independent_difference=None
    independent_detects=False
    if exception is None:
        mapping={namespace['u']:x,namespace['w']:y,namespace['v']:z,
                 namespace['z']:u,namespace['r']:v,namespace['t']:w}
        difference=S.simplify(namespace['S'].xreplace(mapping)-own_S)
        independent_difference=str(difference)
        independent_detects=any(entry!=0 for entry in difference)
    results.append({'name':name,'before':before,'after':after,
        'original_sha256':hashlib.sha256(original.encode()).hexdigest(),
        'mutant_sha256':hashlib.sha256(mutant.encode()).hexdigest(),'mutant_source':mutant,
        'author_regression_rejects':exception is not None,'exception':exception,
        'stdout':stdout.getvalue(),'stderr':stderr.getvalue(),
        'independent_sealed_oracle_detects_survivor':independent_detects,
        'independent_Ricci_difference':independent_difference})
out={'count':len(results),'results':results,
     'author_rejections':sum(r['author_regression_rejects'] for r in results),
     'author_survivors':[r['name'] for r in results if not r['author_regression_rejects']],
     'all_detected_by_author_or_independent':all(r['author_regression_rejects'] or r['independent_sealed_oracle_detects_survivor'] for r in results),
     'scope':'These are artificial incorrect programs, not changes to the candidate or its frozen implementation. Contrasts alone are not end-to-end catch proofs.'}
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['all_detected_by_author_or_independent'] else 1)
