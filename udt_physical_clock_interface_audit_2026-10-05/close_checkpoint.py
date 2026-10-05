"""PIA1 configuration of unchanged pinned closure engine; no generated verdict."""
from pathlib import Path
import hashlib
source_path=Path('udt_free_clock_completion_2026-10-03/close_checkpoint.py')
assert hashlib.sha256(source_path.read_bytes()).hexdigest()=='d6b0fec3f680fda86c7a223750dd7b6bc6833112441039cfa28f32a5dc8f49c9'
source=source_path.read_text()
replacements={"B=Path('udt_free_clock_completion_2026-10-03')": "B=Path('udt_physical_clock_interface_audit_2026-10-05')", "a['context']=='/root/fcl_'+lane": "a['context']=='/root/pia_'+lane", 'FCL1 conditional single-free-receiver conformal normal limit, infinite proper time and positive finite OmegaZ for supplied C3 RG and regular interior-emitter null family. Receiver bound derived, RG UNADOPTED. No native geometry, distance/population, scale/X_max or physical adoption. Original candidate unchanged; two fresh independent source-first/exposed/final reviewers and exact parent controls': 'PIA1 conditional physical clock/source interface audit of the existing FRI1 domain: extreme total-ratio and geometric requirements, finite readout conversion and source/error admission. Three primary-source protocol classes supply no complete physical admission. No empirical exclusion, native selection, source law, mass or X_max adoption.', 'Two fresh source-first/exposed/final reviewer contexts, independent conformal-energy derivations and hand recomputation of actual-clock controls/one rational force case. Parent distinct spatial-momentum proof and direct-Christoffel controls. Shared model/premises, parent SymPy; no different-model/human/formal/empirical review. No scientific repair required': 'Two actual fresh same-model source-first/exposed/final contexts. Independent algebra and arithmetic implementations; fidelity reviewer directly rechecks the five primary-source methods. Discovery leads exchanged, saved outputs exposed after independent controls. Shared model/premises/Python, some libraries; no different-model/human/instrument validation/formal or empirical confirmation.'}

for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(source_path)+' [PIA1 config]','exec'))
