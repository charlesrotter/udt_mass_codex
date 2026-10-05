"""Final file correspondence and bounded semantic-routing checks, no science upgrade."""
import csv,datetime,hashlib,json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[1];P=R.parent
freeze_path=P/'INTEGRATION_FREEZE.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert len(sys.argv)==2,'expected independently supplied integration freeze SHA'
assert sha(freeze_path)==sys.argv[1],'freeze identity changed'
freeze=json.loads(freeze_path.read_text());accepted=freeze['accepted_sha256']
protected=('udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
blocked=[p for p in accepted if p.startswith(protected)]
assert not blocked,'protected path in accepted map; do not read it'
mismatches=[]
for relative,expected in accepted.items():
    p=ROOT/relative; resolved=p.resolve()
    assert resolved.is_relative_to(ROOT),'out-of-repo path'
    assert not str(resolved.relative_to(ROOT)).startswith(protected),'protected resolved path'
    if sha(p)!=expected:mismatches.append(relative)
assert not mismatches,mismatches
branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert branch=='grok' and head==freeze['base_head']
central=(ROOT/'UDT_DEVELOPMENT.md').read_text();insert=(P/'CENTRAL_INSERT.md').read_text()
assert insert.strip() in central
assert 'The incidence left-hand side atB=.0001' in insert
assert 'W(z)(Ez+W(z))' in insert
orientation=central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->',1)[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->',1)[0].strip()
program=(ROOT/'CURRENT_RESEARCH_PROGRAM.md').read_text().split('<!-- GENERATED_DEVELOPMENT_BEGIN -->',1)[1].split('<!-- GENERATED_DEVELOPMENT_END -->',1)[0].strip()
assert orientation==program
work=(P/'WORK_RECORD.md').read_text()
assert 'Exposed replay recomputed\nall25 saved states' in work or 'Exposed replay recomputed all25 saved states' in work
graph=json.loads((ROOT/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
assert nodes['C_FRI_SHAPE']['kind']=='conditional_protocol'
assert nodes['C_FRI_RECORD']['kind']=='conditional_protocol'
assert nodes['O_FRI_ADMISSION']['kind']=='open_join'
assert set(nodes['R16FRI']['required_conditions'])=={'C_FRI_SHAPE','C_FRI_RECORD'}
assert not nodes['R16FRI']['registry_ids']
edges={(e['from'],e['to'],e['kind']) for e in graph['edges']}
for source,kind in [('R8CPR','proof'),('R16TSI','proof'),('R16','proof'),('C_FRI_SHAPE','hypothesis'),('C_FRI_RECORD','hypothesis'),('O_FRI_ADMISSION','open_boundary')]:
    assert (source,'R16FRI',kind) in edges
assert ('R16FRI','R18','context') in edges
for relative,expected in graph['sources_sha256'].items():
    if relative.startswith(P.name+'/'):assert accepted[relative]==expected
for entry in graph['review_support']:
    if entry['path'].startswith(P.name+'/'):
        assert entry['role']=='review_evidence'
        assert accepted[entry['path']]==entry['sha256']
rows=list(csv.DictReader((ROOT/'development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv').open(),delimiter='\t'))
fri=[r for r in rows if 'FRI1_RETURN' in r.values()]
assert len(fri)==1
assert 'VERIFIED-WITH-CAVEATS_CONDITIONAL_FINITE_RECORD_SCALE_BOUNDS_AND_AMBIGUITY' in '\t'.join(fri[0].values())
assert sha(freeze_path)==sys.argv[1],'freeze changed during check'
out={'status':'PASS','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'freeze_sha256':sys.argv[1],'accepted_entries_checked':len(accepted),
     'mismatches':mismatches,'protected_prefix_hits':blocked,'actual_branch':branch,'actual_HEAD':head,
     'semantic_controls':['central insert present','root bracket pronoun and W(z) clarified','generated orientation matches',
     'saved replay accurately described','conditional nodes and required conditions','proof/hypothesis/open-boundary edges',
     'review support remains review evidence','new disposition remains conditional'],
     'scope':'Corroborates actual human-readable semantic review; hashes establish correspondence only',
     'new_incidence_cases':0,'cumulative_incidence_cases':63}
with (R/'FINAL_HASH_RESULT.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
