import datetime
import hashlib
import json
from pathlib import Path
import subprocess

b=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
for n in ['SOURCE_HASHES.json','EXPOSED_HASHES.json']:
    for p,digest in json.loads((b/n).read_text()).items():
        checks.append(dict(path=p,expected=digest,actual=sha(Path(p)),passed=sha(Path(p))==digest))
seal=json.loads((b/'SOURCE_FIRST_SEAL.json').read_text())
for n,digest in seal['payload_sha256'].items():
    checks.append(dict(path=str(b/n),expected=digest,actual=sha(b/n),passed=sha(b/n)==digest))
checks.append(dict(path='SOURCE_FIRST_SEAL.json',passed=sha(b/'SOURCE_FIRST_SEAL.json')=='d8c0c56bf695004ad29cf1af00663e30051ee3c40b54df927fd4669745ae9ff1'))
head=subprocess.run(['git','--no-optional-locks','rev-parse','HEAD'],capture_output=True,text=True,check=True)
checks.append(dict(path='HEAD',passed=head.stdout.strip()=='8593f11cd96a575be3513d1ec56e92ac4f5811ff'))
print(json.dumps(dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),all_pass=all(c['passed'] for c in checks),
    count=len(checks),checks=checks,head_stdout=head.stdout,head_stderr=head.stderr,
    scope='Explicit pinned sources, candidate, prior review evidence and focused source-first payloads; no scientific upgrade'),indent=2))
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
