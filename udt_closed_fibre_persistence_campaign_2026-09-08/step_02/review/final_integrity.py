"""Final correspondence only. Does not replay a scientific or premise audit."""
import datetime
import hashlib
import json
import pathlib
import re
import subprocess

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
snap=json.loads((HERE/'SOURCE_SNAPSHOT.json').read_text())
changed={p:{'sealed':h,'current':sha(ROOT/p)} for p,h in snap['hashes'].items() if sha(ROOT/p)!=h}
allowed='udt_g376_g378_conditional_banking_2026-09-08/EXECUTION_RECORD.md'
assert set(changed)<=set([allowed]),changed
freeze=HERE.parent/'CANDIDATE_FREEZE.md'
pins={n:sha(HERE.parent/n)==h for h,n in re.findall(r'^    ([0-9a-f]{64})  (.+)$',freeze.read_text(),re.M)}
assert pins and all(pins.values())
assert sha(HERE/'SOURCE_FIRST_SEAL.md')=='35f8a90819c250b035d4c91eeed258dfef779c88cadd29297fabe836dcf0e214'
assert sha(freeze)=='e69ac41987d57b1f97de98f2821c91cd977b51c9b6cb930602bacff5b9944091'
captures={}
for name,code in [('source_first_check',0),('post_exposure_check',1),('post_exposure_check_corrected',0)]:
    r=json.loads((HERE/(name+'.json')).read_text())
    assert r['returncode']==code and not r['timeout']
    assert r['address_space_bytes']==512*1024**2 and r['cpu_seconds']==60
    captures[name]=r
result=json.loads((HERE/'post_exposure_check_corrected.stdout').read_text())
assert len(result['author_replays'])==5
assert all(r['stdout_matches_author'] and r['stderr_matches_author'] and r['saved_receipt_returncode_matches'] for r in result['author_replays'])
assert len(result['actual_false_pass_probes'])==len(result['focused_reviewer_catches'])==2
assert all(r['author_suite_false_pass'] for r in result['actual_false_pass_probes'])
assert all(r['returncode']==1 for r in result['focused_reviewer_catches'])
audit_reuse={}
for n in ['prebank_358','postbank_361']:
    p=ROOT/'udt_g376_g378_conditional_banking_2026-09-08'
    r=json.loads((p/(n+'.json')).read_text())
    assert r['command']==['python3','-B','verify_current_scientific_premises.py']
    assert r['returncode']==0 and not r['timeout'] and r['cwd']==str(ROOT)
    assert all((p/(n+'.'+s)).read_bytes()==r[s].encode() for s in ['stdout','stderr'])
    audit_reuse[n]={'receipt_sha256':sha(p/(n+'.json')),'separate_streams_match':True,'replayed':False}
d=json.loads((HERE/'REVIEW_DISPOSITION.json').read_text())
assert d['disposition']=='VERIFIED-WITH-CAVEATS' and not d['unresolved_load_bearing_objections']
assert not d['scientific_repair_required'] and d['author_repair_cycles_consumed_by_reviewer']==0
assert len(d['defects'])==2
author_hashes={p.name:sha(p) for p in HERE.parent.iterdir() if p.is_file() and (p.name.startswith('check_') or p.name in ['QUESTION.md','CANDIDATE_INITIAL.md','CANDIDATE_FREEZE.md','REVIEW_DISPATCH.md'])}
review_hashes={p.name:sha(p) for p in HERE.iterdir() if p.is_file() and not p.name.startswith('final_integrity.') and p.name!='FINAL_REVIEW_SEAL.md'}
review_hashes['final_integrity.py']=sha(HERE/'final_integrity.py')
print(json.dumps({'status':'PASS_CORRESPONDENCE_ONLY','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),'source_snapshot_changes':changed,'author_freeze_pins':pins,'parent_audits':audit_reuse,'captures':captures,'author_file_sha256':author_hashes,'review_file_sha256':review_hashes,'limits':'Hashes/receipts check correspondence; no fresh scientific proof, network sync, full audit or host-wide preservation claim.'},indent=2))
