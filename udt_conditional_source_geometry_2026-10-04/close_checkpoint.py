"""CGE1 configuration of unchanged pinned FCL closure engine.
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
        "B=Path('udt_conditional_source_geometry_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=='/root/cge_'+lane",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'CGE1 conditional Ric=Lambda g static spherical exterior with circular test clocks and free radial receiver, actual null incidences, received frequency and finite sky directions. Restricted candidate and exact single-shift receiver freedom; native class selection, additional GR contrast, source interior/full angular/data realization OPEN. No fit or physical adoption',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'Two actual fresh same-model source-first/exposed/final contexts, exact revision unexposed. Source and matching pre-candidate math-message exposure disclosed. Independent original-coordinate arguments, affine/proper-time ODE shooting and Gauss-Legendre saved-incidence checks, distinct Decimal and analytic drift checks. Initial parent wrong-denominator failure preserved and one-line repair independently checked. No human, different-model, formal interval or empirical confirmation',
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [CGE1 config]','exec'))
