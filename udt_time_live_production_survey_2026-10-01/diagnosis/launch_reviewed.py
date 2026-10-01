"""Durable starts of the finite reviewed diagnostic stages, without time cutoffs."""
import argparse, datetime, hashlib, json, subprocess, sys
from pathlib import Path

D = Path(__file__).resolve().parent
B = D.parent
ROOT = B.parent

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read(p):
    return json.loads(Path(p).read_text())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['first_pair', 'continuation', 'original_clocks'])
    args = ap.parse_args()
    manifest = D / 'repair_runtime/campaign.json'
    bound = {}
    if args.stage == 'original_clocks':
        review = D / 'review_runtime/CLOCK_COMPLETION_REVIEW.json'
        freeze = D / 'review_runtime/CLOCK_COMPLETION_FREEZE.json'
        r = read(review)
        if r['freeze_sha256'] != sha(freeze) or any(r[k] != 'CLEARED' for k in ['parent_source_review', 'math_source_review', 'scientific_diagnostic_readouts']):
            raise ValueError('CLOCK_REVIEW_REQUIRED')
        prefix = D / 'checks/original_clocks'
        command = [sys.executable, str(D / 'review_runtime/clock_completion.py')]
        bound = {str(p.relative_to(ROOT)): sha(p) for p in [review, freeze]}
        gpu = []
    else:
        paths = [D / 'review_math/REPAIR_READINESS.json', D / 'review_runtime/REPAIR_PRELAUNCH_REVIEW.json', D / 'PARENT_REPAIR_REVIEW.json']
        for p, key, expected in zip(paths, ['manifest_sha256', 'repair_manifest_sha256', 'manifest_sha256'], ['PASS', 'FIRST_PAIR_OPERATIONAL_GATE_CLEARED', 'CLEARED']):
            r = read(p)
            if r['status'] != expected or r[key] != sha(manifest):
                raise ValueError('REPAIR_REVIEW_REQUIRED')
        if args.stage == 'continuation':
            p = D / 'FIRST_PAIR_GATE.json'
            r = read(p)
            if r['status'] != 'PASS' or r['manifest_sha256'] != sha(manifest):
                raise ValueError('ACTUAL_FIRST_PAIR_REQUIRED')
            paths.append(p)
        for p, h in read(manifest)['source_sha256'].items():
            if sha(p) != h:
                raise ValueError('MANIFEST_SOURCE_CHANGED: ' + p)
        bound = {str(p.relative_to(ROOT)): sha(p) for p in paths + [manifest]}
        prefix = D / 'repair_runtime' / args.stage
        command = [sys.executable, str(B / 'supervise.py'), str(manifest), str(D / 'repair_runtime')]
        if args.stage == 'first_pair':
            command += ['--stop-after', '2']
        gpu = ['--gpu']
    call = [sys.executable, str(B / 'capture.py'), *gpu, str(prefix), *command]
    outputs = {s: Path(str(prefix) + '.' + s) for s in ['launch.json', 'controller.stdout', 'controller.stderr', 'json', 'stdout', 'stderr']}
    if any(p.exists() for p in outputs.values()):
        raise ValueError('REFUSE_LAUNCH_OVERWRITE')
    with outputs['controller.stdout'].open('x') as out, outputs['controller.stderr'].open('x') as err:
        process = subprocess.Popen(call, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out, stderr=err, start_new_session=True, close_fds=True)
    stat = Path('/proc') / str(process.pid) / 'stat'
    try:
        identity = stat.read_text().rsplit(')', 1)[1].split()[19]
    except FileNotFoundError:
        identity = None
    result = dict(stage=args.stage, pid=process.pid, proc_start_ticks=identity, command=call, cwd=str(ROOT), utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), source_sha256=bound, launcher_sha256=sha(__file__), capture_sha256=sha(B / 'capture.py'), wall_timeout_seconds=None, cpu_timeout_seconds=None, receipt=str(prefix)+'.json', manual_stop='Verify PID/start identity then SIGTERM capture PID for forwarding. No automatic elapsed-time stop.')
    with outputs['launch.json'].open('x') as stream:
        json.dump(result, stream, indent=2); stream.write('\n')
    print(json.dumps(result), flush=True)

if __name__ == '__main__':
    main()
