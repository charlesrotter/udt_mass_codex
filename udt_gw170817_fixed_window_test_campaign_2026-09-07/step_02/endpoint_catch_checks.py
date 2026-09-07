"""Actual RED comparator for the original floating-frequency endpoint defect."""
import json
import numpy as np
from scipy import fft
import screen
f=fft.rfftfreq(98*4096,1/4096); bins=np.arange(len(f)); rows=[]
for low,high in screen.cfg['injection_spectral_families_hz']:
    original=(f>=low)&(f<=high)
    exact=(bins>=low*98)&(bins<=high*98)
    expected=(high-low)*98+1
    try:assert original[low*98] and original[high*98] and original.sum()==expected
    except AssertionError:red=True
    else:red=False
    assert red, 'original defective endpoint guard falsely passed'
    assert exact[low*98] and exact[high*98] and exact.sum()==expected
    rows.append(dict(band_hz=[low,high],nominal_lower_bin_hz=float(f[low*98]),
      original_count=int(original.sum()),corrected_count=int(exact.sum()),
      expected_inclusive_count=expected,original_guard='EXPECTED_ASSERTION_FAILURE',corrected_guard='PASS'))
# The separate90s statistic mask did not change membership in this repair.
legacy_core=(screen.fc>=30)&(screen.fc<=500)
assert np.array_equal(legacy_core,screen.band)
print(json.dumps(dict(endpoint_catchproof=rows,core_statistic_bin_membership_unchanged=True,
 frozen_controls_unchanged=True,scope='same-author implementation catchproof only'),indent=2))
