#!/usr/bin/env python3
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def main():
    r=subprocess.run([sys.executable,str(HERE/'verify_repository_gates.py')],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode:raise AssertionError(r.stderr or r.stdout)
    x=json.loads(r.stdout);assert x['result']=='PASS';(HERE/'REPOSITORY_GATES.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
    print('PASS repository gate capture');return 0
if __name__=='__main__':raise SystemExit(main())
