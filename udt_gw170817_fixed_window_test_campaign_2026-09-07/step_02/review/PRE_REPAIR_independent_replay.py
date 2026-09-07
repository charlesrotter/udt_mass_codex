"""Independent observed-data replay after source seal and author-ready.

No author implementation imports. Uses the source-first independent_operator.
Only exact 99 offsource detector extracts can be opened as sample arrays.
"""
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import independent_operator as op

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent
REPO = HERE.parents[2]
CACHE = Path('/tmp/udt-gw170817-fixed-window-xshnIR/offsource')
def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024**2), b''):
            h.update(chunk)
    return h.hexdigest()
ready = json.loads((TARGET/'AUTHOR_CANDIDATE_READY.json').read_text())
assert (HERE/'SOURCE_FIRST_SEAL.md').exists()
pin_names = {'candidate':'CANDIDATE.md','producer':'screen.py','evaluation':'evaluation_run.stdout',
             'training':'training_run.stdout','diagnostic':'diagnostic_run.stdout',
             'psd':'PSD_training.npz','coefficients':'reinjection_coefficients.npz'}
for key, name in pin_names.items():
    assert sha(TARGET/name) == ready[key+'_sha256']
freeze = TARGET.parent/'step_01/FREEZE.json'
assert sha(freeze) == 'fa0506eaea5ef20dcd92aabf3b2d1a0efc7fb75ef6c7272c00e5e6764c591324'
cfg = json.loads(freeze.read_text())
metadata = TARGET.parent/'step_01/metadata_filtered_run.stdout'
assert sha(metadata) == '9e6c1d6fa98e14e0b2c060e18d4e7b46aacc35890aff46c51474ca03ce1f74af'
meta = json.loads(metadata.read_text())
design_path = REPO/cfg['design_dependency']
assert sha(design_path) == cfg['design_sha256']
design = json.loads(design_path.read_text())
F = np.array(design['F_HLV_plus_cross'])
delays = np.array(design['arrival_minus_geocenter_seconds'])
b = op.nullrow(F)
starts = meta['offsource_core_starts_gps']
assert len(starts) == 33 and starts[:12] == meta['training_core_starts_gps']
assert starts[12:] == meta['reference_core_starts_gps']
manifest_by_det = {}
extract_hashes = {}
for det in ('H1','L1','V1'):
    manifest = json.loads((TARGET/(det+'_extract_run.stdout')).read_text())
    assert manifest['source_sha256'] == meta['files'][det]['sha256']
    assert [r['core_gps'] for r in manifest['records']] == starts
    for row in manifest['records']:
        start = row['core_gps']
        support = [start-4, start+94]
        assert support[1] <= 1187008680 or support[0] >= 1187008980
        assert row['support_gps'] == support and row['count'] == op.N
        assert row['sample_start'] == (support[0]-1187008512)*op.FS
        assert row['bytes'] == op.N*8 and row['returncode'] == 0 and row['stderr'] == ''
        command = row['command']
        assert command[command.index('-s')+1] == str(row['sample_start'])
        assert command[command.index('-c')+1] == str(op.N)
        assert command[command.index('-b')+1] == 'LE'
        path = CACHE/f'{det}_{start}_98s_f64le.bin'
        assert str(path) == command[command.index('-o')+1]
        assert path.stat().st_size == op.N*8
        extract_hashes[path.name] = sha(path)
        assert extract_hashes[path.name] == row['sha256']
    manifest_by_det[det] = manifest

def load_raw(start):
    assert start in starts
    assert start+94 <= 1187008680 or start-4 >= 1187008980
    values = []
    for det in ('H1','L1','V1'):
        x = np.fromfile(CACHE/f'{det}_{start}_98s_f64le.bin',dtype='<f8')
        assert x.shape == (op.N,) and np.isfinite(x).all()
        values.append(x*1e21)
    return np.array(values)

training_psds = []
training_reconstruction_errors = []
training_diagonal_psds = []
for start in starts[:12]:
    raw = load_raw(start)
    aligned = np.array([op.shift(x,tau)[op.CROP:-op.CROP] for x,tau in zip(raw,delays)])
    r = b @ aligned
    training_psds.append(op.welch_manual(r))
    diagonal = sum(b[i]**2*op.welch_manual(aligned[i]) for i in range(3))
    training_diagonal_psds.append(diagonal)
    # Polarization identity gives real cross covariance without scipy.csd.
    reconstructed = diagonal.copy()
    for i,j in ((0,1),(0,2),(1,2)):
        plus = op.welch_manual(b[i]*aligned[i]+b[j]*aligned[j])
        minus = op.welch_manual(b[i]*aligned[i]-b[j]*aligned[j])
        reconstructed += (plus-minus)/2
    training_reconstruction_errors.append(float(np.linalg.norm(reconstructed-training_psds[-1])/np.linalg.norm(training_psds[-1])))

