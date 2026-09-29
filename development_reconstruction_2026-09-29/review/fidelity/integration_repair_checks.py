"""Bounded independent repair re-review; synthetic overlays never reach disk."""
import copy,csv,hashlib,io,json,pathlib,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
import verify_udt_development as v
W=v.WORK;OUT=W+'review/fidelity/'
def raw(p):return (ROOT/p).read_bytes()
def h(x):return hashlib.sha256(x.encode() if isinstance(x,str) else x).hexdigest()
def dump(x):return json.dumps(x,sort_keys=True,indent=2)+'\n'
def rows(p):return list(csv.DictReader(io.StringIO(raw(p).decode()),delimiter='\t'))
freeze=json.loads(raw(W+'INTEGRATION_REPAIR_FREEZE.json'));old=json.loads(raw(W+'INTEGRATION_CANDIDATE_FREEZE.json'));checks=[]
def note(name,passed,detail):checks.append(dict(name=name,passed=bool(passed),detail=detail))
for p,d in freeze['accepted_sha256'].items():note('repair_freeze:'+p,h(raw(p))==d,'exact correspondence')
for p,d in old['accepted_sha256'].items():note('preserved_initial:'+p,h(raw(W+'integration_initial/'+p))==d,'initial bytes preserved')
base={};record={'status':'REVIEWED_WITH_LIMITS','accepted_sha256':freeze['accepted_sha256'],'reviewers':[]}
for i in range(2):
 context='IN_MEMORY_REPAIR_FIXTURE_'+str(i);path=OUT+'SYNTHETIC_ATTESTATION_'+str(i)+'.json';report=OUT+'SYNTHETIC_REPORT_'+str(i)+'.md';base[report]='Synthetic report, not actual review.\n'
 base[path]=dump({'context':context,'verdict':'ACCEPT_WITH_LIMITS','accepted_sha256':record['accepted_sha256'],'report_path':report,'report_sha256':h(base[report])})
 record['reviewers'].append({'context':context,'attestation':path,'sha256':h(base[path])})
base[W+'REVIEW_RECORD.json']=dump(record)
def attempt(name,overlay,expected,accept=False):
 try:
  result=v.validate(ROOT,overrides=base|overlay);note(name,accept,result)
 except (v.DevelopmentError,KeyError,OSError) as e:
  note(name,not accept and all(t in str(e) for t in expected),str(e))
attempt('strict_synthetic_baseline',{},[],True)
attempt('changed_actual_report_rejected',{OUT+'SYNTHETIC_REPORT_0.md':'Unattested replacement'},['review report bytes changed'])
attempt('arbitrary_stale_adapter_rejected',{'MEMORY.md':raw('MEMORY.md').decode()+'\nEvery observer configuration fixes one physical population uniquely.\n'},['changed reviewed file','MEMORY.md'])
# Give a modified attestation its correct synthetic envelope hash: unsafe report paths must still fail.
attpath=record['reviewers'][0]['attestation'];att=json.loads(base[attpath]);att['report_path']='../outside_review.md';rec=copy.deepcopy(record);rec['reviewers'][0]['sha256']=h(dump(att))
attempt('unsafe_report_path_rejected',{attpath:dump(att),W+'REVIEW_RECORD.json':dump(rec)},['unsafe/protected dependency path'])
graph=json.loads(raw(W+'DEVELOPMENT_GRAPH.json'))
p176=next(p for p in graph['sources_sha256'] if 'g176' in p)
p310=next(p for p in graph['sources_sha256'] if 'g310' in p and p.endswith('EXACT_DERIVATION.md'))
owner='udt_repository_cleanup_2026-09-27/local_clock_impact_2026-09-29/OWNER_CLARIFICATION.md'
for name,p,expected in [('G176_fixed_impact',p176,['R4','R5','R6','R7','R8','R13','R14','R18']),('source_positive_negative',p310,['R9','R10','R11','R12','R17','R18']),('C1_correction_impact',W+'SOURCE_CORRECTIONS.md',['R9','R10','R11','R12','R17','R18']),('owner_definition_impact',owner,[f'R{i}' for i in range(1,19)])]:
 attempt(name,{p:raw(p).decode()+'\nIN-MEMORY SOURCE CHANGE\n'},['REVIEW_REQUIRED']+[repr(x) for x in expected])
