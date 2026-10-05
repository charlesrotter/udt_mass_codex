"""OAA1 configuration of unchanged pinned FCL closure engine.
Four substitutions: package, actual contexts, scope and exposure.
This adapter never manufactures a review verdict.
"""
from pathlib import Path
import hashlib
source_path=Path('udt_free_clock_completion_2026-10-03/close_checkpoint.py')
assert hashlib.sha256(source_path.read_bytes()).hexdigest()=='d6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
source=source_path.read_text()
replacements={
    "B=Path('udt_free_clock_completion_2026-10-03')":
        "B=Path('udt_operational_asymptote_attachment_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=='/root/oaa_'+lane",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'OAA1 conditional endpoint-affine distance attachment: D_o tends1/H with received-clock pole on stated eventual b_star0 tail; exact counterexample to universal affine ceiling; causal late-return obstruction and conditional circular-source radar bound. Native distance/metric and observational attachment OPEN. No extra matched-GR prediction, X_max selection, fit or physical adoption',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'Two actual fresh same-model source-first/exposed/final contexts, preliminary formula exposure disclosed. Independent affine-limit/incidence/causal arguments and saved-quantity implementations; reviewer-discovered counterexample independently checked with exact rational bounds and negative controls. Initial early-branch failure, source-preserving tail clarification and reviewer resource-enforcement repair retained. No human, different-model, interval, full-corpus or empirical confirmation',
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [OAA1 config]','exec'))
