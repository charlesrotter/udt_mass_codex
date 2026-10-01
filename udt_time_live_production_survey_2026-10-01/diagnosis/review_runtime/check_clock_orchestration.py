"""Actual first-three receipt check plus synthetic finite stage/join controls."""
import hashlib
import importlib.util
import json
from pathlib import Path
import types

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ADAPTER = HERE / 'clock_completion.py'

def read(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
def load():
    spec = importlib.util.spec_from_file_location('orchestration_control', ADAPTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    base = HERE / 'clock_orchestration_fixtures'
    base.mkdir(exist_ok=False)
    manifest = read(B / 'production_runtime/campaign.json')
    original = read(B / 'production_analysis/postprocess/MATH_CANDIDATE.json')
    module = load()
    module.authenticated_producer_receipts({'cases': manifest['cases'][:3]})
    checks = ['actual_first_three_captured_reports_equal_immutable_outputs']
    for mode in ['complete', 'stage_failure', 'comparison_failure', 'join_mutation']:
        module = load(); fixture = base / mode; fixture.mkdir()
        module.B = fixture; module.OUT = fixture / 'output'; module.ROOT = fixture
        module.FREEZE = fixture / 'freeze.json'; module.REVIEW = fixture / 'review.json'
        write(fixture / 'production_runtime/campaign.json', manifest)
        original_fixture = json.loads(json.dumps(original))
        if mode == 'join_mutation':
            original_fixture['datasets'][0]['original_equations'] = {'wrong_case': 'PASS'}
        write(fixture / 'production_analysis/postprocess/MATH_CANDIDATE.json', original_fixture)
        write(module.FREEZE, dict(source_sha256={str(ADAPTER): sha(ADAPTER)}, reserve_bytes=1024, total_output_bytes=2**30))
        write(module.REVIEW, dict(freeze_sha256=sha(module.FREEZE), parent_source_review='CLEARED', math_source_review='CLEARED', scientific_diagnostic_readouts='CLEARED'))
        passed = mode != 'comparison_failure'
        (fixture / 'postprocess.py').write_text('import json\ndef compare_clocks(manifest,analysis,independent,output):\n with open(output,"x") as f:json.dump({"machine_diagnostic":' + repr('PASS' if passed else 'FAIL') + ',"matched":[]},f)\n return ' + repr(passed) + '\n')
        # Actual scientific methods are not invoked by these operation-only
        # fixtures. The real scalar comparison remains separately source reviewed.
        module.authenticated_producer_receipts = lambda value: None
        class Process:
            pid = 999999
            def __init__(self, command, **kwargs):
                prefix = Path(command[2]); child_command = command[3:]
                self.code = 2 if mode == 'stage_failure' else 0
                prefix.with_suffix('.stdout').write_text('{}\n')
                prefix.with_suffix('.stderr').write_text('')
                write(prefix.with_suffix('.json'), dict(command=child_command, returncode=self.code, wall_timeout_seconds=None, cpu_timeout_seconds=None, address_space_bytes=2*1024**3, stdout_sha256=sha(prefix.with_suffix('.stdout')), stderr_sha256=sha(prefix.with_suffix('.stderr'))))
            def poll(self): return self.code
            def wait(self): return self.code
        module.subprocess = types.SimpleNamespace(Popen=Process)
        code = module.main(); result = read(module.OUT / 'COMPLETION_RESULT.json')
        if mode == 'complete':
            qualifications = read(module.OUT / 'ORIGINAL_FIELD_QUALIFICATIONS.json')
            assert code == 0 and result['status'] == 'CLOCK_CHARACTERIZATION_COMPLETE_PENDING_REVIEW'
            assert len(result['stages']) == 2 and len(qualifications['datasets']) == 78
            assert sum(x['original_field_qualification'] == 'PASS' for x in qualifications['datasets']) == 65
            assert sum(x['original_field_qualification'] == 'UNQUALIFIED' for x in qualifications['datasets']) == 13
            assert [x['original_numerical_gate'] for x in qualifications['datasets']] == original['datasets']
        elif mode == 'stage_failure':
            assert code == 2 and result['status'] == 'CLOCK_DIAGNOSTIC_STOP' and len(result['stages']) == 1
            assert not (module.OUT / 'ORIGINAL_FIELD_QUALIFICATIONS.json').exists()
        elif mode == 'comparison_failure':
            assert code == 2 and result['status'] == 'CLOCK_COMPARISON_DIAGNOSTIC'
            assert sum(x['original_field_qualification'] == 'UNQUALIFIED' for x in read(module.OUT / 'ORIGINAL_FIELD_QUALIFICATIONS.json')['datasets']) == 13
        else:
            assert code == 2 and result['status'] == 'UNRESOLVED_OPERATIONAL_ERROR' and result['error'] == 'ORIGINAL_DATASET_CASE_JOIN'
        checks.append(mode + '_expected_behavior')
    report = dict(status='ORCHESTRATION_CONTROLS_PASS', adapter_sha256=sha(ADAPTER), checker_sha256=sha(__file__), checks=checks, actual_first_three_sha256={str(B / 'production_analysis' / x['id'] / 'clock.json'): sha(B / 'production_analysis' / x['id'] / 'clock.json') for x in manifest['cases'][:3]}, scope='Author-side actual receipt checks and mocked operation fixtures only; actual234 clocks and separate30 still pending.')
    write(HERE / 'CLOCK_ORCHESTRATION_CONTROLS.json', report)
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
