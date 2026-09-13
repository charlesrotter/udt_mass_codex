# Reused from the FE1 publication adapter pinned in SOURCE_PINS.json.
# Only the published documentary/candidate scope is specialized.
from pathlib import Path
import json,hashlib,subprocess,datetime,sys
p=Path(sys.argv[1]);phase=sys.argv[2]
state=Path('/tmp')/(p.name+'_publication.json')
if state.exists(): out=json.loads(state.read_text())
else: out={'package':str(p),'events':[]}
def run(args):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat(); r=subprocess.run(args,text=True,capture_output=True)
 out['events'].append({'utc':t,'command':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 state.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'command':args,'exit':r.returncode,'stdout':r.stdout[-2200:],'stderr':r.stderr[-2200:]}))
 if r.returncode: raise SystemExit(r.returncode)
 return r.stdout
h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
if phase=='prepare':
 assert run(['git','rev-parse','--abbrev-ref','HEAD']).strip()=='grok'
 refs=run(['git','rev-parse','HEAD','origin/grok']).splitlines();assert refs[0]==refs[1]
 staged_before=run(['git','diff','--cached','--name-only']).splitlines(); assert not staged_before or staged_before==out.get('planned_paths'), 'unexpected prior index contents'
 unstaged=run(['git','diff','--name-only']).splitlines()
 allowed={'CURRENT_RESEARCH_PROGRAM.md','HANDOFF.md','INDEX.md','LIVE.md','MEMORY.md','UDT_RESEARCH_ROADMAP.md','udt_native_theory_research_plan_2026-09-13/PLAN.md','UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md'}
 all_changed=set(staged_before+unstaged)
 assert all(x in allowed or x.startswith(str(p)+'/') for x in all_changed), 'unexpected external tracked path'
 roots=sorted(all_changed & allowed)
 original=json.loads((p/'LAUNCH.json').read_text())['original_untracked_status']
 current=run(['git','status','--short','--untracked-files=all'])
 actual=''.join(x+'\n' for x in current.splitlines() if x.startswith('?? ') and not x[3:].startswith(str(p)+'/'))
 assert actual==original
 paths=sorted(roots+[str(f) for f in p.rglob('*') if f.is_file()])
 assert not any('__pycache__' in x or x.endswith('.pyc') for x in paths)
 plan=p/'PUBLISH_PLAN.json';manifest=p/'SHA256SUMS.json'
 out.update(baseline_head=refs[0],original_untracked_status_sha256=hashlib.sha256(original.encode()).hexdigest())
 final=sorted(set(paths+[str(plan),str(manifest)]))
 plan.write_text(json.dumps({'baseline_head':refs[0],'scope':'JRC1 reviewed source-preserving joint-relation scope correction; no new native admission, exclusion, law or scientific promotion; maintained direction and explanatory pointers','paths':final,'original_untracked_names_preserved':True},indent=2)+'\n')
 manifest.write_text(json.dumps({x:h(x) for x in final if x!=str(manifest)},indent=2)+'\n')
 Path('/tmp/'+p.name+'.nul').write_bytes(b'\0'.join(x.encode() for x in final)+b'\0')
 out['planned_paths']=final
 state.write_text(json.dumps(out,indent=2)+'\n')
 print('PREPARED',len(final),'paths')
elif phase=='stage':
 run(['git','add','-f','--pathspec-from-file=/tmp/'+p.name+'.nul','--pathspec-file-nul'])
 run(['git','diff','--cached','--check'])
 names=run(['git','diff','--cached','--name-only']).splitlines();assert names==out['planned_paths']
 for x,v in json.loads((p/'SHA256SUMS.json').read_text()).items():
  assert hashlib.sha256(subprocess.check_output(['git','show',':'+x])).hexdigest()==v,x
 print('EXACT STAGING PASS',len(names))
elif phase=='commit':
 run(['git','diff','--cached','--check'])
 assert run(['git','diff','--cached','--name-only']).splitlines()==out['planned_paths']
 run(['git','commit','-m',sys.argv[3]])
 out['science_commit']=run(['git','rev-parse','HEAD']).strip()
 assert run(['git','diff-tree','--no-commit-id','--name-only','-r','HEAD']).splitlines()==out['planned_paths']
 state.write_text(json.dumps(out,indent=2)+'\n')
elif phase=='push':
 run(['git','push','origin','grok'])
 refs=run(['git','rev-parse','HEAD','origin/grok']).splitlines();assert refs[0]==refs[1]==out['science_commit']
 assert not run(['git','diff','--name-only']).strip()
 assert not run(['git','diff','--cached','--name-only']).strip()
 original=json.loads((p/'LAUNCH.json').read_text())['original_untracked_status']
 actual=run(['git','status','--short','--untracked-files=all'])
 assert actual==original
 out['postpush_verified_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();out['postpush_refs']=refs;out['tracked_clean']=True;out['original51_status_names_exact']=True
 state.write_text(json.dumps(out,indent=2)+'\n')
 print('PUBLISHED VERIFIED',out['science_commit'])