training_psds = np.array(training_psds)
psd = training_psds.mean(axis=0)
diagonal_psd = np.mean(training_diagonal_psds,axis=0)
retained_psd = np.interp(op.CORE_FREQ[op.KEEP],op.WFREQ,psd)
assert np.isfinite(retained_psd).all() and (retained_psd > 0).all()
floor_count = int(np.count_nonzero(retained_psd < 1e-18))
assert floor_count == 0
with np.load(TARGET/'PSD_training.npz',allow_pickle=False) as author:
    assert np.array_equal(author['frequency_hz'],op.WFREQ)
    psd_relative = float(np.linalg.norm(psd-author['residual_psd_scaled'])/np.linalg.norm(psd))
    psd_band_max_relative = float(np.max(np.abs(np.interp(op.CORE_FREQ[op.KEEP],op.WFREQ,author['residual_psd_scaled'])/retained_psd-1)))
    each_relative = float(np.linalg.norm(training_psds-author['per_window_residual_psd_scaled'])/np.linalg.norm(training_psds))
assert max(psd_relative,psd_band_max_relative,each_relative) < 1e-10

cores = []
features = []
q_values = []
decompositions = []
fourier_anchors = []
for start in starts[12:]:
    raw = load_raw(start)
    core = op.residual(raw,delays,b)
    z = op.core_transform(core)
    q = op.weighted_Q(z,retained_psd)
    cores.append(core)
    features.append(z)
    q_values.append(q)
    if start in (1187010216,1187011516):
        channel_z = [op.core_transform(b[i]*op.shift(raw[i],delays[i])[op.CROP:-op.CROP]) for i in range(3)]
        diag = [op.weighted_Q(v,retained_psd) for v in channel_z]
        cross = [float(np.mean(4*np.real(channel_z[i].conj()*channel_z[j])/(op.FS*op.TAPER_ENERGY*retained_psd))) for i,j in ((0,1),(0,2),(1,2))]
        reconstructed = sum(diag)+sum(cross)
        decompositions.append({'start':start,'Q':q,'diagonal_Q':diag,'cross_HL_HV_LV':cross,
                               'relative_reconstruction':abs(reconstructed-q)/q})
        chosen = np.array([30*90,61*90,137*90,500*90])
        summed = op.direct_bins(core,chosen)
        fast = np.fft.fft(core*op.HANN)[chosen]
        fourier_anchors.append(float(np.linalg.norm(summed-fast)/np.linalg.norm(fast)))

features = np.array(features)
q_values = np.array(q_values)
threshold = float(q_values.max())
author_evaluation = json.loads((TARGET/'evaluation_run.stdout').read_text())
author_q = np.array(author_evaluation['reference_Q'])
q_relative = float(np.max(abs(q_values-author_q)/q_values))
assert q_relative < 1e-10
grid = np.array(cfg['effect_grid'])*1e21
grid_fractions = []
target_direct_counts = []
target_quad_counts = []
max_direct_quad_error = 0.
minimum_target_margin = np.inf
all_c = []
all_u = []
full_channel_checks = []
fraction_mismatches = []
for family in range(3):
    grid_crossings = []
    direct_count = 0
    quad_count = 0
    cs = []
    us = []
    for phase in range(8):
        s = op.waveform(family,phase)
        core_s = s[op.CROP:-op.CROP]
        zs = op.core_transform(core_s)
        u = op.weighted_Q(zs,retained_psd)
        c = np.real(np.mean(2*features.conj()*zs/(op.FS*op.TAPER_ENERGY*retained_psd),axis=1))
        quad_grid = q_values[:,None]+2*c[:,None]*grid[None,:]+u*grid[None,:]**2
        grid_crossings.append(quad_grid > threshold)
        cs.append(c)
        us.append(u)
        target_quad = q_values+2*c+u
        direct_values = []
        for index, background in enumerate(cores):
            direct = op.weighted_Q(op.core_transform(background+core_s),retained_psd)
            direct_values.append(direct)
            rel = abs(direct-target_quad[index])/max(abs(direct),abs(target_quad[index]))
            max_direct_quad_error = max(max_direct_quad_error,float(rel))
        direct_values = np.array(direct_values)
        assert np.array_equal(direct_values > threshold,target_quad > threshold)
        direct_count += int(np.count_nonzero(direct_values > threshold))
        quad_count += int(np.count_nonzero(target_quad > threshold))
        minimum_target_margin = min(minimum_target_margin,float(np.min(abs(direct_values-threshold))/threshold))
        if phase == 0:
            for index in (0,int(q_values.argmax()),20):
                for amplitude in (1.,100.):
                    raw = load_raw(starts[12+index])
                    raw[2] += amplitude*op.shift(s,-delays[2])
                    direct = op.weighted_Q(op.core_transform(op.residual(raw,delays,b)),retained_psd)
                    quad = q_values[index]+2*amplitude*c[index]+amplitude**2*u
                    full_channel_checks.append(float(abs(direct-quad)/max(abs(direct),abs(quad))))
    fractions = np.mean(np.array(grid_crossings),axis=(0,1))
    grid_fractions.append(fractions.tolist())
    target_direct_counts.append(direct_count)
    target_quad_counts.append(quad_count)
    if not np.array_equal(fractions,np.array(author_evaluation['families'][family]['crossing_fractions'])):
        fraction_mismatches.append({'family':family,'independent_fractions':fractions.tolist(),
                                   'author_fractions':author_evaluation['families'][family]['crossing_fractions']})
    all_c.append(cs)
    all_u.append(us)
