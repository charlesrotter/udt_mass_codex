"""Replay the immutable initial validator at its preserved file path."""
import contextlib
import hashlib
import io
import json
import pathlib

HERE=pathlib.Path(__file__).resolve().parent
driver=HERE/'inspect_candidate_checks.py'
assert hashlib.sha256(driver.read_bytes()).hexdigest()=='4518890ce59cd89d3e989ccaf226677313f1fc14273d4fbd07a7e7bd6fee3130'
source=driver.read_text()
old="CODE = STEP / 'evaluate_benchmark.py'"
new="CODE = STEP / 'INITIAL_evaluate_benchmark.py'"
assert source.count(old)==1
source=source.replace(old,new)
captured=io.StringIO()
with contextlib.redirect_stdout(captured):
    exec(compile(source,str(driver)+'[preserved initial path]','exec'),{'__file__':str(driver),'__name__':'__main__'})
initial=json.loads(captured.getvalue())
expected_false_passes={
    'wrong_acceleration_uncertainty', 'wrong_clock_only_band',
    'wrong_zero_mismatch_displacement', 'coherent_negative_standard_uncertainty_width',
}
actual_false_passes={case['case'] for case in initial['hostile_checks'] if not case['rejected']}
assert actual_false_passes==expected_false_passes
final=json.loads((HERE/'focused_rereview_run.stdout').read_text())
assert final['R1']=='CLOSED' and all(case['rejected'] for case in final['hostile_checks'])
print(json.dumps({
    'status':'PASS_PRESERVED_INITIAL_FALSE_PASSES_AND_REPAIRED_REJECTIONS',
    'initial_validator_imported_from':'step_02/INITIAL_evaluate_benchmark.py',
    'initial_driver_unchanged':True,
    'initial_full_result_replay_agrees':initial['candidate_replay_matches_saved'],
    'initial_actual_false_passes':sorted(actual_false_passes),
    'initial_seven_advertised_defects_rejected':True,
    'final_all_eleven_defects_rejected':True,
    'final_output_sha256':hashlib.sha256((HERE/'focused_rereview_run.stdout').read_bytes()).hexdigest(),
    'note':'The original inspector targets the historical active-code hash; this adapter changes only its import path to preserved initial code. Final re-review uses final pins in the separate focused adapter.',
},indent=2))
