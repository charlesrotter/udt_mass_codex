"""Fresh-context runtime audit; report authentication plus six saved-array anchors."""
import collections, datetime, hashlib, json, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ROOT = B.parent

def read(path):
    return json.loads(Path(path).read_text())

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def used(root):
    return sum(p.stat().st_size for p in root.rglob('*') if p.is_file())

def main():
    manifest_path = B / 'production_runtime/campaign.json'
    m = read(manifest_path); mh = sha(manifest_path)
    initial_freeze = read(B / 'diagnosis/INITIAL_FREEZE.json')
    for path, value in initial_freeze['sha256'].items():
        assert sha(ROOT / path) == value, path
    for path, value in m['source_sha256'].items():
        assert sha(path) == value, path
    aggregate_path = B / 'production_analysis/postprocess/MATH_CANDIDATE.json'
    aggregate = read(aggregate_path)
    attempts = sorted((B / 'production_runtime/attempts').iterdir())
    assert len(m['cases']) == len(attempts) == 234
    assert m['wall_seconds'] is None and m['output_bytes'] == 64 * 1024 ** 3
    rows = []; anchors = []; schedules = {}; cp_count = 0
    selected = {row['id'] for row in m['cases'][:3] + m['cases'][-3:]}
    for row, attempt in zip(m['cases'], attempts, strict=True):
        name = row['id']; spec = read(row['spec']); run = Path(row['run'])
        assert sha(row['spec']) == row['spec_sha256'] == sha(run / 'spec.json')
        receipt = read(attempt / 'receipt.json'); launch = read(attempt / 'launch.json')
        assert receipt['case'] == launch['case'] == name
        assert launch['manifest_sha256'] == mh and launch['wall_seconds_limit'] is None
        assert receipt['command'] == launch['command'] == [sys.executable, str(B / 'production_worker.py'), row['spec'], row['run']]
        assert receipt['returncode'] == 0 and receipt['worker_status'] == 'TPS1_RUN_COMPLETE'
        assert not any(receipt[x] for x in ['resume', 'sigint_sent', 'sigterm_sent', 'sigkill_sent', 'forwarded_signal'])
        for stream in ['stdout', 'stderr']:
            assert sha(attempt / stream) == receipt[stream + '_sha256']
        logs = [json.loads(line) for line in (attempt / 'stdout').read_text().splitlines()]
        saves = {0, spec['end_tick'], *range(spec['checkpoint_ticks'], spec['end_tick'], spec['checkpoint_ticks'])}
        for window in spec['windows']:
            saves.update(window['center'] + (i - window['count'] // 2) * window['stride'] for i in range(window['count']))
        checks = saves | set(range(spec['check_ticks'], spec['end_tick'], spec['check_ticks']))
        accepted = [x for x in logs if x['status'] == 'ACCEPTED_STEP']
        checked = [x for x in logs if x['status'] == 'CHECKED_STATE']
        assert {x['tick'] for x in checked} == checks
        tick = 0
        for step in accepted:
            jump = step['jump_ticks']
            assert 0 < jump <= spec['max_step_ticks'] and jump & (jump - 1) == 0
            assert not any(tick < event < tick + jump for event in checks)
            tick += jump
            assert step['tick'] == tick and step['t'] == 1 + tick * spec['dt_min']
            assert math.isclose(step['stage_cfl'], jump * spec['dt_min'] * step['stage_omega'], rel_tol=1e-14)
            assert step['stage_cfl'] <= spec['cfl'] * (1 + 1e-12)
        assert tick == spec['end_tick'] == 4800 and spec['wall_seconds'] is None
        assert logs[-1]['status'] == 'TPS1_RUN_COMPLETE' and logs[-1]['steps'] == len(accepted)
        assert logs[-1]['retries'] == sum(x['status'] == 'REJECTED_TRIAL_STEP' for x in logs)
        assert logs[-1]['max_stage_cfl'] == max(x['stage_cfl'] for x in accepted)
        for state in checked:
            assert state['gpu_allocated_peak'] <= spec['gpu_bytes'] == 8 * 1024 ** 3
            assert max(state['metrics'][x] for x in ['hamiltonian', 'momentum', 'harmonic']) <= spec['constraint_limit'] == 2e-5
        checkpoints = {}
        for marker in (run / 'checkpoints').glob('*/COMMITTED'):
            meta = marker.parent / 'metadata.json'; info = read(meta); cp_count += 1
            assert marker.read_text().strip() == sha(meta)
            assert info['eligible_for_resume'] and info['diagnostic'] is None
            assert info['t'] == 1 + info['step'] * spec['dt_min']
            assert info['dtype'] == 'float64' and info['shape'] == [2, spec['n'], spec['n'], spec['n'], 4, 4]
            sig = info['signature']; assert sig['spec'] == row['spec_sha256']
            assert sig['initial'] == m['source_sha256'][str(ROOT / spec['initial'])]
            assert sig['step_semantics'] == 'integer_time_tick'
            for source, value in sig['code'].items():
                assert m['source_sha256'][str(ROOT / source)] == value
            assert info['step'] not in checkpoints
            checkpoints[info['step']] = (marker.parent, info)
        assert set(checkpoints) == saves and len(saves) == 32
        analysis = B / 'production_analysis' / name; assembly_path = analysis / 'ASSEMBLY.json'; assembly = read(assembly_path)
        assert assembly['case'] == name and assembly['input_sha256'][str(manifest_path)] == mh
        assert assembly['input_sha256'][str(attempt / 'receipt.json')] == sha(attempt / 'receipt.json')
        report_path = B / 'review/math/cases' / (name + '.json'); report = read(report_path)
        assert aggregate['result_sha256'][str(report_path)] == sha(report_path)
        assert report['status'] == 'PASS' and report['manifest_sha256'] == mh and len(report['windows']) == 3
        for source, value in report['method_sources'].items():
            assert sha(ROOT / source) == value
        for window in report['windows']:
            bind = window['binding']; history = ROOT / bind['path']; sources = history.with_suffix('.sources.json')
            assert bind['assembly_sha256'] == sha(assembly_path)
            assert bind['sources_sha256'] == sha(sources) == assembly['output_sha256'][str(sources)]
            assert bind['sha256'] == assembly['output_sha256'][str(history)] == read(sources)['history_sha256']
        if name in selected:
            history = analysis / 'histories' / (name + '_window2.npz')
            assert sha(history) == assembly['output_sha256'][str(history)]
            with np.load(history, allow_pickle=False) as data:
                g = data['g']; v = data['v']; times = data['times']
                assert g.dtype == v.dtype == np.float64 and g.shape == v.shape == (9, spec['n'], spec['n'], spec['n'], 4, 4)
                assert np.isfinite(g).all() and np.isfinite(v).all()
                assert np.array_equal(times, 1 + np.arange(4736, 4801, 8) * spec['dt_min'])
                for index in [0, 4, 8]:
                    folder, info = checkpoints[4736 + index * 8]; payload = folder / 'state.npz'
                    assert sha(payload) == info['payload_sha256']
                    with np.load(payload, allow_pickle=False) as raw:
                        assert np.array_equal(g[index], raw['state'][0]) and np.array_equal(v[index], raw['state'][1])
                gamma_eig = np.linalg.eigvalsh(g[-1, ..., 1:, 1:]); inverse = np.linalg.inv(g[-1])
                alpha = 1 / np.sqrt(-inverse[..., 0, 0]); beta = -inverse[..., 0, 1:] / inverse[..., 0, 0, None]
                omega = float(np.max(np.sum(abs(beta), axis=-1) + alpha * np.sqrt(3 / gamma_eig[..., 0])) * math.pi * spec['n'] / spec['period'])
                reported = checked[-1]['metrics']['omega_bound']
                assert math.isclose(omega, reported, rel_tol=5e-14)
                anchors.append(dict(case=name, history_sha256=sha(history), checkpoint_indices=[0, 4, 8], max_omega_cpu=omega, max_omega_worker=reported, exact_array_correspondence=True))
        sizes = dict(run_bytes=used(run), analysis_bytes=used(analysis))
        rows.append(dict(case=name, n=spec['n'], accepted_steps=len(accepted), step_histogram=dict(collections.Counter(x['jump_ticks'] for x in accepted)), max_stage_cfl=max(x['stage_cfl'] for x in accepted), gpu_peak_bytes=max(x['gpu_allocated_peak'] for x in checked), max_reported_constraint=max(max(x['metrics'][k] for k in ['hamiltonian', 'momentum', 'harmonic']) for x in checked), receipt_sha256=sha(attempt / 'receipt.json'), assembly_sha256=sha(assembly_path), mathematical_report_sha256=sha(report_path), **sizes))
        schedules[name] = (spec, accepted)
    matched = []
    for index in range(0, 234, 3):
        a, b, c = m['cases'][index:index + 3]; coarse, fine = schedules[a['id']][0], schedules[b['id']][0]
        assert coarse['initial'] == fine['initial'] and coarse['cfl'] == 2 * fine['cfl'] and coarse['max_step_ticks'] == 2 * fine['max_step_ticks']
        matched.append(dict(dataset=a['id'][:-4], coarse_steps=len(schedules[a['id']][1]), fine_steps=len(schedules[b['id']][1]), fine_ceiling_halved=True))
    flagged = {x['dataset'] for x in aggregate['datasets'] if x['status'] != 'PASS'}
    analogs = [x for x in rows if any(x['case'] == d + suffix for d in flagged for suffix in ['_n24_half', '_n32'])]
    roots = [Path(x) for x in m['storage_roots']] + [B / 'review/math/cases', B / 'review/math/captures', B / 'diagnosis']
    storage = {str(root.relative_to(ROOT)): used(root) for root in roots}
    result = dict(status='RUNTIME_DIAGNOSIS_PASS_WITH_SCOPE', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), reviewer_context='/root/survey_completion_runtime', model='same inherited model; fresh separate context', startup='Parent startup synchronization/orientation/premise audit attributed; branch, HEAD, AGENTS, triggered CLAUDE protocols, R12T and assigned evidence independently inspected', base_head='464dfa03744fe6e74a615d1e15a9ba0e844d0e26', manifest_sha256=mh, initial_freeze_sha256=sha(B / 'diagnosis/INITIAL_FREEZE.json'), audit_sha256=sha(__file__), cases=234, checkpoints=cp_count, rows=rows, matched_schedules=matched, raw_anchors=anchors, original_dataset_pass=78-len(flagged), original_unqualified=sorted(flagged), storage_bytes=storage, total_budgeted_bytes=sum(storage.values()), whole_package_bytes=used(B), proposed_26_saved_analog_bytes=sum(x['run_bytes']+x['analysis_bytes'] for x in analogs), proposed_26_uncompressed_state_bytes=sum(59*2*x['n']**3*16*8 for x in analogs), source_weaknesses=['All 234 authentication paths checked via small reports/metadata and source hashes; full checkpoint/window payload hashing repeated only at six explicit raw anchors, not an independent regeneration of all fields.', 'CFL source bounds Fourier principal speeds at collocation points; finite stage inequalities are numerical controls, not nonlinear/continuum stability.', 'Clock comparison has no field-qualification join: completion must explicitly retain 65 original PASS and 13 UNQUALIFIED labels regardless of clock result.', 'Clock interpolation shares saved fields, Fourier and Hermite mathematics; separate Hamilton/RK45 is not independent evolution.'], omitted=['No GPU launch', 'No all-case original equation recomputation; mathematics reviewer owns substantive diagnosis', 'No remote freshness rerun or premise-verifier rerun in this scoped context'])
    with (HERE / 'RUNTIME_DIAGNOSIS.json').open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False); stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['rows','matched_schedules']}, indent=2))

if __name__ == '__main__':
    main()