all_c = np.array(all_c)
all_u = np.array(all_u)
with np.load(TARGET/'reinjection_coefficients.npz',allow_pickle=False) as author:
    c_relative = float(np.linalg.norm(all_c-author['cross_terms'])/np.linalg.norm(all_c))
    u_relative = float(np.linalg.norm(all_u-author['signal_Q'])/np.linalg.norm(all_u))
assert max(max_direct_quad_error,max(full_channel_checks)) < 1e-10
assert max(fourier_anchors) < 1e-10
assert max(training_reconstruction_errors) < 1e-10
band_welch = (op.WFREQ>=30)&(op.WFREQ<=500)
result = {'scope':'independent finite released-offsource statistic; event never read',
          'implementation':'source-first full complex FFT + manual Welch + polarization-identity covariance; no author imports',
          'versions':{'python':platform.python_version(),'numpy':np.__version__},
          'extract_count':len(extract_hashes),'all_extract_hashes_and_supports_match':True,
          'PSD_L2_relative_error_to_author':psd_relative,'PSD_retained_max_relative_error_to_author':psd_band_max_relative,
          'PSD_all_training_L2_relative_error_to_author':each_relative,'retained_floor_count':floor_count,
          'PSD_retained_min_physical_strain2_per_hz':float(retained_psd.min()/1e42),
          'training_covariance_polarization_identity_max_relative_error':max(training_reconstruction_errors),
          'training_cross_term_band_L2_relative':float(np.linalg.norm((psd-diagonal_psd)[band_welch])/np.linalg.norm(psd[band_welch])),
          'reference_Q':q_values.tolist(),'reference_Q_max_relative_error_to_author':q_relative,
          'threshold':threshold,'threshold_core_gps':starts[12+int(q_values.argmax())],
          'median_first10':float(np.median(q_values[:10])),'median_last11':float(np.median(q_values[10:])),
          'max_over_min':float(q_values.max()/q_values.min()),'grid_hrss':cfg['effect_grid'],
          'grid_fractions':grid_fractions,'target_direct_counts_out_of_168':target_direct_counts,
          'target_quadratic_counts_out_of_168':target_quad_counts,'direct_target_recomputations':504,
          'direct_target_vs_quadratic_max_relative_error':max_direct_quad_error,
          'minimum_target_margin_over_threshold':minimum_target_margin,
          'full_channel_injection_recomputations':len(full_channel_checks),
          'full_channel_injection_max_relative_error':max(full_channel_checks),
          'cross_coefficients_L2_relative_error_to_author':c_relative,
          'signal_Q_coefficients_L2_relative_error_to_author':u_relative,
          'author_synthetic_fidelity_pass':not fraction_mismatches and max(c_relative,u_relative)<1e-10,
          'author_fraction_mismatches':fraction_mismatches,
          'direct_Fourier_sum_anchor_max_relative_error':max(fourier_anchors),
          'diagnostic_decompositions':decompositions,
          'independent_operator_sha256':sha(HERE/'independent_operator.py'),
          'independent_replay_sha256':sha(__file__),
          'target_ready_sha256':sha(TARGET/'AUTHOR_CANDIDATE_READY.json'),
          'conclusion':'frozen finite target screen fails each family; not population power or event/UDT conclusion'}
print(json.dumps(result,indent=2))

