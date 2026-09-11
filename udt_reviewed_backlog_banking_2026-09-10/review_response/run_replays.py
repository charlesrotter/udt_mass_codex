"""Execute the frozen unchanged-code review plan; no scientific formulas."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
repo = out.parent.parent
plan = json.loads((out/'REPLAY_PLAN.json').read_text())
env = os.environ.copy()
env.update(plan['thread_environment'])
env['PYTHONDONTWRITEBYTECODE'] = '1'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
wrapper = repo/'udt_reviewed_backlog_banking_2026-09-10/capture_existing.py'
results = []
for run in plan['runs']:
    assert sha(repo/run['script']) == run['script_sha256'], run['script']
    for suffix, digest in run['saved_sha256'].items():
        assert sha(repo/(run['saved_stem']+suffix)) == digest
    stem = out/('replay_'+run['name'])
    argv = [sys.executable, '-B', str(wrapper), str(stem), '120', '512'] + run['argv']
    proc = subprocess.run(argv, cwd=repo, env=env, capture_output=True)
    for suffix, data in [('.launch.stdout',proc.stdout),('.launch.stderr',proc.stderr)]:
        with Path(str(stem)+suffix).open('xb') as stream:
            stream.write(data)
    receipt_path = Path(str(stem)+'.json')
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
    comparison = {}
    for suffix in ['.stdout','.stderr']:
        p = Path(str(stem)+suffix)
        comparison[suffix] = {'exists':p.exists(), 'sha256':sha(p) if p.exists() else None,
            'saved_sha256':run['saved_sha256'][suffix],
            'byte_identical':p.exists() and sha(p)==run['saved_sha256'][suffix]}
    row = {'name':run['name'],'launch_argv':argv,'launch_returncode':proc.returncode,
        'receipt':receipt,'comparison':comparison}
    results.append(row)
    print(json.dumps({'name':run['name'],'returncode':proc.returncode,
        'stdout_byte_identical':comparison['.stdout']['byte_identical'],
        'stderr_byte_identical':comparison['.stderr']['byte_identical'],
        'seconds':receipt['duration_seconds'] if receipt else None}), flush=True)
    if proc.returncode != 0 or not all(c['byte_identical'] for c in comparison.values()):
        break
summary = {'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'plan_sha256':sha(out/'REPLAY_PLAN.json'), 'thread_environment':plan['thread_environment'],
    'results':results,'all_pass':len(results)==len(plan['runs']) and all(
        r['launch_returncode']==0 and all(c['byte_identical'] for c in r['comparison'].values())
        for r in results)}
with (out/'REPLAY_RESULTS.json').open('x') as stream:
    json.dump(summary,stream,indent=2);stream.write('\n')
raise SystemExit(0 if summary['all_pass'] else 1)
