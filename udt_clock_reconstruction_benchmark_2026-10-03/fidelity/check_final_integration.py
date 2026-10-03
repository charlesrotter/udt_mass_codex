"""Read-only integration/version checks; writes only new fidelity receipt data."""
import json,hashlib,datetime,csv,subprocess,re
from pathlib import Path

B=Path('udt_clock_reconstruction_benchmark_2026-10-03');F=B/'fidelity'
protected=('udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
def sha(path):
    assert not str(path).startswith(protected),path
    digest=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
    return digest.hexdigest()

freeze_path=B/'INTEGRATION_FREEZE.json';freeze=json.loads(freeze_path.read_text())
assert sha(freeze_path)=='ed43ff1a1d4f73b2e07c73079e57d4638900e6fed303bbd010d206f365b0be28'
accepted=freeze['accepted_sha256'];assert len(accepted)==13024
assert not any(k.startswith(protected) for k in accepted)
for path,expected in accepted.items():assert sha(path)==expected,path
prior=json.loads((B/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert len(prior)==12892 and set(prior)<=set(accepted)
changed=sorted(path for path,old in prior.items() if accepted[path]!=old)
assert changed==sorted(freeze['changed_inherited']) and len(changed)==6

central=Path('UDT_DEVELOPMENT.md').read_text();program=Path('CURRENT_RESEARCH_PROGRAM.md').read_text()
orientation=central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->',1)[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->',1)[0].strip()
excerpt=program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->',1)[1].split('<!-- GENERATED_DEVELOPMENT_END -->',1)[0].strip()
assert orientation==excerpt
for anchor in ['r8cbr','r17cbr']:assert central.count(f'<a id="{anchor}"></a>')==1

graph=json.loads(Path('development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
assert len(nodes)==len(graph['nodes'])==109
for name,conditions in [('R8CBR',{'C_CMF_PREP','C_CMF_ERRORS','C_CBR_NUMERICS'}),('R17CBR',{'C_CMF_TRACE','C_CMF_ERRORS','C_CBR_NUMERICS'})]:
    assert set(nodes[name]['required_conditions'])==conditions
    for c in conditions:assert {'from':c,'to':name,'kind':'hypothesis'} in graph['edges']
for path,digest in graph['sources_sha256'].items():assert sha(path)==digest,path
for item in graph['review_support']:
    if item['path'].startswith(str(B)):
        assert item['role']=='review_evidence' and sha(item['path'])==item['sha256']
        assert {'R8CBR','R17CBR','O_PSW_ATTRIBUTION'}<=set(item['targets'])
rows=list(csv.DictReader(Path('development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv').open(),delimiter='\t'))
assert len(rows)==50
entry=next(r for r in rows if r['id']=='CBR1_RETURN')
assert entry['source_sha256']==sha(entry['source']) and 'no native/physical adoption' in entry['current_scope']

receipts={}
for name,expected in [('draft',0),('normal_before_binding',1)]:
    path=B/'checks'/name;r=json.loads(Path(str(path)+'.json').read_text())
    assert r['returncode']==expected
    for ext in ['stdout','stderr']:assert sha(str(path)+'.'+ext)==r[ext+'_sha256']
    output=Path(str(path)+'.stdout').read_text()
    if name=='normal_before_binding':assert 'REVIEW_REQUIRED' in output
    receipts[name]=dict(returncode=r['returncode'],stdout_sha256=r['stdout_sha256'])

# Verify quoted peer numerical maxima by saved machine records only, without
# adopting the peer's verdict or claiming its independent work as our own.
peer=json.loads((B/'math/MAIN_SAVED_METRIC_CHECK.json').read_text())
max_tensor=max(r['max_tensor'] for r in peer['summary'] if r['case']=='A')
assert max_tensor<4.694e-8
max_clock=max(abs(r['difference']) for r in peer['clock_spots']) if peer['clock_spots'] and 'difference' in peer['clock_spots'][0] else None
state=dict(branch=subprocess.check_output(['git','branch','--show-current']).decode().strip(),head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip())
assert state['branch']=='grok' and state['head']==freeze['base_head']
result=dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_FROZEN_INTEGRATION_CORRESPONDENCE',
    freeze_sha256=sha(freeze_path),accepted_files=len(accepted),inherited_count=len(prior),changed_inherited=changed,
    protected_paths_hashed=0,program_exact_orientation=True,graph_nodes=len(nodes),later_dispositions=len(rows),
    prebinding_receipts=receipts,peer_saved_max_positive_tensor=max_tensor,peer_saved_max_clock_difference=max_clock,
    state=state,limits='Hashes are correspondence only; inherited12892 evidence files not scientifically re-proved. Normal binding/maintenance/full406 closure, commit and push are not yet attested.')
with (F/'FINAL_CORRESPONDENCE_RESULT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
