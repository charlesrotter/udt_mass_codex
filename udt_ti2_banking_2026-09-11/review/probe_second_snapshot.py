"""Freeze actual changed-second-read exposure in eleven historical adapters."""
from pathlib import Path
import csv
import datetime
import io
import json
import sys
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import verify_current_scientific_premises as v
target=ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv'
raw=target.read_bytes()
poison=raw.replace(b'NOT_PHYSICAL_ADOPTION',b'PHYSICAL_LAW_ADOPTED',1)
assert poison != raw
assert next(x for x in poison.splitlines() if x.startswith(b'G414\t')) != next(x for x in raw.splitlines() if x.startswith(b'G414\t'))
real_read_tsv=v.read_tsv
results=[]
for name in ['validate_conditional_banking','validate_shared_constraint_banking',
 'validate_persistence_banking','validate_restrictiveness_banking',
 'validate_source_metric_banking','validate_reconstruction_banking',
 'validate_coupled_banking','validate_vacuum_scale_banking','validate_berger_banking',
 'validate_closed_fibre_banking','validate_neighboring_tidal_banking']:
 seen=[]
 def changed_read(path):
  if path==target:
   seen.append(path)
   return list(csv.DictReader(io.StringIO(poison.decode()),delimiter='\t'))
  return real_read_tsv(path)
 with patch.object(v,'read_tsv',changed_read):
  try:
   getattr(v,name)(ROOT,authenticate_sources=False)
   outcome='FALSE_PASS_CHANGED_SECOND_SNAPSHOT' if seen else 'NO_SECOND_REGISTRY_READ'
  except SystemExit as exc:
   outcome='REJECTED: '+str(exc)
 results.append({'guard':name,'second_registry_reads':len(seen),'outcome':outcome})
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verifier_sha256':__import__('hashlib').sha256(Path(v.__file__).read_bytes()).hexdigest(),
 'results':results,'mutation':'monkeypatched parsed second read; real sources unchanged'},indent=2))
assert not any(r['outcome'].startswith('FALSE_PASS') for r in results), 'present changed G414 was discarded on unvalidated second registry snapshot'
