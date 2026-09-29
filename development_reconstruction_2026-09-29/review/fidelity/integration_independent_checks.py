"""Independent integration audit. All injected fixtures remain in memory."""
import copy,csv,hashlib,io,json,pathlib,sys,time
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
import verify_udt_development as v
W=v.WORK; OUT=W+'review/fidelity/'
def raw(p):return (ROOT/p).read_bytes()
def h(x):return hashlib.sha256(x.encode() if isinstance(x,str) else x).hexdigest()
def dump(x):return json.dumps(x,sort_keys=True,indent=2)+'\n'
freeze=json.loads(raw(W+'INTEGRATION_CANDIDATE_FREEZE.json'))
checks=[]
def note(name,passed,detail):
 checks.append(dict(name=name,passed=bool(passed),detail=detail))
for p,d in freeze['accepted_sha256'].items():note('freeze:'+p,h(raw(p))==d,'exact SHA256 correspondence')
base={}; record={'status':'REVIEWED_WITH_LIMITS','accepted_sha256':freeze['accepted_sha256'],'reviewers':[]}
for i in range(2):
 context='SYNTHETIC_FIXTURE_'+str(i); path=OUT+'SYNTHETIC_ATTESTATION_'+str(i)+'.json'; report=OUT+'SYNTHETIC_REPORT_'+str(i)+'.md'
 base[report]='Synthetic original report, not actual review.\n'
 att={'context':context,'verdict':'ACCEPT_WITH_LIMITS','accepted_sha256':record['accepted_sha256'],'report_path':report,'report_sha256':h(base[report]),'limitations':['Synthetic in-memory fixture only']}
 base[path]=dump(att); record['reviewers'].append({'context':context,'attestation':path,'sha256':h(base[path])})
base[W+'REVIEW_RECORD.json']=dump(record)
def attempt(name,overlay,required,should_reject=True):
 try:
  result=v.validate(ROOT,overrides=base|overlay)
  note(name,not should_reject,result);return result
 except v.DevelopmentError as e:
  msg=str(e);note(name,should_reject and all(s in msg for s in required),msg);return msg
attempt('synthetic_strict_baseline',{},[],False)
attempt('arbitrary_stale_adapter_sentence',{'MEMORY.md':raw('MEMORY.md').decode()+'\nEach metric admits exactly one physically admissible clock population.\n'},['changed reviewed file','MEMORY.md'])
graph=json.loads(raw(W+'DEVELOPMENT_GRAPH.json'))
source=next(p for p in graph['sources_sha256'] if 'g310' in p and p.endswith('.md'))
changed=raw(source).decode()+'\nIN-MEMORY DEFECT: response premise changed.\n'
attempt('source_change_positive_negative_descendants',{source:changed},['REVIEW_REQUIRED','R9','R10','R11','R12','R17','R18'])
registry=list(csv.DictReader(io.StringIO(raw('CURRENT_SCIENTIFIC_PREMISES.tsv').decode()),delimiter='\t'))
row=next(r for r in registry if r['premise_id']=='G310');key=next(k for k in row if k not in ('premise_id','term'));row[key]+=' IN-MEMORY DEFECT'
buf=io.StringIO();wr=csv.DictWriter(buf,fieldnames=list(registry[0]),delimiter='\t');wr.writeheader();wr.writerows(registry)
attempt('row_change_positive_negative_descendants',{'CURRENT_SCIENTIFIC_PREMISES.tsv':buf.getvalue()},['REVIEW_REQUIRED','G310','R9','R10','R17','R18'])
gone=copy.deepcopy(graph);gone['nodes']=[n for n in gone['nodes'] if n['id']!='C_RESPONSE'];gone['edges']=[e for e in gone['edges'] if 'C_RESPONSE' not in [e['from'],e['to']]]
for n in gone['nodes']:n['required_conditions']=[x for x in n.get('required_conditions',[]) if x!='C_RESPONSE']
attempt('vanished_class_even_with_deleted_required_list',{W+'DEVELOPMENT_GRAPH.json':dump(gone)},['changed reviewed file','DEVELOPMENT_GRAPH.json'])
refreshed=copy.deepcopy(graph);refreshed['sources_sha256'][source]=h(changed)
attempt('source_hash_refresh_cannot_hide_change',{source:changed,W+'DEVELOPMENT_GRAPH.json':dump(refreshed)},['changed reviewed file','DEVELOPMENT_GRAPH.json'])
rec2=copy.deepcopy(record);rec2['accepted_sha256'][W+'DEVELOPMENT_GRAPH.json']=h(dump(refreshed))
attempt('changed_graph_and_record_still_need_actual_attestation',{source:changed,W+'DEVELOPMENT_GRAPH.json':dump(refreshed),W+'REVIEW_RECORD.json':dump(rec2)},['review version mismatch'])
# These two probes record actual gaps rather than falsely claiming rejection.
stale=attempt('report_bytes_binding_gap',{OUT+'SYNTHETIC_REPORT_0.md':'Changed report; no longer the attested bytes.\n'},[],False)
source176=next(p for p in graph['sources_sha256'] if 'g176' in p)
impact=v.affected_nodes(graph,[source176]);note('G176_full_record_dependency_gap_observed','R5' not in impact,{'source':source176,'affected':impact,'missing_expected':'R5'})
# Independent exact central-route anchor: shifted h = [-4,2;2,8].
from fractions import Fraction as F
h00,h01,h11=F(-4),F(2),F(8);T2=-h00;beta=h01/h00;L2=h11-h01*h01/h00;det=h00*h11-h01*h01
note('central_pair_example',T2==4 and beta==F(-1,2) and L2==9 and det==-36 and T2*L2==-det,{'T':2,'L':3,'m':6,'beta':'-1/2','chi':'-3/5','normalized_determinant':-1})
result={'purpose':'Independent overlay and exact reading-route tests, not actual acceptance or full science replay','runtime':sys.version,'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'report_gap_detected':isinstance(stale,dict),'G176_missing_R5':'R5' not in impact}
(ROOT/OUT/'INTEGRATION_INDEPENDENT_CHECKS.json').write_text(dump(result))
print(dump({k:v for k,v in result.items() if k!='checks'}))
assert all(c['passed'] for c in checks)
