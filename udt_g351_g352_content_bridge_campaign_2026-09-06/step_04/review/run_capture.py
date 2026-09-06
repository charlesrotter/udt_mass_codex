import datetime
import json
import pathlib
import resource
import subprocess
import sys
import time

root = pathlib.Path(__file__).resolve().parent
name, cwd, *command = sys.argv[1:]
paths = [root / (name + suffix) for suffix in ('.stdout', '.stderr', '.json')]
assert not any(path.exists() for path in paths), 'refuse evidence overwrite'

def limits():
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))

started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.monotonic()
try:
    result = subprocess.run(command, cwd=cwd, capture_output=True,
                            timeout=60, preexec_fn=limits)
    code, out, err, timeout = result.returncode, result.stdout, result.stderr, False
except subprocess.TimeoutExpired as exc:
    code, out, err, timeout = None, exc.stdout or b'', exc.stderr or b'', True
duration = time.monotonic() - t0
for path, data in zip(paths[:2], [out, err]):
    with path.open('xb') as stream:
        stream.write(data)
record = dict(command=command, cwd=cwd, started_utc=started,
              duration_seconds=duration, returncode=code, timeout=timeout,
              address_space_bytes=512 * 1024**2, cpu_seconds=60,
              maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
with paths[2].open('x') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
print(json.dumps(record, sort_keys=True))
sys.exit(0 if code == 0 else 1)
