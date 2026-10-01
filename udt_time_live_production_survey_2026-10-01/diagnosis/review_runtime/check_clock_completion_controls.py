"""Finite adversarial operational fixtures; no geometry or production output mutation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ADAPTER = HERE / 'clock_completion.py'
B = HERE.parents[1]

def read(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')

def load():
    spec = importlib.util.spec_from_file_location('completion_fixture', ADAPTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def main():
    base = HERE / 'clock_completion_fixtures'
    base.mkdir(exist_ok=False)
    checks = []
    module = load(); fixture = base / 'guards'; fixture.mkdir()
    module.B = fixture; module.ROOT = fixture
    source = fixture / 'bound_source'; source.write_text('unchanged\n')
    freeze = dict(source_sha256={'bound_source': sha(source)}, reserve_bytes=1, total_output_bytes=1024)
    assert module.guard(freeze) == source.stat().st_size
    checks.append('matching_source_and_budget_pass')
    for label, mutant, expected in [
        ('source_mutation_rejected', {**freeze, 'source_sha256': {'bound_source': '0'*64}}, 'CLOCK_COMPLETION_SOURCE_CHANGED'),
        ('output_reserve_rejected', {**freeze, 'total_output_bytes': 1}, 'CLOCK_COMPLETION_OUTPUT_RESERVE'),
    ]:
        try:
            module.guard(mutant)
        except ValueError as error:
            assert str(error).startswith(expected)
            checks.append(label)
        else:
            raise AssertionError(label)
    module.FREEZE = fixture / 'freeze.json'; module.REVIEW = fixture / 'review.json'; module.OUT = fixture / 'not_created'
    write(module.FREEZE, freeze); write(module.REVIEW, {'freeze_sha256': sha(module.FREEZE), 'parent_source_review': 'CLEARED', 'math_source_review': 'PENDING', 'scientific_diagnostic_readouts': 'CLEARED'})
    try:
        module.main()
    except ValueError as error:
        assert str(error) == 'CLOCK_COMPLETION_REVIEW_REQUIRED' and not module.OUT.exists()
        checks.append('missing_math_review_rejected_before_output')
    else:
        raise AssertionError('missing review passed')
    for mode in ['valid', 'output_mismatch', 'time_limit', 'command_mismatch']:
        module = load(); fixture = base / mode; module.B = fixture; module.TPP = fixture / 'tpp'
        directory = fixture / 'production_analysis/case'; directory.mkdir(parents=True)
        history = directory / 'histories/case_window2.npz'
        value = {'fixture': 'same captured output'}
        write(directory / 'clock.json', {'fixture': 'tampered'} if mode == 'output_mismatch' else value)
        write(directory / 'clock_capture.stdout', value)
        (directory / 'clock_capture.stderr').write_text('')
        command = [sys.executable, str(module.TPP / 'clock_checks.py'), str(history), str(directory / 'clock.json')]
        receipt = dict(command=command if mode != 'command_mismatch' else ['wrong'], returncode=0, wall_timeout_seconds=1 if mode == 'time_limit' else None, cpu_timeout_seconds=None, address_space_bytes=2*1024**3, stdout_sha256=sha(directory / 'clock_capture.stdout'), stderr_sha256=sha(directory / 'clock_capture.stderr'))
        write(directory / 'clock_capture.json', receipt)
        try:
            module.authenticated_producer_receipts({'cases': [{'id': 'case'}]})
        except ValueError:
            assert mode != 'valid'
            checks.append(mode + '_rejected')
        else:
            assert mode == 'valid'
            checks.append('authentic_capture_pass')
    fixture = base / 'manual_signal'; fixture.mkdir()
    shutil.copyfile(B / 'capture.py', fixture / 'capture.py')
    ready = fixture / 'READY'
    (fixture / 'clock_batch.py').write_text('import signal\nfrom pathlib import Path\nPath(' + repr(str(ready)) + ').write_text("ready")\nsignal.pause()\n')
    write(fixture / 'production_runtime/campaign.json', {'cases': [{} for _ in range(234)]})
    write(fixture / 'production_analysis/postprocess/MATH_CANDIDATE.json', {'datasets': [{} for _ in range(78)], 'checked_cases': 234})
    freeze_path = fixture / 'freeze.json'; review_path = fixture / 'review.json'
    write(freeze_path, dict(source_sha256={str(ADAPTER): sha(ADAPTER)}, reserve_bytes=1024, total_output_bytes=1024**2))
    write(review_path, dict(freeze_sha256=sha(freeze_path), parent_source_review='CLEARED', math_source_review='CLEARED', scientific_diagnostic_readouts='CLEARED'))
    runner = fixture / 'runner.py'
    runner.write_text('import importlib.util\nfrom pathlib import Path\ns=importlib.util.spec_from_file_location("m",' + repr(str(ADAPTER)) + ')\nm=importlib.util.module_from_spec(s);s.loader.exec_module(m)\nm.B=Path(' + repr(str(fixture)) + ')\nm.ROOT=m.B\nm.OUT=m.B/"output"\nm.FREEZE=m.B/"freeze.json"\nm.REVIEW=m.B/"review.json"\nraise SystemExit(m.main())\n')
    with (fixture / 'runner.stdout').open('x') as out, (fixture / 'runner.stderr').open('x') as err:
        process = subprocess.Popen([sys.executable, str(runner)], stdout=out, stderr=err)
        # Readiness rather than elapsed time triggers this authorized manual-signal
        # fixture. No deadline, automatic timer kill, or new scientific work.
        while not ready.exists():
            assert process.poll() is None, 'signal fixture exited before readiness'
            time.sleep(.01)
        process.send_signal(signal.SIGTERM)
        code = process.wait()
    result = read(fixture / 'output/COMPLETION_RESULT.json')
    assert code == 75 and result['status'] == 'MANUAL_INTERRUPTION' and result['manual_signal'] == signal.SIGTERM
    receipt = read(fixture / 'output/producer_clocks.json')
    assert receipt['forwarded_signals'] == [signal.SIGTERM] and receipt['wall_timeout_seconds'] is None and receipt['cpu_timeout_seconds'] is None
    checks.append('readiness_triggered_manual_signal_forwarded_without_timeout')
    report = dict(status='OPERATIONAL_CONTROLS_PASS', adapter_sha256=sha(ADAPTER), checker_sha256=sha(__file__), checks=checks, scope='Author-side negative operational fixtures. No independent scientific review, geometry computation, or production output mutation.')
    write(HERE / 'CLOCK_COMPLETION_CONTROLS.json', report)
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
