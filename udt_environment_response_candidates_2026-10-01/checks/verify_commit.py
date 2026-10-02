from pathlib import Path
import csv,hashlib,json,subprocess,sys
b=Path('udt_environment_response_candidates_2026-10-01'); manifest=b/'SHA256_MANIFEST.tsv'
run=lambda *args:subprocess.check_output(args,text=True).strip()
rows=list(csv.DictReader(manifest.open(),delimiter='\t'))
expected={r['path']:r['sha256'] for r in rows}
expected[str(manifest)]=hashlib.sha256(manifest.read_bytes()).hexdigest()
changed=set(run('git','diff-tree','--no-commit-id','--name-only','-r','HEAD').splitlines())
assert changed==set(expected),(changed-set(expected),set(expected)-changed)
for p,digest in expected.items():
 assert hashlib.sha256(subprocess.check_output(['git','show','HEAD:'+p])).hexdigest()==digest,p
assert run('git','diff','--name-only')==''
assert run('git','diff','--cached','--name-only')==''
assert run('git','branch','--show-current')=='grok'
initial=set(json.loads((b/'SNAPSHOT.json').read_text())['initial_untracked_names'])
current=set(run('git','ls-files','--others','--exclude-standard').splitlines())
assert initial==current,(initial-current,current-initial)
freeze=json.loads((b/'INTEGRATION_FREEZE.json').read_text())
assert run('git','rev-parse','HEAD^')==freeze['base_head']
result={'head':run('git','rev-parse','HEAD'),'parent':run('git','rev-parse','HEAD^'),'committed_files_checked':len(expected),'committed_manifest_sha256':expected[str(manifest)],'tracked_clean':True,'preserved_untracked_names':len(initial),'branch':'grok'}
if len(sys.argv)>1 and sys.argv[1]=='remote':
 remote=run('git','ls-remote','origin','refs/heads/grok').split()[0]
 assert remote==result['head']==run('git','rev-parse','origin/grok')
 result['remote_verified']=remote
print(json.dumps(result,indent=2))
