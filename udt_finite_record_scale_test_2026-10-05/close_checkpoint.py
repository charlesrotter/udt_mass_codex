"""FRI1 configuration of unchanged pinned closure engine; no generated verdict."""
from pathlib import Path
import hashlib
source_path=Path('udt_free_clock_completion_2026-10-03/close_checkpoint.py')
assert hashlib.sha256(source_path.read_bytes()).hexdigest()=='d6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
source=source_path.read_text()
replacements={"B=Path('udt_free_clock_completion_2026-10-03')": "B=Path('udt_finite_record_scale_test_2026-10-05')", "a['context']=='/root/fcl_'+lane": "a['context']=='/root/fri_'+lane", 'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls': 'FRI1 conditional finite timing scale enclosure and explicit same-time factor2 scale ambiguity in finite timing/angular records. Exact dimensionless-domain derivative/error bounds, synthetic controls only. Physical domain/source/error admission, native metric selection, mass and X_max OPEN; matched GR identical.', 'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required': 'Two actual fresh same-model source-first/exposed/final contexts independently derive bounds and replay saved original-incidence/proper-time/finite-window quantities. Theoretical leads exposed during discovery; parent reused pinned TSI evaluator, reviewer implementations separate. Shared premises/model/Python/mpmath; no human, different-model, formal, numerical-interval or empirical review.'}

for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [FRI1 config]','exec'))
