"""Independent point-in-time correspondence for the running parent audit inputs."""
from pathlib import Path
import datetime
import hashlib
import json
repo=Path(__file__).resolve().parents[2]
bank=repo/'udt_ti2_banking_2026-09-11'
record=json.loads((bank/'FULL397_INPUTS.json').read_text())
rows=[]
for path,expected in record['sha256'].items():
 actual=hashlib.sha256((repo/path).read_bytes()).hexdigest()
 rows.append({'path':path,'expected':expected,'actual':actual,'equal':actual==expected})
assert all(x['equal'] for x in rows), [x for x in rows if not x['equal']]
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'PASS','matching_input_count':len(rows),'inputs':rows,
 'scope':'point-in-time correspondence; parent full397 execution/outcome not rerun or anticipated'},indent=2))
