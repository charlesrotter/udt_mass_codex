"""Portable evidence runner. Generated records stay beside this file."""
from pathlib import Path
import datetime, hashlib, json, resource, subprocess, sys, time

root = Path(__file__).resolve().parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def limits():
    resource.setrlimit(resource.RLIMIT_AS, (512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU, (60,60))
command = [sys.executable,"-B",str(root/"stage_a_checks.py")]
start, tick = now(), time.monotonic()
result = subprocess.run(command,cwd=root,capture_output=True,timeout=60,preexec_fn=limits)
(root/"stage_a_checks.stdout").write_bytes(result.stdout)
(root/"stage_a_checks.stderr").write_bytes(result.stderr)
record={"command":command,"cwd":str(root),"start_utc":start,"end_utc":now(),
        "duration_seconds":time.monotonic()-tick,"child_exit":result.returncode,
        "python":sys.version,"memory_limit_bytes":512*1024**2,"timeout_seconds":60,
        "max_child_rss_kib":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        "stdout_sha256":hashlib.sha256(result.stdout).hexdigest(),
        "stderr_sha256":hashlib.sha256(result.stderr).hexdigest()}
(root/"STAGE_A_RUN.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record,indent=2))
print(result.stdout.decode())
sys.exit(result.returncode)
