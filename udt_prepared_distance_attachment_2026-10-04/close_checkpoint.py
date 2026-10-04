"""PDA1 configuration adapter for the pinned FCL1 binding/banking engine.

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
    "B=Path('udt_prepared_distance_attachment_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
    "a['context']=={'math':'/root/pda_math','fidelity':'/root/pda_fidelity'}[lane]",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
    'PDA1 conditional fixed-ray prepared initial-distance pole under explicit H1 uniform collar, H2 endpoint derivatives/invertibility and H3 transversality; smooth bounded noncrossing square-root-pole counterexample to automatic H3. RG UNADOPTED. No native geometry, universal distance-only law, physical positional attribution, scale/X_max or adoption. Original candidate unchanged; two fresh source-first/exposed/final reviewers and45 exact controls; stop for discussion.',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
    'Two fresh source-first/exposed/final contexts independently derived wavefront/path attachment routes before parent fixed-ray candidate exposure; actual exposed review checked its separate quantifier, H1/H2/H3 and bounded noncrossing degeneracy. Independent hand recomputation of original-metric geodesics and implicit distance jets. Parent frozen SymPy program45checks/fivefamilies; no reviewer scientific execution or scientific repair. Shared inherited model/premises; no different-model/human/formal/empirical review.'
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [PDA1 config]','exec'))