reg=rows('CURRENT_SCIENTIFIC_PREMISES.tsv');next(r for r in reg if r['premise_id']=='G310')['term']+=' IN-MEMORY CHANGE';buf=io.StringIO();wr=csv.DictWriter(buf,fieldnames=list(reg[0]),delimiter='\t');wr.writeheader();wr.writerows(reg)
attempt('row_positive_negative',{'CURRENT_SCIENTIFIC_PREMISES.tsv':buf.getvalue()},['REVIEW_REQUIRED','G310',"'R9'","'R10'","'R17'","'R18'"])
for support in graph['review_support']:
 attempt('support_change:'+support['path'],{support['path']:raw(support['path']).decode()+'\nIN-MEMORY REVIEW CHANGE\n'},['REVIEW_REQUIRED']+[repr(t) for t in support['targets']])
paths={s['path'] for s in graph['review_support']};proofsources={p for n in graph['nodes'] for p in n.get('sources',[])}
note('support_roles_separate',len(paths)==7 and not(paths&proofsources) and all(s['role'] in ['review_evidence','repair_scope'] and s['targets'] for s in graph['review_support']),'Seven support records distinct from proof/source inputs; scopes explicit')
invalid=copy.deepcopy(graph);invalid['review_support'][0]['role']='physical_premise'
attempt('support_cannot_acquire_proof_role',{W+'DEVELOPMENT_GRAPH.json':dump(invalid)},['invalid review support role/target'])
gone=copy.deepcopy(graph);gone['nodes']=[n for n in gone['nodes'] if n['id']!='C_RESPONSE'];gone['edges']=[e for e in gone['edges'] if 'C_RESPONSE' not in [e['from'],e['to']]]
for n in gone['nodes']:n['required_conditions']=[x for x in n.get('required_conditions',[]) if x!='C_RESPONSE']
attempt('vanished_response_class_rejected',{W+'DEVELOPMENT_GRAPH.json':dump(gone)},['changed reviewed file','DEVELOPMENT_GRAPH.json'])
changed=raw(p310).decode()+'\nIN-MEMORY CHANGE\n';refreshed=copy.deepcopy(graph);refreshed['sources_sha256'][p310]=h(changed)
attempt('refreshed_sourcehash_rejected',{p310:changed,W+'DEVELOPMENT_GRAPH.json':dump(refreshed)},['changed reviewed file','DEVELOPMENT_GRAPH.json'])
rec2=copy.deepcopy(record);rec2['accepted_sha256'][W+'DEVELOPMENT_GRAPH.json']=h(dump(refreshed))
attempt('refreshed_graph_record_rejected_by_attestations',{p310:changed,W+'DEVELOPMENT_GRAPH.json':dump(refreshed),W+'REVIEW_RECORD.json':dump(rec2)},['review version mismatch'])
no_support=copy.deepcopy(graph);no_support['review_support']=[]
attempt('removed_review_support_rejected',{W+'DEVELOPMENT_GRAPH.json':dump(no_support)},['changed reviewed file','DEVELOPMENT_GRAPH.json'])
regids={r['premise_id'] for r in reg};disp=rows(W+'CLAIM_DISPOSITIONS.tsv');before=rows(W+'integration_initial/'+W+'CLAIM_DISPOSITIONS.tsv')
new={r['premise_id']:r for r in disp};previous={r['premise_id']:r for r in before}
note('all_406_metadata_preserved',len(disp)==len(new)==406 and set(new)==regids and all({k:x for k,x in new[i].items() if k!='central_location'}=={k:x for k,x in previous[i].items() if k!='central_location'} for i in new),'Only editorial routes changed, no disposition/depth/grade-row hash changed')
routeids={f'G{i}' for i in list(range(353,367))+[374,375]+list(range(395,402))}
note('retained_routes_complete',all('R18' in new[i]['central_location'].split(';') for i in routeids) and all('D1' in new[i]['central_location'].split(';') for i in ['W5','W6']),'Retained rows and explicit definitions route correctly')
recent=rows(W+'RECENT_DISPOSITIONS.tsv');original=rows(OUT+'RECENT_DISPOSITIONS.tsv');orig={r['id']:r for r in original}
note('all_25_scopes_preserved',len(recent)==len(orig)==25 and set(orig)=={r['id'] for r in recent} and all(all(r[k]==orig[r['id']][k] for k in orig[r['id']]) for r in recent),'Current root rows preserve all25 suggested source-specific scopes/depths, with hashes added')
note('master_science_unchanged',freeze['accepted_sha256']['UDT_DEVELOPMENT.md']==old['accepted_sha256']['UDT_DEVELOPMENT.md'],'No science re-review/replay needed for integration delta')
result={'runtime':sys.version,'resource_limits':'timeout60s,512MiB virtual memory,OMP/BLAS threads1','scope':'Independent overlay/version/routing repair audit; synthetic attestations are not actual reviews','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks)}
(ROOT/OUT/'INTEGRATION_REPAIR_CHECKS.json').write_text(dump(result));print(dump({k:x for k,x in result.items() if k!='checks'}));assert all(x['passed'] for x in checks)
