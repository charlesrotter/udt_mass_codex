"""Independent repair controls; synthetic attestations are never actual reviews."""
import ast
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import verify_udt_development as guard

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(x): return json.dumps(x, sort_keys=True).encode()
def read(p): return (ROOT/p).read_bytes()

freeze_path = guard.WORK+'INTEGRATION_REPAIR_FREEZE.json'
freeze = json.loads(read(freeze_path))
accepted = freeze['accepted_sha256']
observed = {'scope':'synthetic correspondence controls, not actual review',
            'freeze_sha256':sha(read(freeze_path)), 'checks':[]}
def check(label, condition):
    assert condition, label
    observed['checks'].append(label)

check('all22_repair_freeze_bindings_match',len(accepted)==22 and all(sha(read(p))==h for p,h in accepted.items()))
initial = json.loads(read(guard.WORK+'INTEGRATION_CANDIDATE_FREEZE.json'))['accepted_sha256']
check('all_initial_integration_snapshots_preserved',all(sha(read(guard.WORK+'integration_initial/'+p))==h for p,h in initial.items()))
check('mathematical_manuscript_unchanged',accepted[guard.MASTER]==initial[guard.MASTER])

graph = json.loads(read(guard.WORK+'DEVELOPMENT_GRAPH.json'))
dispositions = list(csv.DictReader(io.StringIO(read(guard.WORK+'CLAIM_DISPOSITIONS.tsv').decode()),delimiter='\t'))
fixture={};reviewers=[]
for i in range(2):
    context='SYNTHETIC_REPAIR_CONTROL_'+str(i)
    apath=guard.WORK+'review/math/synthetic_repair_att_'+str(i)+'.json'
    rpath=guard.WORK+'review/math/synthetic_repair_report_'+str(i)+'.md'
    report=b'SYNTHETIC ONLY: this is a regression control, not scientific review.'
    fixture[rpath]=report
    fixture[apath]=dump({'context':context,'verdict':'ACCEPT_WITH_LIMITS','accepted_sha256':accepted,
                        'report_path':rpath,'report_sha256':sha(report)})
    reviewers.append({'context':context,'attestation':apath,'sha256':sha(fixture[apath])})
recordpath=guard.WORK+'REVIEW_RECORD.json'
fixture[recordpath]=dump({'status':'REVIEWED_WITH_LIMITS','accepted_sha256':accepted,'reviewers':reviewers})
check('strict_valid_synthetic_fixture',guard.validate(overrides=fixture)['status']=='PASS')
check('draft_is_explicitly_not_strict',guard.validate(draft=True)['status']=='DRAFT_COHERENCE_ONLY')

def rejects(label, delta, phrase=None):
    try: guard.validate(overrides=fixture|delta)
    except (guard.DevelopmentError,KeyError,OSError) as exc:
        check(label, phrase is None or phrase in str(exc))
        return str(exc)
    raise AssertionError('FALSE PASS: '+label)

def revised_attestation(mutator):
    apath=reviewers[0]['attestation'];att=json.loads(fixture[apath]);mutator(att)
    modified=dump(att); rec=json.loads(fixture[recordpath]);rec['reviewers'][0]['sha256']=sha(modified)
    return {apath:modified,recordpath:dump(rec)}

rejects('missing_report_path_now_rejected', revised_attestation(lambda a:a.pop('report_path')), 'report_path')
rejects('missing_report_hash_now_rejected', revised_attestation(lambda a:a.pop('report_sha256')), 'report_sha256')
reportpath=json.loads(fixture[reviewers[0]['attestation']])['report_path']
rejects('changed_report_bytes_now_rejected',{reportpath:b'Altered report'},'review report bytes changed')
rejects('nonexistent_declared_report_rejected',revised_attestation(lambda a:a.update(report_path=guard.WORK+'review/math/THIS_SYNTHETIC_REPORT_DOES_NOT_EXIST.md')))

