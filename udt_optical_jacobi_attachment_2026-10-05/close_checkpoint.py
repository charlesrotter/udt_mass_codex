"""OJM1 configuration of the unchanged pinned FCL closure engine.
Four substitutions: package, actual contexts, scope, exposure. No generated verdict.
"""
from pathlib import Path
import hashlib
source_path=Path('udt_free_clock_completion_2026-10-03/close_checkpoint.py')
assert hashlib.sha256(source_path.read_bytes()).hexdigest()=='d6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
source=source_path.read_text()
replacements={"B=Path('udt_free_clock_completion_2026-10-03')": "B=Path('udt_optical_jacobi_attachment_2026-10-05')", "a['context']=='/root/fcl_'+lane": "a['context']=='/root/ojm_'+lane", 'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls': 'OJM1 conditional full two-dimensional optical map from existing metric and actual clocks; signed caustics and pre-caustic area bound; actual b_star0 late angular-area endpoint1/H and clock pole. Native metric/comparison, known source and physical scale OPEN; matched GR identical; no fit, flux, X_max or physical adoption', 'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required': 'Two actual fresh same-model source-first/exposed/final contexts, independent geodesic-variation arguments, original4D metric/Jacobi and distinct saved-quantity replays. Matching preliminary formula exposure disclosed. Strong-ray finite-angle failure and smaller-step repair at unchanged tolerance retained; map/error and null-ray wording clarified. No different-model, human, interval, full-corpus or empirical review'}

for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [OJM1 config]','exec'))
