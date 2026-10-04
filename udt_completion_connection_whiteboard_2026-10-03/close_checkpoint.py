"""CCW1 configuration adapter for the pinned FCL1 binding/banking engine.

Reuse its exact freeze/hash/preservation/staging logic; replace only workspace,
scope and actual reviewer metadata. No scientific test or verdict is generated.
"""
from pathlib import Path
import hashlib

source_path=Path('udt_free_clock_completion_2026-10-03/close_checkpoint.py')
assert hashlib.sha256(source_path.read_bytes()).hexdigest()==\
    'd6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
source=source_path.read_text()
replacements={
    "B=Path('udt_free_clock_completion_2026-10-03')":
    "B=Path('udt_completion_connection_whiteboard_2026-10-03')",
    "a['context']=='/root/fcl_'+lane":
    "a['context']=={'math':'/root/ccw_review','fidelity':'/root/ccw_physical'}[lane]",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
    'CCW1 conditional invariant emitter-clock-gap and scalar-curvature relation; explicit-extension local chosen-emitter existence; same-tail beta2 obstruction and unbounded-free-population counterexample. RG UNADOPTED. Three fresh source-first contributors, fourth fresh independent reviewer and reused physical/fidelity integration reviewer. Original candidate unchanged; exact supplied controls. Prepared-distance successor unexecuted; no native geometry, physical adoption, scale/X_max or distance-law claim.',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
    'Three fresh source-first contributors. Fourth fresh reviewer independently recovered invariant clock-gap/curvature relation before candidate exposure, then checked all load-bearing arguments/controls. Reused physical contributor supplied second exposed/final fidelity review, not independent authorship of its own argument. Parent direct-Christoffel symbolic controls; reviewer hand recomputations. Shared inherited model/premises; no different-model/human/formal/empirical review. No scientific repair required.'
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [CCW1 config]','exec'))
