"""ACI1 configuration of the unchanged pinned FCL closure engine.
Five unique replacements: package, contexts, scope, exposure and actual review paths.
No scientific verdict is manufactured by this adapter.
"""
from pathlib import Path
import hashlib
source_path=Path('udt_free_clock_completion_2026-10-03/close_checkpoint.py')
assert hashlib.sha256(source_path.read_bytes()).hexdigest()=='d6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
source=source_path.read_text()
replacements={
    "B=Path('udt_free_clock_completion_2026-10-03')":
        "B=Path('udt_asymptotic_curvature_implication_2026-10-04')",
    "a['context']=='/root/fcl_'+lane":
        "a['context']=={'math':'/root/aci_math','fidelity':'/root/aci_fidelity'}[lane]",
    'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls':
        'ACI1 native physical assignment remains UNCLOSED; conditional finite Lorentz4 curvature bound for declared actual null clocks, reference paths and fixed-endpoint sweeps, with bounded preparation/accumulated acceleration for asymptotic exclusion. Sharp supplied scalar-zero regular controls; no RG or native field/population/scale adoption. Original candidate, early-reviewer-outline parent exposure and both normal-form failures preserved.',
    'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required':
        'Two fresh source-first/exposed/final contexts independently reconstructed and hand-checked finite transport, incidence, curvature and integrals after old source/verdict exposure. Parent heard unsolicited math outline before file freeze; no independent pre-review parent discovery claim. Supplement credits fidelity idea. One parent program passed51 symbolic assertions after2 normalizer failures; consistency assertions not independent confirmations. No reviewer scientific CPU, different-model, human, formal, independent-code or empirical review.',
    "p=B/('review_'+lane)/'FINAL_ATTESTATION.json'":
        "p=B/'B'/lane/'FINAL_ATTESTATION.json'",
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [ACI1 config]','exec'))
