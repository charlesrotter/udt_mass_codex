#!/usr/bin/env python3
"""Reuse the existing no-overwrite capture utility with explicit work-order limits.

This adapts only its five literal resource settings, in memory. No original
utility is changed and no new scientific implementation is supplied.
Usage: python3 capture_existing.py ABS_STEM SECONDS MIB COMMAND [ARGS...]
"""
import hashlib
import json
import os
from pathlib import Path
import sys

repo = Path(__file__).resolve().parent.parent
source = repo/'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py'
stem, seconds, mib, *command = sys.argv[1:]
seconds, mib = int(seconds), int(mib)
if not Path(stem).is_absolute() or not command or not (0 < seconds <= 900 and 0 < mib <= 2048):
    raise SystemExit('Require absolute evidence stem and authorized bounded limits')
Path(stem).parent.mkdir(parents=True, exist_ok=True)
raw = source.read_text()
changes = {
    '(512 * 1024**2, 512 * 1024**2)': f'({mib} * 1024**2, {mib} * 1024**2)',
    '(60, 60)': f'({seconds}, {seconds})',
    'timeout=60': f'timeout={seconds}',
    'address_space_bytes=512 * 1024**2': f'address_space_bytes={mib} * 1024**2',
    'cpu_seconds=60': f'cpu_seconds={seconds}',
}
adapted = raw
for old, new in changes.items():
    if raw.count(old) != 1:
        raise SystemExit('Capture adaptation target must be unique: '+old)
    adapted = adapted.replace(old, new, 1)
thread_env = {k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')}
os.environ.update(thread_env)
provenance = {'source':str(source.relative_to(repo)),
    'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),
    'adapted_capture_sha256':hashlib.sha256(adapted.encode()).hexdigest(),
    'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'replacements':changes, 'thread_environment':thread_env,
    'limits':{'seconds':seconds,'mib':mib}, 'command':command}
with Path(stem+'.capture_provenance.json').open('x') as stream:
    json.dump(provenance,stream,indent=2); stream.write('\n')
sys.argv = [str(source),stem,str(repo),*command]
exec(compile(adapted,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
