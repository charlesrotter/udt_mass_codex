"""PRT1 configuration of unchanged pinned FCL closure engine.
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
        "B=Path('udt_positional_requirement_translation_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=='/root/prt_'+lane",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'PRT1 steps1-3 conditional positional translation using existing prepared free-clock comparison; weak tidal inequalities, supplied non-Einstein sign control and cubic-onset future asymptote control. Native positional assignment remains OPEN. No physical reference, field equation, population, response, scale/X_max or physical adoption. Steps4/5 receive a reviewed handoff only; no data campaign or numerical solve.',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'Two actual fresh source-first/exposed/final reviewer contexts; old owner/proof/verdict exposure disclosed. Parent froze candidate before reading either new reviewer substantive findings; prior hand exploration disclosed. Both independently hand-checked original metric curvature, boost contractions, reverse preparation, actual arrival derivative, integral/tail and first/echo limits. Precision and handoff wording correction reviewed; original editions preserved. Shared inherited model, exact revision unexposed; no scientific program, human, different-model, formal, independent-code or empirical review.',
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [PRT1 config]','exec'))
