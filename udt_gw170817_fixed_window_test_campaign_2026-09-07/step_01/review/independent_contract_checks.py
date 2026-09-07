"""Metadata/calibration-only FW1 checks; never open HDF5 strain datasets.

Standard-library independent archive parsing and exact finite operator examples.
The examples disprove universal shortcuts; they are not a model of the event.
"""
import bisect
import cmath
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path
import re
import sys
import tarfile

CACHE = Path('/tmp/udt-gw170817-fixed-window-xshnIR')
CORE = (1187008780, 1187008870)
BAND = (30, 500)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def summarize(name, raw):
    rows = [list(map(float, line.split())) for line in raw.decode().splitlines()
            if line.strip() and not line.lstrip().startswith('#')]
    assert rows and all(len(r) == 7 for r in rows)
    assert all(all(math.isfinite(x) for x in r) for r in rows)
    assert all(a[0] < b[0] for a, b in zip(rows, rows[1:]))
    assert all(0 < r[3] <= r[1] <= r[5] and r[4] <= r[2] <= r[6]
               for r in rows)
    selected = [r for r in rows if BAND[0] <= r[0] <= BAND[1]]
    assert rows[0][0] <= BAND[0] and rows[-1][0] >= BAND[1] and selected
    # These are sample values of pointwise1sigma limits, NOT a hard/joint envelope.
    values = {str(f): {'median_magnitude': g, 'median_phase_rad': p,
                      'minus1sigma_magnitude': gl, 'plus1sigma_magnitude': gh,
                      'minus1sigma_phase_rad': pl, 'plus1sigma_phase_rad': ph}
              for f, g, p, gl, pl, gh, ph in selected}
    return dict(member=name, sha256=sha(raw), rows=len(rows),
                full_frequency_range=[rows[0][0], rows[-1][0]],
                sampled_band_rows=len(selected),
                sampled_band_frequency_range=[selected[0][0], selected[-1][0]],
                median_magnitude_range=[min(r[1] for r in selected), max(r[1] for r in selected)],
                median_phase_range_rad=[min(r[2] for r in selected), max(r[2] for r in selected)],
                sigma_boundary_magnitude_range=[min(r[3] for r in selected), max(r[5] for r in selected)],
                sigma_boundary_phase_range_rad=[min(r[4] for r in selected), max(r[6] for r in selected)],
                maximum_sampled_median_true_model_distance=max(abs(cmath.rect(r[1], r[2])-1) for r in selected),
                maximum_sampled_median_model_true_distance=max(abs(1/cmath.rect(r[1], r[2])-1) for r in selected),
                sample_values=values)


def calibration():
    result = {}
    archive = CACHE / 'LIGO_O2_cal_uncertainty.tgz'
    with tarfile.open(archive, 'r:gz') as tf:
        members = {}
        for info in tf.getmembers():
            match = re.fullmatch(r'(H1|L1)/.*_GPSTime_(\d+)_C02_RelativeResponseUncertainty_FinalResults\.txt', info.name)
            if match:
                members.setdefault(match[1], []).append((int(match[2]), info))
        for detector, items in members.items():
            items.sort(key=lambda x: x[0])
            times = [t for t, _ in items]
            loc = bisect.bisect_right(times, CORE[0])
            previous, following = items[loc-1], items[loc]
            nearest = min(items, key=lambda pair: abs(pair[0]-(CORE[0]+CORE[1])/2))
            result[detector] = dict(archive_member_count=len(items),
                preceding_gps=previous[0], following_gps=following[0],
                preceding_gap_to_core_seconds=CORE[0]-previous[0],
                following_gap_from_core_seconds=following[0]-CORE[1],
                nearest_gps=nearest[0],
                records=[summarize(info.name, tf.extractfile(info).read())
                         for _, info in (previous, following)])
    with tarfile.open(CACHE/'Virgo_O2_cal_uncertainty.tgz', 'r:gz') as tf:
        members = [m for m in tf.getmembers() if m.isfile() and m.name.endswith('.txt')]
        assert len(members) == 1
        result['V1'] = summarize(members[0].name, tf.extractfile(members[0]).read())
    # Known constant toy calibration verifies correction direction independently.
    true_signal = 2 + 3j
    true_over_model = cmath.rect(1.1, 0.2)
    released = true_signal / true_over_model
    assert abs(released * true_over_model - true_signal) < 1e-14
    wrong_residual = abs(released / true_over_model - true_signal)
    assert wrong_residual > 1
    result['ratio_direction_control'] = dict(correct_residual=abs(released*true_over_model-true_signal),
                                             wrong_inverse_residual=wrong_residual)
    return result


def operator_controls():
    # Valid instantaneous response F(t)=((1,0),(0,1),(t,1)).
    times = list(range(5))
    a = [Q(t) for t in times]
    b = [Q(2-t) for t in times]
    d = [a, b, [t*x+y for t, x, y in zip(times, a, b)]]
    pointwise = [d[2][i]-times[i]*d[0][i]-d[1][i] for i in times]
    assert not any(pointwise)
    smooth = lambda x: [sum(x[i-1:i+2], Q(0))/3 for i in range(1, 4)]
    sd = [smooth(x) for x in d]
    wrong = [sd[2][j]-times[i]*sd[0][j]-sd[1][j] for j, i in enumerate(range(1, 4))]
    correct = smooth(pointwise)
    assert wrong == [Q(2,3)]*3 and correct == [0]*3
    # Actual defect insertion into this finite test: claiming prefiltered null zero
    # must fail the exact equality, not merely print a rejection label.
    caught = False
    try:
        assert wrong == [0]*3
    except AssertionError:
        caught = True
    assert caught
    # Frequency-dependent toy response includes one sample delay on first waveform.
    taper = list(map(Q, [0, 1, 2, 1, 0]))
    shift = lambda x: [Q(0)] + x[:-1]
    delayed = [x+y for x, y in zip(shift(a), b)]
    w = lambda x: [p*y for p, y in zip(taper, x)]
    taper_wrong = [x-y-z for x, y, z in zip(w(delayed), shift(w(a)), w(b))]
    assert taper_wrong == [0, 0, 1, -2, -3]
    taper_caught = False
    try:
        assert not any(taper_wrong)
    except AssertionError:
        taper_caught = True
    assert taper_caught
    return dict(time_varying_response_before_filter_null=list(map(str, pointwise)),
                filter_before_time_varying_null=list(map(str, wrong)),
                filter_after_null=list(map(str, correct)),
                varying_response_shortcut_caught=caught,
                taper_before_delay_null=list(map(str, taper_wrong)),
                taper_delay_shortcut_caught=taper_caught,
                scope='Exact finite counterexamples; no observed samples or producer implementation tested.')


if __name__ == '__main__':
    print(json.dumps(dict(python=sys.version, question='Independent calibration metadata and operator-contract audit',
                         core=CORE, band=BAND, calibration=calibration(),
                         operators=operator_controls()), indent=2, sort_keys=True))
