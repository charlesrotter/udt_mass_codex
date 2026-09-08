"""Final bounded evidence correspondence, with SHA256 manifest; not science replay."""
import datetime
import hashlib
import json
from pathlib import Path
import re

root=Path.cwd()
step=root/'udt_berger_initial_data_preservation_campaign_2026-09-08/step_01'
review=step/'review'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
checks=[]
def check(name,value):
    checks.append({'name':name,'pass':bool(value)})
check('sealed manifest unchanged',sha(review/'source_first_hashes.stdout')==
      'f33db4ea6bb25ebc090ec83bd7b7cbce443484aa22ee1e24430b0efed9227bec')
for line in (review/'source_first_hashes.stdout').read_text().splitlines():
    expected,name=line.split('  ',1)
    check('sealed payload '+name,sha(root/name)==expected)
check('source seal unchanged',sha(review/'SOURCE_FIRST_SEAL.md')==
      'eae600025c2602e6fb704497d7b11f0eab2b6c5f08cd56aebb1fd148baed7a6e')
check('candidate freeze unchanged',sha(step/'CANDIDATE_FREEZE.md')==
      '4733699b0158ccc9d443b58467058157ec562543b526fe228d8393bd9499dfb1')
for expected,name in re.findall(r'^    ([0-9a-f]{64})  (\S+)\s*$',
                              (step/'CANDIDATE_FREEZE.md').read_text(),re.M):
    check('frozen author payload '+name,sha(step/name)==expected)
check('author regression exact bytes',(review/'author_regression.stdout').read_bytes()==
      (step/'author_check_02.stdout').read_bytes())
captures=['source_first_run','source_first_hashes','intake_authentication',
          'candidate_comparison','author_regression','mutation_probe_run']
for stem in captures:
    receipt=json.loads((review/(stem+'.json')).read_text())
    check('capture success '+stem,receipt['returncode']==0 and receipt['timeout'] is False)
    check('capture resources '+stem,receipt['address_space_bytes']==536870912
          and receipt['cpu_seconds']==60 and receipt['duration_seconds']<60
          and receipt['maxrss_kib']*1024<536870912)
for stem in ['source_first_run','intake_authentication','candidate_comparison']:
    result=json.loads((review/(stem+'.stdout')).read_text())
    check('saved exact checks '+stem,result['all_pass'] and all(c['pass'] for c in result['checks']))
mut=json.loads((review/'mutation_probe_run.stdout').read_text())
check('mutation blind spots preserved',mut['author_rejections']==6 and len(mut['author_survivors'])==2
      and mut['all_detected_by_author_or_independent'])
check('each mutant code hash',all(hashlib.sha256(m['mutant_source'].encode()).hexdigest()==m['mutant_sha256']
      for m in mut['results']))
check('final result verdict',json.loads((review/'REVIEW_RESULT.json').read_text())['verdict']=='VERIFIED-WITH-CAVEATS')
manifest={str(path.relative_to(root)):sha(path) for path in sorted(review.iterdir()) if path.is_file()}
out={'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'all_pass':all(c['pass'] for c in checks),'checks':checks,
     'review_artifact_manifest_sha256':manifest,
     'scope':'Correspondence only; excludes this capture stdout/stderr/receipt because they are generated after this script exits. Final review seal hashes those separately.'}
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['all_pass'] else 1)
