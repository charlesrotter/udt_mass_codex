"""Reviewer bookkeeping only; no scientific execution or verdict generation."""
import pathlib,json,hashlib,subprocess,datetime,csv
root=pathlib.Path.cwd(); b=pathlib.Path('udt_prepared_distance_attachment_2026-10-04')
fpath=b/'INTEGRATION_FREEZE.json'; f=json.loads(fpath.read_text()); m=f['accepted_sha256']
forbid=('udt_native_onshell_timelive_reset_owner_audit_2026-08-10/','udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/','udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/','udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/')
oldnames=set(json.loads((b/'BASELINE.json').read_text())['existing_untracked_names_only'])
def safe(name):
 name=str(name); p=pathlib.Path(name)
 assert not p.is_absolute() and '..' not in p.parts and not name.startswith(forbid),name
 assert name not in oldnames,name
 resolved=p.resolve(); assert resolved.is_relative_to(root),name
 assert not str(resolved.relative_to(root)).startswith(forbid),name
 return p
# Check every map name before opening any mapped payload.
for name in m: safe(name)
def sha(path):
 path=safe(path); h=hashlib.sha256()
 with path.open('rb') as stream:
  while True:
   chunk=stream.read(1024*1024)
   if not chunk: break
   h.update(chunk)
 return h.hexdigest()
assert len(m)==13462
failed=[]; total=0
for p,want in m.items():
 total+=pathlib.Path(p).stat().st_size
 if sha(p)!=want: failed.append(p)
assert not failed,failed
prior=json.loads((b/'PRIOR_REVIEW_RECORD.json').read_text())['accepted_sha256']
assert len(prior)==f['inherited_count']==13422 and prior.keys()<=m.keys()
changed=sorted(p for p in prior if prior[p]!=m[p])
assert changed==sorted(f['changed_inherited']),changed
expected=['UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md','development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json','development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv']
assert set(changed)==set(expected)
assert all(p.startswith(str(b)+'/') for p in m.keys()-prior.keys())
assert sha(b/'INITIAL_CANDIDATE.md')=='ac895bd3e9b7691ef94eef15274484a10d6883bba962e46b18ae35c91c2d7453'
assert sha(fpath)=='2ca818e902ebb26fba4addfa92e7c889fada60b7d31cc89b7e65358dd158de34'
assert sha('udt_free_clock_completion_2026-10-03/close_checkpoint.py')=='d6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
gp='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'; g=json.loads(pathlib.Path(gp).read_text())
oldg=json.loads(subprocess.check_output(['git','show',f['base_head']+':'+gp],text=True))
assert all(g['sources_sha256'][p]==v for p,v in oldg['sources_sha256'].items())
assert len(g['nodes'])==132 and len(g['edges'])==380 and len(g['sources_sha256'])==229 and len(g['review_support'])==152
# The graph owns direct pins as well as the accepted-map binding; not every
# historical graph source is itself a key of the accepted map.
for p in g['sources_sha256']: safe(p)
for item in g['review_support']: safe(item['path'])
for p,v in g['sources_sha256'].items(): assert sha(p)==v,p
for item in g['review_support']: assert sha(item['path'])==item['sha256'],item['path']
node=next(n for n in g['nodes'] if n['id']=='R16PDA')
assert set(node['required_conditions'])=={'P_NULL','C_PDA_RG_RAY','C_PDA_PREPARATION','C_PDA_ENDPOINT','C_PDA_TRANSVERSE'}
assert all(e['kind']=='open_boundary' for e in g['edges'] if e['to']=='R16PDA' and e['from'].startswith('O_'))
ct=pathlib.Path('UDT_DEVELOPMENT.md').read_text(); pt=pathlib.Path('CURRENT_RESEARCH_PROGRAM.md').read_text()
co=ct.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->',1)[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->',1)[0].strip()
po=pt.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->',1)[1].split('<!-- GENERATED_DEVELOPMENT_END -->',1)[0].strip()
assert co==po
assert ct.count((b/'CENTRAL_INSERT.md').read_text().strip())==1
rows=list(csv.DictReader(pathlib.Path('development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv').open(),delimiter='\t'))
assert len(rows)==57
receipts={}
for name in ['draft_coherence','final_maintenance']:
 r=json.loads((b/'checks'/f'{name}.json').read_text()); assert r['returncode']==0
 for stream in ['stdout','stderr']: assert sha(b/'checks'/f'{name}.{stream}')==r[stream+'_sha256']
 receipts[name]={'returncode':0,'duration_seconds':r['duration_seconds'],'stdout_sha256':r['stdout_sha256'],'stderr_sha256':r['stderr_sha256']}
assert 'Ran 57 tests' in (b/'checks/final_maintenance.stderr').read_text() and (b/'checks/final_maintenance.stderr').read_text().rstrip().endswith('OK')
assert json.loads((b/'checks/draft_coherence.stdout').read_text())['status']=='DRAFT_COHERENCE_ONLY'
statusnames=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().rstrip('\0').split('\0'))
assert oldnames<=statusnames
assert set(subprocess.check_output(['git','diff','--name-only'],text=True).splitlines())==set(expected)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','context':'/root/pda_math','integration_freeze_sha256':sha(fpath),'accepted_paths_checked':len(m),'accepted_bytes_stream_hashed':total,'protected_prefixes_rejected_before_open':list(forbid),'baseline_untracked_names_excluded_and_preserved':len(oldnames),'inherited_paths':len(prior),'changed_inherited':changed,'new_paths':len(m)-len(prior),'prior_graph_source_pins_unchanged':len(oldg['sources_sha256']),'graph_counts':{'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'review_support':len(g['review_support'])},'graph_source_pins_independently_hashed':len(g['sources_sha256']),'graph_review_support_independently_hashed':len(g['review_support']),'later_returns':len(rows),'generated_orientation_matches':True,'orientation_words_with_markers':len(ct[ct.index('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->'):ct.index('<!-- DEVELOPMENT_ORIENTATION_END -->')].split()),'candidate_unchanged':True,'receipts':receipts,'current_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'current_branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'independent_scientific_rerun':False,'prior_metadata_failure':'First audit completed every accepted-map hash then raised KeyError by assuming all graph source paths were map keys. Corrected to direct protected-path-screened graph-pin hashing; no scientific artifact changed.','limits':'Bookkeeping, source correspondence and scoped integration checks; not an independent reproof of the inherited corpus. Normal/full406/binding/commit/push remain pending.'}
(b/'review_math/FINAL_MAP_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
