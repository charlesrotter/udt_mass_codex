"""Final shared-byte/preservation/banking-scope audit; no scientific solve."""
import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;B=HERE.parents[1];D=B/'diagnosis';ROOT=B.parent
def read(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 fp=D/'FINAL_INTEGRATION_FREEZE.json';freeze=read(fp);old=read(D/'PREVIOUS_REVIEW_RECORD.json')['accepted_sha256'];accepted=freeze['accepted_sha256']
 assert sha(fp)=='97cffde48522b68e4b4544d1d7b33a0d198296b73ce22708206d99fde8f751ad'
 assert len(old)==7707 and len(accepted)==12102 and set(old)<=set(accepted)
 changed={p for p in old if old[p]!=accepted[p]}
 assert changed==set(freeze['explicit_changed_previous']) and len(changed)==7
 protected=['udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/','udt_native_onshell_timelive_reset_owner_audit_2026-08-10/','udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/','udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/']
 total=0
 for p,h in accepted.items():
  assert not any(p.startswith(x) for x in protected),p
  path=(ROOT/p).resolve();assert path.is_relative_to(ROOT)
  assert not any(path.is_relative_to(ROOT/x) for x in protected),p
  assert sha(path)==h,p
  total+=path.stat().st_size
 banking=freeze['banking_candidates'];assert len(banking)==len(set(banking))==freeze['banking_candidate_count']==4414
 assert set(banking)<=set(accepted)
 for p in banking:
  path=Path(p)
  assert path.suffix not in ['.npz','.npy','.pt','.pth','.lock'],p
  assert 'checkpoints' not in path.parts and not any(x.endswith('fixtures') for x in path.parts),p
  assert not ('attempts' in path.parts and path.name in ['stdout','stderr']),p
  assert not any(p.startswith(x) for x in protected),p
 assert sum((ROOT/p).stat().st_size for p in banking)==freeze['banking_candidate_bytes']
 for p in ['CANON.md','CURRENT_SCIENTIFIC_PREMISES.tsv','CURRENT_SCIENTIFIC_PREMISES.md','AGENTS.md']:
  before=subprocess.check_output(['git','show','HEAD:'+p],cwd=ROOT)
  assert hashlib.sha256(before).hexdigest()==sha(ROOT/p),p
 graph=read(ROOT/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json')
 for p,h in graph['sources_sha256'].items():assert sha(ROOT/p)==h,p
 for row in graph['review_support']:assert sha(ROOT/row['path'])==row['sha256'],row['path']
 r12=next(x for x in graph['nodes'] if x['id']=='R12T');assert r12['required_conditions']==['C_EINSTEIN','C_TDS_ARENA','P_NULL']
 oldgraph=json.loads(subprocess.check_output(['git','show','HEAD:development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'],cwd=ROOT,text=True));assert oldgraph['edges']==graph['edges']
 assert all(row['role']=='review_evidence' for row in graph['review_support'] if '/diagnosis/' in row['path'])
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip();origin=subprocess.check_output(['git','rev-parse','origin/grok'],cwd=ROOT,text=True).strip()
 assert branch=='grok' and head==origin==freeze['head']
 result=dict(status='FINAL_FREEZE_PRESERVATION_AND_SCOPE_PASS',freeze_sha256=sha(fp),checker_sha256=sha(__file__),head=head,branch=branch,origin_grok_cached=origin,accepted_count=len(accepted),accepted_bytes_hashed=total,prior_count=len(old),preserved_prior_count=len(old)-len(changed),explicit_changed_prior=sorted(changed),banking_candidates=len(banking),banking_candidate_bytes=freeze['banking_candidate_bytes'],unchanged_canon_registry_authority=True,typed_graph_conditions_and_edges_preserved=True,protected_payload_access=False,scope='All12102acceptedbytes authenticated; prior7707minus7explicitintegrationedits preserved. Bankingcandidateallowlist excludesnewrawarrays/checkpoints/workerstreams/generatedfixtures/locks/protectedpayloads. This is not yet an actual git-index/staging audit or final repository verifier run; parent must perform those after both attestations.')
 with (HERE/'FINAL_FREEZE_CHECK.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
