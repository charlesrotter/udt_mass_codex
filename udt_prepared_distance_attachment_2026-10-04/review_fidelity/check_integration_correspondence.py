"""Read-only integration correspondence audit; no scientific calculation."""
import pathlib,json,hashlib,datetime,subprocess
root=pathlib.Path.cwd(); b=root/'udt_prepared_distance_attachment_2026-10-04'; rd=b/'review_fidelity'
protected=('udt_native_onshell_timelive_reset_owner_audit_2026-08-10/','udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/','udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/','udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/')
def safe(path):
    p=pathlib.Path(path)
    assert not p.is_absolute() and '..' not in p.parts,path
    assert not p.as_posix().startswith(protected),path
    actual=(root/p).resolve().relative_to(root).as_posix()
    assert not actual.startswith(protected),actual
    return root/p
def digest(path):
    h=hashlib.sha256()
    with safe(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
frel='udt_prepared_distance_attachment_2026-10-04/INTEGRATION_FREEZE.json'
fh=digest(frel);assert fh=='2ca818e902ebb26fba4addfa92e7c889fada60b7d31cc89b7e65358dd158de34'
f=json.loads((b/'INTEGRATION_FREEZE.json').read_text());m=f['accepted_sha256'];assert len(m)==13462
# Check all exclusions before opening any accepted payload.
for p in m:safe(p)
bad=[p for p,h in m.items() if digest(p)!=h];assert not bad,bad
old=json.loads((b/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256'];assert len(old)==13422
changed=sorted(p for p,h in old.items() if m[p]!=h)
assert changed==sorted(f['changed_inherited'])
assert set(subprocess.check_output(['git','diff','--name-only'],text=True).splitlines())==set(changed)
authority={}
baseline=json.loads((b/'BASELINE.json').read_text())['source_sha256']
for p in ('CANON.md','CURRENT_SCIENTIFIC_PREMISES.tsv','founding.md','AGENTS.md','CLAUDE.md'):
    actual=digest(p);assert actual==hashlib.sha256(subprocess.check_output(['git','show','HEAD:'+p])).hexdigest()
    if p in baseline:assert actual==baseline[p]
    authority[p]={'unchanged_against_HEAD':True,'baseline_checked':p in baseline,'sha256':actual}
receipts={}
for name in ('draft_coherence','final_maintenance','parent_controls'):
    r=json.loads((b/'checks'/f'{name}.json').read_text());assert r['returncode']==0
    for ext in ('stdout','stderr'):
        assert digest(f'udt_prepared_distance_attachment_2026-10-04/checks/{name}.{ext}')==r[ext+'_sha256']
    receipts[name]={'returncode':r['returncode'],'duration_seconds':r['duration_seconds'],'hashes_match':True}
assert 'Ran 57 tests' in (b/'checks/final_maintenance.stderr').read_text()
g=json.loads((root/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
assert (len(g['nodes']),len(g['edges']),len(g['sources_sha256']),len(g['review_support']))==(132,380,229,152)
for p,h in g['sources_sha256'].items():assert digest(p)==h
for support in g['review_support']:assert digest(support['path'])==support['sha256']
for e in g['edges']:
    if e['to']=='R16PDA' and e['from'].startswith('O_'):assert e['kind']=='open_boundary'
central=(root/'UDT_DEVELOPMENT.md').read_text();ins=(b/'CENTRAL_INSERT.md').read_text().strip();assert ins in central
ori=central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->')[0].strip()
program=(root/'CURRENT_RESEARCH_PROGRAM.md').read_text().split('<!-- GENERATED_DEVELOPMENT_BEGIN -->')[1].split('<!-- GENERATED_DEVELOPMENT_END -->')[0].strip();assert ori==program
orientation_count_with_marker=len(central[central.index('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->'):central.index('<!-- DEVELOPMENT_ORIENTATION_END -->')].split())
assert len(ori.split())==560 and orientation_count_with_marker==563
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','scope':'Artifact correspondence and scoped integration structure; not full-corpus semantic review','freeze_sha256':fh,'accepted_paths_verified':len(m),'protected_prefixes_excluded_before_payload_reads':list(protected),'protected_payload_reads':0,'changed_inherited':changed,'new_package_paths':len(m)-len(old),'unchanged_authority_files':authority,'source_pins':len(g['sources_sha256']),'review_support':len(g['review_support']),'graph_nodes':len(g['nodes']),'graph_edges':len(g['edges']),'orientation_whitespace_tokens_excluding_markers':len(ori.split()),'orientation_counter_including_open_marker':orientation_count_with_marker,'generated_orientation_exact':True,'central_insert_exact':True,'receipts':receipts,'normal_full406_binding_commit':'Pending; not represented as passed here'}
(rd/'INTEGRATION_CORRESPONDENCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
