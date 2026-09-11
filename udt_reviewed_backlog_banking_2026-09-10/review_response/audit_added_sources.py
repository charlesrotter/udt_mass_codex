"""Check added source pins and authenticate historical registry provenance."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

repo=Path(__file__).resolve().parent.parent.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
tm='udt_tidal_measurement_feasibility_campaign_2026-09-07'
manifests=[tm+'/SOURCE_SHA256SUMS',tm+'/step_01/review/SOURCE_SHA256SUMS',
    tm+'/step_02/review/SOURCE_SHA256SUMS',tm+'/step_01/review/REVIEW_SHA256SUMS',
    tm+'/step_02/review/REVIEW_SHA256SUMS']
pins=[]
for manifest in manifests:
    for line in (repo/manifest).read_text().splitlines():
        if not line.strip():continue
        expected,p=line.split(maxsplit=1)
        actual=sha((repo/p).read_bytes()) if (repo/p).is_file() else None
        pins.append({'manifest':manifest,'path':p,'expected_sha256':expected,
            'current_sha256':actual,'current_byte_match':actual==expected})
# Versioned original349 registry provenance is explicitly authenticated, never
# treated as current authority or silently substituted into current checks.
version='9ed73efe3d7d24a5fd6666bd904557cf0b24e0fd'
argv=['git','show',version+':CURRENT_SCIENTIFIC_PREMISES.tsv']
proc=subprocess.run(argv,cwd=repo,capture_output=True,check=True)
expected='ccd1fd2752a5884dfa2864fc9f3904f9dcc7e22557f6d4057e92ec2c54caf81f'
assert sha(proc.stdout)==expected
old=list(csv.DictReader(io.StringIO(proc.stdout.decode()),delimiter='\t'))
current=list(csv.DictReader((repo/'CURRENT_SCIENTIFIC_PREMISES.tsv').open(),delimiter='\t'))
now={r['premise_id']:r for r in current}
differences=[]
for row in old:
    assert row['premise_id'] in now
    cols=[k for k in row if row[k]!=now[row['premise_id']][k]]
    if cols:differences.append({'id':row['premise_id'],'columns':cols})
assert differences==[{'id':'G312','columns':['current_status','active_use','open_scope','forbidden_regression','precedence_rule']}],differences
assert len(old)==349
# Only registry-history differences are expected in these scientific/source pins.
unexpected=[p for p in pins if not p['current_byte_match'] and p['path']!='CURRENT_SCIENTIFIC_PREMISES.tsv']
assert not unexpected,unexpected
for p in pins:
    if not p['current_byte_match']:assert p['expected_sha256']==expected
print(json.dumps({'status':'PASS_CURRENT_SOURCE_PINS_AND_AUTHENTICATED_349_HISTORY',
    'pins':pins,'historical_registry':{'argv':argv,'git_exitcode':proc.returncode,
        'git_stderr':proc.stderr.decode(),'sha256':sha(proc.stdout),'rows':len(old)},
    'current_registry_rows':len(current),'old_row_differences':differences,
    'current_authority':'udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md',
    'current_authority_sha256':sha((repo/'udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md').read_bytes()),
    'interpretation':'Old349 registry snapshot authenticated at exact Git bytes. Existing rows differ only in five current G312 authority cells; source mathematics remains byte-identical. Current authority wins; no historical substitution made.'},indent=2,sort_keys=True))
