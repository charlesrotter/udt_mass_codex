"""ACP1 configuration of unchanged pinned FCL closure engine.
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
        "B=Path('udt_first_astronomical_comparison_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=='/root/acp_'+lane",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'ACP1 conditional CGCG074-064 metric/source/null comparison: full angular map and correct optical spectral drift, source-owned likelihood and statistical summary restrictions. Regular reference clock, native metric selection and full source replay remain OPEN; no metric fit, physical adoption or empirical confirmation',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'Two actual fresh same-model source-first/exposed/final reviewer contexts, exact model revision unexposed. Source proof/outcome and parent pre-candidate reviewer-summary exposure disclosed. Separate Fraction/Decimal70 and Decimal80 implementations;18 math cases and45 fidelity cases, source/fixed-sign/reference-clock/estimator/systematic repairs actually re-reviewed. Initial parent output-write and reviewer syntax failures preserved/repaired. No human, different-model, full source replay, formal interval or empirical confirmation',
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [ACP1 config]','exec'))
