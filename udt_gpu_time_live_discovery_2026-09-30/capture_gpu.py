"""Reuse pinned capture implementation with CUDA virtual-address allowance.

This does not enlarge the PLAN physical working-data/allocation limits.
"""
from pathlib import Path
import hashlib, json, os, sys
sourcepath = Path('udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py').resolve()
source = sourcepath.read_text()
assert hashlib.sha256(source.encode()).hexdigest() == '8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef'
prefix, *command = sys.argv[1:]
for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[n] = '1'
changes = {'(512 * 1024**2, 512 * 1024**2)': '(128 * 1024**3, 128 * 1024**3)',
           '(60, 60)': '(600, 600)', 'timeout=60': 'timeout=600',
           'address_space_bytes=512 * 1024**2': 'address_space_bytes=128 * 1024**3',
           'cpu_seconds=60': 'cpu_seconds=600'}
for a,b in changes.items():
    assert a in source
    source=source.replace(a,b)
prefix=str(Path(prefix).resolve())
meta=Path(prefix+'.capture_provenance.json')
with meta.open('x') as f:
    json.dump({'source':str(sourcepath),'source_sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),
               'adapted_sha256':hashlib.sha256(source.encode()).hexdigest(),
               'cuda_virtual_address_limit_gib':128,'cpu_working_data_budget_gib':2,
               'gpu_allocated_budget_gib':24,'command':command}, f, indent=2)
sys.argv=[str(sourcepath),prefix,str(Path.cwd()),*command]
exec(compile(source,str(sourcepath),'exec'),{'__name__':'__main__','__file__':str(sourcepath)})