def manual_impact(source=None, rowid=None):
    # Separately implemented traversal of the declared data; no parent helper code.
    active=set()
    for node in graph['nodes']:
        if source in node.get('sources',[]) or rowid in node.get('registry_ids',[]):active.add(node['id'])
    for support in graph.get('review_support',[]):
        if source==support['path']:active.update(support['targets'])
    for row in dispositions:
        if row['premise_id']==rowid:active.update(row['central_location'].split(';'))
    todo=list(active)
    while todo:
        current=todo.pop()
        for edge in graph['edges']:
            if edge['from']==current and edge['to'] not in active:
                active.add(edge['to']);todo.append(edge['to'])
    return active

correction=guard.WORK+'SOURCE_CORRECTIONS.md'
pair='udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md'
owner='udt_repository_cleanup_2026-09-27/local_clock_impact_2026-09-29/OWNER_CLARIFICATION.md'
support='udt_directional_clock_release_2026-09-14/review/REVIEW.md'
expected=[('correction',correction,{'R9','R10','R11','R12','R17','R18'}),
          ('completed_pair',pair,{'R4','R5','R6','R7','R8','R13','R14','R18'}),
          ('owner_definition',owner,{f'R{i}' for i in range(1,19)}),
          ('historical_review',support,{'R5','R10','R18'})]
observed['source_impacts']={}
for name,path,required in expected:
    ours=manual_impact(source=path)
    check(name+'_routing_matches_independent_traversal',ours==set(guard.affected_nodes(graph,[path])))
    check(name+'_required_descendants_present',required<=ours)
    message=rejects(name+'_actual_changed_bytes_rejected',{path:read(path)+b'\nSYNTHETIC CHANGE\n'},'REVIEW_REQUIRED')
    check(name+'_rejection_names_all_recorded_descendants',all("'"+x+"'" in message for x in ours))
    observed['source_impacts'][name]=sorted(ours)

byrow={r['premise_id']:r for r in dispositions}
families=list(range(353,367))+[374,375]+list(range(395,402))
check('retained_branches_have_direct_R18_routes',all('R18' in byrow['G'+str(i)]['central_location'].split(';') for i in families))
check('W5_W6_have_definition_routes',all('D1' in byrow[i]['central_location'].split(';') for i in ('W5','W6')))
check('seven_historical_support_records_separate_from_edges',len(graph['review_support'])==7 and all(s['role'] in ('review_evidence','repair_scope') for s in graph['review_support']))
g2=json.loads(dump(graph));g2['edges'].remove({'from':'C_RESPONSE','to':'R10','kind':'hypothesis'})
rejects('conditional_class_edge_cannot_be_dropped',{guard.WORK+'DEVELOPMENT_GRAPH.json':dump(g2)},'missing required hypothesis')
g2=json.loads(dump(graph));g2['edges'].append({'from':'O_ASSIGNMENT','to':'R1','kind':'proof'})
rejects('open_assignment_cannot_be_promoted',{guard.WORK+'DEVELOPMENT_GRAPH.json':dump(g2)},'open join promoted')

before=subprocess.check_output(['git','show','26da433f090a7c10717649a47c4f2383612f05cd:verify_current_scientific_premises.py'],cwd=ROOT).decode()
after=read('verify_current_scientific_premises.py').decode()
def funcs(s):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
a,b=funcs(before),funcs(after)
check('all_original_package_validator_ASTs_unchanged',[n for n in sorted(a.keys()|b.keys()) if a.get(n)!=b.get(n)]==['main','validate_startup_surface'])
replacement=before.replace('xmax_controls = ("AGENTS.md", "LIVE.md", "CURRENT_SCIENTIFIC_PREMISES.md")','xmax_controls = ("AGENTS.md", "UDT_DEVELOPMENT.md", "CURRENT_SCIENTIFIC_PREMISES.md")')
check('main_AST_only_declared_Xmax_owner_change',funcs(replacement)['main']==b['main'])
observed['count']=len(observed['checks'])
observed['guard_sha256']=sha(read('verify_udt_development.py'))
observed['graph_sha256']=sha(read(guard.WORK+'DEVELOPMENT_GRAPH.json'))
(HERE/'integration_repair_results.json').write_text(json.dumps(observed,indent=2)+'\n')
print(json.dumps(observed,indent=2))
