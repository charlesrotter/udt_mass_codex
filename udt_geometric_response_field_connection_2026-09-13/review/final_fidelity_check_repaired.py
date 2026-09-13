"""GFC1 final administrative correspondence; not another science replay.

Reuse inspected generic helpers from the prior NR2 final fidelity checker.
"""
from pathlib import Path
import ast,csv,datetime,hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[2];pkg=root/'udt_geometric_response_field_connection_2026-09-13';checks=[]
utility=root/'udt_geometric_field_choice_discrimination_2026-09-13/review/final_fidelity_checks.py'
tree=ast.parse(utility.read_text());names={'sha','gate','pincheck'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(utility),'exec'))
def get(name):return json.loads((pkg/name).read_text())
request=get('FINAL_FIDELITY_REQUEST.json')
pincheck('16_frozen_package_documents',request['package_pins'],pkg)
pincheck('6_frozen_navigation_documents',request['navigation_pins'],root)
pincheck('18_scientific_sources',get('SOURCE_PINS.json')['sources'],root)
pincheck('5_audited_inputs',get('AUDIT_INPUT_PINS.json')['pins'],root)
for path,base in [('CANDIDATE_FREEZE.json',pkg),('CHECK_FREEZE.json',pkg),('REPAIR_FREEZE.json',pkg),('SUPPLEMENT_FREEZE.json',pkg),('review/INDEPENDENT_FREEZE.json',root),('review/INDEPENDENT_REPAIR_FREEZE.json',pkg/'review'),('review/REPAIR_SUPPLEMENT_CHECK_FREEZE.json',pkg/'review'),('review/DIRECT_REVIEW_PINS.json',pkg)]:pincheck(path,get(path)['pins'],base)
gate('source_first_frozen_bytes',sha(pkg/'review/SOURCE_FIRST.md')==get('review/SOURCE_FIRST_FREEZE.json')['sha256'])
for path,code,n,p,expected in [('CONNECTION_RESULT.json','check_connection.py',37,36,False),('CONNECTION_REPAIRED_RESULT.json','check_connection_repaired.py',41,41,True),('SUPPLEMENT_RESULT.json','check_supplement.py',15,15,True),('review/INDEPENDENT_RESULT.json','review/independent_connection_repaired.py',99,99,True),('review/REPAIR_SUPPLEMENT_RESULT.json','review/check_repair_supplement.py',9,9,True)]:
    result=get(path)
    gate(path+'_actual_groups',result['count']==n and len(result['checks'])==n and result['passed']==p and sum(c['pass'] for c in result['checks'])==p and result['all_pass']==expected)
    if 'code_sha256' in result:gate(path+'_code_correspondence',sha(pkg/code)==result['code_sha256'])
gate('original_reviewer_no_result_claim',not (pkg/'review/INDEPENDENT_INITIAL_RESULT.json').exists() and 'AssertionError' in (pkg/'review/independent_initial_capture.stderr').read_text() and not (pkg/'review/independent_initial_capture.stdout').read_bytes())
for stem,want in [('checks/premise406',0),('checks/connection',1),('checks/connection_repaired',0),('checks/supplement',0),('checks/current_surface',0),('checks/navigation',0),('review/independent_initial_capture',1),('review/independent_repaired_capture',0),('review/repair_supplement_capture',0)]:
    cap=get(stem+'.json');gate(stem+'_actual_exit',cap['returncode']==want and not cap['timeout'],started=cap['started_utc'],seconds=cap['duration_seconds'])
    gate(stem+'_stdout_stderr_present',(pkg/(stem+'.stdout')).is_file() and (pkg/(stem+'.stderr')).is_file())
gate('actual_full406_PASS','PASS: 406-row premise registry' in (pkg/'checks/premise406.stdout').read_text())
gate('actual_current_startup_surface_PASS','PASS: actual GFC1 current startup surface' in (pkg/'checks/current_surface.stdout').read_text())
gate('actual_navigation359_1','359 passed, 1 deselected' in (pkg/'checks/navigation.stdout').read_text())
rows=list(csv.DictReader((root/'CURRENT_SCIENTIFIC_PREMISES.tsv').open(),delimiter='\t'));byid={r['premise_id']:r for r in rows};selected=get('SELECTED_PREMISES.json')
gate('406_registry_and7_exact_selected',len(rows)==406 and len(selected)==7 and all(byid[r['premise_id']]==r for r in selected))
raw=subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','status','--porcelain=v1','--untracked-files=all'],cwd=root,text=True)
old=[s for s in raw.splitlines() if s.startswith('?? ') and not s[3:].startswith(pkg.name+'/')]
oldraw='\n'.join(old)+'\n';launch=get('LAUNCH.json')
gate('original51_names_exact',len(old)==51 and oldraw==launch['original_untracked_status'] and hashlib.sha256(oldraw.encode()).hexdigest()==launch['original_status_names_sha256'],boundary='status names only; no protected payload content read or hashed')
changed=subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','diff','--name-only'],cwd=root,text=True).splitlines();index=subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','diff','--cached','--name-only'],cwd=root,text=True)
gate('exact_six_navigation_changes_and_empty_index',changed==sorted(request['navigation_pins']) and not index,tracked=changed)
refs=subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','rev-parse','HEAD','origin/grok'],cwd=root,text=True).splitlines();branch=subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','branch','--show-current'],cwd=root,text=True).strip()
gate('actual_baseline_refs_branch',refs==[launch['head'],launch['origin']] and branch=='grok',refs=refs,branch=branch)
diffcheck=subprocess.run(['git','-c','core.preloadIndex=false','-c','index.threads=1','diff','--check'],cwd=root,text=True,capture_output=True);gate('actual_diff_check',diffcheck.returncode==0,stdout=diffcheck.stdout,stderr=diffcheck.stderr)
ledger=get('EXECUTION_INTERVALS.json');intervals=[]
for item in ledger['intervals']:
    cap=get(item['capture']);start=datetime.datetime.fromisoformat(cap['started_utc']);end=start+datetime.timedelta(seconds=cap['duration_seconds'])
    gate('interval_'+item['capture'],item['start_utc']==start.isoformat() and item['end_utc']==end.isoformat() and item['seconds']==cap['duration_seconds'] and item['exit']==cap['returncode'] and item['command']==cap['command'])
    intervals.append((item['capture'],start,end))
overlap=[]
for i,a in enumerate(intervals):
    for b in intervals[i+1:]:
        d=(min(a[2],b[2])-max(a[1],b[1])).total_seconds()
        if d>0:overlap.append([a[0],b[0],d])
gate('nine_recorded_operations_no_overlap',len(intervals)==9 and not overlap and not ledger['captured_process_overlaps'],limitation='captured operations only; not a full process census or absence of context coexistence')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'final administrative byte/result/status correspondence; no mathematical reproof','request_sha256':sha(pkg/'FINAL_FIDELITY_REQUEST.json'),'helper_utility':str(utility.relative_to(root)),'helper_utility_sha256':sha(utility),'helper_definitions':sorted(names),'code_sha256':sha(Path(__file__)),'checks':checks,'count':len(checks),'passed':sum(c['pass'] for c in checks),'all_pass':all(c['pass'] for c in checks)}
with Path(sys.argv[1]).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'count':result['count'],'passed':result['passed'],'all_pass':result['all_pass'],'failed':[c for c in checks if not c['pass']]}));sys.exit(0 if result['all_pass'] else 1)
