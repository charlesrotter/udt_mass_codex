import datetime,hashlib,json,pathlib,subprocess
repo=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(__file__).resolve().parents[1]
inputs=root/'CLOSEOUT_PREMISE_INPUTS.json'
obj=json.loads(inputs.read_text());summary=json.loads((root/'CLOSEOUT_PREMISE_RESULT.json').read_text())
assert hashlib.sha256(inputs.read_bytes()).hexdigest()==summary['audit_input_record_sha256']
receipt=json.loads((root/'checks/current396_closeout.json').read_text())
assert receipt==summary['audit'] and receipt['returncode']==0 and not receipt['timeout']
assert (root/'checks/current396_closeout.stderr').read_bytes()==b''
assert 'PASS: 396-row premise registry' in (root/'checks/current396_closeout.stdout').read_text()
rows=[]
for p,digest in obj['sha256'].items():
 live=hashlib.sha256((repo/p).read_bytes()).hexdigest()
 frozen=hashlib.sha256(subprocess.check_output(['git','show','1de84bf0e8b8781201ede8d0486489a22dbf7d07:'+p],cwd=repo)).hexdigest()
 assert frozen==digest,('banked audit baseline',p)
 rows.append({'path':p,'banked_baseline_matches_audit_pin':True,'current_matches_audit_pin':live==digest})
print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Actual audit capture inspected, attributed not rerun; snapshot correspondence is not independent proof of run-time immutability',
 'duration_seconds':receipt['duration_seconds'],'input_rows':rows},indent=2))
