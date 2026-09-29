from pathlib import Path
import csv,hashlib,io,json,subprocess,sys
root=Path.cwd();base='cffe75fa4bb027d7975f46f27a80d7f7d5731997';pkg=Path('udt_lorentz_kernel_transport_2026-09-29')
results={}
def check(name,cond):
    if not cond:raise AssertionError(name)
    results[name]=True

def sha(data):return hashlib.sha256(data).hexdigest()
def old(p):return subprocess.check_output(['git','show',base+':'+str(p)])
def rows(data):return list(csv.DictReader(io.StringIO(data.decode()),delimiter='\t'))
frozen=json.loads((pkg/'INTEGRATION_FREEZE.json').read_text())['accepted_sha256']
check('exact39_current_hashes',len(frozen)==39 and all(sha(Path(p).read_bytes())==h for p,h in frozen.items()))
changed=subprocess.check_output(['git','diff','--name-only',base],text=True).splitlines()
check('all9_tracked_changes_in_map',len(changed)==9 and set(changed)<=set(frozen))
cf=json.loads((pkg/'CANDIDATE_FREEZE.json').read_text())['sha256']
check('initial8_frozen_members_unchanged',len(cf)==8 and all(sha(Path(p).read_bytes())==h for p,h in cf.items()))
sp=json.loads((pkg/'SOURCE_PINS.json').read_text())['sources']
check('launch_source_pins_with_baseline_central',all(sha(old(p['path']) if p['path']=='UDT_DEVELOPMENT.md' else Path(p['path']).read_bytes())==p['sha256'] for p in sp))
gp='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json';g=json.loads(Path(gp).read_text());gb=json.loads(old(gp))
check('all65_predecessor_source_pins_preserved',len(gb['sources_sha256'])==65 and all(g['sources_sha256'].get(p)==h for p,h in gb['sources_sha256'].items()))
check('all70_current_source_pins_match',len(g['sources_sha256'])==70 and all(sha(Path(p).read_bytes())==h for p,h in g['sources_sha256'].items()))
check('registry_and_canon_unchanged',all(Path(p).read_bytes()==old(p) for p in ['CURRENT_SCIENTIFIC_PREMISES.tsv','CANON.md']))
cp='development_reconstruction_2026-09-29/CLAIM_DISPOSITIONS.tsv';cr=rows(Path(cp).read_bytes());cbr=rows(old(cp));d={r['premise_id']:r for r in cr};db={r['premise_id']:r for r in cbr}
changed_rows={i for i in d if d[i]!=db[i]}
check('exact3_editorial_rows_and406_preserved',len(d)==406 and changed_rows=={'G02','G220','G274'})
check('all_registry_row_pins_preserved',all(d[i]['source_row_sha256']==db[i]['source_row_sha256'] for i in d))
central=Path('UDT_DEVELOPMENT.md').read_text();ins=(pkg/'CENTRAL_INSERTION.md').read_text().strip()
check('central_insertion_exact',ins in central)
check('other_endpoint_potential_survivor_present','A different endpoint potential\nin an evolving geometry is not excluded.' in ins)
sys.path.insert(0,str(root));import verify_udt_development as v
check('generated_program_exact',Path('CURRENT_RESEARCH_PROGRAM.md').read_text()==v.program_text(central))
affected=set(v.affected_nodes(g,[str(pkg/'INITIAL_CANDIDATE.md')]))
check('positive_and_negative_descendants_routed',{'R7','R7C','R7L','R7E','R8S','R18'}<=affected)
for source,target in [('C_LKT_CHARACTER','R7C'),('C_LKT2D','R7L'),('C_LKT2D','R7E'),('C_LKT_RECIPROCAL','R7E'),('C_LKT_SAME_PHI','R7E')]:
    check('required_edge_'+source+'_'+target,{'from':source,'to':target,'kind':'hypothesis'} in g['edges'])
recent=rows(Path('development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv').read_bytes())
check('27_later_returns',len(recent)==27)
unchanged=[]
for p in frozen:
    r=subprocess.run(['git','cat-file','-e',base+':'+p],capture_output=True)
    if r.returncode==0 and Path(p).read_bytes()==old(p):unchanged.append(p)
print(json.dumps({'status':'PASS','checks':results,'count':len(results),'changed_paths':changed,'unchanged_accepted_baseline_files':unchanged,'source_pin_count':len(g['sources_sha256']),'disposition_changed_ids':sorted(changed_rows),'candidate_freeze_members':len(cf),'accepted_map':frozen},indent=2))
