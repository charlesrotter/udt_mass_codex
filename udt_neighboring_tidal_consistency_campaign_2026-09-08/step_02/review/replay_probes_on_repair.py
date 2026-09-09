"""Reapply EXACT original NT2 corruption rules, changing only target filename."""
import hashlib
import json
from pathlib import Path

path=Path(__file__).resolve().with_name('run_development_probe.py')
source=path.read_text()
old="/'check_development.py'"
new="/'check_development_repaired.py'"
assert source.count(old)==1
modified=source.replace(old,new)
print(json.dumps({'original_probe_sha256':hashlib.sha256(source.encode()).hexdigest(),
 'replay_change_only':[old,new],
 'replayed_probe_sha256':hashlib.sha256(modified.encode()).hexdigest()}),flush=True)
exec(compile(modified,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
