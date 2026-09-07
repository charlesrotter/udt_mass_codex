"""LC2 source-first arithmetic; imports no candidate code or candidate results."""
import hashlib
import json
import math
import pathlib
import platform
import sys
from fractions import Fraction as F

ROOT = pathlib.Path(__file__).resolve().parents[3]
CAMPAIGN = ROOT / 'udt_local_clock_metric_benchmark_campaign_2026-09-07'
INPUTS = CAMPAIGN / 'step_01/INPUTS.json'
PINS = {
    INPUTS: 'a006e39a03b2ee70418ecee614c9056fe3e1c4a04b110478cdb536d01f410b9f',
    CAMPAIGN / 'step_01/COMPARISON_CONTRACT.md': 'ac6cbaeb359713d90abb71b43e83a47bc2e7d669f878c01c1b1455cb1c8541e4',
    ROOT / 'udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/EXACT_DERIVATION.md': '26897a999e6ad83e1f50c75ba76efe47e9c4c02edd896022a54a69810e57dc12',
    ROOT / 'udt_g276_proper_clock_ce_scale_anchor_reconciliation_2026-08-26/AUDIT_REPORT.md': 'cc66be850523fac561b411b32d7532069d838a6d6e6800568afd72f5560b862d',
    pathlib.Path('/tmp/udt-observation-sources-Kk6TO6/zheng_main.pdf'): '1cb85cfaf2783841e7dc29f8ef38edec258437eec38071b5aba5594ceec4c3b6',
    pathlib.Path('/tmp/udt-observation-sources-Kk6TO6/zheng_supp.pdf'): '111b47f8a3625391178b7d8c5d0753ae8bedbe9f38ea07d6ebdad56cb06f7432',
    pathlib.Path('/tmp/udt-observation-sources-Kk6TO6/zheng_metadata.json'): '827c6152b6a0cc32e4a2991c9acd2910da2006451add08a423eaa9f5371185cc',
}
actual_hashes = {}
for path, expected in PINS.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected, (str(path), actual, expected)
    actual_hashes[str(path)] = actual

raw = json.loads(INPUTS.read_text())
m, c = raw['measurement'], raw['calibration']
y = F(m['corrected_gradient'])
uy = F(m['total_standard_uncertainty'])
usys = F(m['systematic_standard_uncertainty_sensitivity_only'])
gmag = F(c['g_magnitude_m_s2'])
ce = F(c['c_E_m_s'])
cm = F(c['metres_per_centimetre'])
unit = F(c['fractional_frequency_unit'])
ur = F(c['reference_standard_uncertainty_upper_cap'])
mu = -(gmag / ce**2) / (unit / cm)
residual = y - mu
q_var_upper = uy**2 + ur**2
q_sd_upper = math.sqrt(float(q_var_upper))
c_sd_upper = uy + ur
kappa = -y * unit / cm
u_kappa = uy * unit / cm
accel = kappa * ce**2
u_accel = u_kappa * ce**2

def exact_value(value):
    return {'fraction': str(value), 'float': float(value)}

def exact_band(center, width):
    return [float(center - width), float(center + width)]

scenarios = []
for multiplier in raw['diagnostic_controls']['systematic_shift_multipliers']:
    shift = F(multiplier) * usys
    center = residual + shift
    scenarios.append({
        't': multiplier, 'b': exact_value(shift), 'D_plus_b': exact_value(center),
        'Q_band': [float(center) - q_sd_upper, float(center) + q_sd_upper],
        'C_band': exact_band(center, c_sd_upper),
        'Q_zero_inclusion_exact_squared_comparison': center**2 <= q_var_upper,
        'C_zero_inclusion_exact_comparison': abs(center) <= c_sd_upper,
    })

# Independent algebraic endpoint/guard counterexamples; finite checks, not proof.
assert cm == F(1, 100) and unit == F(1, 10**19)
assert mu < 0 and kappa > 0 and accel > 0
assert abs(mu - F(c['printed_reference_gradient_rounding_check_only'])) <= F(c['rounding_check_absolute_tolerance'])
assert y == -kappa * cm / unit
assert accel / ce**2 == kappa
assert m['independent_experiment_count'] == 1 and not c['reference_from_clock_target']
assert residual**2 <= q_var_upper and abs(residual) <= c_sd_upper
covariance_checks = []
for test_ur in (F(0), ur / 2, ur):
    for rho in (F(-1), F(0), F(1)):
        variance = uy**2 + test_ur**2 - 2*rho*uy*test_ur
        assert (uy-test_ur)**2 <= variance <= (uy+test_ur)**2 <= c_sd_upper**2
        covariance_checks.append({'u_ref': str(test_ur), 'rho': str(rho), 'variance': str(variance)})
# Concrete LC1 R1 false pass: moving center is outside zero overlap, old-center rule passes.
r1_d, r1_b, r1_width = F(-3, 2), F(-3, 2), F(13, 5)
assert abs(r1_d+r1_b) > r1_width
assert r1_d-r1_width <= r1_d+r1_b <= r1_d+r1_width
# For rational C threshold, all signed extreme shifts meet the condition exactly.
threshold_c = c_sd_upper - abs(residual)
for shift in (-threshold_c, threshold_c):
    assert abs(residual + shift) <= c_sd_upper
assert abs(residual - threshold_c - F(1, 10**12)) > c_sd_upper

result = {
    'status': 'PASS_SOURCE_FIRST_EXACT_RATIONAL_AND_BINARY64_ARITHMETIC',
    'python': sys.version, 'platform': platform.platform(),
    'implementation': 'Fraction for input/algebra/membership; math.sqrt for Q display only',
    'scope': 'conditional rounded published-summary benchmark; no empirical certification or coverage probability',
    'source_hashes': actual_hashes,
    'mu_U': exact_value(mu), 'D_U': exact_value(residual),
    'Q_upper_variance_U2': exact_value(q_var_upper), 'Q_upper_SD_U': q_sd_upper,
    'C_upper_SD_U': exact_value(c_sd_upper),
    'nominal_Q_band_U': [float(residual)-q_sd_upper, float(residual)+q_sd_upper],
    'nominal_C_band_U': exact_band(residual,c_sd_upper),
    'kappa_up_per_m': exact_value(kappa), 'kappa_SD_per_m': exact_value(u_kappa),
    'kappa_band_per_m': exact_band(kappa,u_kappa),
    'a_clock_m_s2': exact_value(accel), 'a_clock_SD_m_s2': exact_value(u_accel),
    'a_clock_band_m_s2': exact_band(accel,u_accel),
    'zero_mismatch_b0_U': exact_value(-residual),
    'all_shift_threshold_Q_U': q_sd_upper-abs(float(residual)),
    'all_shift_threshold_C_U': exact_value(threshold_c),
    'scenarios': scenarios, 'covariance_endpoint_checks': covariance_checks,
    'old_center_rule_counterexample': {
        'D': str(r1_d), 'b': str(r1_b), 'U': str(r1_width),
        'wrong_rule_includes': True, 'correct_rule_includes': False,
    },
    'unbounded_bias': 'For every proposed true slope theta, beta=y-theta explains the same y; slope is unidentifiable without bias restriction.',
    'limits': '512MiB address space and 60s CPU/wall enforced by existing capture runner; one CPU child, no GPU/grid',
}
print(json.dumps(result,indent=2,sort_keys=True))
