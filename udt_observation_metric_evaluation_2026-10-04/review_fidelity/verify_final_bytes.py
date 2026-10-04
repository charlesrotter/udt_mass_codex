"""Final OEV1 byte correspondence; semantic acceptance is in FINAL_REVIEW."""
from pathlib import Path
import hashlib,json,subprocess,datetime
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from verify_udt_development import program_text
B=ROOT/'udt_observation_metric_evaluation_2026-10-04'
O=B/'review_fidelity'
F=B/'INTEGRATION_FREEZE.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads(F.read_text());m=f['accepted_sha256']
PROTECTED=('udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/','udt_native_onshell_timelive_reset_owner_audit_2026-08-10/','udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/','udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
# Every name and resolved route is preflighted before ANY accepted payload hash.
rejected=[]
for name in m:
 p=Path(name)
 if p.is_absolute() or '..' in p.parts or any(name.startswith(x) for x in PROTECTED):
  rejected.append(name);continue
 resolved=(ROOT/p).resolve()
 if not resolved.is_relative_to(ROOT):rejected.append(name);continue
 relative=str(resolved.relative_to(ROOT))
 if any(relative.startswith(x) for x in PROTECTED):rejected.append(name)
assert not rejected,rejected
mismatch=[];total=0
for name,digest in m.items():
 p=ROOT/name
 if not p.is_file():mismatch.append([name,'MISSING']);continue
 h=hashlib.sha256()
 with p.open('rb') as stream:
  while True:
   chunk=stream.read(1<<20)
   if not chunk:break
   total+=len(chunk);h.update(chunk)
 if h.hexdigest()!=digest:mismatch.append([name,h.hexdigest()])
assert not mismatch,mismatch
master=(ROOT/'UDT_DEVELOPMENT.md').read_text()
assert (ROOT/'CURRENT_RESEARCH_PROGRAM.md').read_text()==program_text(master)
assert (B/'CENTRAL_INSERT.md').read_text().strip() in master
tracked_changes=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
assert sorted(tracked_changes)==sorted(f['changed_inherited'])
graph=json.loads((ROOT/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
proof=[e['from'] for e in graph['edges'] if e['to']=='R8OEV' and e['kind']=='proof']
assert sorted(proof)==['R6','R7']
receipts=[]
for name in ['final_draft','final_maintenance','production']:
 r=json.loads((B/'checks'/(name+'.json')).read_text());assert r['returncode']==0
 for ext in ['stdout','stderr']:
  p=B/'checks'/(name+'.'+ext)
  assert sha(p)==r[ext+'_sha256'],str(p)
 receipts.append({'name':name,'returncode':r['returncode'],'streams_hash_match':True})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ACCEPTED_BYTES_AND_BOUNDED_INTEGRATION_STRUCTURE','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),'freeze_sha256':sha(F),'accepted_entries':len(m),'inherited_count':f['inherited_count'],'bytes_read':total,'path_preflight':'All13914 lexical/resolved routes checked before accepted payload hashing','protected_prefixes':PROTECTED,'protected_or_unsafe_paths':rejected,'mismatches':mismatch,'tracked_changes':tracked_changes,'central_insert_exact':True,'generated_program_exact':True,'R8OEV_proof_dependencies':proof,'receipt_stream_checks':receipts,'limitations':'Byte correspondence and bounded graph/generation checks; no old-corpus scientific reproof or operational normal/full406 completion.'}
(O/'FINAL_BYTE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
