"""Manifest-aware TPS1 independent original-equation checks.

Reuses audited independent TDS/TPP diagnostic mathematics; imports no producer.
Artifacts/results are immutable, except a caller may choose a new output path.
No elapsed-time stop, following the explicit user instruction.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ROOT = BASE.parent
TPP = ROOT / 'udt_time_live_production_preparation_2026-10-01/review/math'
TDS = ROOT / 'udt_three_spatial_smoke_2026-10-01/review'
sys.path[:0] = [str(TPP), str(TDS / 'data'), str(TDS / 'equations_recovery')]
from check_constraints import constraints, derivative, selftest as adm_controls
from check_harmonic import contracted
from check_saved_data import extrinsic
from diagnose_window_truncation import center_ricci, verify_weights
from history_ricci import analyze, own_kasner, selftest as ricci_controls

LIMIT = 2e-5
TIME_LIMIT = 2e-7
SMALL = 1e-8


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(data, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def checked_path(path, expected=None):
    path = Path(path)
    path = (ROOT / path).resolve() if not path.is_absolute() else path.resolve()
    if not path.is_relative_to(BASE):
        raise ValueError('SURVEY_PATH_SCOPE')
    if expected is not None and sha(path) != expected:
        raise ValueError('ARTIFACT_HASH_MISMATCH: ' + str(path))
    return path


def method_sources():
    sources = [Path(__file__), TDS / 'data/check_constraints.py',
               TDS / 'data/check_harmonic.py', TPP / 'check_saved_data.py',
               TPP / 'diagnose_window_truncation.py',
               TDS / 'equations_recovery/history_ricci.py']
    return {str(p.relative_to(ROOT)): sha(p) for p in sources}


def manifest(path):
    path = checked_path(path)
    m = read(path)
    ids = [row['id'] for row in m['cases']]
    if len(ids) != len(set(ids)) or len(ids) != 234:
        raise ValueError('EXPECTED_EXACTLY_234_UNIQUE_CASES')
    for row in m['cases']:
        checked_path(row['spec'], row['spec_sha256'])
    m['_manifest_sha256'] = sha(path)
    m['_manifest_path'] = str(path)
    return m


def check_geometry(g, v):
    if g.dtype != np.float64 or v.dtype != np.float64 or g.shape != v.shape:
        raise ValueError('INVALID_METRIC_SCHEMA')
    if g.ndim != 5 or g.shape[-2:] != (4, 4) or not (np.isfinite(g).all() and np.isfinite(v).all()):
        raise ValueError('INVALID_METRIC_VALUES')
    if max(abs(g - g.swapaxes(-1, -2)).max(), abs(v - v.swapaxes(-1, -2)).max()) > 1e-12:
        raise ValueError('NONSYMMETRIC_STATE')
    if np.linalg.eigvalsh(g[..., 1:, 1:]).min() <= 0 or np.linalg.inv(g)[..., 0, 0].max() >= 0:
        raise ValueError('NONSPACELIKE_SLICE')


def adm_row(g, v, period):
    check_geometry(g, v)
    periods = np.broadcast_to(period, (3,))
    gamma, K, lapse, shift = extrinsic(g, v, periods)
    data, _ = constraints(gamma, K, periods)
    covector = contracted(g, v, periods)
    vector = np.einsum('...ab,...b->...a', np.linalg.inv(g), covector)
    data.update(harmonic_vector_abs_max=float(abs(vector).max()),
                harmonic_covector_abs_max=float(abs(covector).max()),
                lapse_minmax=[float(lapse.min()), float(lapse.max())],
                shift_abs_max=float(abs(shift).max()))
    values = [data['hamiltonian_abs_max'], *data['momentum_abs_max_by_component'], data['harmonic_vector_abs_max']]
    data['status'] = 'PASS' if all(np.isfinite(v) and v <= LIMIT for v in values) else 'FAIL'
    return data


def initial_one(path, expected_sha):
    path = checked_path(path, expected_sha)
    with np.load(path, allow_pickle=False) as data:
        period = float(data['period'])
        if not np.isfinite(period) or abs(period - 2 * np.pi) > 1e-14:
            raise ValueError('INITIAL_PERIOD')
        g, v, seed = data['g'], data['v'], data['seed']
        result = adm_row(g, v, period)
        gamma, K, _, _ = extrinsic(g, v, np.full(3, period))
        if np.max(abs(gamma - data['gamma'])) != 0 or np.max(abs(K - data['K'])) >= 1e-14:
            raise ValueError('SAVED_INITIAL_ADM_DISAGREEMENT')
        trace = float(abs(np.trace(seed, axis1=-2, axis2=-1)).max())
        divergence = float(abs(sum(derivative(seed[..., j, :], j, np.full(3, period)) for j in range(3))).max())
        n = g.shape[0]
        if g.shape[:3] != (n, n, n) or n not in [24, 32]:
            raise ValueError('INITIAL_MESH')
        coordinates = np.meshgrid(*([period * np.arange(n) / n] * 3), indexing='ij')
        expected = np.broadcast_to(np.diag([2 / 3, -1 / 3, -1 / 3]), seed.shape).copy()
        mode_rows = []
        for mode in json.loads(str(data['modes_json'])):
            k, s = np.asarray(mode['k'], dtype=float), np.asarray(mode['matrix'], dtype=float)
            if not (np.isfinite(k).all() and np.isfinite(s).all()) or not np.any(k) or np.any(k != np.rint(k)) or max(abs(k)) >= n / 2:
                raise ValueError('MODE_DOMAIN')
            _, _, vh = np.linalg.svd(k.reshape(1, 3), full_matrices=True)
            p, q = vh[1:]
            plus, cross = np.outer(p, p) - np.outer(q, q), np.outer(p, q) + np.outer(q, p)
            tensor = .5 * (p @ s @ p - q @ s @ q) * plus + (p @ s @ q) * cross
            tensor *= np.sqrt(2) / np.linalg.norm(tensor)
            angle = sum(k[i] * coordinates[i] for i in range(3)) + mode['phase']
            expected += mode['amplitude'] * np.cos(angle)[..., None, None] * tensor
            mode_rows.append(dict(k=k.tolist(), trace=float(abs(np.trace(tensor))),
                                  transversality=float(abs(k @ tensor).max()), norm=float(np.linalg.norm(tensor))))
        reconstruction = float(abs(expected - seed).max())
        bad_v = v.copy()
        bad_v[..., 0, 0] += .02
        bad = float(abs(contracted(g, bad_v, np.full(3, period))).max())
        tt_pass = trace < 2e-14 and divergence < 2e-13 and reconstruction < 2e-14 and bad > .009
        result.update(path=str(path.relative_to(ROOT)), sha256=expected_sha,
                      trace_abs_max=trace, divergence_abs_max=divergence,
                      independent_svd_reconstruction_max=reconstruction,
                      mode_checks=mode_rows, deliberately_invalid_harmonic_velocity=bad)
        if not tt_pass:
            result['status'] = 'FAIL'
    return result


def initial_checks(m, limit):
    sources = {str(Path(k).resolve()): v for k, v in m['source_sha256'].items()}
    paths = []
    for row in m['cases']:
        initial = checked_path(read(row['spec'])['initial'])
        if initial not in paths:
            paths.append(initial)
    if len(paths) != 156:
        raise ValueError('EXPECTED_156_INITIAL_ARTIFACTS')
    selected = paths[:limit] if limit else paths
    rows = []
    for path in selected:
        result = initial_one(path, sources[str(path)])
        rows.append(result)
        print(json.dumps(dict(event='INITIAL_CHECK', index=len(rows), total=len(selected),
                              path=str(path), status=result['status'])), flush=True)
    return dict(status='PASS' if all(r['status'] == 'PASS' for r in rows) else 'FAIL',
                rows=rows, selected=len(selected), full_initial_count=len(paths),
                scope='Independent original initial constraints, harmonic/TT checks and SVD seed reconstruction on saved mesh points.')


def authenticated_window(case, window_index, analysis):
    directory = checked_path(Path(analysis) / case)
    record_path = directory / 'ASSEMBLY.json'
    record = read(record_path)
    if record['case'] != case:
        raise ValueError('ASSEMBLY_CASE')
    for path, expected in record['input_sha256'].items():
        checked_path(path, expected)
    history = directory / 'histories' / f'{case}_window{window_index}.npz'
    if str(history) not in record['output_sha256']:
        raise ValueError('UNBOUND_HISTORY')
    checked_path(history, record['output_sha256'][str(history)])
    source_path = history.with_suffix('.sources.json')
    checked_path(source_path, record['output_sha256'][str(source_path)])
    source = read(source_path)
    if source['history_sha256'] != sha(history):
        raise ValueError('WINDOW_HASH')
    for path, expected in source['source_sha256'].items():
        checked_path(path, expected)
    with np.load(history, allow_pickle=False) as data:
        values = {k: data[k] for k in data.files}
    times, g, v = values['times'], values['g'], values['v']
    expected_centers = [1.025, 1.75, 2.49]
    if len(times) != 9 or np.max(abs(np.diff(times) - .0025)) >= 1e-12 or abs(times[4] - expected_centers[window_index]) >= 1e-12:
        raise ValueError('WINDOW_SAMPLING')
    if g.shape != v.shape or g.dtype != np.float64 or v.dtype != np.float64:
        raise ValueError('WINDOW_STATE_SCHEMA')
    # Independently replay all saved arrays from immutable checkpoint payloads.
    # Hash agreement alone would not establish the assembler's array mapping.
    by_tick = {}
    for path in source['source_sha256']:
        if Path(path).name != 'metadata.json':
            continue
        metadata_path = checked_path(path)
        metadata = read(metadata_path)
        if not metadata['eligible_for_resume'] or metadata['diagnostic'] is not None:
            raise ValueError('INELIGIBLE_WINDOW_CHECKPOINT')
        payload = metadata_path.with_name('state.npz')
        if str(payload.relative_to(ROOT)) not in source['source_sha256']:
            raise ValueError('WINDOW_PAYLOAD_NOT_LISTED')
        checked_path(payload, metadata['payload_sha256'])
        marker = metadata_path.with_name('COMMITTED')
        if marker.read_text().strip() != sha(metadata_path):
            raise ValueError('CHECKPOINT_COMMIT')
        tick = metadata['step']
        if tick in by_tick:
            raise ValueError('DUPLICATE_WINDOW_TICK')
        by_tick[tick] = (payload, metadata['t'])
    if sorted(by_tick) != source['ticks'] or len(by_tick) != 9:
        raise ValueError('WINDOW_TICK_COVERAGE')
    for i, tick in enumerate(source['ticks']):
        payload, saved_time = by_tick[tick]
        with np.load(payload, allow_pickle=False) as checkpoint:
            state = checkpoint['state']
        if saved_time != times[i] or not np.array_equal(state[0], g[i]) or not np.array_equal(state[1], v[i]):
            raise ValueError('ASSEMBLER_ARRAY_REPLAY_DISAGREEMENT')
    return values, dict(path=str(history.relative_to(ROOT)), sha256=sha(history),
                        sources_sha256=sha(source_path), assembly_sha256=sha(record_path))


def check_case(m, case, analysis):
    choices = [r for r in m['cases'] if r['id'] == case]
    if len(choices) != 1:
        raise ValueError('CASE_MEMBERSHIP')
    spec = read(choices[0]['spec'])
    assembly = read(checked_path(Path(analysis) / case / 'ASSEMBLY.json'))
    source_spec = checked_path(choices[0]['spec'])
    if assembly['input_sha256'].get(str(source_spec)) != choices[0]['spec_sha256']:
        raise ValueError('ASSEMBLY_CURRENT_SPEC_UNBOUND')
    if assembly['input_sha256'].get(m['_manifest_path']) != m['_manifest_sha256']:
        raise ValueError('ASSEMBLY_CURRENT_MANIFEST_UNBOUND')
    n = spec['n']
    if n not in [24, 32]:
        raise ValueError('CHECK_CASE_MESH')
    windows = []
    verify_weights()
    for index in range(3):
        data, binding = authenticated_window(case, index, analysis)
        if data['g'].shape != (9, n, n, n, 4, 4):
            raise ValueError('CASE_WINDOW_SHAPE')
        period = float(data['period'])
        if abs(period - spec['period']) >= 1e-14:
            raise ValueError('WINDOW_PERIOD')
        original = analyze(data['g'], data['times'], period)
        computed = {order: center_ricci(data['g'], data['times'], period, order) for order in [6, 8]}
        stride = n // 8
        centers = {str(order): dict(ricci_max=float(abs(r).max()),
                                    common8_max=float(abs(r[::stride, ::stride, ::stride]).max()),
                                    ricci_rms=float(np.sqrt(np.mean(r * r))))
                   for order, r in computed.items()}
        row = dict(index=index, binding=binding, original=original, centers=centers,
                   sixth_eighth_tensor_max_difference=float(abs(computed[6] - computed[8]).max()))
        if index == 2:
            row['late_adm'] = [dict(time=float(data['times'][j]), **adm_row(data['g'][j], data['v'][j], period))
                               for j in [0, 4, 8]]
        windows.append(row)
        print(json.dumps(dict(event='WINDOW_CHECK', case=case, window=index,
                              original_ricci_max=original['ricci_max'])), flush=True)
    residuals_pass = all(w['original']['ricci_max'] <= LIMIT for w in windows)
    late_pass = all(r['status'] == 'PASS' for r in windows[2]['late_adm'])
    return dict(status='PASS' if residuals_pass and late_pass else 'FAIL', case=case, n=n,
                windows=windows, residual_limit=LIMIT,
                scope='Original saved-g Ricci:15 interior time slices; late original ADM:3 slices; sixth/eighth center diagnostics:3 events. All spatial points, except explicitly common8 summary.')


def controls():
    verify_weights()
    records = []
    times = 2.49 + np.arange(-4, 5) * .0025
    for label, p in [('kasner', (-1/3, 2/3, 2/3)), ('nonvacuum_kasner', (.2, .3, .5))]:
        history = own_kasner(times, 4, p)
        expected = np.zeros((4, 4))
        expected[0, 0] = sum(p) - sum(x * x for x in p)
        for order in [6, 8]:
            r = center_ricci(history, times, 2 * np.pi, order)
            error = float(abs(r - expected).max())
            if error >= 2e-8 or (label.startswith('nonvacuum') and abs(r).max() <= .6):
                raise ValueError('STENCIL_ANALYTIC_CONTROL')
            records.append(dict(label=label, order=order, error=error, ricci_max=float(abs(r).max())))
    for h in [.2, 5.]:
        history = np.zeros((9, 4, 4, 4, 4, 4))
        history[..., 0, 0] = -1
        for i in range(1, 4):
            history[..., i, i] = np.exp(2 * h * (times - 2.49))[:, None, None, None]
        expected = np.diag([-3*h*h, 3*h*h, 3*h*h, 3*h*h])
        for order in [6, 8]:
            r = center_ricci(history, times, 2*np.pi, order)
            error = float(abs(r-expected).max())
            if error >= 1e-7 or abs(r).max() <= .1:
                raise ValueError('STENCIL_NONVACUUM_FLRW_CONTROL')
            records.append(dict(label='exponential_flrw', h=h, order=order,
                                error=error, ricci_max=float(abs(r).max())))
    return dict(status='PASS', rational_stencil_moments=True, adm=adm_controls(),
                original_ricci=ricci_controls(), stencil_controls=records)


def aggregate(m, analysis, results, limit):
    cases = m['cases'][:limit] if limit else m['cases']
    names = [r['id'] for r in cases]
    if len(cases) % 3:
        raise ValueError('AGGREGATE_REQUIRES_COMPLETE_DATASET_TRIPLES')
    rows, missing = {}, []
    for case in cases:
        p = checked_path(Path(results) / (case['id'] + '.json'))
        if not p.exists():
            missing.append(case['id'])
            continue
        result = read(p)
        if (result['case'] != case['id'] or result['method_sources'] != method_sources()
                or result['manifest_sha256'] != m['_manifest_sha256']):
            raise ValueError('RESULT_METHOD_OR_CASE_CHANGED')
        rows[case['id']] = result
    datasets = []
    for start in range(0, len(names), 3):
        a, b, c = names[start:start+3]
        dataset = a.removesuffix('_n24')
        if [a, b, c] != [dataset+'_n24', dataset+'_n24_half', dataset+'_n32']:
            raise ValueError('DATASET_TRIPLE_ORDER')
        if any(name not in rows for name in [a, b, c]):
            datasets.append(dict(dataset=dataset, status='UNTESTED_OR_INCOMPLETE'))
            continue
        coarse, fine = [authenticated_window(name, 2, analysis)[0] for name in [a, b]]
        if not np.array_equal(coarse['times'], fine['times']):
            raise ValueError('FINAL_TIME_MISMATCH')
        temporal = {key: float(abs(coarse[key][-1] - fine[key][-1]).max()) for key in ['g', 'v']}
        spatial = []
        for order in ['6', '8']:
            low = max(w['centers'][order]['common8_max'] for w in rows[a]['windows'])
            high = max(w['centers'][order]['common8_max'] for w in rows[c]['windows'])
            all_max = max(w['centers'][order]['ricci_max'] for name in [a, c] for w in rows[name]['windows'])
            # The small-error exception uses all points of both meshes; the
            # improvement ratio compares the same common8 marked events.
            passed = low >= 10 * high or all_max < SMALL
            spatial.append(dict(order=int(order), coarse_common8_max=low, fine_common8_max=high,
                                ratio=None if high == 0 else low/high, all_points_both_meshes_max=all_max,
                                status='PASS' if passed else 'INCONCLUSIVE_REFINEMENT'))
        passed = (all(rows[name]['status'] == 'PASS' for name in [a, b, c])
                  and max(temporal.values()) <= TIME_LIMIT
                  and all(r['status'] == 'PASS' for r in spatial))
        datasets.append(dict(dataset=dataset, status='PASS' if passed else 'DIAGNOSTIC_NOT_QUALIFIED',
                             original_equations={name: rows[name]['status'] for name in [a, b, c]},
                             final_time_refinement=temporal,
                             temporal_status='PASS' if max(temporal.values()) <= TIME_LIMIT else 'FAIL',
                             spatial=spatial))
    return dict(status='PASS' if not missing and all(d['status'] == 'PASS' for d in datasets) else 'INCOMPLETE_OR_DIAGNOSTIC',
                selected_cases=len(cases), checked_cases=len(rows), missing_cases=missing,
                datasets=datasets, result_sha256={str(Path(results)/f'{name}.json'):sha(Path(results)/f'{name}.json') for name in rows},
                scope='Finite dataset-level diagnostics. Inconclusive refinement is not physical exclusion, nonexistence or an equation-selection result.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['controls', 'initial', 'case', 'aggregate'])
    parser.add_argument('--manifest', default=str(BASE/'production_runtime/campaign.json'))
    parser.add_argument('--analysis', default=str(BASE/'production_analysis'))
    parser.add_argument('--results', default=str(HERE/'cases'))
    parser.add_argument('--case')
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.limit < 0:
        parser.error('nonnegative limit required')
    start = time.monotonic()
    if args.mode == 'controls':
        result = controls()
    else:
        m = manifest(args.manifest)
        if args.mode == 'initial':
            result = initial_checks(m, args.limit)
        elif args.mode == 'case':
            if not args.case:
                parser.error('--case required')
            result = check_case(m, args.case, args.analysis)
        else:
            result = aggregate(m, args.analysis, args.results, args.limit)
        result['manifest_sha256'] = sha(args.manifest)
    result.update(method_sources=method_sources(), numpy=np.__version__, seconds=time.monotonic()-start,
                  reviewer_context='/root/survey_math', producer_imports=False,
                  attribution='Reuses fixed independently authored TDS1 NumPy Ricci/ADM and TPP1 center-stencil/Lie-shift methods. Shared fields and Fourier mathematics, no independent general-data time integrator.')
    write(args.output, result)
    print(json.dumps(dict(status=result['status'], output=args.output, seconds=result['seconds'])), flush=True)
    if result['status'] not in ['PASS']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
