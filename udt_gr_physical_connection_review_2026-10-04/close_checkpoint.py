"""GRL1 configuration of unchanged pinned FCL closure engine.
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
        "B=Path('udt_gr_physical_connection_review_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=='/root/grl_'+lane",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'GRL1 bounded ten-primary-paper review; conditional operational rigidity and corrected local geodesic-congruence drift tests with exact adverse controls. Native physical assignment remains OPEN; no response, sign, field equation, population, scale/X_max or physical adoption. Initial candidate fixed; one same-premise precision repair and actual re-review.',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'Three separate sealed research contexts and two additional fresh source-first/exposed/final reviewers; old proof/verdict exposure disclosed. Parent candidate frozen after research reports before new reviewers substantive findings; prior hand exploration disclosed. Reviewers independently hand-derived rigidity, C1 drift and original incidence controls. One precision repair re-reviewed, credited C1/Riccati additions. Shared inherited model, exact revision unexposed; no scientific CPU/GPU, human, different-model, formal, independent-code or empirical review.',
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [GRL1 config]','exec'))
