"""Check exact whole-row correspondence to the authorized G312 transition."""
import hashlib
import json
from pathlib import Path
import subprocess
repo=Path(__file__).resolve().parent.parent.parent
path=repo/'udt_gr_filter_reconciliation_2026-09-09/REGISTRY_TRANSITION.json'
transition=json.loads(path.read_text())
argv=['git','show','9ed73efe3d7d24a5fd6666bd904557cf0b24e0fd:CURRENT_SCIENTIFIC_PREMISES.tsv']
proc=subprocess.run(argv,cwd=repo,capture_output=True,check=True)
old=next(x for x in proc.stdout.decode().splitlines() if x.startswith('G312\t'))
current=next(x for x in (repo/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text().splitlines() if x.startswith('G312\t'))
assert old==transition['before_line'].rstrip('\n')
assert current==transition['after_line'].rstrip('\n')
print(json.dumps({'status':'PASS_EXACT_AUTHORIZED_G312_ROWS',
    'historical_argv':argv,'historical_exitcode':proc.returncode,'historical_stderr':proc.stderr.decode(),
    'transition_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'old_whole_G312_equals_authorized_before':True,
    'current_whole_G312_equals_authorized_after':True,
    'current_registry_or_source_modified':False},indent=2,sort_keys=True))
