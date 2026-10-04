"""CPR1 configuration of unchanged pinned FCL closure engine.
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
        "B=Path('udt_candidate_commitment_restriction_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=='/root/cpr_'+lane",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'CPR1 existing-commitment audit of conditional CGE1: bounded static received ratio, regular outward-extension divergent clock limit requiring positive Lambda for the specified escaping fixed-history realization, proper-orbital recovery inequality, angular/DDR scope. Physical attachment to additional positional separation/X_max and native response admission OPEN; no fit, new premise or adoption',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'Two actual fresh same-model source-first/exposed/final contexts; parent preliminary formula exposure disclosed. Independent original-coordinate curvature, actual nonradial incidence, proper-recovery and source-fidelity checks. Parent root stopping defect preserved and tightened without acceptance relaxation; reduced coverage and reviewer early-branch failure/arithmetic-summary correction retained. Independent saved-endpoint and neighbor recomputation. No human, different-model, interval, whole-corpus or empirical confirmation',
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [CPR1 config]','exec'))
