"""LC2: one frozen published-summary calculation; no observation fit.

All physical/calibration numbers come from reviewed LC1 INPUTS.json. Its
interpretive/error assumptions and exclusions remain load-bearing. Decimal
arithmetic and local guards are method/regression, not empirical certification.
"""
import copy
import hashlib
import json
import platform
import sys
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 60
D = Decimal
PACKAGE = Path(__file__).resolve().parents[1]
INPUTS = PACKAGE / "step_01/INPUTS.json"
EXPECTED_INPUT_SHA = "a006e39a03b2ee70418ecee614c9056fe3e1c4a04b110478cdb536d01f410b9f"
EXPECTED_CONTRACT_SHA = "ac6cbaeb359713d90abb71b43e83a47bc2e7d669f878c01c1b1455cb1c8541e4"
ARITHMETIC_TOLERANCE = D('1e-45')  # numeric regression, not observation tolerance


def load_inputs():
    raw = INPUTS.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_INPUT_SHA:
        raise ValueError("frozen input hash mismatch")
    contract = (PACKAGE / "step_01/COMPARISON_CONTRACT.md").read_bytes()
    if hashlib.sha256(contract).hexdigest() != EXPECTED_CONTRACT_SHA:
        raise ValueError("reviewed contract hash mismatch")
    return json.loads(raw)


def evaluate(data):
    m, c = data['measurement'], data['calibration']
    y, uy = D(m['corrected_gradient']), D(m['total_standard_uncertainty'])
    us = D(m['systematic_standard_uncertainty_sensitivity_only'])
    g, ce = D(c['g_magnitude_m_s2']), D(c['c_E_m_s'])
    length, unit = D(c['metres_per_centimetre']), D(c['fractional_frequency_unit'])
    ur = D(c['reference_standard_uncertainty_upper_cap'])
    mu = -g * length / (ce*ce*unit)
    residual = y - mu
    q, envelope = (uy*uy+ur*ur).sqrt(), uy+ur
    kappa, ukappa = -y*unit/length, uy*unit/length
    bands = {}
    for name, width in [('Q', q), ('C', envelope)]:
        threshold = width-abs(residual)
        bands[name] = {'width': str(width),
                       'lower': str(residual-width), 'upper': str(residual+width),
                       'zero_in_band': abs(residual) <= width,
                       'all_displacements_threshold': str(threshold) if threshold >= 0 else None}
    shifts = []
    for t in data['diagnostic_controls']['systematic_shift_multipliers']:
        shift = D(t)*us
        center = residual+shift
        shifts.append({'multiplier': t, 'displacement': str(shift), 'center': str(center),
                       'Q_zero_in_shifted_band': abs(center) <= q,
                       'C_zero_in_shifted_band': abs(center) <= envelope})
    return {
        'input_sha256': EXPECTED_INPUT_SHA, 'contract_sha256': EXPECTED_CONTRACT_SHA,
        'experiment_count': m['independent_experiment_count'],
        'reference_origin': 'independent_calibration',
        'measurement_uncertainty_origin': 'reported_total',
        'error_hard_bound_or_confidence_coverage_claimed': False,
        'gradient_coefficient_units': '1e-19 per cm, downward ordering',
        'y': str(y), 'measurement_standard_uncertainty': str(uy),
        'reference': str(mu), 'reference_standard_uncertainty_cap': str(ur),
        'printed_reference_difference': str(mu-D(c['printed_reference_gradient_rounding_check_only'])),
        'residual': str(residual), 'bands': bands,
        'normalized_difference_fixed_reference': str(residual/abs(mu)),
        'Q_standardized_difference_using_upper_width': str(residual/q),
        'C_standardized_difference_using_upper_width': str(residual/envelope),
        'clock_only': {
            'effective_linear_kappa_up_per_m': str(kappa), 'standard_uncertainty_per_m': str(ukappa),
            'band_lower_per_m': str(kappa-ukappa), 'band_upper_per_m': str(kappa+ukappa),
            'equivalent_support_acceleration_m_s2': str(ce*ce*kappa),
            'standard_uncertainty_acceleration_m_s2': str(ce*ce*ukappa),
            'independent_gravimeter_measurement': False},
        'zero_mismatch_displacement': str(-residual),
        'diagnostic_displacements': shifts,
        'interpretation': 'retrospective conditional effective-linear metric benchmark; not a fit or unique UDT test'}


def close(a, b):
    return abs(D(a)-D(b)) <= ARITHMETIC_TOLERANCE


