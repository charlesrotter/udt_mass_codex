"""Complete frozen original clock queries; preserve original field qualifications.

Operational adapter only. Reuses producer and Hamiltonian computations and the
frozen scalar comparison; performs no field repair or scientific promotion.
"""
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ROOT = B.parent
TPP = ROOT / 'udt_time_live_production_preparation_2026-10-01'
OUT = B / 'diagnosis/clock_completion'
FREEZE = HERE / 'CLOCK_COMPLETION_FREEZE.json'
REVIEW = HERE / 'CLOCK_COMPLETION_REVIEW.json'

def read(path):
    return json.loads(Path(path).read_text())

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def write(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')

def guard(freeze):
    for path, value in freeze['source_sha256'].items():
        if sha(ROOT / path) != value:
            raise ValueError('CLOCK_COMPLETION_SOURCE_CHANGED: ' + path)
    # Count the whole TPS1 package once, conservatively including historical
    # smoke/review artifacts and all simultaneous diagnosis/repair outputs.
    size = sum(p.stat().st_size for p in B.rglob('*') if p.is_file())
    if size + freeze['reserve_bytes'] > freeze['total_output_bytes']:
        raise ValueError('CLOCK_COMPLETION_OUTPUT_RESERVE')
    return size

def authenticated_producer_receipts(manifest):
    for row in manifest['cases']:
        directory = B / 'production_analysis' / row['id']
        history = directory / 'histories' / (row['id'] + '_window2.npz')
        prefix = directory / 'clock_capture'
        receipt = read(prefix.with_suffix('.json'))
        expected = [sys.executable, str(TPP / 'clock_checks.py'), str(history), str(directory / 'clock.json')]
        if receipt['command'] != expected or receipt['returncode'] != 0:
            raise ValueError('PRODUCER_CAPTURE_COMMAND')
        if receipt['wall_timeout_seconds'] is not None or receipt['cpu_timeout_seconds'] is not None or receipt['address_space_bytes'] != 2 * 1024 ** 3:
            raise ValueError('PRODUCER_CAPTURE_RESOURCES')
        for stream in ['stdout', 'stderr']:
            if sha(prefix.with_suffix('.' + stream)) != receipt[stream + '_sha256']:
                raise ValueError('PRODUCER_CAPTURE_STREAM')
        if read(directory / 'clock.json') != read(prefix.with_suffix('.stdout')):
            raise ValueError('PRODUCER_OUTPUT_CAPTURE_MISMATCH')

def main():
    freeze = read(FREEZE)
    review = read(REVIEW)
    if review.get('freeze_sha256') != sha(FREEZE) or any(review.get(key) != 'CLEARED' for key in ['parent_source_review', 'math_source_review', 'scientific_diagnostic_readouts']):
        raise ValueError('CLOCK_COMPLETION_REVIEW_REQUIRED')
    guard(freeze)
    manifest = read(B / 'production_runtime/campaign.json')
    original = read(B / 'production_analysis/postprocess/MATH_CANDIDATE.json')
    if len(manifest['cases']) != 234 or len(original['datasets']) != 78 or original['checked_cases'] != 234:
        raise ValueError('ORIGINAL_COVERAGE_CHANGED')
    OUT.mkdir(exist_ok=False)
    stopped = {'signal': None}; active = {'process': None}; stages = []
    def stop(signum, frame):
        stopped['signal'] = signum
        process = active['process']
        if process is not None and process.poll() is None:
            try:
                os.killpg(process.pid, signum)
            except ProcessLookupError:
                pass
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    def finish(status, code, **extra):
        result = dict(status=status, freeze_sha256=sha(FREEZE), review_sha256=sha(REVIEW), stages=stages, manual_signal=stopped['signal'], utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), **extra)
        write(OUT / 'COMPLETION_RESULT.json', result)
        print(json.dumps(result), flush=True)
        return code
    try:
        commands = [
            ('producer_clocks', [sys.executable, str(B / 'clock_batch.py')]),
            ('independent_clocks', [sys.executable, str(TPP / 'review/runtime/check_clock_hamilton.py'), str(B / 'review/runtime/SUBSET_CLOCK_QUERIES.json')]),
        ]
        for name, command in commands:
            if stopped['signal']:
                return finish('MANUAL_INTERRUPTION', 75)
            guard(freeze)
            prefix = OUT / name
            call = [sys.executable, str(B / 'capture.py'), str(prefix), *command]
            with (OUT / (name + '.controller.stdout')).open('x') as out, (OUT / (name + '.controller.stderr')).open('x') as err:
                process = subprocess.Popen(call, stdout=out, stderr=err, start_new_session=True)
                active['process'] = process
                if stopped['signal']:
                    stop(stopped['signal'], None)
                code = process.wait()
                active['process'] = None
            stages.append(dict(name=name, command=call, returncode=code))
            if code:
                return finish('MANUAL_INTERRUPTION' if stopped['signal'] else 'CLOCK_DIAGNOSTIC_STOP', 75 if stopped['signal'] else 2)
            receipt = read(prefix.with_suffix('.json'))
            if receipt['command'] != command or receipt['returncode'] != 0 or receipt['wall_timeout_seconds'] is not None or receipt['cpu_timeout_seconds'] is not None or receipt['address_space_bytes'] != 2 * 1024 ** 3:
                raise ValueError('CLOCK_STAGE_CAPTURE')
            for stream in ['stdout', 'stderr']:
                if sha(prefix.with_suffix('.' + stream)) != receipt[stream + '_sha256']:
                    raise ValueError('CLOCK_STAGE_STREAM')
            guard(freeze)
        if stopped['signal']:
            return finish('MANUAL_INTERRUPTION', 75)
        authenticated_producer_receipts(manifest)
        module_spec = importlib.util.spec_from_file_location('frozen_tps1_postprocess', B / 'postprocess.py')
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        passed = module.compare_clocks(manifest, B / 'production_analysis', OUT / 'independent_clocks.stdout', OUT / 'CLOCK_CANDIDATE.json')
        comparison = read(OUT / 'CLOCK_CANDIDATE.json')
        qualifications = []
        for index, dataset in enumerate(original['datasets']):
            cases = [row['id'] for row in manifest['cases'][index * 3:index * 3 + 3]]
            if set(cases) != set(dataset['original_equations']):
                raise ValueError('ORIGINAL_DATASET_CASE_JOIN')
            qualifications.append(dict(dataset=dataset['dataset'], cases=cases, original_field_qualification='PASS' if dataset['status'] == 'PASS' else 'UNQUALIFIED', original_numerical_gate=dataset, clock_interpretation='Conditional supplied-field readout' if dataset['status'] == 'PASS' else 'Diagnostic supplied-field readout on an originally unqualified dataset', matched_clock_diagnostics=[row for row in comparison['matched'] if row['reference'] in cases]))
        if sum(x['original_field_qualification'] == 'UNQUALIFIED' for x in qualifications) != 13:
            raise ValueError('ORIGINAL_QUALIFICATION_COUNT')
        write(OUT / 'ORIGINAL_FIELD_QUALIFICATIONS.json', dict(status='DIAGNOSTIC_CHARACTERIZATION_PENDING_ACTUAL_REVIEW', original_aggregate_sha256=sha(B / 'production_analysis/postprocess/MATH_CANDIDATE.json'), clock_candidate_sha256=sha(OUT / 'CLOCK_CANDIDATE.json'), datasets=qualifications, qualification_policy='Original 65 PASS / 13 UNQUALIFIED preserved regardless of clock diagnostic. Any later repair has separate evidence and labels; no retroactive replacement.', scope='Original 234 supplied histories and fixed 30-dataset independent subset; all signs retained. No scientific promotion or gap-spanning ray.'))
        size = guard(freeze)
        return finish('CLOCK_CHARACTERIZATION_COMPLETE_PENDING_REVIEW' if passed else 'CLOCK_COMPARISON_DIAGNOSTIC', 0 if passed else 2, original_pass=65, original_unqualified=13, clock_machine_diagnostic=comparison['machine_diagnostic'], whole_package_bytes=size)
    except Exception as error:
        return finish('UNRESOLVED_OPERATIONAL_ERROR', 2, error_type=type(error).__name__, error=str(error))

if __name__ == '__main__':
    raise SystemExit(main())
