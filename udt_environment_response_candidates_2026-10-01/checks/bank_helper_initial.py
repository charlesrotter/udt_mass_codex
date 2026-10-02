from pathlib import Path
import json,hashlib,csv,subprocess,sys,datetime
B=Path('udt_environment_response_candidates_2026-10-01')
central=['UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md','development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json','development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv','development_reconstruction_2026-09-29/REVIEW_RECORD.json']
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest=B/'SHA256_MANIFEST.tsv'
if sys.argv[1]=='manifest':
 assert not manifest.exists()
 for name in ['final_normal_bound','final_maintenance','final_premises_windowed']:
  p=B/'checks'/name;r=json.loads(Path(str(p)+'.json').read_text());assert r['returncode']==0,name
  for ext in ['stdout','stderr']:assert r[ext+'_sha256']==h(str(p)+'.'+ext)
 freeze=json.loads((B/'INTEGRATION_FREEZE.json').read_text())
 for p,digest in freeze['accepted_sha256'].items():assert h(p)==digest,p
 record=json.loads(Path(central[-1]).read_text());assert record['accepted_sha256']==freeze['accepted_sha256']
 for r in record['reviewers']:
  assert h(r['attestation'])==r['sha256'];att=json.loads(Path(r['attestation']).read_text());assert h(att['report_path'])==att['report_sha256']
 initial=set(json.loads((B/'SNAPSHOT.json').read_text())['initial_untracked_names'])
 current=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],text=True).splitlines());assert initial<=current
 assert subprocess.check_output(['git','diff','--cached','--name-only'],text=True)==''
 changed=set(subprocess.check_output(['git','diff','--name-only'],text=True).splitlines());assert changed==set(central),changed
 receipt={'status':'CHECKS_AND_REVIEW_BINDINGS_PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head_before_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'origin_before_commit':subprocess.check_output(['git','rev-parse','origin/grok'],text=True).strip(),'freeze_sha256':h(B/'INTEGRATION_FREEZE.json'),'accepted_files':len(freeze['accepted_sha256']),'preserved_initial_untracked_names':len(initial),'claim_limit':'ERC1 reviewed conditional response comparison. Both response identifications remain UNADOPTED; no native law/source/scale, empirical recovery, general stability, registry-grade or CANON change.'}
 assert receipt['head_before_commit']==receipt['origin_before_commit']
 with (B/'checks/BANKING_READINESS.json').open('x')as f:json.dump(receipt,f,indent=2);f.write('\n')
 files=sorted(central+[str(p) for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=manifest])
 size=sum(p.stat().st_size for p in B.rglob('*') if p.is_file());assert size<64*1024**2,size
 with manifest.open('x',newline='')as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['path','sha256','bytes']);w.writerows((p,h(p),Path(p).stat().st_size) for p in files)
 print(json.dumps({'manifest_entries':len(files),'package_bytes_before_manifest':size,'manifest_sha256':h(manifest)},indent=2))
elif sys.argv[1]=='stage':
 rows=list(csv.DictReader(manifest.open(),delimiter='\t'));files=[r['path'] for r in rows]+[str(manifest)]
 assert len(files)==len(set(files))
 for r in rows:assert h(r['path'])==r['sha256']
 subprocess.run(['git','add','-f','--',*files],check=True)
 staged=subprocess.check_output(['git','diff','--cached','--name-only','-z']).decode().split('\0');staged=[p for p in staged if p]
 assert set(staged)==set(files),(set(staged)^set(files))
 for p in files:
  blob=subprocess.check_output(['git','show',':'+p]);assert hashlib.sha256(blob).hexdigest()==h(p),p
 subprocess.run(['git','diff','--cached','--check'],check=True)
 print(json.dumps({'exact_staged_files':len(files),'staged_blob_sha256_checks':'PASS'},indent=2))
else:raise ValueError(sys.argv[1])
