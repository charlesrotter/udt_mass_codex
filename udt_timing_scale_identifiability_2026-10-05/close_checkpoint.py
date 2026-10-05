"""TSI1 configuration of unchanged pinned closure engine; no generated verdict."""
from pathlib import Path
import hashlib
source_path=Path('udt_free_clock_completion_2026-10-03/close_checkpoint.py')
assert hashlib.sha256(source_path.read_bytes()).hexdigest()=='d6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
source=source_path.read_text()
replacements={"B=Path('udt_free_clock_completion_2026-10-03')": "B=Path('udt_timing_scale_identifiability_2026-10-05')", "a['context']=='/root/fcl_'+lane": "a['context']=='/root/tsi_'+lane", 'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls': 'TSI1 conditional ideal receiver-clock redshift drift determines c_E H, principal angular track gives same limit; untimed records retain homothety. No known source size, native metric selection, finite empirical access, physical mass law, X_max or extra matched-GR prediction.', 'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required': 'Two fresh same-model source-first/exposed/final contexts independently derive smooth-tail rates and record limits; distinct implementations recompute saved incidences, rates and scale transforms. Parent preliminary timing formula disclosed at dispatch; candidate/code/results exposed after source-first. Shared premises/model/libraries; no human, different-model, formal, interval or empirical review.'}

for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [TSI1 config]','exec'))
