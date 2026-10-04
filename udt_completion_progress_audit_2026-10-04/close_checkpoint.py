"""CPA1 configuration of the unchanged pinned FCL binding/banking engine.
Only package, actual reviewer contexts and audit scope differ; no verdict generated.
"""
from pathlib import Path
import hashlib
source_path=Path('udt_free_clock_completion_2026-10-03/close_checkpoint.py')
assert hashlib.sha256(source_path.read_bytes()).hexdigest()=='d6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
source=source_path.read_text()
replacements={
    "B=Path('udt_free_clock_completion_2026-10-03')":
        "B=Path('udt_completion_progress_audit_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=={'math':'/root/cpa_math','fidelity':'/root/cpa_fidelity'}[lane]",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'CPA1 source-relative progress audit of FCL/CCW/PDA and the FCW/CPW trial ancestry: real conditional mathematical gains, unchanged native RG admission and additional-effect attribution. RG UNADOPTED; no source regrade, new premise, universal insufficiency/GR-equivalence theorem or selected successor. Retain tools and discuss redirecting physical work to a named implication/concrete use. Original audit preserved; source-precision addendum; two fresh source-first/exposed/final contexts.',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'Two fresh source-first/exposed/final contexts audited sources and independently recomputed load-bearing algebra by hand after old-proof/verdict exposure, before parent audit exposure. Parent audit frozen before new reviewer arguments. No new scientific program, prior-script replay, different-model, independent-code, human, formal, empirical or literature-priority review. No blocking scientific defect; nonblocking smooth/C2-to-C3 provenance clarification retained separately.',
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [CPA1 config]','exec'))
