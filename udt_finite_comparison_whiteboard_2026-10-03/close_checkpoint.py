"""FCW1 binding/banking adapter of the preserved CMF1 helper; no science checks.
Only package/context/scope/output-cap substitutions; capture and maintenance
checks are reused unchanged. No helper manufactures reviewer acceptance.
"""
from pathlib import Path
import sys,json,hashlib,csv,subprocess,datetime
B=Path('udt_finite_comparison_whiteboard_2026-10-03');W=Path('development_reconstruction_2026-09-29')
central=['UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md',str(W/'DEVELOPMENT_GRAPH.json'),str(W/'RECENT_DISPOSITIONS.tsv'),str(W/'REVIEW_RECORD.json')]
protected=('udt_native_onshell_timelive_reset_owner_audit_2026-08-10/','udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/','udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/','udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/')
def h(p):
 assert not str(p).startswith(protected),p
 return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,obj):
 with Path(p).open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args]).decode().strip()
def checkmap(m):
 for p,d in m.items():assert h(p)==d,p
mode=sys.argv[1]
if mode=='freeze':
 prior=json.loads((B/'PRIOR_REVIEW_RECORD.json').read_text());old=prior['accepted_sha256']
 changed=[p for p,d in old.items() if h(p)!=d]
 assert set(changed)==set(central[:-1]),changed
 accepted={p:h(p) for p in old}
 for p in B.rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:accepted[str(p)]=h(p)
 for p in central[:-1]:accepted[p]=h(p)
 save(B/'INTEGRATION_FREEZE.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'FCW1 supplied product sixth-order finite echo discriminator and restricted C2 simple-zero clock asymptote; FC/RG UNADOPTED, general invariant and native physical selection OPEN. Two fresh source-first/exposed/final contexts; inherited evidence retains its original scope.','base_head':git('rev-parse','HEAD'),'changed_inherited':changed,'inherited_count':len(old),'accepted_sha256':dict(sorted(accepted.items()))})
 print(json.dumps({'accepted_files':len(accepted),'changed_inherited':changed,'freeze_sha256':h(B/'INTEGRATION_FREEZE.json')}))
elif mode=='bind':
 freeze=json.loads((B/'INTEGRATION_FREEZE.json').read_text());checkmap(freeze['accepted_sha256']);reviewers=[]
 for lane in ['math','fidelity']:
  p=B/('review_'+lane)/'FINAL_ATTESTATION.json';a=json.loads(p.read_text())
  assert a['context']=='/root/fcw_'+lane+'_review' and a['verdict']=='ACCEPT_WITH_LIMITS'
  assert a['accepted_sha256']==freeze['accepted_sha256']
  assert h(a['report_path'])==a['report_sha256']
  reviewers.append({'context':a['context'],'attestation':str(p),'sha256':h(p)})
 record={'status':'REVIEWED_WITH_LIMITS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':freeze['scope'],'independence':'Two fresh separate source-first/exposed/final reviews; independently arranged actual-incidence series and original-metric curvature checks. Shared model, Python/SymPy and embedding identity. Preserved quartic failures, reviewer same-premise extraction repair, attribution and dimensional wording corrections. No different-model/human/formal/empirical review.','freeze':str(B/'INTEGRATION_FREEZE.json'),'freeze_sha256':h(B/'INTEGRATION_FREEZE.json'),'prior_review_record':str(B/'PRIOR_REVIEW_RECORD.json'),'prior_review_record_sha256':h(B/'PRIOR_REVIEW_RECORD.json'),'reviewers':reviewers,'accepted_sha256':freeze['accepted_sha256']}
 assert h(W/'REVIEW_RECORD.json')==h(B/'PRIOR_REVIEW_RECORD.json')
 (W/'REVIEW_RECORD.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'status':record['status'],'accepted_files':len(record['accepted_sha256']),'reviewers':reviewers}))
elif mode=='manifest':
 for name in ['final_normal_bound','final_maintenance','final_premises_windowed']:
  p=B/'checks'/name;r=json.loads(Path(str(p)+'.json').read_text());assert r['returncode']==0,name
  for ext in ['stdout','stderr']:assert h(str(p)+'.'+ext)==r[ext+'_sha256']
 record=json.loads((W/'REVIEW_RECORD.json').read_text());checkmap(record['accepted_sha256'])
 assert git('rev-parse','HEAD')==git('rev-parse','origin/grok')
 assert not git('diff','--cached','--name-only')
 assert set(git('diff','--name-only').splitlines())==set(central)
 old=set(json.loads((B/'BASELINE.json').read_text())['existing_untracked_names_only'])
 current=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().rstrip('\0').split('\0'))
 assert old<=current
 save(B/'checks/BANKING_READINESS.json',{'status':'REVIEW_AND_REQUIRED_CHECKS_PASS','head_before_commit':git('rev-parse','HEAD'),'origin_before_commit':git('rev-parse','origin/grok'),'preserved_existing_untracked_names':len(old),'accepted_files':len(record['accepted_sha256']),'claim_limit':record['scope']})
 manifest=B/'SHA256_MANIFEST.tsv';files=sorted(central+[str(p) for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=manifest])
 size=sum(Path(p).stat().st_size for p in files if p.startswith(str(B)))
 assert size<100*1024**2,size
 with manifest.open('x',newline='') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['path','sha256','bytes']);w.writerows((p,h(p),Path(p).stat().st_size) for p in files)
 print(json.dumps({'manifest_files':len(files),'package_bytes':size,'manifest_sha256':h(manifest)}))
elif mode=='stage':
 manifest=B/'SHA256_MANIFEST.tsv';rows=list(csv.DictReader(manifest.open(),delimiter='\t'));files=[r['path'] for r in rows]+[str(manifest)]
 for r in rows:assert h(r['path'])==r['sha256']
 subprocess.run(['git','add','-f','--',*files],check=True)
 assert set(git('diff','--cached','--name-only').splitlines())==set(files)
 for p in files:assert hashlib.sha256(subprocess.check_output(['git','show',':'+p])).hexdigest()==h(p),p
 subprocess.run(['git','diff','--cached','--check'],check=True)
 print(json.dumps({'status':'EXACT_STAGE_PASS','files':len(files)}))
elif mode=='verify':
 manifest=B/'SHA256_MANIFEST.tsv';rows=list(csv.DictReader(manifest.open(),delimiter='\t'))
 for r in rows:assert hashlib.sha256(subprocess.check_output(['git','show','HEAD:'+r['path']])).hexdigest()==r['sha256'],r['path']
 assert not git('status','--porcelain','--untracked-files=no')
 old=set(json.loads((B/'BASELINE.json').read_text())['existing_untracked_names_only'])
 current=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().rstrip('\0').split('\0'))
 assert old==current,(old^current)
 assert git('branch','--show-current')=='grok'
 if len(sys.argv)>2:
  remote=git('ls-remote','origin','refs/heads/grok').split()[0]
  assert remote==git('rev-parse','HEAD')==git('rev-parse','origin/grok')
 print(json.dumps({'status':'COMMITTED_BYTES_AND_PRESERVATION_PASS','head':git('rev-parse','HEAD'),'remote_verified':len(sys.argv)>2,'manifest_entries':len(rows),'untracked_preserved':len(old)}))
else:raise ValueError(mode)
