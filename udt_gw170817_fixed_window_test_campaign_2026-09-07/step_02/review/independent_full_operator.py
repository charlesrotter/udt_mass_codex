"""Frozen-size synthetic operator checks, still without observed arrays."""
import hashlib
import json
from pathlib import Path
import numpy as np
import independent_operator as op

repo = Path(__file__).resolve().parents[3]
d = json.loads((repo/'udt_complementary_wave_observable_campaign_2026-09-07/step_02/design_run.stdout').read_text())
F = np.array(d['F_HLV_plus_cross'])
tau = np.array(d['arrival_minus_geocenter_seconds'])
b = op.nullrow(F)
h = np.array([op.waveform(0, 0), op.waveform(1, 1)])
raw = np.array([op.shift(F[i] @ h, -tau[i]) for i in range(3)])
network_norm = np.linalg.norm(raw)
good = op.residual(raw, tau, b)
bad_sign = op.residual(raw, -tau, b)
b_omit = b.copy()
b_omit[0] = 0
bad_H = op.residual(raw, tau, b_omit)
measured = {key: float(np.linalg.norm(v)/network_norm) for key, v in
            [('correct', good), ('wrong_sign', bad_sign), ('omitted_H', bad_H)]}
catches = {}
for label in ('wrong_sign', 'omitted_H'):
    try:
        assert measured[label] < 1e-10
    except AssertionError:
        catches[label] = True
    else:
        catches[label] = False
assert measured['correct'] < 1e-10
assert all(measured[k] > 1e-3 for k in catches)
assert all(catches.values())
norm_errors = []
roundtrip_errors = []
fourier_anchors = []
for family in range(3):
    for phase in range(8):
        s = op.waveform(family, phase)
        core = s[op.CROP:-op.CROP]
        norm_errors.append(abs(np.sqrt(np.dot(core, core)/op.FS)-1))
        if phase == 0:
            rt = op.shift(op.shift(s, -tau[2]), tau[2])[op.CROP:-op.CROP]
            roundtrip_errors.append(np.linalg.norm(rt-core)/np.linalg.norm(core))
            chosen = np.array([30*90, 61*90, 137*90, 500*90])
            a = op.direct_bins(core, chosen)
            z = np.fft.fft(core*op.HANN)[chosen]
            fourier_anchors.append(float(np.linalg.norm(a-z)/np.linalg.norm(z)))
assert max(norm_errors) < 1e-12
assert max(roundtrip_errors) < 1e-10
assert max(fourier_anchors) < 1e-10
print(json.dumps({'source_first': True, 'observed_arrays': False,
                  'N':op.N,'M':op.M,'retained_bin_count':len(op.KEEP),
                  'method':'full FFT operator; direct Fourier sum anchors; no author imports',
                  'relative_errors':measured, 'actually_failed_bad_zero_assertions':catches,
                  'maximum_hrss_norm_error':float(max(norm_errors)),
                  'roundtrip_errors':list(map(float,roundtrip_errors)),
                  'direct_fourier_anchor_errors':fourier_anchors,
                  'operator_source_sha256':hashlib.sha256(Path(op.__file__).read_bytes()).hexdigest()},indent=2))
