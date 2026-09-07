"""Actual floating-grid endpoint false failure versus exact frozen bin set."""
import json
import numpy as np
from scipy import fft
from independent_operator import N, FS

f = fft.rfftfreq(N,1/FS)
rows = []
for low,high in ((30,500),(30,100),(100,500)):
    exact = np.arange(low*98,high*98+1)
    floating = np.flatnonzero((f>=low)&(f<=high))
    rejected = False
    try:
        assert np.array_equal(floating,exact)
    except AssertionError:
        rejected = True
    assert rejected
    omitted = np.setdiff1d(exact,floating)
    assert np.array_equal(omitted,[low*98])
    # The proposed exact-integer correction includes both endpoints, all and
    # only indices solving low <= k/98 <= high.
    corrected = np.flatnonzero((np.arange(len(f))>=low*98)&(np.arange(len(f))<=high*98))
    assert np.array_equal(corrected,exact)
    rows.append({'band':[low,high],'intended_count':len(exact),'producer_count':len(floating),
                 'omitted_indices':omitted.tolist(),'omitted_float_labels':f[omitted].tolist(),
                 'floating_gate_actually_failed':rejected,'integer_correction_passed':True})
print(json.dumps({'scope':'frozen inclusive-bin fidelity, no strain input',
                  'failure':'floating low-edge label rounds below exact inclusive cutoff',
                  'rows':rows},indent=2))
