#!/usr/bin/env python3
"""Independent final correspondence audit; never a scientific corpus reproof."""
import argparse,hashlib,json,resource,sys,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
sys.dont_write_bytecode=True
ap=argparse.ArgumentParser()
ap.add_argument('--expected-freeze',required=True)
args=ap.parse_args()
root=Path(__file__).resolve().parents[2]
package=root/'udt_candidate_commitment_restriction_2026-10-04'
review=package/'review_math'
freeze_path=package/'INTEGRATION_FREEZE.json'
freeze_bytes=freeze_path.read_bytes()
digest=hashlib.sha256(freeze_bytes).hexdigest()
assert digest==args.expected_freeze,'Unexpected freeze version'
frozen=json.loads(freeze_bytes)
accepted=frozen['accepted_sha256']
protected=['udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/','udt_native_onshell_timelive_reset_owner_audit_2026-08-10/','udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/','udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/']
baseline=json.loads((package/'BASELINE.json').read_text())
for path in accepted:
 assert not any(path.startswith(x) for x in protected),'Protected path in acceptance map'
 assert path not in baseline['existing_untracked_names_only'],'Unrelated baseline local work in map'
 assert not Path(path).is_absolute() and '..' not in Path(path).parts

start=time.time();errors=[];total_bytes=0
for path,expected in accepted.items():
 h=hashlib.sha256()
 with (root/path).open('rb') as stream:
  for block in iter(lambda:stream.read(1024*1024),b''):
   h.update(block);total_bytes+=len(block)
 actual=h.hexdigest()
 if actual!=expected:errors.append({'path':path,'expected':expected,'actual':actual})

prior=json.loads((root/'development_reconstruction_2026-09-29/REVIEW_RECORD.json').read_text())
prior_map=prior['accepted_sha256']
missing=sorted(set(prior_map)-set(accepted))
changes=sorted(path for path,previous in prior_map.items() if accepted.get(path)!=previous)
assert not missing,missing
assert changes==sorted(frozen['changed_inherited']),(changes,frozen['changed_inherited'])
assert len(prior_map)==frozen['inherited_count']
sys.path.insert(0,str(root))
import verify_udt_development as vd
assert vd.program_text((root/'UDT_DEVELOPMENT.md').read_text())==(root/'CURRENT_RESEARCH_PROGRAM.md').read_text(),'Generated program differs'
graph=json.loads((root/'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
for path,expected in graph['sources_sha256'].items():
 assert accepted[path]==expected,('graph source pin',path)
for support in graph['review_support']:
 assert accepted[support['path']]==support['sha256'],('review support pin',support['path'])
correction='udt_candidate_commitment_restriction_2026-10-04/review_math/CHECK_REVIEW_CORRECTION.md'
assert correction in accepted
original=json.loads((package/'CANDIDATE_FREEZE.json').read_text())['sha256']
assert accepted['udt_candidate_commitment_restriction_2026-10-04/INITIAL_CANDIDATE.md']==original['udt_candidate_commitment_restriction_2026-10-04/INITIAL_CANDIDATE.md']
out={'status':'PASS' if not errors else 'FAIL','freeze_sha256':digest,'accepted_count':len(accepted),'inherited_count':len(prior_map),'changed_inherited':changes,'hashed_bytes':total_bytes,'mismatches':errors,'program_generated_exactly':True,'graph_source_and_review_support_pins_match':True,'initial_candidate_unchanged':True,'review_numerical_summary_correction_pinned':True,'protected_and_baseline_local_payloads_excluded':True,'duration_seconds':time.time()-start,'meaning':'Exact file correspondence and bounded routing checks; not full-corpus semantic review, chronology proof or full406 result.'}
(review/'FINAL_HASH_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert not errors,'Accepted-file mismatch'
