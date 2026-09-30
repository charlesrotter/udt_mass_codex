"""Save reproducible scope/readout correspondence receipts; no GPU imports."""
from pathlib import Path
import hashlib
import json
import resource
import subprocess
import sys
import time

resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
import numpy as np

started = time.monotonic()
HERE = Path(__file__).resolve().parent
B = HERE.parent.parent
ROOT = B.parent
source_map = json.loads((B/'PREVIOUS_REVIEW_RECORD.json').read_text())['accepted_sha256']
changed, missing = [], []
for name, expected in source_map.items():
    p = ROOT/name
    if not p.exists(): missing.append(name)
    elif hashlib.sha256(p.read_bytes()).hexdigest() != expected: changed.append(name)
a = json.loads((HERE/'SAVED_READOUT_RECOMPUTATION.json').read_text())
c = json.loads((B/'execution_repaired/CLOCK_READOUT.json').read_text())
log_error = float(np.max(np.abs(np.array([x['logZ'] for x in a['cases']])-c['logZ'])))
z_error = float(np.max(np.abs(np.array([x['Z'] for x in a['cases']])-c['Z'])))
ids_equal = [x['id'] for x in a['cases']] == [x['id'] for x in c['cases']]
assert log_error <= 2e-12 and z_error <= 2e-12 and ids_equal
assert len(source_map) == 643 and not missing
assert set(changed) == {'AGENTS.md', 'HANDOFF.md', 'LIVE.md'}
inputs = [ROOT/x for x in ('AGENTS.md','HANDOFF.md','LIVE.md','UDT_DEVELOPMENT.md')]
inputs += [B/x for x in ('WORK_ORDER.md','WORK_RECORD.md','checkpoint_io.py','smoke_runner.py',
                        'smoke_checks.py','LAUNCH.json','REPAIR_FREEZE.json',
                        'execution_repaired/CLOCK_READOUT.json','execution_repaired/SMOKE_RESULT.json')]
diff = subprocess.check_output(['git','diff','--','AGENTS.md','LIVE.md','HANDOFF.md'], cwd=ROOT)
with (HERE/'OPERATIONAL_DIFF.patch').open('xb') as f: f.write(diff)
result = {'status':'PASS', 'prior_accepted_map_count':len(source_map), 'changed':changed,
          'missing':missing, 'max_logZ_error':log_error, 'max_Z_error':z_error,
          'tolerance':2e-12, 'case_ids_match':ids_equal, 'python':sys.version,
          'numpy':np.__version__, 'elapsed_seconds':time.monotonic()-started, 'gpu_used':False,
          'reviewed_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
          'limitation':'source correspondence and operational scope; prior scientific reviews retained, not re-proved'}
with (HERE/'SCOPE_EVIDENCE.json').open('x') as f: json.dump(result,f,indent=2); f.write('\n')
print(json.dumps(result,indent=2))
