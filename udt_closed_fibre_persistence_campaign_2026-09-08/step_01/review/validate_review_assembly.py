"""Correspondence/assembly checks only; not a theorem or independent review."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

review=Path(__file__).resolve().parent
step=review.parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name): return json.loads((review/name).read_text())
result=read('REVIEW_RESULT.json')
assert result['disposition']=='VERIFIED-WITH-CAVEATS'
assert result['unresolved_load_bearing_objections']==[]
for key,name in [('candidate_sha256','CANDIDATE_INITIAL.md'),
                 ('candidate_freeze_sha256','CANDIDATE_FREEZE.md'),
                 ('author_checker_sha256','check_cf1.py')]:
    assert sha(step/name)==result[key], name
assert sha(review/'SOURCE_FIRST_SEAL.md')==result['source_first_seal_sha256']
concurrent_surfaces={'AGENTS.md','LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md',
                     'CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_SCIENTIFIC_PREMISES.tsv',
                     'verify_current_scientific_premises.py','INDEX.md','MEMORY.md'}
snapshot_changes=[]
for expected,name in re.findall(r'^([a-f0-9]{64})  (.+)$',
                               (review/'SOURCE_FIRST_SEAL.md').read_text(),re.M):
    actual=sha(Path(name))
    if expected!=actual:
        assert name in concurrent_surfaces, name
        snapshot_changes.append({'path':name,'sealed_sha256':expected,'current_sha256':actual,
                                 'classification':'concurrent shared surface; not covered by reused snapshot audit'})
first=read('source_first_run.stdout')
assert first['all_passed'] and len(first['checks'])==331 and len(first['cases'])==55
assert all(x['passed'] for x in first['checks'])
replay=read('author_replay_driver.stdout')
assert replay['all_expected_outcomes'] and len(replay['rows'])==5
assert all(x['saved_stdout_byte_identical'] for x in replay['rows'])
false=read('false_pass_either_axis.stdout')
catch=read('catch_either_axis.stdout')
assert false['passed']==29 and false['failed']==[]
assert catch['passed']==37 and catch['failed']==['regular_2','regular_1/2']
receipts=[]
for prefix,expected_exit in [('source_first_run',0),('author_replay_driver',0),
                            ('false_pass_either_axis',0),('catch_either_axis',1)]:
    r=read(prefix+'.json')
    assert r['returncode']==expected_exit and not r['timeout']
    assert r['address_space_bytes']==536870912 and r['cpu_seconds']==60
    assert (review/(prefix+'.stderr')).read_bytes()==b''
    receipts.append({'prefix':prefix, 'returncode':r['returncode'],
                     'duration_seconds':r['duration_seconds'],'maxrss_kib':r['maxrss_kib']})
report=(review/'REVIEW_REPORT.md').read_text()
for phrase in ['VERIFIED-WITH-CAVEATS','29/29','37/39','331','CF2']:
    assert phrase in report
author_pins=[]
for name in ['CANDIDATE_FREEZE.md','CANDIDATE_INITIAL.md','check_cf1.py','QUESTION.md']:
    author_pins.append({'path':str(step/name),'sha256':sha(step/name)})
for mode in ['baseline','integer_only','all_rational_regular','wrong_period','swap_axes']:
    for suffix in ['stdout','stderr','json']:
        name='check_'+mode+'.'+suffix
        author_pins.append({'path':str(step/name),'sha256':sha(step/name)})
print(json.dumps({'kind':'assembly and byte-correspondence verification, not scientific evidence',
                  'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                  'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
                  'all_assembly_checks_passed':True,'retained_expected_receipts':receipts,
                  'source_snapshot_changes':snapshot_changes,'author_artifact_pins':author_pins},indent=2))
