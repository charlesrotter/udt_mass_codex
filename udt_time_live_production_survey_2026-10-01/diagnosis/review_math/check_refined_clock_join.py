"""Independent tiny catch-proof of the identified reviewed-field input seam."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];B=ROOT/'udt_time_live_production_survey_2026-10-01';D=B/'diagnosis';HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    with Path(p).open('x') as f:json.dump(x,f,indent=2);f.write('\n')
def read(p):return json.loads(Path(p).read_text())

freeze_path=D/'review_runtime/REFINED_CLOCK_FREEZE.json';freeze=read(freeze_path)
assert sha(freeze_path)=='f0680062c7f0753a5baa3806413f0d61ae96765f7c514ac880b0b920c42b74af'
for p,h in freeze['source_sha256'].items():assert sha(ROOT/p)==h
source=D/'review_runtime/refined_clock_completion.py'
s=importlib.util.spec_from_file_location('reviewed_refined_clock',source);module=importlib.util.module_from_spec(s);s.loader.exec_module(module)
fixture=HERE/'joined_input_fixture';fixture.mkdir(exist_ok=False)
history=fixture/'mock_history.bin';history.write_bytes(b'initial admitted mock field; no real metric data')
assembly=fixture/'mock_assembly.json';write(assembly,dict(output_sha256={str(history):sha(history)}))
report=fixture/'mock_report.json';write(report,dict(case='mock_case',status='PASS',manifest_sha256='mock_manifest',windows=[dict(index=0),dict(index=1),dict(index=2,binding=dict(path=str(history.relative_to(ROOT)),sha256=sha(history),assembly_sha256=sha(assembly)))]))
bound_report=sha(report)
module.checked_field_report('mock_case',report,bound_report,'mock_manifest',history,assembly)
good=dict(history_sha256=sha(history),assembly_sha256=sha(assembly),report_sha256=bound_report)
# Retain prior fixture bytes, then simulate the exact coupled replacement seam.
(fixture/'original_history.bin').write_bytes(history.read_bytes());(fixture/'original_assembly.json').write_bytes(assembly.read_bytes())
history.write_bytes(b'changed mock field after mathematical review')
assembly.write_text(json.dumps(dict(output_sha256={str(history):sha(history)})))
assert read(assembly)['output_sha256'][str(history)]==sha(history)
assert sha(report)==bound_report
try:module.checked_field_report('mock_case',report,bound_report,'mock_manifest',history,assembly)
except ValueError as e:
    assert str(e)=='CLOCK_FIELD_REVIEW_HISTORY_JOIN';caught=str(e)
else:raise AssertionError('COUPLED_REPLACEMENT_FALSE_PASS')
result=dict(status='CLEARED_FOR_FIXED_REFINED_CLOCK_SOURCE',reviewer_context='/root/survey_completion_math',freeze_sha256=sha(freeze_path),adapter_sha256=sha(source),source_sha256=sha(__file__),identified_seam='First edition authenticated review and current assembly independently without joining exact reviewed input; initial finding retained separately.',independent_catchproof=dict(valid_join='PASS',coupled_current_history_assembly_is_self_consistent=True,unchanged_review_hash=True,defect_rejected=caught,initial_fixture_hashes=good),source_review='Actual repaired source requires canonical26case mathematical report coverage, original-equationPASS, matching manifest, and latehistory/assembly identity; old13anchors joined to original aggregate-bound case reports. Fixed4query directions/origin/times and2e-7criteria unchanged. Original13unqualified labels preserved. No sign criterion.',limits='Source clearance and mock provenance control only; no geodesics or field equations executed. All26actual field review, exactinputjoins and result review still required before completion. Original30Hamiltonian subset remains on old24half anchors; new26producer queries are not an independent new clock method.')
write(HERE/'REFINED_CLOCK_SOURCE_REVIEW.json',result)
print(json.dumps({k:result[k] for k in ['status','freeze_sha256','adapter_sha256']}))
