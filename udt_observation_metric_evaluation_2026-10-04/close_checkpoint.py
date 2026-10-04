"""OEV1 configuration of unchanged pinned FCL closure engine.
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
        "B=Path('udt_observation_metric_evaluation_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=='/root/oev_'+lane",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'OEV1 three-channel eight-primary-source observation assessment, exploratory six-maser marginal conversion and finite supplied-metric evaluator:14queries at3settings,246 production rays. Native astronomical comparison/evolution remain OPEN; no metric selection, source-physics adoption, field equation, response, scale/X_max or empirical confirmation. Narrowed4B constraints and completed5A controls; no5B native solve.',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'One scoped observation researcher plus two actual fresh source-first/exposed/final reviewers; same inherited model, exact revision unexposed. Old proof/verdict and published outcome exposure disclosed. Parent equations/code/matrix and diagnostic rules frozen before execution; result prose assembled after scoped reviews. Independent60-digit quadrature/affine/transport implementation checked6393samples and246endpoint roles with3fault catches; Decimal60 independent source transcription/conversion. One source-precision repair actually re-reviewed. No human, different-model, formal interval, raw-observation replay or empirical confirmation.',
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [OEV1 config]','exec'))
