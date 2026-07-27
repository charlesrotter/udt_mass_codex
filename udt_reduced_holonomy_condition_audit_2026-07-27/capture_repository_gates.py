#!/usr/bin/env python3
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def main():
    done=subprocess.run([sys.executable,str(HERE/'verify_repository_gates.py')],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if done.returncode:raise AssertionError(done.stderr or done.stdout)
    value=json.loads(done.stdout);assert value['result']=='PASS';(HERE/'REPOSITORY_GATES.json').write_text(json.dumps(value,indent=2,sort_keys=True)+'\n');print('PASS repository gate capture');return 0
if __name__=='__main__':raise SystemExit(main())