def validate(data, result):
    """Claim-relevant regression guards; independent review checks the argument."""
    c, m = data['calibration'], data['measurement']
    ce, g = D(c['c_E_m_s']), D(c['g_magnitude_m_s2'])
    length, unit = D(c['metres_per_centimetre']), D(c['fractional_frequency_unit'])
    y, uy = D(m['corrected_gradient']), D(m['total_standard_uncertainty'])
    ur, mu = D(c['reference_standard_uncertainty_upper_cap']), D(result['reference'])
    assert result['experiment_count'] == 1, 'duplicate experiment'
    assert result['reference_origin'] == 'independent_calibration', 'target-derived reference'
    assert result['measurement_uncertainty_origin'] == 'reported_total', 'wrong uncertainty type'
    assert result['error_hard_bound_or_confidence_coverage_claimed'] is False, 'unsupported coverage'
    assert mu < 0, 'reference sign'
    assert close(mu*ce*ce*unit/length, -g), 'inverse dimension/sign mapping'
    assert abs(mu-D(c['printed_reference_gradient_rounding_check_only'])) <= D(c['rounding_check_absolute_tolerance']), 'printed reference correspondence'
    assert D(result['measurement_standard_uncertainty']) == uy, 'stat-only/double-counted uncertainty'
    assert close(D(result['residual'])+mu, y), 'residual identity'
    assert close(D(result['bands']['Q']['width'])**2, uy*uy+ur*ur), 'quadrature equation'
    assert D(result['bands']['C']['width']) == uy+ur, 'covariance envelope'
    co = result['clock_only']
    assert close(-D(co['effective_linear_kappa_up_per_m'])*length/unit, y), 'clock-only gradient units/sign'
    assert close(D(co['standard_uncertainty_per_m'])*length/unit, uy), 'clock-only marginal uncertainty'
    assert close(D(co['equivalent_support_acceleration_m_s2'])/(ce*ce), co['effective_linear_kappa_up_per_m']), 'acceleration conversion'
    residual = D(result['residual'])
    for name in ('Q', 'C'):
        b = result['bands'][name]
        width = D(b['width'])
        assert close(b['lower'], residual-width) and close(b['upper'], residual+width), 'band endpoints'
        assert b['zero_in_band'] == (D(b['lower']) <= 0 <= D(b['upper'])), 'band overlap'
        t = width-abs(residual)
        assert b['all_displacements_threshold'] == (str(t) if t >= 0 else None), 'all-displacements threshold'
    assert len(result['diagnostic_displacements']) == len(data['diagnostic_controls']['systematic_shift_multipliers']), 'scenario coverage'
    for row, t in zip(result['diagnostic_displacements'], data['diagnostic_controls']['systematic_shift_multipliers']):
        shift = D(t)*D(m['systematic_standard_uncertainty_sensitivity_only'])
        center = D(row['center'])
        assert row['multiplier'] == t and D(row['displacement']) == shift, 'scenario identity'
        assert close(center, residual+shift), 'shifted center'
        for name in ('Q', 'C'):
            width = D(result['bands'][name]['width'])
            assert row[name+'_zero_in_shifted_band'] == (center-width <= 0 <= center+width), 'R1 moving-band criterion'


def catch_proofs(data, original):
    mutations = {}
    r = copy.deepcopy(original); r['reference'] = str(-D(r['reference'])); mutations['sign_reversal'] = r
    r = copy.deepcopy(original); r['reference'] = str(D(r['reference'])/D(data['calibration']['metres_per_centimetre'])); mutations['missing_cm_conversion'] = r
    r = copy.deepcopy(original); r['measurement_standard_uncertainty'] = data['measurement']['statistical_standard_uncertainty_documentation_only']; mutations['statistical_only_uncertainty'] = r
    r = copy.deepcopy(original); r['experiment_count'] = 2; mutations['same_experiment_counted_twice'] = r
    r = copy.deepcopy(original); r['reference_origin'] = 'clock_target'; r['reference'] = r['y']; mutations['circular_reference'] = r
    r = copy.deepcopy(original)
    for row in r['diagnostic_displacements']:
        for name in ('Q', 'C'):
            row[name+'_zero_in_shifted_band'] = abs(D(row['displacement'])) <= D(r['bands'][name]['width'])
    mutations['R1_old_center_rule'] = r
    r = copy.deepcopy(original); r['error_hard_bound_or_confidence_coverage_claimed'] = True; mutations['unsupported_coverage_label'] = r
    caught = []
    for name, mutant in mutations.items():
        try:
            validate(data, mutant)
        except AssertionError as exc:
            caught.append({'mutation': name, 'rejected': True, 'guard': str(exc)})
        else:
            raise AssertionError('false pass: '+name)
    return caught


if __name__ == '__main__':
    data = load_inputs()
    result = evaluate(data)
    validate(data, result)
    catches = catch_proofs(data, result)
    print(json.dumps({'python': sys.version, 'platform': platform.platform(),
                      'decimal_digits': getcontext().prec, 'arithmetic_tolerance': str(ARITHMETIC_TOLERANCE),
                      'result': result, 'catch_proofs': catches,
                      'limits': ['rounded source errors assumed adequate/centered',
                                 'no Gaussian, confidence-coverage or realized-error bound',
                                 'C varies only cross-correlation of the two summaries',
                                 'bias scenarios not fitted or added uncertainty',
                                 'source local stationary/linear readout model supplied',
                                 'no raw fit, new independent experiment or physical adoption']}, indent=2))
