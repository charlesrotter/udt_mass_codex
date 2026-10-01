"""CPU-only fail-closed catches; Torch imports are blocked explicitly."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
FIXTURES = HERE/'guard_fixtures'
FIXTURES.mkdir(exist_ok=False)
base = json.loads((BASE/'specs/n8.json').read_text())
cases = [
    ('nan_threshold', 'constraint_limit', float('nan'), 'INVALID_CONSTRAINT_LIMIT'),
    ('zero_threshold', 'constraint_limit', 0, 'INVALID_CONSTRAINT_LIMIT'),
    ('negative_threshold', 'constraint_limit', -1, 'INVALID_CONSTRAINT_LIMIT'),
    ('loose_threshold', 'constraint_limit', 2.1e-5, 'INVALID_CONSTRAINT_LIMIT'),
    ('wrong_period', 'period', base['period']+.1, 'INITIAL_PERIOD_MISMATCH'),
    ('nan_period', 'period', float('nan'), 'INITIAL_PERIOD_MISMATCH'),
    ('zero_gpu', 'gpu_bytes', 0, 'INVALID_BUDGET'),
    ('negative_gpu', 'gpu_bytes', -1, 'INVALID_BUDGET'),
    ('float_gpu', 'gpu_bytes', 100., 'INVALID_BUDGET'),
    ('zero_output', 'output_bytes', 0, 'INVALID_BUDGET'),
    ('negative_output', 'output_bytes', -1, 'INVALID_BUDGET'),
    ('float_output', 'output_bytes', 100., 'INVALID_BUDGET'),
]
launcher = '''import runpy,sys
class NoTorch:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0]=='torch': raise RuntimeError('UNEXPECTED_TORCH_IMPORT')
sys.meta_path.insert(0,NoTorch())
sys.argv=sys.argv[1:]
runpy.run_path(sys.argv[0],run_name='__main__')
'''
records=[]
for name,key,value,reason in cases:
    spec=dict(base);spec[key]=value
    specpath=FIXTURES/f'{name}.json';run=FIXTURES/f'{name}_run'
    specpath.write_text(json.dumps(spec,indent=2)+'\n')
    command=[sys.executable,'-c',launcher,str(BASE/'run_smoke.py'),str(specpath),str(run)]
    result=subprocess.run(command,cwd=BASE.parent,env=dict(os.environ,CUDA_VISIBLE_DEVICES='',CUBLAS_WORKSPACE_CONFIG=':4096:8'),capture_output=True,timeout=10)
    (FIXTURES/f'{name}.stdout').write_bytes(result.stdout)
    (FIXTURES/f'{name}.stderr').write_bytes(result.stderr)
    actual=json.loads(result.stderr)
    assert result.returncode==2 and actual['reason']==reason,(name,result.returncode,actual)
    assert not run.exists(),name
    records.append(dict(case=name,returncode=result.returncode,reason=actual['reason'],run_created=False,
                        spec_sha256=hashlib.sha256(specpath.read_bytes()).hexdigest(),command=command))
print(json.dumps(dict(status='GUARD_REPAIR_CATCHES_PASS',checks=records,
    runner_sha256=hashlib.sha256((BASE/'run_smoke.py').read_bytes()).hexdigest(),
    scope='CPU fail-closed pre-Torch guards only; Torch import explicitly blocked; no GPU'),indent=2))
