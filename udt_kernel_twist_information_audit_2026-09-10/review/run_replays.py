#!/usr/bin/env python3
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

p=Path(__file__).resolve().parent
cases=[('author_exact_replay',[sys.executable,str(p.parent/'check_candidate.py')],0,None),
 ('author_optimized_guard',[sys.executable,'-O',str(p.parent/'check_candidate.py')],1,'Evidence diagnostics require assertions enabled'),
 ('initial_failure_reproduction',[sys.executable,str(p/'reproduce_initial_failure.py')],1,'Matrix size mismatch: (3, 3) + (3, 1)'),
 ('author_mutant_guard_replay',[sys.executable,str(p/'replay_author_guards.py')],0,None),
 ('author_harness_guards',[sys.executable,str(p/'check_author_harness_guards.py')],0,None)]
records=[]
for stem,cmd,expected,needle in cases:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(); begin=time.monotonic()
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
 (p/(stem+'.stdout.txt')).write_text(r.stdout)
 (p/(stem+'.stderr.txt')).write_text(r.stderr)
 record={'case':stem,'command':cmd,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'elapsed_seconds':time.monotonic()-begin,'exit_code':r.returncode,'expected_exit_code':expected,'timeout_seconds':120,
  'device':'CPU','cwd':str(Path.cwd()),'expected_error_substring':needle,
  'expected_result_observed':r.returncode==expected and (needle is None or needle in r.stderr),
  'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()}
 if r.returncode==0:
  data=json.loads(r.stdout)
  record['output_status']=data.get('status')
  record['output_check_count']=data.get('check_count',len(data.get('guard_rejections',[])))
 (p/(stem+'.run.json')).write_text(json.dumps(record,indent=2)+'\n')
 records.append(record)
 if not record['expected_result_observed']:
  raise AssertionError(record)
(p/'REPLAY_RESULTS.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{'case':r['case'],'exit_code':r['exit_code'],'expected_result_observed':r['expected_result_observed'],'check_count':r.get('output_check_count')} for r in records],indent=2))
