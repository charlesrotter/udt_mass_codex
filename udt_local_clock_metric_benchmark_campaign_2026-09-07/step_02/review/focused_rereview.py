"""Reuse immutable initial review driver against the one repaired candidate."""
import contextlib
import hashlib
import io
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parent
driver = HERE / 'inspect_candidate_checks.py'
assert hashlib.sha256(driver.read_bytes()).hexdigest() == '4518890ce59cd89d3e989ccaf226677313f1fc14273d4fbd07a7e7bd6fee3130'
pins = {
    STEP/'INITIAL_evaluate_benchmark.py':'27c87e02c3cc2591b6735ef80e9fb40161cbf234733263600105271db2d65240',
    STEP/'INITIAL_CANDIDATE_RESULT.md':'c55bf4a085d9c94a50e9f2cb9b168c03143b15304beb52a9be596f7a38982710',
    ROOT/'INITIAL_DECISION_BRIEF.md':'e698a87014c4de8ed2d6fc92ee44e9c78500736c6cbe2216ed6708a85f276bcb',
    STEP/'benchmark_run.stdout':'94f823ad0475c487f412d0ef0d3871d505a78e914da47f40825904465e77d1b8',
    STEP/'CANDIDATE_RESULT.md':'1ba9a49fd103188983ebb34e9c02c8236513a0c8c597e9fc1ff0a546f1d90918',
    ROOT/'DECISION_BRIEF.md':'128e93d4b898a185284163cd9c38ef3780657fa84b0f61e46e95ab5e914dd7ca',
}
for path,expected in pins.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, str(path)
# Adapt only the final candidate code/output pins and output filename in memory.
# The existing comparison and hostile checks remain byte-identical on disk.
source = driver.read_text()
for old,new in [
    ('27c87e02c3cc2591b6735ef80e9fb40161cbf234733263600105271db2d65240','989150132a9d54b9384a3884c1dc61c0f75e419c7cf7c84cb0d299628828172a'),
    ('94f823ad0475c487f412d0ef0d3871d505a78e914da47f40825904465e77d1b8','3a57cfff536868bd3fad14ffaafe0b8faeb704e71b855fbea2892a339f08c00a'),
    ('benchmark_run.stdout','repair_run.stdout'),
]:
    assert old in source
    source=source.replace(old,new)
output=io.StringIO()
with contextlib.redirect_stdout(output):
    exec(compile(source,str(driver)+'[focused final pins]','exec'),{'__file__':str(driver),'__name__':'__main__'})
report=json.loads(output.getvalue())
assert all(case['rejected'] for case in report['hostile_checks'])
assert len(report['hostile_checks'])==11
required = {
    'wrong_acceleration_uncertainty':'acceleration uncertainty conversion',
    'wrong_clock_only_band':'clock-only band endpoints',
    'wrong_zero_mismatch_displacement':'zero-mismatch displacement',
    'coherent_negative_standard_uncertainty_width':'negative standard uncertainty width',
}
for case in report['hostile_checks']:
    if case['case'] in required:
        assert case['guard']==required[case['case']]
original=json.loads((STEP/'benchmark_run.stdout').read_text())
repaired=json.loads((STEP/'repair_run.stdout').read_text())
assert original['result']==repaired['result']
assert original['limits']==repaired['limits']
assert len(original['catch_proofs'])==7 and len(repaired['catch_proofs'])==11
report.update(
    interpretation='R1 closed: four original false passes are rejected by matching new guards; science unchanged; finite checks are not exhaustive validation or empirical certification.',
    original_scientific_result_exactly_unchanged=True,
    original_scientific_limits_exactly_unchanged=True,
    original_candidates_and_output_preserved=True,
    final_original_independent_comparison_count=len(report['source_first_comparisons']),
    R1='CLOSED',
)
print(json.dumps(report,indent=2))
