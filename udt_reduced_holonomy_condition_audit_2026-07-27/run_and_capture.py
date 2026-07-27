#!/usr/bin/env python3
from __future__ import annotations
import json,os,platform,subprocess,sys
from pathlib import Path
import numpy,sympy,torch
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
def execute(script):
    env=dict(os.environ);env.update({'CUDA_VISIBLE_DEVICES':'','PYTHONDONTWRITEBYTECODE':'1'})
    done=subprocess.run([sys.executable,str(HERE/script)],cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if done.returncode:raise AssertionError(done.stderr or done.stdout)
    return done.stdout,done.stderr,json.loads(done.stdout)
def main():
    out,err,prod=execute('derive_reduced_holonomy.py');(HERE/'DERIVATION_STDOUT.txt').write_text(out);(HERE/'DERIVATION_STDERR.txt').write_text(err)
    (HERE/'DERIVATION_RESULT.json').write_text(json.dumps(prod,indent=2,sort_keys=True)+'\n')
    out,err,ind=execute('verify_reduced_holonomy_independent.py');(HERE/'INDEPENDENT_STDOUT.txt').write_text(out);(HERE/'INDEPENDENT_STDERR.txt').write_text(err)
    (HERE/'INDEPENDENT_RESULT.json').write_text(json.dumps(ind,indent=2,sort_keys=True)+'\n')
    assert prod['status']=='COMPUTED' and ind['status']=='PASS'
    env={'python':platform.python_version(),'platform':platform.platform(),'numpy':numpy.__version__,'sympy':sympy.__version__,'torch':torch.__version__,'dtype':'float64','cpu_only':True,'CUDA_VISIBLE_DEVICES':'','production_command':f'PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 {HERE.relative_to(ROOT)}/derive_reduced_holonomy.py','independent_command':f'PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 {HERE.relative_to(ROOT)}/verify_reduced_holonomy_independent.py'}
    (HERE/'RUN_ENVIRONMENT.json').write_text(json.dumps(env,indent=2,sort_keys=True)+'\n');print('PASS production and independent captures');return 0
if __name__=='__main__':raise SystemExit(main())
